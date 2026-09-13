"""CPU reproduction in a new directory; never reset the historical stage clock."""
import argparse
from datetime import datetime, timezone
import gzip
import json
from pathlib import Path
import time

from research.oversight_workflow.common import read, write
from .inputs import OUT, workload
from .run import verify_freeze, environment
from .simulation import simulate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--max-minutes', type=float, default=30)
    parser.add_argument('--config')
    parser.add_argument('--seed', type=int)
    parser.add_argument('--rotation', type=int)
    args = parser.parse_args()
    if not 0 < args.max_minutes <= 90:
        parser.error('CPU reproduction limit must be in (0, 90] minutes')
    verify_freeze()
    design = read(OUT/'design.json')
    configs = [c for c in design['configs'] if args.config is None or c['id'] == args.config]
    seeds = [s for s in design['seeds'] if args.seed is None or s == args.seed]
    rotations = [r for r in design['rotations'] if args.rotation is None or r == args.rotation]
    if not configs or not seeds or not rotations:
        parser.error('Only declared configurations, seeds and rotations may be replayed')
    args.out.mkdir(parents=True, exist_ok=False)
    inputs = read(OUT/'inputs.json')
    env = environment(inputs)
    started = time.perf_counter()
    start_utc = datetime.now(timezone.utc).isoformat()
    expected = len(configs)*len(seeds)*len(rotations)*len(design['policies'])
    count = 0
    expired = False
    with gzip.open(args.out/'results.jsonl.gz', 'wt') as results, gzip.open(args.out/'traces.jsonl.gz', 'wt') as traces:
        for cfg in configs:
            for rotation in rotations:
                items = workload(inputs, cfg, rotation)
                for seed in seeds:
                    if time.perf_counter()-started >= args.max_minutes*60:
                        expired = True
                        break
                    for policy in design['policies']:
                        ident = dict(record_kind='computational_simulation',
                                     scenario_id=cfg['id']+'/rotation'+str(rotation),
                                     simulation_run_id=cfg['id']+'/r'+str(rotation)+'/s'+str(seed)+'/'+policy,
                                     config=cfg['id'], family=cfg['family'], rotation=rotation,
                                     seed=seed, policy=policy)
                        summary, trace = simulate(items, inputs['sources'], cfg, policy, seed, env)
                        results.write(json.dumps({**ident, **summary}, separators=(',', ':'))+'\n')
                        traces.write(json.dumps({**ident, **trace}, separators=(',', ':'))+'\n')
                        count += 1
                if expired:
                    break
            results.flush()
            traces.flush()
            if expired:
                break
    record = dict(record_kind='computational_simulation_reproduction', start_utc=start_utc,
                  max_minutes=args.max_minutes, elapsed_seconds=time.perf_counter()-started,
                  expected=expected, completed=count, complete=count == expected,
                  subset=expected != 31680, inference_calls=0, historical_files_modified=False)
    write(args.out/'reproduction.json', record)
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
