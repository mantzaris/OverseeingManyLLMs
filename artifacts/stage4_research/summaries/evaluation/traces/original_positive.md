# Paired queue example

First numerical seed with search lower loss than greedy at two ticks.

Offline scoring view: hidden faults and initial correctness below were not supplied to schedulers.

## replication/original/10022/a3/s2/frozen/delay/lambda0

Loss 24.0; incorrect closures 2; corrections 1.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a2j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 1; c=3; K=8 |
| 0 | planning_decision | eligible ; choose None |
| 0 | queue_snapshot | waiting a2j0; active None |
| 1 | request_expired | a2j0: infeasible_at_arrival |
| 1 | job_closed | a2j0: correct=False, job loss=11 |
| 1 | proposal | a0j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 6; c=1; K=0 |
| 1 | proposal | a1j0: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 6; c=1; K=8 |
| 1 | planning_decision | eligible a0j0(d=6,p=0.146,G_at_completion=3.000), a1j0(d=6,p=0.146,G_at_completion=11.000); choose a0j0 |
| 1 | queue_snapshot | waiting a1j0; active {'finish': 3, 'job_id': 'a0j0', 'start': 1} |
| 2 | queue_snapshot | waiting a1j0; active {'finish': 3, 'job_id': 'a0j0', 'start': 1} |
| 3 | review_completed | a0j0: reset_sensor, applied=True, corrected=True |
| 3 | planning_decision | eligible a1j0(d=6,p=0.146,G_at_completion=9.000); choose a1j0 |
| 3 | queue_snapshot | waiting ; active {'finish': 5, 'job_id': 'a1j0', 'start': 3} |
| 4 | queue_snapshot | waiting ; active {'finish': 5, 'job_id': 'a1j0', 'start': 3} |
| 5 | review_completed | a1j0: replace_filter, applied=True, corrected=False |
| 5 | planning_decision | eligible ; choose None |
| 5 | queue_snapshot | waiting ; active None |
| 6 | job_closed | a0j0: correct=True, job loss=2 |
| 6 | job_closed | a1j0: correct=True, job loss=0 |
| 6 | proposal | a1j1: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 8; c=3; K=0 |
| 6 | planning_decision | eligible ; choose None |
| 6 | queue_snapshot | waiting a1j1; active None |
| 7 | proposal | a0j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 12; c=1; K=0 |
| 7 | proposal | a2j1: clues sensor/filter; first replace_filter; second reset_sensor; initial wrong (offline label); p=0.1837; deadline 8; c=3; K=8 |
| 7 | planning_decision | eligible a0j1(d=12,p=0.146,G_at_completion=3.000); choose a0j1 |
| 7 | queue_snapshot | waiting a1j1, a2j1; active {'finish': 9, 'job_id': 'a0j1', 'start': 7} |
| 8 | request_expired | a1j1: infeasible_at_arrival |
| 8 | job_closed | a1j1: correct=True, job loss=0 |
| 8 | request_expired | a2j1: infeasible_at_arrival |
| 8 | job_closed | a2j1: correct=False, job loss=11 |
| 8 | queue_snapshot | waiting ; active {'finish': 9, 'job_id': 'a0j1', 'start': 7} |
| 9 | review_completed | a0j1: replace_filter, applied=True, corrected=False |
| 9 | planning_decision | eligible ; choose None |
| 9 | queue_snapshot | waiting ; active None |
| 10 | planning_decision | eligible ; choose None |
| 10 | queue_snapshot | waiting ; active None |
| 11 | planning_decision | eligible ; choose None |
| 11 | queue_snapshot | waiting ; active None |
| 12 | job_closed | a0j1: correct=True, job loss=0 |
| 12 | queue_snapshot | waiting ; active None |

## replication/original/10022/a3/s2/frozen/greedy/lambda0

Loss 26.0; incorrect closures 2; corrections 1.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a2j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 1; c=3; K=8 |
| 0 | planning_decision | eligible ; choose None |
| 0 | queue_snapshot | waiting a2j0; active None |
| 1 | request_expired | a2j0: infeasible_at_arrival |
| 1 | job_closed | a2j0: correct=False, job loss=11 |
| 1 | proposal | a0j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 6; c=1; K=0 |
| 1 | proposal | a1j0: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 6; c=1; K=8 |
| 1 | planning_decision | eligible a0j0(d=6,p=0.146,G_at_completion=3.000), a1j0(d=6,p=0.146,G_at_completion=11.000); choose a1j0 |
| 1 | queue_snapshot | waiting a0j0; active {'finish': 3, 'job_id': 'a1j0', 'start': 1} |
| 2 | queue_snapshot | waiting a0j0; active {'finish': 3, 'job_id': 'a1j0', 'start': 1} |
| 3 | review_completed | a1j0: replace_filter, applied=True, corrected=False |
| 3 | planning_decision | eligible a0j0(d=6,p=0.146,G_at_completion=1.000); choose a0j0 |
| 3 | queue_snapshot | waiting ; active {'finish': 5, 'job_id': 'a0j0', 'start': 3} |
| 4 | queue_snapshot | waiting ; active {'finish': 5, 'job_id': 'a0j0', 'start': 3} |
| 5 | review_completed | a0j0: reset_sensor, applied=True, corrected=True |
| 5 | planning_decision | eligible ; choose None |
| 5 | queue_snapshot | waiting ; active None |
| 6 | job_closed | a0j0: correct=True, job loss=4 |
| 6 | job_closed | a1j0: correct=True, job loss=0 |
| 6 | proposal | a1j1: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 8; c=3; K=0 |
| 6 | planning_decision | eligible ; choose None |
| 6 | queue_snapshot | waiting a1j1; active None |
| 7 | proposal | a0j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 12; c=1; K=0 |
| 7 | proposal | a2j1: clues sensor/filter; first replace_filter; second reset_sensor; initial wrong (offline label); p=0.1837; deadline 8; c=3; K=8 |
| 7 | planning_decision | eligible a0j1(d=12,p=0.146,G_at_completion=3.000); choose a0j1 |
| 7 | queue_snapshot | waiting a1j1, a2j1; active {'finish': 9, 'job_id': 'a0j1', 'start': 7} |
| 8 | request_expired | a1j1: infeasible_at_arrival |
| 8 | job_closed | a1j1: correct=True, job loss=0 |
| 8 | request_expired | a2j1: infeasible_at_arrival |
| 8 | job_closed | a2j1: correct=False, job loss=11 |
| 8 | queue_snapshot | waiting ; active {'finish': 9, 'job_id': 'a0j1', 'start': 7} |
| 9 | review_completed | a0j1: replace_filter, applied=True, corrected=False |
| 9 | planning_decision | eligible ; choose None |
| 9 | queue_snapshot | waiting ; active None |
| 10 | planning_decision | eligible ; choose None |
| 10 | queue_snapshot | waiting ; active None |
| 11 | planning_decision | eligible ; choose None |
| 11 | queue_snapshot | waiting ; active None |
| 12 | job_closed | a0j1: correct=True, job loss=0 |
| 12 | queue_snapshot | waiting ; active None |
