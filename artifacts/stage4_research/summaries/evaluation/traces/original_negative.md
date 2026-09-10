# Paired queue example

First numerical seed with search higher loss than greedy at two ticks.

Offline scoring view: hidden faults and initial correctness below were not supplied to schedulers.

## replication/original/10000/a3/s2/frozen/delay/lambda0

Loss 33.0; incorrect closures 2; corrections 2.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a1j0: clues sensor/filter; first replace_filter; second reset_sensor; initial wrong (offline label); p=0.1837; deadline 1; c=0; K=8 |
| 0 | proposal | a2j0: clues sensor/sensor; first reset_sensor; second reset_sensor; initial wrong (offline label); p=0.1461; deadline 2; c=1; K=8 |
| 0 | planning_decision | eligible a2j0(d=2,p=0.146,G_at_completion=8.000); choose a2j0 |
| 0 | queue_snapshot | waiting a1j0; active {'finish': 2, 'job_id': 'a2j0', 'start': 0} |
| 1 | request_expired | a1j0: infeasible_at_arrival |
| 1 | job_closed | a1j0: correct=False, job loss=8 |
| 1 | proposal | a0j0: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 6; c=3; K=0 |
| 1 | queue_snapshot | waiting a0j0; active {'finish': 2, 'job_id': 'a2j0', 'start': 0} |
| 2 | review_completed | a2j0: replace_filter, applied=True, corrected=True |
| 2 | job_closed | a2j0: correct=True, job loss=2 |
| 2 | planning_decision | eligible a0j0(d=6,p=0.146,G_at_completion=6.000); choose a0j0 |
| 2 | queue_snapshot | waiting ; active {'finish': 4, 'job_id': 'a0j0', 'start': 2} |
| 3 | queue_snapshot | waiting ; active {'finish': 4, 'job_id': 'a0j0', 'start': 2} |
| 4 | review_completed | a0j0: replace_filter, applied=True, corrected=False |
| 4 | planning_decision | eligible ; choose None |
| 4 | queue_snapshot | waiting ; active None |
| 5 | planning_decision | eligible ; choose None |
| 5 | queue_snapshot | waiting ; active None |
| 6 | job_closed | a0j0: correct=True, job loss=0 |
| 6 | planning_decision | eligible ; choose None |
| 6 | queue_snapshot | waiting ; active None |
| 7 | proposal | a0j1: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 8; c=3; K=8 |
| 7 | proposal | a1j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 9; c=0; K=8 |
| 7 | proposal | a2j1: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 12; c=3; K=8 |
| 7 | planning_decision | eligible a1j1(d=9,p=0.146,G_at_completion=8.000), a2j1(d=12,p=0.146,G_at_completion=17.000); choose a1j1 |
| 7 | queue_snapshot | waiting a0j1, a2j1; active {'finish': 9, 'job_id': 'a1j1', 'start': 7} |
| 8 | request_expired | a0j1: infeasible_at_arrival |
| 8 | job_closed | a0j1: correct=False, job loss=11 |
| 8 | queue_snapshot | waiting a2j1; active {'finish': 9, 'job_id': 'a1j1', 'start': 7} |
| 9 | review_completed | a1j1: replace_filter, applied=True, corrected=False |
| 9 | job_closed | a1j1: correct=True, job loss=0 |
| 9 | planning_decision | eligible a2j1(d=12,p=0.146,G_at_completion=11.000); choose a2j1 |
| 9 | queue_snapshot | waiting ; active {'finish': 11, 'job_id': 'a2j1', 'start': 9} |
| 10 | queue_snapshot | waiting ; active {'finish': 11, 'job_id': 'a2j1', 'start': 9} |
| 11 | review_completed | a2j1: reset_sensor, applied=True, corrected=True |
| 11 | planning_decision | eligible ; choose None |
| 11 | queue_snapshot | waiting ; active None |
| 12 | job_closed | a2j1: correct=True, job loss=12 |
| 12 | queue_snapshot | waiting ; active None |

## replication/original/10000/a3/s2/frozen/greedy/lambda0

Loss 27.0; incorrect closures 2; corrections 2.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a1j0: clues sensor/filter; first replace_filter; second reset_sensor; initial wrong (offline label); p=0.1837; deadline 1; c=0; K=8 |
| 0 | proposal | a2j0: clues sensor/sensor; first reset_sensor; second reset_sensor; initial wrong (offline label); p=0.1461; deadline 2; c=1; K=8 |
| 0 | planning_decision | eligible a2j0(d=2,p=0.146,G_at_completion=8.000); choose a2j0 |
| 0 | queue_snapshot | waiting a1j0; active {'finish': 2, 'job_id': 'a2j0', 'start': 0} |
| 1 | request_expired | a1j0: infeasible_at_arrival |
| 1 | job_closed | a1j0: correct=False, job loss=8 |
| 1 | proposal | a0j0: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 6; c=3; K=0 |
| 1 | queue_snapshot | waiting a0j0; active {'finish': 2, 'job_id': 'a2j0', 'start': 0} |
| 2 | review_completed | a2j0: replace_filter, applied=True, corrected=True |
| 2 | job_closed | a2j0: correct=True, job loss=2 |
| 2 | planning_decision | eligible a0j0(d=6,p=0.146,G_at_completion=6.000); choose a0j0 |
| 2 | queue_snapshot | waiting ; active {'finish': 4, 'job_id': 'a0j0', 'start': 2} |
| 3 | queue_snapshot | waiting ; active {'finish': 4, 'job_id': 'a0j0', 'start': 2} |
| 4 | review_completed | a0j0: replace_filter, applied=True, corrected=False |
| 4 | planning_decision | eligible ; choose None |
| 4 | queue_snapshot | waiting ; active None |
| 5 | planning_decision | eligible ; choose None |
| 5 | queue_snapshot | waiting ; active None |
| 6 | job_closed | a0j0: correct=True, job loss=0 |
| 6 | planning_decision | eligible ; choose None |
| 6 | queue_snapshot | waiting ; active None |
| 7 | proposal | a0j1: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 8; c=3; K=8 |
| 7 | proposal | a1j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 9; c=0; K=8 |
| 7 | proposal | a2j1: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 12; c=3; K=8 |
| 7 | planning_decision | eligible a1j1(d=9,p=0.146,G_at_completion=8.000), a2j1(d=12,p=0.146,G_at_completion=17.000); choose a2j1 |
| 7 | queue_snapshot | waiting a0j1, a1j1; active {'finish': 9, 'job_id': 'a2j1', 'start': 7} |
| 8 | request_expired | a0j1: infeasible_at_arrival |
| 8 | job_closed | a0j1: correct=False, job loss=11 |
| 8 | queue_snapshot | waiting a1j1; active {'finish': 9, 'job_id': 'a2j1', 'start': 7} |
| 9 | review_completed | a2j1: reset_sensor, applied=True, corrected=True |
| 9 | request_expired | a1j1: opportunity_lost_while_waiting |
| 9 | job_closed | a1j1: correct=True, job loss=0 |
| 9 | planning_decision | eligible ; choose None |
| 9 | queue_snapshot | waiting ; active None |
| 10 | planning_decision | eligible ; choose None |
| 10 | queue_snapshot | waiting ; active None |
| 11 | planning_decision | eligible ; choose None |
| 11 | queue_snapshot | waiting ; active None |
| 12 | job_closed | a2j1: correct=True, job loss=6 |
| 12 | queue_snapshot | waiting ; active None |
