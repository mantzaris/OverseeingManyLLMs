# Paired queue example

First numerical seed with search lower loss than greedy at two ticks.

Offline scoring view: hidden faults and initial correctness below were not supplied to schedulers.

## capacity/larger/12001/a6/s2/frozen/delay/lambda0

Loss 32.0; incorrect closures 4; corrections 4.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a2j0: clues sensor/sensor; first reset_sensor; second reset_sensor; initial wrong (offline label); p=0.1461; deadline 2; c=0; K=0 |
| 0 | proposal | a3j0: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 4; c=0; K=4 |
| 0 | proposal | a4j0: clues sensor/filter; first replace_filter; second reset_sensor; initial wrong (offline label); p=0.1837; deadline 4; c=1; K=0 |
| 0 | planning_decision | eligible a3j0(d=4,p=0.146,G_at_completion=4.000), a4j0(d=4,p=0.184,G_at_completion=2.000); choose a4j0 |
| 0 | queue_snapshot | waiting a2j0, a3j0; active {'finish': 2, 'job_id': 'a4j0', 'start': 0} |
| 1 | proposal | a0j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 3; c=0; K=12 |
| 1 | proposal | a1j0: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 7; c=0; K=8 |
| 1 | proposal | a5j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 7; c=1; K=12 |
| 1 | queue_snapshot | waiting a0j0, a1j0, a2j0, a3j0, a5j0; active {'finish': 2, 'job_id': 'a4j0', 'start': 0} |
| 2 | review_completed | a4j0: reset_sensor, applied=True, corrected=True |
| 2 | request_expired | a2j0: zero_value |
| 2 | job_closed | a2j0: correct=False, job loss=0 |
| 2 | planning_decision | eligible a3j0(d=4,p=0.146,G_at_completion=4.000), a1j0(d=7,p=0.146,G_at_completion=8.000), a5j0(d=7,p=0.146,G_at_completion=15.000); choose a5j0 |
| 2 | queue_snapshot | waiting a0j0, a1j0, a3j0; active {'finish': 4, 'job_id': 'a5j0', 'start': 2} |
| 3 | request_expired | a0j0: opportunity_lost_while_waiting |
| 3 | job_closed | a0j0: correct=False, job loss=12 |
| 3 | queue_snapshot | waiting a1j0, a3j0; active {'finish': 4, 'job_id': 'a5j0', 'start': 2} |
| 4 | review_completed | a5j0: reset_sensor, applied=True, corrected=True |
| 4 | request_expired | a3j0: opportunity_lost_while_waiting |
| 4 | job_closed | a3j0: correct=True, job loss=0 |
| 4 | job_closed | a4j0: correct=True, job loss=2 |
| 4 | planning_decision | eligible a1j0(d=7,p=0.146,G_at_completion=8.000); choose a1j0 |
| 4 | queue_snapshot | waiting ; active {'finish': 6, 'job_id': 'a1j0', 'start': 4} |
| 5 | queue_snapshot | waiting ; active {'finish': 6, 'job_id': 'a1j0', 'start': 4} |
| 6 | review_completed | a1j0: reset_sensor, applied=True, corrected=False |
| 6 | planning_decision | eligible ; choose None |
| 6 | queue_snapshot | waiting ; active None |
| 7 | job_closed | a1j0: correct=True, job loss=0 |
| 7 | job_closed | a5j0: correct=True, job loss=3 |
| 7 | planning_decision | eligible ; choose None |
| 7 | queue_snapshot | waiting ; active None |
| 8 | proposal | a2j1: clues sensor/filter; first replace_filter; second reset_sensor; initial wrong (offline label); p=0.1837; deadline 12; c=1; K=0 |
| 8 | proposal | a3j1: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 14; c=3; K=0 |
| 8 | planning_decision | eligible a2j1(d=12,p=0.184,G_at_completion=2.000), a3j1(d=14,p=0.146,G_at_completion=12.000); choose a3j1 |
| 8 | queue_snapshot | waiting a2j1; active {'finish': 10, 'job_id': 'a3j1', 'start': 8} |
| 9 | proposal | a0j1: clues filter/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 15; c=3; K=4 |
| 9 | proposal | a1j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 11; c=0; K=12 |
| 9 | proposal | a4j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 15; c=0; K=8 |
| 9 | proposal | a5j1: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 13; c=1; K=0 |
| 9 | queue_snapshot | waiting a0j1, a1j1, a2j1, a4j1, a5j1; active {'finish': 10, 'job_id': 'a3j1', 'start': 8} |
| 10 | review_completed | a3j1: reset_sensor, applied=True, corrected=False |
| 10 | planning_decision | eligible a0j1(d=15,p=0.146,G_at_completion=13.000), a4j1(d=15,p=0.146,G_at_completion=8.000), a5j1(d=13,p=0.146,G_at_completion=1.000); choose a0j1 |
| 10 | queue_snapshot | waiting a1j1, a2j1, a4j1, a5j1; active {'finish': 12, 'job_id': 'a0j1', 'start': 10} |
| 11 | request_expired | a1j1: opportunity_lost_while_waiting |
| 11 | job_closed | a1j1: correct=True, job loss=0 |
| 11 | queue_snapshot | waiting a2j1, a4j1, a5j1; active {'finish': 12, 'job_id': 'a0j1', 'start': 10} |
| 12 | review_completed | a0j1: reset_sensor, applied=True, corrected=True |
| 12 | request_expired | a2j1: opportunity_lost_while_waiting |
| 12 | job_closed | a2j1: correct=False, job loss=4 |
| 12 | planning_decision | eligible a4j1(d=15,p=0.146,G_at_completion=8.000); choose a4j1 |
| 12 | queue_snapshot | waiting a5j1; active {'finish': 14, 'job_id': 'a4j1', 'start': 12} |
| 13 | request_expired | a5j1: opportunity_lost_while_waiting |
| 13 | job_closed | a5j1: correct=True, job loss=0 |
| 13 | queue_snapshot | waiting ; active {'finish': 14, 'job_id': 'a4j1', 'start': 12} |
| 14 | review_completed | a4j1: replace_filter, applied=True, corrected=False |
| 14 | job_closed | a3j1: correct=True, job loss=0 |
| 14 | planning_decision | eligible ; choose None |
| 14 | queue_snapshot | waiting ; active None |
| 15 | job_closed | a0j1: correct=True, job loss=9 |
| 15 | job_closed | a4j1: correct=True, job loss=0 |
| 15 | planning_decision | eligible ; choose None |
| 15 | queue_snapshot | waiting ; active None |
| 16 | proposal | a2j2: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 20; c=0; K=8 |
| 16 | planning_decision | eligible a2j2(d=20,p=0.146,G_at_completion=8.000); choose a2j2 |
| 16 | queue_snapshot | waiting ; active {'finish': 18, 'job_id': 'a2j2', 'start': 16} |
| 17 | proposal | a0j2: clues sensor/filter; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 19; c=3; K=4 |
| 17 | proposal | a1j2: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 23; c=1; K=4 |
| 17 | proposal | a3j2: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 19; c=1; K=0 |
| 17 | proposal | a4j2: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 19; c=3; K=0 |
| 17 | proposal | a5j2: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 19; c=1; K=12 |
| 17 | queue_snapshot | waiting a0j2, a1j2, a3j2, a4j2, a5j2; active {'finish': 18, 'job_id': 'a2j2', 'start': 16} |
| 18 | review_completed | a2j2: reset_sensor, applied=True, corrected=True |
| 18 | planning_decision | eligible a1j2(d=23,p=0.146,G_at_completion=7.000); choose a1j2 |
| 18 | queue_snapshot | waiting a0j2, a3j2, a4j2, a5j2; active {'finish': 20, 'job_id': 'a1j2', 'start': 18} |
| 19 | request_expired | a0j2: opportunity_lost_while_waiting |
| 19 | job_closed | a0j2: correct=True, job loss=0 |
| 19 | request_expired | a3j2: infeasible_at_arrival |
| 19 | job_closed | a3j2: correct=False, job loss=2 |
| 19 | request_expired | a4j2: infeasible_at_arrival |
| 19 | job_closed | a4j2: correct=True, job loss=0 |
| 19 | request_expired | a5j2: opportunity_lost_while_waiting |
| 19 | job_closed | a5j2: correct=True, job loss=0 |
| 19 | queue_snapshot | waiting ; active {'finish': 20, 'job_id': 'a1j2', 'start': 18} |
| 20 | review_completed | a1j2: reset_sensor, applied=True, corrected=False |
| 20 | job_closed | a2j2: correct=True, job loss=0 |
| 20 | planning_decision | eligible ; choose None |
| 20 | queue_snapshot | waiting ; active None |
| 21 | planning_decision | eligible ; choose None |
| 21 | queue_snapshot | waiting ; active None |
| 22 | planning_decision | eligible ; choose None |
| 22 | queue_snapshot | waiting ; active None |
| 23 | job_closed | a1j2: correct=True, job loss=0 |
| 23 | planning_decision | eligible ; choose None |
| 23 | queue_snapshot | waiting ; active None |
| 24 | queue_snapshot | waiting ; active None |

## capacity/larger/12001/a6/s2/frozen/greedy/lambda0

Loss 34.0; incorrect closures 5; corrections 3.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a2j0: clues sensor/sensor; first reset_sensor; second reset_sensor; initial wrong (offline label); p=0.1461; deadline 2; c=0; K=0 |
| 0 | proposal | a3j0: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 4; c=0; K=4 |
| 0 | proposal | a4j0: clues sensor/filter; first replace_filter; second reset_sensor; initial wrong (offline label); p=0.1837; deadline 4; c=1; K=0 |
| 0 | planning_decision | eligible a3j0(d=4,p=0.146,G_at_completion=4.000), a4j0(d=4,p=0.184,G_at_completion=2.000); choose a3j0 |
| 0 | queue_snapshot | waiting a2j0, a4j0; active {'finish': 2, 'job_id': 'a3j0', 'start': 0} |
| 1 | proposal | a0j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 3; c=0; K=12 |
| 1 | proposal | a1j0: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 7; c=0; K=8 |
| 1 | proposal | a5j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 7; c=1; K=12 |
| 1 | queue_snapshot | waiting a0j0, a1j0, a2j0, a4j0, a5j0; active {'finish': 2, 'job_id': 'a3j0', 'start': 0} |
| 2 | review_completed | a3j0: replace_filter, applied=True, corrected=False |
| 2 | request_expired | a2j0: zero_value |
| 2 | job_closed | a2j0: correct=False, job loss=0 |
| 2 | planning_decision | eligible a1j0(d=7,p=0.146,G_at_completion=8.000), a5j0(d=7,p=0.146,G_at_completion=15.000); choose a5j0 |
| 2 | queue_snapshot | waiting a0j0, a1j0, a4j0; active {'finish': 4, 'job_id': 'a5j0', 'start': 2} |
| 3 | request_expired | a0j0: opportunity_lost_while_waiting |
| 3 | job_closed | a0j0: correct=False, job loss=12 |
| 3 | queue_snapshot | waiting a1j0, a4j0; active {'finish': 4, 'job_id': 'a5j0', 'start': 2} |
| 4 | review_completed | a5j0: reset_sensor, applied=True, corrected=True |
| 4 | job_closed | a3j0: correct=True, job loss=0 |
| 4 | request_expired | a4j0: opportunity_lost_while_waiting |
| 4 | job_closed | a4j0: correct=False, job loss=4 |
| 4 | planning_decision | eligible a1j0(d=7,p=0.146,G_at_completion=8.000); choose a1j0 |
| 4 | queue_snapshot | waiting ; active {'finish': 6, 'job_id': 'a1j0', 'start': 4} |
| 5 | queue_snapshot | waiting ; active {'finish': 6, 'job_id': 'a1j0', 'start': 4} |
| 6 | review_completed | a1j0: reset_sensor, applied=True, corrected=False |
| 6 | planning_decision | eligible ; choose None |
| 6 | queue_snapshot | waiting ; active None |
| 7 | job_closed | a1j0: correct=True, job loss=0 |
| 7 | job_closed | a5j0: correct=True, job loss=3 |
| 7 | planning_decision | eligible ; choose None |
| 7 | queue_snapshot | waiting ; active None |
| 8 | proposal | a2j1: clues sensor/filter; first replace_filter; second reset_sensor; initial wrong (offline label); p=0.1837; deadline 12; c=1; K=0 |
| 8 | proposal | a3j1: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 14; c=3; K=0 |
| 8 | planning_decision | eligible a2j1(d=12,p=0.184,G_at_completion=2.000), a3j1(d=14,p=0.146,G_at_completion=12.000); choose a3j1 |
| 8 | queue_snapshot | waiting a2j1; active {'finish': 10, 'job_id': 'a3j1', 'start': 8} |
| 9 | proposal | a0j1: clues filter/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 15; c=3; K=4 |
| 9 | proposal | a1j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 11; c=0; K=12 |
| 9 | proposal | a4j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 15; c=0; K=8 |
| 9 | proposal | a5j1: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 13; c=1; K=0 |
| 9 | queue_snapshot | waiting a0j1, a1j1, a2j1, a4j1, a5j1; active {'finish': 10, 'job_id': 'a3j1', 'start': 8} |
| 10 | review_completed | a3j1: reset_sensor, applied=True, corrected=False |
| 10 | planning_decision | eligible a0j1(d=15,p=0.146,G_at_completion=13.000), a4j1(d=15,p=0.146,G_at_completion=8.000), a5j1(d=13,p=0.146,G_at_completion=1.000); choose a0j1 |
| 10 | queue_snapshot | waiting a1j1, a2j1, a4j1, a5j1; active {'finish': 12, 'job_id': 'a0j1', 'start': 10} |
| 11 | request_expired | a1j1: opportunity_lost_while_waiting |
| 11 | job_closed | a1j1: correct=True, job loss=0 |
| 11 | queue_snapshot | waiting a2j1, a4j1, a5j1; active {'finish': 12, 'job_id': 'a0j1', 'start': 10} |
| 12 | review_completed | a0j1: reset_sensor, applied=True, corrected=True |
| 12 | request_expired | a2j1: opportunity_lost_while_waiting |
| 12 | job_closed | a2j1: correct=False, job loss=4 |
| 12 | planning_decision | eligible a4j1(d=15,p=0.146,G_at_completion=8.000); choose a4j1 |
| 12 | queue_snapshot | waiting a5j1; active {'finish': 14, 'job_id': 'a4j1', 'start': 12} |
| 13 | request_expired | a5j1: opportunity_lost_while_waiting |
| 13 | job_closed | a5j1: correct=True, job loss=0 |
| 13 | queue_snapshot | waiting ; active {'finish': 14, 'job_id': 'a4j1', 'start': 12} |
| 14 | review_completed | a4j1: replace_filter, applied=True, corrected=False |
| 14 | job_closed | a3j1: correct=True, job loss=0 |
| 14 | planning_decision | eligible ; choose None |
| 14 | queue_snapshot | waiting ; active None |
| 15 | job_closed | a0j1: correct=True, job loss=9 |
| 15 | job_closed | a4j1: correct=True, job loss=0 |
| 15 | planning_decision | eligible ; choose None |
| 15 | queue_snapshot | waiting ; active None |
| 16 | proposal | a2j2: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 20; c=0; K=8 |
| 16 | planning_decision | eligible a2j2(d=20,p=0.146,G_at_completion=8.000); choose a2j2 |
| 16 | queue_snapshot | waiting ; active {'finish': 18, 'job_id': 'a2j2', 'start': 16} |
| 17 | proposal | a0j2: clues sensor/filter; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 19; c=3; K=4 |
| 17 | proposal | a1j2: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 23; c=1; K=4 |
| 17 | proposal | a3j2: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 19; c=1; K=0 |
| 17 | proposal | a4j2: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 19; c=3; K=0 |
| 17 | proposal | a5j2: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 19; c=1; K=12 |
| 17 | queue_snapshot | waiting a0j2, a1j2, a3j2, a4j2, a5j2; active {'finish': 18, 'job_id': 'a2j2', 'start': 16} |
| 18 | review_completed | a2j2: reset_sensor, applied=True, corrected=True |
| 18 | planning_decision | eligible a1j2(d=23,p=0.146,G_at_completion=7.000); choose a1j2 |
| 18 | queue_snapshot | waiting a0j2, a3j2, a4j2, a5j2; active {'finish': 20, 'job_id': 'a1j2', 'start': 18} |
| 19 | request_expired | a0j2: opportunity_lost_while_waiting |
| 19 | job_closed | a0j2: correct=True, job loss=0 |
| 19 | request_expired | a3j2: infeasible_at_arrival |
| 19 | job_closed | a3j2: correct=False, job loss=2 |
| 19 | request_expired | a4j2: infeasible_at_arrival |
| 19 | job_closed | a4j2: correct=True, job loss=0 |
| 19 | request_expired | a5j2: opportunity_lost_while_waiting |
| 19 | job_closed | a5j2: correct=True, job loss=0 |
| 19 | queue_snapshot | waiting ; active {'finish': 20, 'job_id': 'a1j2', 'start': 18} |
| 20 | review_completed | a1j2: reset_sensor, applied=True, corrected=False |
| 20 | job_closed | a2j2: correct=True, job loss=0 |
| 20 | planning_decision | eligible ; choose None |
| 20 | queue_snapshot | waiting ; active None |
| 21 | planning_decision | eligible ; choose None |
| 21 | queue_snapshot | waiting ; active None |
| 22 | planning_decision | eligible ; choose None |
| 22 | queue_snapshot | waiting ; active None |
| 23 | job_closed | a1j2: correct=True, job loss=0 |
| 23 | planning_decision | eligible ; choose None |
| 23 | queue_snapshot | waiting ; active None |
| 24 | queue_snapshot | waiting ; active None |
