"""Matched comparison adapter using the frozen pilot shell and Desk lifecycle."""
import argparse
from copy import deepcopy
from http.server import ThreadingHTTPServer
from itertools import zip_longest
import threading
import uuid

from research.oversight_workflow.common import read, digest
from research.oversight_workflow.data import task
from research.oversight_workflow.driver import ReplayDriver
from research.oversight_workflow.pilot.server import Pilot, PilotHandler, utc
from research.oversight_workflow.pilot.materials import PILOT
from research.oversight_workflow.pilot.adapter import saved_output
from .materials import HERE, VERSION, SCHEMA
from .protocol import MatchedDesk
from .freeze import runtime_fingerprint, verify


def desk_condition(condition):
    return 'sessions' if condition in ('G', 'training') else 'queue'


def setup_html():
    # Reuse the pilot's form/navigation implementation. Only condition instructions change.
    html = (PILOT / 'setup.html').read_text()
    for old, new in [("==='B'", "==='Q'"), ("==='C'", "==='G'"), ("==='S'", "==='M'")]:
        html = html.replace(old, new)
    html = html.replace('Formative pilot', 'Matched review comparison')
    html = html.replace('source-only diagnostic', 'manual source-only review')
    html = html.replace('You have four minutes for six original questions.', 'You have nine minutes for twelve original questions, offered in the same two waves as the other blocks.')
    html = html.replace('This block checks the source task’s difficulty.', 'Use the source and calculator, and release only answers you judge correct.')
    html = html.replace('and pause new task starts. Decisions remain separate. In-flight work continues while starts are paused, and unstarted tasks still count.', 'using the source-session cards and Next. Decisions remain separate. Admission controls are disabled in every block.')
    html = html.replace('Try the optional source controls.', 'Try grouping related questions, then supplying your own answer and releasing it separately. No admission controls are available.')
    html = html.replace('Neither interface is expected to be better; we are testing task feasibility and usability.', 'Use each assigned interface as you find appropriate. We are testing these tasks and interfaces, not you.')
    html = html.replace('alex-practice', 'matched-practice')
    return html


def desk_js():
    # Preserve the same display projection, notes, calculator and answer-entry handlers.
    text = (PILOT / 'desk.js').read_text().replace("condition==='S'", "condition==='M'")
    text = text.replace('Source-only task.', 'Manual source-only task.')
    text = text.replace('(114 - 108) / 108 * 100', '(12 - 3) / 3 * 100')
    text += """
const matchedRender = render;
render = function(s) {
  matchedRender(s);
  const pause = document.getElementById('pause'); pause.hidden=true; pause.disabled=true;
  const metric = document.querySelector('#metrics .metric:nth-child(4)');
  if(metric) metric.innerHTML='<strong>'+ (s.counts.offered-s.counts.released) +'</strong><span>Unfinished answers</span>';
};
if(state) render(state);
"""
    return text


class MatchedReplayDriver(ReplayDriver):
    def __init__(self, *args, source_only=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_only = source_only

    def cmd(self, action, payload):
        if action == 'receive' and self.source_only:
            payload = {**payload, 'origin': 'source_only_placeholder'}
        return super().cmd(action, payload)


class MatchedPilot(Pilot):
    def __init__(self, logdir, kind='investigator_practice', authorization=None):
        super().__init__(logdir, kind, authorization)
        self.manifest = read(HERE / 'manifest.json')
        self.runtime_sha256 = runtime_fingerprint()
        if kind == 'participant':
            if authorization.get('study_version') != VERSION or authorization.get('manifest_sha256') != self.manifest['manifest_sha256'] or not authorization.get('assignment_schedule_reference'):
                raise ValueError('Authorization must identify this matched version, manifest and pre-recorded assignment schedule')
            verify()

    def create(self, payload):
        with self.lock:
            if runtime_fingerprint() != self.runtime_sha256:
                raise ValueError('Runtime files changed after server launch; restart under a declared version')
            super().create(payload)
            self.run.update(schema=SCHEMA, pilot_version=VERSION,
                            runtime_version=VERSION, runtime_sha256=self.runtime_sha256, comparison='Q/G/M matched allocations')
            self.save()
            return self.status()

    def status(self):
        result = super().status()
        result['version'] = VERSION
        return result

    def status_no_check(self):
        result = super().status_no_check()
        result['version'] = VERSION
        return result

    def begin(self, payload):
        with self.lock:
            if not self.run or self.current or self.run['withdrawn']:
                raise ValueError('No ready run, or an active block remains')
            step = self.run['next_block']
            if step >= 4:
                raise ValueError('All blocks completed')
            if self.run['sessions'] and self.run['sessions'][-1].get('questionnaire') is None:
                raise ValueError('Save the prior form, including any unanswered items')
            if 'seconds' in payload and self.kind != 'software_fixture':
                raise ValueError('Duration override is restricted to software fixtures')
            self.stop()
            block = None if step == 0 else self.manifest['assignments'][self.run['assignment']]['blocks'][step-1]
            condition = 'training' if block is None else block['condition']
            packet = None if block is None else block['packet']
            self.desk = MatchedDesk(desk_condition(condition))
            self.session = uuid.uuid4().hex; self.journal_count = 0; self.mode = 'matched'
            if condition == 'training':
                material = read(PILOT.parent / 'study/training.json')
                contexts = [material['context']]; qids = {q['id'] for q in material['questions']}
                stage = 'pilot'; declared = self.manifest['training_seconds']
                offsets = self.manifest['training_start_offsets']
            else:
                spec = self.manifest['packets'][packet]
                contexts = [next(c for c in self.contexts if c['id'] == i) for i in spec['context_ids']]
                qids = set(spec['question_ids']); stage = 'primary'
                declared = self.manifest['review_seconds']; offsets = self.manifest['review_start_offsets']
            duration = float(payload.get('seconds', declared))
            if not .2 <= duration <= 1000:
                raise ValueError('Invalid duration')
            offsets = [v * duration / declared for v in offsets]
            raw_proposals = {}; groups = []
            for c in contexts:
                group = []
                for q in c['questions']:
                    if q['id'] not in qids: continue
                    if condition == 'M':
                        output = dict(answer=[], scale='', evidence=[], derivation='Manual source-only task. No model proposal is shown.', issues=[])
                        raw = None
                    else:
                        output, raw = saved_output(c, q, stage)
                    t = task(c, q, 0); group.append(dict(task=t, output=output)); raw_proposals[t['id']] = raw
                groups.append(group)
            items = [x for row in zip_longest(*groups) for x in row if x]
            self.current = dict(session_id=self.session, block_index=step, condition=condition,
                                desk_condition=desk_condition(condition), packet=packet,
                                duration_seconds=duration, declared_duration_seconds=declared,
                                start_utc=utc(), question_ids=[x['task']['question_id'] for x in items],
                                source_ids=[c['id'] for c in contexts], start_offsets=offsets,
                                raw_proposals=raw_proposals, record_kind=self.kind,
                                admission_controls=False, generation_delay=.25)
            self.study = dict(duration_seconds=duration, packet=packet, status=self.kind)
            self.driver = MatchedReplayDriver(self.desk, items, generation_delay=.25, start_offsets=offsets, source_only=condition == 'M').start()
            self.timer = threading.Timer(duration, lambda: self.finish('cutoff'))
            self.timer.daemon = True; self.timer.start(); self.save()
            return self.status()

    def view(self):
        result = super().view()
        if self.current:
            result['banner'] = ('Write answers from the source. No model draft is supplied.' if self.current['condition'] == 'M'
                                else 'Check each proposed answer against the source. You may correct, reject or defer.')
            result['banner'] += ' Admission controls are disabled. Record type: ' + self.kind.replace('_', ' ')
        return result


class MatchedHandler(PilotHandler):
    def do_GET(self):
        if self.path == '/':
            return self.response(setup_html(), ctype='text/html; charset=utf-8')
        if self.path == '/desk':
            html = (PILOT.parent / 'prototype/index.html').read_text()
            html = html.replace('</head>', '<style>#pause{display:none!important}</style></head>')
            html = html.replace('</body>', '<script src="/pilot/desk.js"></script></body>')
            return self.response(html, ctype='text/html; charset=utf-8')
        if self.path == '/pilot/desk.js':
            return self.response(desk_js(), ctype='text/javascript')
        return super().do_GET()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--port', type=int, default=9043)
    p.add_argument('--log-dir', default='/tmp/oversight-matched-practice')
    p.add_argument('--kind', choices=['investigator_practice', 'software_fixture', 'participant'], default='investigator_practice')
    p.add_argument('--authorization')
    args = p.parse_args()
    app = MatchedPilot(args.log_dir, args.kind, read(args.authorization) if args.authorization else None)
    MatchedHandler.app = app
    server = ThreadingHTTPServer(('127.0.0.1', args.port), MatchedHandler)
    print('Matched comparison http://127.0.0.1:%d (%s)' % (args.port, args.kind), flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: app.stop(); app.save(); server.server_close()


if __name__ == '__main__': main()
