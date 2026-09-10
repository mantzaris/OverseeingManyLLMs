"""Separate staggered workload with stable per-agent/job public and hidden streams."""
import random
from .domain import PrivateJob, PublicJob, Scenario, digest, generate_scenario
from .competition_condition import generate_competition_scenario, hidden_fault_and_clues

SPEC = dict(agents=[3,6], jobs_per_agent=3, horizon=24, wave_bases=[0,8,16],
            release_jitter=[0,1], deadline_windows=[2,4,6], downtime_rates=[0,1,3],
            terminal_penalties=[0,4,8,12], fault_prior=[.5,.5], clue_accuracies=[.8,.6],
            streams='SHA256(seed,agent_id,job_number,component); public fields and hidden fault/clues separate')


def job_rng(seed, agent, job, component):
    return random.Random(int(digest(dict(seed=seed, agent_id=agent, job_number=job, component=component)),16))


def generate_larger_scenario(seed, agents):
    if agents not in (3,6):
        raise ValueError('Research workload permits exactly three or six agents')
    jobs=[]
    for agent in range(agents):
        for job in range(3):
            release=8*job+job_rng(seed,agent,job,'arrival').choice((0,1))
            window=job_rng(seed,agent,job,'deadline').choice((2,4,6))
            downtime=job_rng(seed,agent,job,'downtime').choice((0,1,3))
            penalty=job_rng(seed,agent,job,'penalty').choice((0,4,8,12))
            fault,clues=hidden_fault_and_clues(job_rng(seed,agent,job,'hidden'))
            jobs.append(PrivateJob(PublicJob('a{}j{}'.format(agent,job),agent,release,release+window,downtime,penalty,clues),fault))
    return Scenario(seed,tuple(jobs),24)


def scenario_for(entry):
    if entry['workload']=='original':return generate_scenario(entry['seed'])
    if entry['workload']=='competition':return generate_competition_scenario(entry['seed'])
    if entry['workload']=='larger':return generate_larger_scenario(entry['seed'],entry['agents'])
    raise ValueError('Unknown workload')
