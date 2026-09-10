# Paired queue example

First numerical seed with search lower loss than greedy at two ticks.

Offline scoring view: hidden faults and initial correctness below were not supplied to schedulers.

## replication/competition/11000/a3/s2/frozen/delay/lambda0

Loss 4.0; incorrect closures 1; corrections 1.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a0j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 2; c=0; K=8 |
| 0 | proposal | a1j0: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 4; c=0; K=12 |
| 0 | proposal | a2j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 5; c=0; K=4 |
| 0 | planning_decision | eligible a0j0(d=2,p=0.146,G_at_completion=8.000), a1j0(d=4,p=0.146,G_at_completion=12.000), a2j0(d=5,p=0.146,G_at_completion=4.000); choose a0j0 |
| 0 | queue_snapshot | waiting a1j0, a2j0; active {'finish': 2, 'job_id': 'a0j0', 'start': 0} |
| 1 | queue_snapshot | waiting a1j0, a2j0; active {'finish': 2, 'job_id': 'a0j0', 'start': 0} |
| 2 | review_completed | a0j0: reset_sensor, applied=True, corrected=True |
| 2 | job_closed | a0j0: correct=True, job loss=0 |
| 2 | planning_decision | eligible a1j0(d=4,p=0.146,G_at_completion=12.000), a2j0(d=5,p=0.146,G_at_completion=4.000); choose a1j0 |
| 2 | queue_snapshot | waiting a2j0; active {'finish': 4, 'job_id': 'a1j0', 'start': 2} |
| 3 | queue_snapshot | waiting a2j0; active {'finish': 4, 'job_id': 'a1j0', 'start': 2} |
| 4 | review_completed | a1j0: replace_filter, applied=True, corrected=False |
| 4 | job_closed | a1j0: correct=True, job loss=0 |
| 4 | planning_decision | eligible ; choose None |
| 4 | queue_snapshot | waiting a2j0; active None |
| 5 | request_expired | a2j0: opportunity_lost_while_waiting |
| 5 | job_closed | a2j0: correct=False, job loss=4 |
| 5 | planning_decision | eligible ; choose None |
| 5 | queue_snapshot | waiting ; active None |
| 6 | proposal | a0j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 8; c=0; K=12 |
| 6 | proposal | a1j1: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 10; c=0; K=4 |
| 6 | proposal | a2j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 11; c=0; K=8 |
| 6 | planning_decision | eligible a0j1(d=8,p=0.146,G_at_completion=12.000), a1j1(d=10,p=0.146,G_at_completion=4.000), a2j1(d=11,p=0.146,G_at_completion=8.000); choose a0j1 |
| 6 | queue_snapshot | waiting a1j1, a2j1; active {'finish': 8, 'job_id': 'a0j1', 'start': 6} |
| 7 | queue_snapshot | waiting a1j1, a2j1; active {'finish': 8, 'job_id': 'a0j1', 'start': 6} |
| 8 | review_completed | a0j1: replace_filter, applied=True, corrected=False |
| 8 | job_closed | a0j1: correct=True, job loss=0 |
| 8 | planning_decision | eligible a1j1(d=10,p=0.146,G_at_completion=4.000), a2j1(d=11,p=0.146,G_at_completion=8.000); choose a2j1 |
| 8 | queue_snapshot | waiting a1j1; active {'finish': 10, 'job_id': 'a2j1', 'start': 8} |
| 9 | queue_snapshot | waiting a1j1; active {'finish': 10, 'job_id': 'a2j1', 'start': 8} |
| 10 | review_completed | a2j1: replace_filter, applied=True, corrected=False |
| 10 | request_expired | a1j1: opportunity_lost_while_waiting |
| 10 | job_closed | a1j1: correct=True, job loss=0 |
| 10 | planning_decision | eligible ; choose None |
| 10 | queue_snapshot | waiting ; active None |
| 11 | job_closed | a2j1: correct=True, job loss=0 |
| 11 | planning_decision | eligible ; choose None |
| 11 | queue_snapshot | waiting ; active None |
| 12 | queue_snapshot | waiting ; active None |

## replication/competition/11000/a3/s2/frozen/greedy/lambda0

Loss 8.0; incorrect closures 1; corrections 1.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a0j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 2; c=0; K=8 |
| 0 | proposal | a1j0: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 4; c=0; K=12 |
| 0 | proposal | a2j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 5; c=0; K=4 |
| 0 | planning_decision | eligible a0j0(d=2,p=0.146,G_at_completion=8.000), a1j0(d=4,p=0.146,G_at_completion=12.000), a2j0(d=5,p=0.146,G_at_completion=4.000); choose a1j0 |
| 0 | queue_snapshot | waiting a0j0, a2j0; active {'finish': 2, 'job_id': 'a1j0', 'start': 0} |
| 1 | queue_snapshot | waiting a0j0, a2j0; active {'finish': 2, 'job_id': 'a1j0', 'start': 0} |
| 2 | review_completed | a1j0: replace_filter, applied=True, corrected=False |
| 2 | request_expired | a0j0: opportunity_lost_while_waiting |
| 2 | job_closed | a0j0: correct=False, job loss=8 |
| 2 | planning_decision | eligible a2j0(d=5,p=0.146,G_at_completion=4.000); choose a2j0 |
| 2 | queue_snapshot | waiting ; active {'finish': 4, 'job_id': 'a2j0', 'start': 2} |
| 3 | queue_snapshot | waiting ; active {'finish': 4, 'job_id': 'a2j0', 'start': 2} |
| 4 | review_completed | a2j0: reset_sensor, applied=True, corrected=True |
| 4 | job_closed | a1j0: correct=True, job loss=0 |
| 4 | planning_decision | eligible ; choose None |
| 4 | queue_snapshot | waiting ; active None |
| 5 | job_closed | a2j0: correct=True, job loss=0 |
| 5 | planning_decision | eligible ; choose None |
| 5 | queue_snapshot | waiting ; active None |
| 6 | proposal | a0j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 8; c=0; K=12 |
| 6 | proposal | a1j1: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 10; c=0; K=4 |
| 6 | proposal | a2j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 11; c=0; K=8 |
| 6 | planning_decision | eligible a0j1(d=8,p=0.146,G_at_completion=12.000), a1j1(d=10,p=0.146,G_at_completion=4.000), a2j1(d=11,p=0.146,G_at_completion=8.000); choose a0j1 |
| 6 | queue_snapshot | waiting a1j1, a2j1; active {'finish': 8, 'job_id': 'a0j1', 'start': 6} |
| 7 | queue_snapshot | waiting a1j1, a2j1; active {'finish': 8, 'job_id': 'a0j1', 'start': 6} |
| 8 | review_completed | a0j1: replace_filter, applied=True, corrected=False |
| 8 | job_closed | a0j1: correct=True, job loss=0 |
| 8 | planning_decision | eligible a1j1(d=10,p=0.146,G_at_completion=4.000), a2j1(d=11,p=0.146,G_at_completion=8.000); choose a2j1 |
| 8 | queue_snapshot | waiting a1j1; active {'finish': 10, 'job_id': 'a2j1', 'start': 8} |
| 9 | queue_snapshot | waiting a1j1; active {'finish': 10, 'job_id': 'a2j1', 'start': 8} |
| 10 | review_completed | a2j1: replace_filter, applied=True, corrected=False |
| 10 | request_expired | a1j1: opportunity_lost_while_waiting |
| 10 | job_closed | a1j1: correct=True, job loss=0 |
| 10 | planning_decision | eligible ; choose None |
| 10 | queue_snapshot | waiting ; active None |
| 11 | job_closed | a2j1: correct=True, job loss=0 |
| 11 | planning_decision | eligible ; choose None |
| 11 | queue_snapshot | waiting ; active None |
| 12 | queue_snapshot | waiting ; active None |
