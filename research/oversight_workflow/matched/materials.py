"""Versioned Q/G/M manifest. Sources are reused; no outcome-driven reselection."""
from copy import deepcopy
from pathlib import Path
from research.oversight_workflow.common import ART, ROOT, read, write, digest
from research.oversight_workflow.pilot.materials import PILOT
from research.oversight_workflow.pilot.adapter import saved_output

HERE = Path(__file__).resolve().parent
OUT = ART / 'matched_preparation'
VERSION = 'matched-qgm-v1'
SCHEMA = 'oversight-matched-export-v1'


def build():
    old = read(PILOT / 'manifest.json')
    packets = deepcopy(old['packets'])
    for p in packets:
        p.pop('source_only_question_ids')  # Manual now uses all twelve originals.
    assignments = deepcopy(old['assignments'])
    for a in assignments:
        for b in a['blocks']:
            b['condition'] = {'B': 'Q', 'C': 'G', 'S': 'M'}[b['condition']]
    sources = {c['id']: c for c in read(ART / 'frozen/manifest.json')['contexts']}
    outputs = []
    for packet in packets:
        for cid in packet['context_ids']:
            c = sources[cid]
            for q in c['questions']:
                output, raw = saved_output(c, q)
                outputs.append(dict(source_id=cid, question_id=q['id'],
                                    call_id=raw['call_id'], raw_response_sha256=digest(raw['raw_response']),
                                    display_output_sha256=digest(output)))
    m = dict(version=VERSION, parent_manifest_sha256=old['manifest_sha256'],
             selection='Exact formative-v1 packets, selected by public characteristics. No new selection or generation; already inspected benchmark material.',
             packets=packets, assignments=assignments, outputs=outputs, replica=0,
             review_seconds=540, training_seconds=240,
             review_start_offsets=old['review_start_offsets'], training_start_offsets=[0, 1.5],
             generation_delay=.25, maximum_inflight=3, admission_controls=False,
             conditions={'Q': 'Central queue with actual saved drafts',
                         'G': 'Q plus optional same-source groups (maximum three) and session-aware Next',
                         'M': 'Central queue with no drafts or generated explanations; same twelve questions and time'},
             common='Sources, calculator, notes, deferral, individual exact-version approval/release, manual selection, offered-work counts, arrivals, duration and questionnaires',
             primary='Mean participant difference G minus Q in joint-correct current-version releases / all 12 offered questions',
             secondary=['Q minus M', 'G minus M'],
             source_dependence='Six reused contexts; not six independently identified reports. Participant is paired unit; no question-level sample inflation.',
             example_six_run_assignment_ids=old['example_six_run_assignment_ids'],
             collection='Unperformed. Authorized investigator must register tranche and assignment schedule before outcomes.',
             fixture_compression='Only explicit software_fixture records may override duration; all scored fixture conditions use the same declared compression.')
    m['manifest_sha256'] = digest(m)
    return m


if __name__ == '__main__':
    m = build()
    write(HERE / 'manifest.json', m)
    print(m['version'], m['manifest_sha256'])
