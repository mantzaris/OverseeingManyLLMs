"""Measured result tables, concise evaluation report and paper macros."""
from collections import Counter
import csv
from .common import ART,ROOT,read,write

def markdown(rows,keys,names=None):
    names=names or keys
    return '| '+' | '.join(names)+' |\n| '+' | '.join(['---']*len(keys))+' |\n'+'\n'.join('| '+' | '.join(str(r[k]) for k in keys)+' |' for r in rows)

def main():
    a=read(ART/'tables/answer_summary.json');v=read(ART/'verification.json');lat=read(ART/'tables/latency.json');ledger=read(ART/'resource_ledger.json')
    cs=list(csv.DictReader((ART/'tables/conditions.csv').open()));rows=[]
    for r in cs:
        rows.append(dict(condition=r['condition'],load=r['load'],offered=r['offered'],released=r['correct_released'],remaining=r['remaining'],peak=f"{float(r['mean_peak_queued']):.2f}",wait=f"{float(r['mean_wait_seconds'])*1000:.1f}"))
    tab=markdown(rows,['condition','load','offered','released','remaining','peak','wait'],['Interface','Arrivals','Offered','Correct released','Unfinished reviews','Sampled peak queue (mean)','Arrival-to-selection (ms)'])
    issues=Counter(x for p in (ART/'prepared').glob('primary*.json') for x in read(p)['output']['issues'])
    revisions=[]
    m=read(ART/'frozen/manifest.json')
    for c in m['contexts'][:4]:
        q=c['questions'][0];old=read(ART/'prepared'/f"primary_r0_{q['id']}.json")['output'];new=read(ART/'prepared'/f"revision_r0_{q['id']}.json")['output']
        revisions.append(dict(context_id=c['id'],question_id=q['id'],answer_scale_changed=(old['answer'],old['scale'])!=(new['answer'],new['scale']),output_changed=old!=new))
    write(ART/'tables/revision_summary.json',revisions)
    body=f'''# Evaluation of the oversight workflow

The frozen source selection and protocol were committed at `dec24be3` before fresh
collection. All 24 selected source contexts and all 145 original questions were
retained. Two generation replicas yield 290 initial answers. The six old-source
pilot calls and four predetermined rechecks bring the stage to **300 GPU calls and
300 attempts**, without retries, failed attempts or context-preflight rejection.
The unchanged server is Qwen2.5-7B-Instruct at pinned revision
`a09a35458c702b33eeacc393d103063234e8bc28`, BF16 on one RTX 6000 Ada, zero CPU offload.

## Actual answers, before simulated review

Official exact match is **{int(a['em'])}/290 ({a['em']/290*100:.1f}%)**. Mean token F1 is
**{a['f1']/290*100:.2f}%**. Joint answer/scale correctness is **{a['joint']}/290**;
scale agreement alone is {a['scale']}/290. There are {a['unfinished']} empty answers,
including unsupported outputs and parser failures, and {290-a['unfinished']} nonempty
answers. All 290 returned bodies are parseable JSON. These categories must not be
confused with the legacy formatter's stricter `valid` flag ({a['parse_valid']}/290).
Optional evidence supplied as a string rather than a list accounts for
{issues['evidence_shape']} formatting flags; it does not erase the readable answer
or the full source. Other retained issues are {dict(issues)}. No complex executable
representation is required or used to select the evaluation sample.

The context-average joint accuracy is {a['context_mean_joint']*100:.2f}%, with a
source-context bootstrap interval [{a['context_mean_joint_95'][0]*100:.2f},
{a['context_mean_joint_95'][1]*100:.2f}]%. This is model/task evidence, not a user
study. Exact-match scoring can penalize a descriptive span that differs from the
annotation. The original source/question/response remains inspectable.

## Matched wall-clock software scenarios

There are 144 completed scenarios: twelve two-source bundles, two answer replicas,
three interface configurations and two constructed arrival concentrations. The
same saved outputs are used throughout. All tasks are offered at time zero; task
starts become eligible every .15 seconds (lower) or .015 seconds (higher), followed
by a .04-second delivery delay. These are compressed software test timings,
separate from measured GPU generation. The observation cutoff is 2.2 seconds, not
a financial deadline.

A scripted ideal inspection approves or corrects one question after .095 seconds,
then explicitly releases that version. The first request is deferred once for
.35 seconds. C pauses new starts from .25 to .65 seconds and can retain up to three
source-related requests. This script is common in correctness and per-question
service semantics. Its C-only pause/group controls are declared workflow actions,
not assumed human time savings. Actual recheck outputs are inserted at .8 seconds
for the predeclared replica-zero examples. A changed version requires renewed review.

{tab}

Every condition/load releases all 290 answers correctly only because the ideal
script supplies annotations and the cutoff is generous for its artificial service
time. **B versus C is a mechanical completion tie in all 12 paired bundles at both
loads**, with difference 0 and a degenerate script-bootstrap interval [0,0]. This
is not evidence of human equivalence. C has no measured throughput advantage.
Its pause increases the lower-load sampled queue peak by 1.083 requests on average
and approximately doubles arrival-to-selection time. At higher concentration,
all three peak queues average 10.083 requests. Queue peaks are sampled every .02
seconds. Arrival-to-selection includes resumed selections and is not pure reading
time or model latency.

No offered work disappears during pauses. `tables/pause_checkpoint.csv` audits
recorded event prefixes at .45 seconds, the midpoint of the declared pause, as a
descriptive accounting check. It is not a new favorable timing experiment. Some
work is unstarted then, while all is accounted for at the eventual cutoff. The
primary final-cutoff experiment does not test a persistently overloaded human
reviewer. Protocol fixtures separately exercise outstanding work at shutdown,
withdrawal, duplicate delivery and stale decisions.

## Measured software behavior

All **{v['scenario_events']:,} scenario events** replay to their recorded state hashes;
all {v['cutoffs_verified']} cutoff states and released-answer scores are independently
reconstructed. There are zero missed, duplicate or misassociated received request
IDs in the completed matrix and zero unexpected protocol/driver command failures.
All **{v['stable_checks']:,} active-snapshot comparisons** preserve the pinned output.
These repeated checks are not independent sources or human observations.

| Timing boundary | Observations | Median ms | 95th percentile ms |
|---|---:|---:|---:|
'''
    for key,label in [('protocol_handler_ms','Atomic handler'),('replay_delivery_lateness_ms','Scheduled delivery lateness'),('browser_http_roundtrip_ms','Browser HTTP round trip'),('browser_received_to_render_ms','State receipt to DOM update')]:
        z=lat[key];body+=f"| {label} | {z['n']} | {z['median']:.2f} | {z['p95']:.2f} |\n"
    body+=f'''
Handler timing includes validation and hashing. HTTP timing includes serialization
and local transport. DOM timing ends after JavaScript updates, not compositor
paint. GPU generation is separate: **{ledger['generation_seconds']:.1f} summed seconds**,
{ledger['prompt_tokens']:,} prompt and {ledger['completion_tokens']:,} completion tokens.
Hardware, host contention and the local browser limit generality of these timings.

The live integration uses twelve initial answers from two fresh contexts, not extra
unaccounted calls. A six-second active review overlaps observed arrivals while
admission is paused for two seconds. A real recheck creates a new version; the old
approval is rejected. The demonstration leaves its 12 questions visible and
unreleased, rather than claiming a participant completed them. Of four actual
model rechecks, {sum(x['answer_scale_changed'] for x in revisions)} change answer or
scale; {sum(x['output_changed'] for x in revisions)} change the full prepared response.
A version change need not imply an incorrect earlier answer.

Chromium checks exercise all three real interfaces. The final release checks pass
{v['browser_checks']} assertions, including focus/typed-note stability, deferral,
resumption, separate source-session questions, stale HTTP-state rejection,
version-specific approval, explicit release, connection recovery, idempotent retries, restored journals, a timed
prospective-study cutoff, disjoint practice material and a narrow viewport. {v['browser_runs_replayed']} browser journals replay exactly. Their metadata revisions are authored stress events,
separate from actual model revisions. Failed earlier harness runs and the resolved
software annotation-indexing error remain in the artifact namespace.

## What the comparisons do and do not establish

The software study establishes executable accounting and release boundaries on
real source material and actual model outputs. It does not establish better human
review quality, less mental demand, faster source reading, or superior ordering.
Source grouping gives an explicit navigation option, not shared correctness.
The appropriate next comparison is the prepared within-participant B/C study,
with disjoint matched packets and real quality/effort measurements. No new inference
or deeper-search study is needed to run a formative interface pilot.
'''
    (ROOT/'research/oversight_workflow/EVALUATION.md').write_text(body)
    report=f'''# Overseeing many LLMs through a user-controlled review queue

## Finding

The new desk makes concurrent answers inspectable and individually releasable.
It retains active evidence during arrivals, keeps paused/deferred work in the
accounting, and requires approval for the exact current output version. It is a
working asynchronous system with a frozen real-data software evaluation. **It does
not yet demonstrate a human performance or workload advantage.**

Three configurations share one protocol: worker conversations, a central stable
queue, and optional user-controlled source sessions. No new optimizer, adaptive
acquisition policy or automatic correction reuse is introduced. The closest systems
already provide agent dashboards, steering, history and queues; the contribution
is a specific review/release workflow and its testable behavior under concurrency.

## Evidence at a glance

- 24 fresh TAT-QA source contexts, 145 original questions, two model replicas.
- 290 initial model answers; {int(a['em'])} exact matches and {a['unfinished']} empty outputs retained.
- 300 GPU attempts including development and four real rechecks; no failed attempts or retries.
- 144 matched wall-clock scenarios; {v['scenario_events']:,} replayed events and
  {v['stable_checks']:,} successful active-snapshot checks.
- All configurations finish the ideal scripted workload. B/C completion differences
  are zero. C's pause increases lower-load queue pressure and waiting; no automatic
  efficiency advantage is supported.
- A live twelve-task demonstration, actual source displays, version examples,
  final browser checks and a prospective human protocol are included.

See [EVALUATION.md](EVALUATION.md) for exact denominators, timings, failures and tables.

## Claim-evidence map

| Claim | Evidence | Limit |
|---|---|---|
| Arrivals preserve active review and typed notes | Protocol interleaving tests, live/events.json, browser_final_verified journals | Local single-user implementation, not arbitrary external agent tools. |
| Approval is version-specific and individually scoped | Refused stale approvals, immutable version history, replay tests | Does not establish correctness of an approved answer. |
| Pausing cannot conceal offered work | Conservation invariants, pause checkpoint and accounting figure | Pausing may delay progress; it is not automatically beneficial. |
| Actual financial questions can enter one review protocol | Fresh source manifest and 290 raw model answers | Low answer accuracy and incomplete citations remain visible. |
| C improves human review over B | No evidence yet; HUMAN_STUDY.md is prospective | No participants, cognition measurements or powered efficacy claim. |
| The interface is the first oversight dashboard | Not claimed; AgentGUI/AGDebugger and earlier interruption research precede it | The novelty is limited to a specified system/evaluation package. |

## Paper framing and recommendation

The separate ICAART-format draft is `paper/oversight_workflow/main.pdf`. It centers
on inspectable concurrent work and explicit release authority. The historical
maintenance, retail, attention-session and correction-transfer manuscripts remain
unchanged. Their negative findings motivate using simple ordering, direct source
access and separate decisions, rather than being recast as support for this desk.

**Recommend a position-paper framing now.** The real-data systems evaluation is
complete, but the central user-benefit comparison has not been conducted and the
building blocks have strong predecessors. A regular-paper argument would be much
stronger after a formative pilot fixes interaction/packet issues and a prospectively
specified human comparison measures correct releases, unresolved work, resumption
behavior and perceived control. A mechanical script tie cannot substitute for that.

The smallest next step is an authorized formative B/C pilot with the supplied
source-disjoint packets and training materials. It should diagnose usability and
variance, not claim powered efficacy. No further automatic correction-transfer
algorithm is justified by the present result.

## Reproduction and accounting

`bash research/oversight_workflow/reproduce.sh` checks saved outputs/events and
regenerates tables/figures without inference. `python3 -m
research.oversight_workflow.prototype.server` runs the local desk. The exact live,
replay and manuscript commands are in README.md. Historical clocks and publication
redaction provenance are preserved. This stage adds no redaction; private evaluation
annotations are separated by code path from online sources.

The resource ledger records stage and cumulative wall time and explicitly retains
the overrun beyond the original 36-hour target. The existing GPU service is retained;
only local test servers and browser workers started for this stage are stopped.
'''
    def hms(seconds):
        n=int(seconds);return f'{n//3600}h {(n%3600)//60}m {n%60}s'
    report+=f'''
## Recorded resource use and verification

Stage wall time at the {'final closure' if ledger['final'] else 'latest checkpoint'} is
**{hms(ledger['stage_elapsed_seconds'])}**. The authorized deadline remains
{ledger['deadline_utc']}; no historical timestamp is reset. Cumulative elapsed wall
time from the original start, including gaps and subsequent separately authorized
work, is **{hms(ledger['cumulative_wall_seconds'])}**. This exceeds the original
36-hour target by **{hms(ledger['original_36h_overrun_seconds'])}**. It is not work
claimed to fit inside that original window.

This stage used {ledger['scheduled_calls']} scheduled GPU calls and
{ledger['attempts']} actual attempts, {ledger['failed_attempts']} failed attempts,
{ledger['retries']} retries, {ledger['prompt_tokens']:,} prompt tokens and
{ledger['completion_tokens']:,} completion tokens. Summed request time was
{ledger['generation_seconds']:.1f} seconds. The prior cumulative ledger plus this
stage contains {ledger['cumulative']['scheduled_calls']:,} scheduled calls and
{ledger['cumulative']['attempts']:,} attempts; the historical difference is retained.
No paid resource was provisioned and there are zero participant observations.

Saved-output reproduction passed from a clean Git export with original-checkout,
external source-cache and GPU/network access blocked. All nine numerical tables
matched. There are 17 focused protocol/API/closure tests, 41 relevant historical
regression tests and 62 scripted Chromium checks. All 144 completed scenario traces,
six browser journals, the live demonstration and the actual-source walkthrough
replay. The seven-page official-template PDF and all six scientific figures were
rendered and inspected. Evidence is in `artifacts/oversight_workflow/checks/`.
'''
    (ROOT/'research/oversight_workflow/REPORT.md').write_text(report)
    paper=ROOT/'paper/oversight_workflow';paper.mkdir(exist_ok=True)
    (paper/'numbers.tex').write_text('\n'.join([f'\\newcommand{{\\SourceCount}}{{24}}',f'\\newcommand{{\\QuestionCount}}{{145}}',f'\\newcommand{{\\AnswerCount}}{{290}}',f'\\newcommand{{\\ExactCount}}{{{int(a["em"])}}}',f'\\newcommand{{\\JointCount}}{{{a["joint"]}}}',f'\\newcommand{{\\EmptyCount}}{{{a["unfinished"]}}}',f'\\newcommand{{\\EventCount}}{{{v["scenario_events"]:,}}}',f'\\newcommand{{\\StableCount}}{{{v["stable_checks"]:,}}}',f'\\newcommand{{\\BrowserChecks}}{{{v["browser_checks"]}}}'])+'\n')
    with (paper/'numbers.tex').open('a') as f:
        for prefix,key in [('Handler','protocol_handler_ms'),('Http','browser_http_roundtrip_ms'),('Dom','browser_received_to_render_ms'),('Delivery','replay_delivery_lateness_ms')]:
            for suffix,stat in [('Median','median'),('PHigh','p95')]:
                f.write('\\newcommand{\\'+prefix+suffix+'}{'+format(lat[key][stat],'.2f')+'}\n')
    lines=['\\begin{tabular}{llrrr}\\toprule','View & Load & Released & Peak & Wait (ms) \\\\ \\midrule']
    for r in rows:lines.append(f"{dict(threads='A',queue='B',sessions='C')[r['condition']]} & {r['load']} & {r['released']}/290 & {r['peak']} & {r['wait']} \\\\")
    lines+=['\\bottomrule','\\end{tabular}'];(paper/'result_table.tex').write_text('\n'.join(lines)+'\n')
    print('Reports and paper tables generated')

if __name__=='__main__':main()
