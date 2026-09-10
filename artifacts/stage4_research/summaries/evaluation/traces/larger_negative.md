# Paired queue example

First numerical seed with search higher loss than greedy at two ticks.

Offline scoring view: hidden faults and initial correctness below were not supplied to schedulers.

## capacity/larger/12006/a6/s2/frozen/delay/lambda0

Loss 42.0; incorrect closures 3; corrections 2.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a0j0: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 4; c=0; K=8 |
| 0 | proposal | a2j0: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 2; c=3; K=12 |
| 0 | planning_decision | eligible a0j0(d=4,p=0.146,G_at_completion=8.000), a2j0(d=2,p=0.146,G_at_completion=12.000); choose a2j0 |
| 0 | queue_snapshot | waiting a0j0; active {'finish': 2, 'job_id': 'a2j0', 'start': 0} |
| 1 | proposal | a1j0: clues filter/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 3; c=0; K=8 |
| 1 | proposal | a3j0: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 5; c=3; K=0 |
| 1 | proposal | a4j0: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 5; c=0; K=4 |
| 1 | proposal | a5j0: clues sensor/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 7; c=1; K=8 |
| 1 | queue_snapshot | waiting a0j0, a1j0, a3j0, a4j0, a5j0; active {'finish': 2, 'job_id': 'a2j0', 'start': 0} |
| 2 | review_completed | a2j0: replace_filter, applied=True, corrected=False |
| 2 | job_closed | a2j0: correct=True, job loss=0 |
| 2 | planning_decision | eligible a0j0(d=4,p=0.146,G_at_completion=8.000), a3j0(d=5,p=0.146,G_at_completion=3.000), a4j0(d=5,p=0.146,G_at_completion=4.000), a5j0(d=7,p=0.146,G_at_completion=11.000); choose a0j0 |
| 2 | queue_snapshot | waiting a1j0, a3j0, a4j0, a5j0; active {'finish': 4, 'job_id': 'a0j0', 'start': 2} |
| 3 | request_expired | a1j0: opportunity_lost_while_waiting |
| 3 | job_closed | a1j0: correct=False, job loss=8 |
| 3 | queue_snapshot | waiting a3j0, a4j0, a5j0; active {'finish': 4, 'job_id': 'a0j0', 'start': 2} |
| 4 | review_completed | a0j0: replace_filter, applied=True, corrected=False |
| 4 | job_closed | a0j0: correct=True, job loss=0 |
| 4 | planning_decision | eligible a5j0(d=7,p=0.146,G_at_completion=9.000); choose a5j0 |
| 4 | queue_snapshot | waiting a3j0, a4j0; active {'finish': 6, 'job_id': 'a5j0', 'start': 4} |
| 5 | request_expired | a3j0: opportunity_lost_while_waiting |
| 5 | job_closed | a3j0: correct=True, job loss=0 |
| 5 | request_expired | a4j0: opportunity_lost_while_waiting |
| 5 | job_closed | a4j0: correct=False, job loss=4 |
| 5 | queue_snapshot | waiting ; active {'finish': 6, 'job_id': 'a5j0', 'start': 4} |
| 6 | review_completed | a5j0: replace_filter, applied=True, corrected=False |
| 6 | planning_decision | eligible ; choose None |
| 6 | queue_snapshot | waiting ; active None |
| 7 | job_closed | a5j0: correct=True, job loss=0 |
| 7 | planning_decision | eligible ; choose None |
| 7 | queue_snapshot | waiting ; active None |
| 8 | proposal | a1j1: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 10; c=1; K=8 |
| 8 | proposal | a2j1: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 14; c=3; K=12 |
| 8 | proposal | a3j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 14; c=0; K=0 |
| 8 | proposal | a5j1: clues filter/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 10; c=1; K=8 |
| 8 | planning_decision | eligible a1j1(d=10,p=0.146,G_at_completion=8.000), a2j1(d=14,p=0.146,G_at_completion=24.000), a5j1(d=10,p=0.146,G_at_completion=8.000); choose a1j1 |
| 8 | queue_snapshot | waiting a2j1, a3j1, a5j1; active {'finish': 10, 'job_id': 'a1j1', 'start': 8} |
| 9 | proposal | a0j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 11; c=1; K=8 |
| 9 | proposal | a4j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 13; c=3; K=12 |
| 9 | queue_snapshot | waiting a0j1, a2j1, a3j1, a4j1, a5j1; active {'finish': 10, 'job_id': 'a1j1', 'start': 8} |
| 10 | review_completed | a1j1: reset_sensor, applied=True, corrected=True |
| 10 | job_closed | a1j1: correct=True, job loss=2 |
| 10 | request_expired | a5j1: opportunity_lost_while_waiting |
| 10 | job_closed | a5j1: correct=False, job loss=10 |
| 10 | planning_decision | eligible a2j1(d=14,p=0.146,G_at_completion=18.000), a4j1(d=13,p=0.146,G_at_completion=15.000); choose a4j1 |
| 10 | queue_snapshot | waiting a0j1, a2j1, a3j1; active {'finish': 12, 'job_id': 'a4j1', 'start': 10} |
| 11 | request_expired | a0j1: opportunity_lost_while_waiting |
| 11 | job_closed | a0j1: correct=True, job loss=0 |
| 11 | queue_snapshot | waiting a2j1, a3j1; active {'finish': 12, 'job_id': 'a4j1', 'start': 10} |
| 12 | review_completed | a4j1: replace_filter, applied=True, corrected=False |
| 12 | planning_decision | eligible a2j1(d=14,p=0.146,G_at_completion=12.000); choose a2j1 |
| 12 | queue_snapshot | waiting a3j1; active {'finish': 14, 'job_id': 'a2j1', 'start': 12} |
| 13 | job_closed | a4j1: correct=True, job loss=0 |
| 13 | queue_snapshot | waiting a3j1; active {'finish': 14, 'job_id': 'a2j1', 'start': 12} |
| 14 | review_completed | a2j1: reset_sensor, applied=True, corrected=True |
| 14 | job_closed | a2j1: correct=True, job loss=18 |
| 14 | request_expired | a3j1: zero_value |
| 14 | job_closed | a3j1: correct=True, job loss=0 |
| 14 | planning_decision | eligible ; choose None |
| 14 | queue_snapshot | waiting ; active None |
| 15 | planning_decision | eligible ; choose None |
| 15 | queue_snapshot | waiting ; active None |
| 16 | proposal | a0j2: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 18; c=0; K=4 |
| 16 | proposal | a3j2: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 22; c=3; K=0 |
| 16 | planning_decision | eligible a0j2(d=18,p=0.146,G_at_completion=4.000), a3j2(d=22,p=0.146,G_at_completion=12.000); choose a3j2 |
| 16 | queue_snapshot | waiting a0j2; active {'finish': 18, 'job_id': 'a3j2', 'start': 16} |
| 17 | proposal | a1j2: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 19; c=0; K=12 |
| 17 | proposal | a2j2: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 19; c=1; K=8 |
| 17 | proposal | a4j2: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 21; c=0; K=0 |
| 17 | proposal | a5j2: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 23; c=3; K=12 |
| 17 | queue_snapshot | waiting a0j2, a1j2, a2j2, a4j2, a5j2; active {'finish': 18, 'job_id': 'a3j2', 'start': 16} |
| 18 | review_completed | a3j2: replace_filter, applied=True, corrected=False |
| 18 | request_expired | a0j2: opportunity_lost_while_waiting |
| 18 | job_closed | a0j2: correct=True, job loss=0 |
| 18 | planning_decision | eligible a5j2(d=23,p=0.146,G_at_completion=21.000); choose a5j2 |
| 18 | queue_snapshot | waiting a1j2, a2j2, a4j2; active {'finish': 20, 'job_id': 'a5j2', 'start': 18} |
| 19 | request_expired | a1j2: opportunity_lost_while_waiting |
| 19 | job_closed | a1j2: correct=True, job loss=0 |
| 19 | request_expired | a2j2: opportunity_lost_while_waiting |
| 19 | job_closed | a2j2: correct=True, job loss=0 |
| 19 | queue_snapshot | waiting a4j2; active {'finish': 20, 'job_id': 'a5j2', 'start': 18} |
| 20 | review_completed | a5j2: reset_sensor, applied=True, corrected=False |
| 20 | planning_decision | eligible ; choose None |
| 20 | queue_snapshot | waiting a4j2; active None |
| 21 | request_expired | a4j2: zero_value |
| 21 | job_closed | a4j2: correct=True, job loss=0 |
| 21 | planning_decision | eligible ; choose None |
| 21 | queue_snapshot | waiting ; active None |
| 22 | job_closed | a3j2: correct=True, job loss=0 |
| 22 | planning_decision | eligible ; choose None |
| 22 | queue_snapshot | waiting ; active None |
| 23 | job_closed | a5j2: correct=True, job loss=0 |
| 23 | planning_decision | eligible ; choose None |
| 23 | queue_snapshot | waiting ; active None |
| 24 | queue_snapshot | waiting ; active None |

## capacity/larger/12006/a6/s2/frozen/greedy/lambda0

Loss 38.0; incorrect closures 4; corrections 1.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a0j0: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 4; c=0; K=8 |
| 0 | proposal | a2j0: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 2; c=3; K=12 |
| 0 | planning_decision | eligible a0j0(d=4,p=0.146,G_at_completion=8.000), a2j0(d=2,p=0.146,G_at_completion=12.000); choose a2j0 |
| 0 | queue_snapshot | waiting a0j0; active {'finish': 2, 'job_id': 'a2j0', 'start': 0} |
| 1 | proposal | a1j0: clues filter/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 3; c=0; K=8 |
| 1 | proposal | a3j0: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 5; c=3; K=0 |
| 1 | proposal | a4j0: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 5; c=0; K=4 |
| 1 | proposal | a5j0: clues sensor/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 7; c=1; K=8 |
| 1 | queue_snapshot | waiting a0j0, a1j0, a3j0, a4j0, a5j0; active {'finish': 2, 'job_id': 'a2j0', 'start': 0} |
| 2 | review_completed | a2j0: replace_filter, applied=True, corrected=False |
| 2 | job_closed | a2j0: correct=True, job loss=0 |
| 2 | planning_decision | eligible a0j0(d=4,p=0.146,G_at_completion=8.000), a3j0(d=5,p=0.146,G_at_completion=3.000), a4j0(d=5,p=0.146,G_at_completion=4.000), a5j0(d=7,p=0.146,G_at_completion=11.000); choose a5j0 |
| 2 | queue_snapshot | waiting a0j0, a1j0, a3j0, a4j0; active {'finish': 4, 'job_id': 'a5j0', 'start': 2} |
| 3 | request_expired | a1j0: opportunity_lost_while_waiting |
| 3 | job_closed | a1j0: correct=False, job loss=8 |
| 3 | queue_snapshot | waiting a0j0, a3j0, a4j0; active {'finish': 4, 'job_id': 'a5j0', 'start': 2} |
| 4 | review_completed | a5j0: replace_filter, applied=True, corrected=False |
| 4 | request_expired | a0j0: opportunity_lost_while_waiting |
| 4 | job_closed | a0j0: correct=True, job loss=0 |
| 4 | planning_decision | eligible ; choose None |
| 4 | queue_snapshot | waiting a3j0, a4j0; active None |
| 5 | request_expired | a3j0: opportunity_lost_while_waiting |
| 5 | job_closed | a3j0: correct=True, job loss=0 |
| 5 | request_expired | a4j0: opportunity_lost_while_waiting |
| 5 | job_closed | a4j0: correct=False, job loss=4 |
| 5 | planning_decision | eligible ; choose None |
| 5 | queue_snapshot | waiting ; active None |
| 6 | planning_decision | eligible ; choose None |
| 6 | queue_snapshot | waiting ; active None |
| 7 | job_closed | a5j0: correct=True, job loss=0 |
| 7 | planning_decision | eligible ; choose None |
| 7 | queue_snapshot | waiting ; active None |
| 8 | proposal | a1j1: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 10; c=1; K=8 |
| 8 | proposal | a2j1: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 14; c=3; K=12 |
| 8 | proposal | a3j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 14; c=0; K=0 |
| 8 | proposal | a5j1: clues filter/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 10; c=1; K=8 |
| 8 | planning_decision | eligible a1j1(d=10,p=0.146,G_at_completion=8.000), a2j1(d=14,p=0.146,G_at_completion=24.000), a5j1(d=10,p=0.146,G_at_completion=8.000); choose a2j1 |
| 8 | queue_snapshot | waiting a1j1, a3j1, a5j1; active {'finish': 10, 'job_id': 'a2j1', 'start': 8} |
| 9 | proposal | a0j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 11; c=1; K=8 |
| 9 | proposal | a4j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 13; c=3; K=12 |
| 9 | queue_snapshot | waiting a0j1, a1j1, a3j1, a4j1, a5j1; active {'finish': 10, 'job_id': 'a2j1', 'start': 8} |
| 10 | review_completed | a2j1: reset_sensor, applied=True, corrected=True |
| 10 | request_expired | a1j1: opportunity_lost_while_waiting |
| 10 | job_closed | a1j1: correct=False, job loss=10 |
| 10 | request_expired | a5j1: opportunity_lost_while_waiting |
| 10 | job_closed | a5j1: correct=False, job loss=10 |
| 10 | planning_decision | eligible a4j1(d=13,p=0.146,G_at_completion=15.000); choose a4j1 |
| 10 | queue_snapshot | waiting a0j1, a3j1; active {'finish': 12, 'job_id': 'a4j1', 'start': 10} |
| 11 | request_expired | a0j1: opportunity_lost_while_waiting |
| 11 | job_closed | a0j1: correct=True, job loss=0 |
| 11 | queue_snapshot | waiting a3j1; active {'finish': 12, 'job_id': 'a4j1', 'start': 10} |
| 12 | review_completed | a4j1: replace_filter, applied=True, corrected=False |
| 12 | planning_decision | eligible ; choose None |
| 12 | queue_snapshot | waiting a3j1; active None |
| 13 | job_closed | a4j1: correct=True, job loss=0 |
| 13 | planning_decision | eligible ; choose None |
| 13 | queue_snapshot | waiting a3j1; active None |
| 14 | job_closed | a2j1: correct=True, job loss=6 |
| 14 | request_expired | a3j1: zero_value |
| 14 | job_closed | a3j1: correct=True, job loss=0 |
| 14 | planning_decision | eligible ; choose None |
| 14 | queue_snapshot | waiting ; active None |
| 15 | planning_decision | eligible ; choose None |
| 15 | queue_snapshot | waiting ; active None |
| 16 | proposal | a0j2: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 18; c=0; K=4 |
| 16 | proposal | a3j2: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 22; c=3; K=0 |
| 16 | planning_decision | eligible a0j2(d=18,p=0.146,G_at_completion=4.000), a3j2(d=22,p=0.146,G_at_completion=12.000); choose a3j2 |
| 16 | queue_snapshot | waiting a0j2; active {'finish': 18, 'job_id': 'a3j2', 'start': 16} |
| 17 | proposal | a1j2: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 19; c=0; K=12 |
| 17 | proposal | a2j2: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 19; c=1; K=8 |
| 17 | proposal | a4j2: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 21; c=0; K=0 |
| 17 | proposal | a5j2: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 23; c=3; K=12 |
| 17 | queue_snapshot | waiting a0j2, a1j2, a2j2, a4j2, a5j2; active {'finish': 18, 'job_id': 'a3j2', 'start': 16} |
| 18 | review_completed | a3j2: replace_filter, applied=True, corrected=False |
| 18 | request_expired | a0j2: opportunity_lost_while_waiting |
| 18 | job_closed | a0j2: correct=True, job loss=0 |
| 18 | planning_decision | eligible a5j2(d=23,p=0.146,G_at_completion=21.000); choose a5j2 |
| 18 | queue_snapshot | waiting a1j2, a2j2, a4j2; active {'finish': 20, 'job_id': 'a5j2', 'start': 18} |
| 19 | request_expired | a1j2: opportunity_lost_while_waiting |
| 19 | job_closed | a1j2: correct=True, job loss=0 |
| 19 | request_expired | a2j2: opportunity_lost_while_waiting |
| 19 | job_closed | a2j2: correct=True, job loss=0 |
| 19 | queue_snapshot | waiting a4j2; active {'finish': 20, 'job_id': 'a5j2', 'start': 18} |
| 20 | review_completed | a5j2: reset_sensor, applied=True, corrected=False |
| 20 | planning_decision | eligible ; choose None |
| 20 | queue_snapshot | waiting a4j2; active None |
| 21 | request_expired | a4j2: zero_value |
| 21 | job_closed | a4j2: correct=True, job loss=0 |
| 21 | planning_decision | eligible ; choose None |
| 21 | queue_snapshot | waiting ; active None |
| 22 | job_closed | a3j2: correct=True, job loss=0 |
| 22 | planning_decision | eligible ; choose None |
| 22 | queue_snapshot | waiting ; active None |
| 23 | job_closed | a5j2: correct=True, job loss=0 |
| 23 | planning_decision | eligible ; choose None |
| 23 | queue_snapshot | waiting ; active None |
| 24 | queue_snapshot | waiting ; active None |
