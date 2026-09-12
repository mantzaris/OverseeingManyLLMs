"""Study restrictions on the existing protocol; historical Desk stays unchanged."""
from copy import deepcopy
import time
from research.oversight_workflow.protocol import Desk, ProtocolError
from research.oversight_workflow.common import digest


class MatchedDesk(Desk):
    def _apply(self, action, payload, stamp):
        if action in ('pause', 'resume'):
            raise ProtocolError('Admission controls are disabled in every matched condition')
        if action == 'session' and self.state['condition'] != 'sessions':
            raise ProtocolError('Source grouping is available only in G and training')
        return super()._apply(action, payload, stamp)


def replay(events, condition='queue'):
    desk = MatchedDesk(condition)
    for e in events:
        response = desk.command(e['event_id'], e['action'], e['payload'], at=e['at'])
        if response != e['response'] or digest(desk.state) != e['state_sha256']:
            raise AssertionError('Matched replay mismatch at event ' + str(e['sequence']))
        desk.events[-1] = deepcopy(e)
    if events:
        desk.started = time.monotonic() - events[-1]['at']
    return desk
