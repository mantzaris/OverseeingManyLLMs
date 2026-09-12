from datetime import datetime,timezone
from .common import ART,ROOT,read,write,digest
from .inference import SYSTEM
from .transport import client

def main():
    selection=read(ART/'selection.json');pilot=read(ART/'pilot.json')
    avg=sum(x['generation_seconds'] for x in pilot)/len(pilot)
    m=dict(stage='oversight_workflow',frozen_utc=datetime.now(timezone.utc).isoformat(),contexts=selection['contexts'],replicas=2,
        selection_sha256=digest(selection),original_questions=selection['questions'],initial_calls=selection['questions']*2,
        pilot_calls=6,revision_calls=4,total_planned_calls=selection['questions']*2+10,
        revisions='First question of first four selected contexts, replica zero, fresh source recheck; never selected by correctness.',
        model=dict(model=client.MODEL,revision=client.REVISION,dtype='bfloat16',gpu='RTX 6000 Ada',cpu_offload_gb=0,temperature=.3,top_p=1,max_tokens=230,max_model_len=2048,seed_formula='912000 + replica*10000 + original_source_index*10 + original_question_order'),
        prompt=SYSTEM,conditions=['threads','queue','sessions'],
        primary='Software protocol reliability and accounted useful releases for central queue versus source sessions on matched saved outputs. No human efficacy estimand.',
        software_scenarios=dict(bundles=12,contexts_per_bundle=2,question_order='Round robin over original questions in the two source contexts',replicas=2,
            loads=['lower','higher'],start_interval_seconds=dict(lower=.15,higher=.015),delivery_after_start_seconds=.04,observation_seconds=2.2,
            script_action_seconds=.095,session_bound=3,paused_session_condition_interval=[.25,.65],
            deferral='First request once for .35 seconds, preserving notes; resume when due.',
            revision='Saved actual replica-zero continuation inserted at .8s for first source in a bundle when predetermined revision exists.',
            reviewer='Ideal, simulated question-specific annotation correction or approval after .095s; each answer separately released. Time is a software stress input, not human reading time.',
            source_deadlines='None. No financial or business deadlines invented. Observation cutoff is an experimental boundary.',
            failures='Keep all returned failures, malformed and context-limited outputs in offered workload; explicit ideal inspection may correct them. No replacement questions.',
            pairing='Same saved initial answers, eligible-start schedule and revision events per bundle/replica/load. Admission pauses may delay actual arrivals; all offered work remains counted.'),
        statistical_analysis=dict(source_units=24,constructed_bundles=12,replicas='Average within bundle before comparisons',bootstrap_resamples=2000,analysis_seed=91273,
            contrasts=['sessions minus queue correct releases','sessions minus queue unfinished offered work','sessions minus queue peak pending'],
            note='Paired bundle intervals describe these constructed scripts, not human effects. Replays and outputs do not multiply independent sources. All condition results reported.'),
        live_demonstration='First two selected contexts, replica zero, three independent task workers sharing serial GPU transport; hold first review six wall seconds, pause task admission two seconds, defer and resume, inject actual source recheck revision and reject stale approval.',
        examples='First bundle in numerical order for timeline and source display; first predetermined revision for version example. Show failures if present, chosen by first source/question order.',
        forecast=dict(pilot_mean_seconds=avg,conservative_generation_minutes=(selection['questions']*2+4)*max(3,avg*2)/60,software_minutes=12*2*2*3*2.2/60),
        code_hashes={str(p.relative_to(ROOT)):digest(p.read_text()) for p in (ROOT/'research/oversight_workflow').glob('*.py')},
        changes='Bug repairs after freeze must retain original declaration and be logged; no case or model-response replacement.')
    write(ART/'frozen/manifest.json',m);print('Frozen',m['total_planned_calls'],'calls; conservative generation minutes',m['forecast']['conservative_generation_minutes'])
if __name__=='__main__':main()
