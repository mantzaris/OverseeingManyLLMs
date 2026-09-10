# Paired queue example

First numerical seed where λ=8 reduces incorrect closures while increasing original maintenance loss relative to λ=0. First actions differ for 1 jobs; observations differ for 6; identical-request first-action differences: 0. This is an integrated trajectory comparison.

Offline scoring view: hidden faults and initial correctness below were not supplied to schedulers.

## objective_evaluation/larger/13011/a6/s1/frozen/delay/lambda8

Loss 16.0; incorrect closures 0; corrections 7.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a0j0: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 6; c=0; K=8 |
| 0 | proposal | a2j0: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 6; c=0; K=8 |
| 0 | proposal | a4j0: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 4; c=0; K=0 |
| 0 | proposal | a5j0: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 6; c=1; K=0 |
| 0 | planning_decision | eligible a0j0(d=6,p=0.146,G_at_completion=16.000), a2j0(d=6,p=0.146,G_at_completion=16.000), a4j0(d=4,p=0.146,G_at_completion=8.000), a5j0(d=6,p=0.146,G_at_completion=13.000); choose a5j0 |
| 0 | queue_snapshot | waiting a0j0, a2j0, a4j0; active {'finish': 1, 'job_id': 'a5j0', 'start': 0} |
| 1 | review_completed | a5j0: replace_filter, applied=True, corrected=False |
| 1 | proposal | a1j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 7; c=0; K=8 |
| 1 | proposal | a3j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 5; c=0; K=0 |
| 1 | planning_decision | eligible a0j0(d=6,p=0.146,G_at_completion=16.000), a2j0(d=6,p=0.146,G_at_completion=16.000), a4j0(d=4,p=0.146,G_at_completion=8.000), a1j0(d=7,p=0.146,G_at_completion=16.000), a3j0(d=5,p=0.146,G_at_completion=8.000); choose a0j0 |
| 1 | queue_snapshot | waiting a1j0, a2j0, a3j0, a4j0; active {'finish': 2, 'job_id': 'a0j0', 'start': 1} |
| 2 | review_completed | a0j0: reset_sensor, applied=True, corrected=False |
| 2 | planning_decision | eligible a2j0(d=6,p=0.146,G_at_completion=16.000), a4j0(d=4,p=0.146,G_at_completion=8.000), a1j0(d=7,p=0.146,G_at_completion=16.000), a3j0(d=5,p=0.146,G_at_completion=8.000); choose a2j0 |
| 2 | queue_snapshot | waiting a1j0, a3j0, a4j0; active {'finish': 3, 'job_id': 'a2j0', 'start': 2} |
| 3 | review_completed | a2j0: reset_sensor, applied=True, corrected=True |
| 3 | planning_decision | eligible a4j0(d=4,p=0.146,G_at_completion=8.000), a1j0(d=7,p=0.146,G_at_completion=16.000), a3j0(d=5,p=0.146,G_at_completion=8.000); choose a4j0 |
| 3 | queue_snapshot | waiting a1j0, a3j0; active {'finish': 4, 'job_id': 'a4j0', 'start': 3} |
| 4 | review_completed | a4j0: reset_sensor, applied=True, corrected=False |
| 4 | job_closed | a4j0: correct=True, job loss=0 |
| 4 | planning_decision | eligible a1j0(d=7,p=0.146,G_at_completion=16.000), a3j0(d=5,p=0.146,G_at_completion=8.000); choose a3j0 |
| 4 | queue_snapshot | waiting a1j0; active {'finish': 5, 'job_id': 'a3j0', 'start': 4} |
| 5 | review_completed | a3j0: reset_sensor, applied=True, corrected=True |
| 5 | job_closed | a3j0: correct=True, job loss=0 |
| 5 | planning_decision | eligible a1j0(d=7,p=0.146,G_at_completion=16.000); choose a1j0 |
| 5 | queue_snapshot | waiting ; active {'finish': 6, 'job_id': 'a1j0', 'start': 5} |
| 6 | review_completed | a1j0: reset_sensor, applied=True, corrected=True |
| 6 | job_closed | a0j0: correct=True, job loss=0 |
| 6 | job_closed | a2j0: correct=True, job loss=0 |
| 6 | job_closed | a5j0: correct=True, job loss=0 |
| 6 | planning_decision | eligible ; choose None |
| 6 | queue_snapshot | waiting ; active None |
| 7 | job_closed | a1j0: correct=True, job loss=0 |
| 7 | planning_decision | eligible ; choose None |
| 7 | queue_snapshot | waiting ; active None |
| 8 | proposal | a1j1: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 14; c=0; K=0 |
| 8 | proposal | a2j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 12; c=1; K=4 |
| 8 | planning_decision | eligible a1j1(d=14,p=0.146,G_at_completion=8.000), a2j1(d=12,p=0.146,G_at_completion=15.000); choose a2j1 |
| 8 | queue_snapshot | waiting a1j1; active {'finish': 9, 'job_id': 'a2j1', 'start': 8} |
| 9 | review_completed | a2j1: replace_filter, applied=True, corrected=False |
| 9 | proposal | a0j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 13; c=1; K=0 |
| 9 | proposal | a3j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 15; c=0; K=4 |
| 9 | proposal | a4j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 15; c=3; K=4 |
| 9 | proposal | a5j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 15; c=1; K=8 |
| 9 | planning_decision | eligible a1j1(d=14,p=0.146,G_at_completion=8.000), a0j1(d=13,p=0.146,G_at_completion=11.000), a3j1(d=15,p=0.146,G_at_completion=12.000), a4j1(d=15,p=0.146,G_at_completion=27.000), a5j1(d=15,p=0.146,G_at_completion=21.000); choose a4j1 |
| 9 | queue_snapshot | waiting a0j1, a1j1, a3j1, a5j1; active {'finish': 10, 'job_id': 'a4j1', 'start': 9} |
| 10 | review_completed | a4j1: replace_filter, applied=True, corrected=False |
| 10 | planning_decision | eligible a1j1(d=14,p=0.146,G_at_completion=8.000), a0j1(d=13,p=0.146,G_at_completion=10.000), a3j1(d=15,p=0.146,G_at_completion=12.000), a5j1(d=15,p=0.146,G_at_completion=20.000); choose a0j1 |
| 10 | queue_snapshot | waiting a1j1, a3j1, a5j1; active {'finish': 11, 'job_id': 'a0j1', 'start': 10} |
| 11 | review_completed | a0j1: replace_filter, applied=True, corrected=False |
| 11 | planning_decision | eligible a1j1(d=14,p=0.146,G_at_completion=8.000), a3j1(d=15,p=0.146,G_at_completion=12.000), a5j1(d=15,p=0.146,G_at_completion=19.000); choose a5j1 |
| 11 | queue_snapshot | waiting a1j1, a3j1; active {'finish': 12, 'job_id': 'a5j1', 'start': 11} |
| 12 | review_completed | a5j1: replace_filter, applied=True, corrected=False |
| 12 | job_closed | a2j1: correct=True, job loss=0 |
| 12 | planning_decision | eligible a1j1(d=14,p=0.146,G_at_completion=8.000), a3j1(d=15,p=0.146,G_at_completion=12.000); choose a1j1 |
| 12 | queue_snapshot | waiting a3j1; active {'finish': 13, 'job_id': 'a1j1', 'start': 12} |
| 13 | review_completed | a1j1: reset_sensor, applied=True, corrected=False |
| 13 | job_closed | a0j1: correct=True, job loss=0 |
| 13 | planning_decision | eligible a3j1(d=15,p=0.146,G_at_completion=12.000); choose a3j1 |
| 13 | queue_snapshot | waiting ; active {'finish': 14, 'job_id': 'a3j1', 'start': 13} |
| 14 | review_completed | a3j1: replace_filter, applied=True, corrected=False |
| 14 | job_closed | a1j1: correct=True, job loss=0 |
| 14 | planning_decision | eligible ; choose None |
| 14 | queue_snapshot | waiting ; active None |
| 15 | job_closed | a3j1: correct=True, job loss=0 |
| 15 | job_closed | a4j1: correct=True, job loss=0 |
| 15 | job_closed | a5j1: correct=True, job loss=0 |
| 15 | planning_decision | eligible ; choose None |
| 15 | queue_snapshot | waiting ; active None |
| 16 | proposal | a2j2: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 22; c=1; K=0 |
| 16 | proposal | a5j2: clues sensor/sensor; first reset_sensor; second reset_sensor; initial wrong (offline label); p=0.1461; deadline 22; c=0; K=4 |
| 16 | planning_decision | eligible a2j2(d=22,p=0.146,G_at_completion=13.000), a5j2(d=22,p=0.146,G_at_completion=12.000); choose a2j2 |
| 16 | queue_snapshot | waiting a5j2; active {'finish': 17, 'job_id': 'a2j2', 'start': 16} |
| 17 | review_completed | a2j2: replace_filter, applied=True, corrected=False |
| 17 | proposal | a0j2: clues filter/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 23; c=3; K=8 |
| 17 | proposal | a1j2: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 19; c=3; K=12 |
| 17 | proposal | a3j2: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 19; c=0; K=4 |
| 17 | proposal | a4j2: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 23; c=1; K=4 |
| 17 | planning_decision | eligible a5j2(d=22,p=0.146,G_at_completion=12.000), a0j2(d=23,p=0.146,G_at_completion=31.000), a1j2(d=19,p=0.146,G_at_completion=23.000), a3j2(d=19,p=0.146,G_at_completion=12.000), a4j2(d=23,p=0.146,G_at_completion=17.000); choose a1j2 |
| 17 | queue_snapshot | waiting a0j2, a3j2, a4j2, a5j2; active {'finish': 18, 'job_id': 'a1j2', 'start': 17} |
| 18 | review_completed | a1j2: reset_sensor, applied=True, corrected=True |
| 18 | planning_decision | eligible a5j2(d=22,p=0.146,G_at_completion=12.000), a0j2(d=23,p=0.146,G_at_completion=28.000), a3j2(d=19,p=0.146,G_at_completion=12.000), a4j2(d=23,p=0.146,G_at_completion=16.000); choose a3j2 |
| 18 | queue_snapshot | waiting a0j2, a4j2, a5j2; active {'finish': 19, 'job_id': 'a3j2', 'start': 18} |
| 19 | review_completed | a3j2: replace_filter, applied=True, corrected=False |
| 19 | job_closed | a1j2: correct=True, job loss=3 |
| 19 | job_closed | a3j2: correct=True, job loss=0 |
| 19 | planning_decision | eligible a5j2(d=22,p=0.146,G_at_completion=12.000), a0j2(d=23,p=0.146,G_at_completion=25.000), a4j2(d=23,p=0.146,G_at_completion=15.000); choose a0j2 |
| 19 | queue_snapshot | waiting a4j2, a5j2; active {'finish': 20, 'job_id': 'a0j2', 'start': 19} |
| 20 | review_completed | a0j2: reset_sensor, applied=True, corrected=True |
| 20 | planning_decision | eligible a5j2(d=22,p=0.146,G_at_completion=12.000), a4j2(d=23,p=0.146,G_at_completion=14.000); choose a4j2 |
| 20 | queue_snapshot | waiting a5j2; active {'finish': 21, 'job_id': 'a4j2', 'start': 20} |
| 21 | review_completed | a4j2: reset_sensor, applied=True, corrected=True |
| 21 | planning_decision | eligible a5j2(d=22,p=0.146,G_at_completion=12.000); choose a5j2 |
| 21 | queue_snapshot | waiting ; active {'finish': 22, 'job_id': 'a5j2', 'start': 21} |
| 22 | review_completed | a5j2: replace_filter, applied=True, corrected=True |
| 22 | job_closed | a2j2: correct=True, job loss=0 |
| 22 | job_closed | a5j2: correct=True, job loss=0 |
| 22 | planning_decision | eligible ; choose None |
| 22 | queue_snapshot | waiting ; active None |
| 23 | job_closed | a0j2: correct=True, job loss=9 |
| 23 | job_closed | a4j2: correct=True, job loss=4 |
| 23 | planning_decision | eligible ; choose None |
| 23 | queue_snapshot | waiting ; active None |
| 24 | queue_snapshot | waiting ; active None |

## objective_evaluation/larger/13011/a6/s1/frozen/delay/lambda0

Loss 9.0; incorrect closures 1; corrections 5.

| Tick | Event | Details |
| ---: | --- | --- |
| 0 | proposal | a0j0: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 6; c=0; K=8 |
| 0 | proposal | a2j0: clues sensor/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 6; c=0; K=8 |
| 0 | proposal | a4j0: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 4; c=0; K=0 |
| 0 | proposal | a5j0: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 6; c=1; K=0 |
| 0 | planning_decision | eligible a0j0(d=6,p=0.146,G_at_completion=8.000), a2j0(d=6,p=0.146,G_at_completion=8.000), a5j0(d=6,p=0.146,G_at_completion=5.000); choose a5j0 |
| 0 | queue_snapshot | waiting a0j0, a2j0, a4j0; active {'finish': 1, 'job_id': 'a5j0', 'start': 0} |
| 1 | review_completed | a5j0: replace_filter, applied=True, corrected=False |
| 1 | proposal | a1j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 7; c=0; K=8 |
| 1 | proposal | a3j0: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 5; c=0; K=0 |
| 1 | planning_decision | eligible a0j0(d=6,p=0.146,G_at_completion=8.000), a2j0(d=6,p=0.146,G_at_completion=8.000), a1j0(d=7,p=0.146,G_at_completion=8.000); choose a0j0 |
| 1 | queue_snapshot | waiting a1j0, a2j0, a3j0, a4j0; active {'finish': 2, 'job_id': 'a0j0', 'start': 1} |
| 2 | review_completed | a0j0: reset_sensor, applied=True, corrected=False |
| 2 | planning_decision | eligible a2j0(d=6,p=0.146,G_at_completion=8.000), a1j0(d=7,p=0.146,G_at_completion=8.000); choose a2j0 |
| 2 | queue_snapshot | waiting a1j0, a3j0, a4j0; active {'finish': 3, 'job_id': 'a2j0', 'start': 2} |
| 3 | review_completed | a2j0: reset_sensor, applied=True, corrected=True |
| 3 | planning_decision | eligible a1j0(d=7,p=0.146,G_at_completion=8.000); choose a1j0 |
| 3 | queue_snapshot | waiting a3j0, a4j0; active {'finish': 4, 'job_id': 'a1j0', 'start': 3} |
| 4 | review_completed | a1j0: reset_sensor, applied=True, corrected=True |
| 4 | request_expired | a4j0: zero_value |
| 4 | job_closed | a4j0: correct=True, job loss=0 |
| 4 | planning_decision | eligible ; choose None |
| 4 | queue_snapshot | waiting a3j0; active None |
| 5 | request_expired | a3j0: zero_value |
| 5 | job_closed | a3j0: correct=False, job loss=0 |
| 5 | planning_decision | eligible ; choose None |
| 5 | queue_snapshot | waiting ; active None |
| 6 | job_closed | a0j0: correct=True, job loss=0 |
| 6 | job_closed | a2j0: correct=True, job loss=0 |
| 6 | job_closed | a5j0: correct=True, job loss=0 |
| 6 | planning_decision | eligible ; choose None |
| 6 | queue_snapshot | waiting ; active None |
| 7 | job_closed | a1j0: correct=True, job loss=0 |
| 7 | planning_decision | eligible ; choose None |
| 7 | queue_snapshot | waiting ; active None |
| 8 | proposal | a1j1: clues sensor/sensor; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 14; c=0; K=0 |
| 8 | proposal | a2j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 12; c=1; K=4 |
| 8 | planning_decision | eligible a2j1(d=12,p=0.146,G_at_completion=7.000); choose a2j1 |
| 8 | queue_snapshot | waiting a1j1; active {'finish': 9, 'job_id': 'a2j1', 'start': 8} |
| 9 | review_completed | a2j1: replace_filter, applied=True, corrected=False |
| 9 | proposal | a0j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 13; c=1; K=0 |
| 9 | proposal | a3j1: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 15; c=0; K=4 |
| 9 | proposal | a4j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 15; c=3; K=4 |
| 9 | proposal | a5j1: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 15; c=1; K=8 |
| 9 | planning_decision | eligible a0j1(d=13,p=0.146,G_at_completion=3.000), a3j1(d=15,p=0.146,G_at_completion=4.000), a4j1(d=15,p=0.146,G_at_completion=19.000), a5j1(d=15,p=0.146,G_at_completion=13.000); choose a4j1 |
| 9 | queue_snapshot | waiting a0j1, a1j1, a3j1, a5j1; active {'finish': 10, 'job_id': 'a4j1', 'start': 9} |
| 10 | review_completed | a4j1: replace_filter, applied=True, corrected=False |
| 10 | planning_decision | eligible a0j1(d=13,p=0.146,G_at_completion=2.000), a3j1(d=15,p=0.146,G_at_completion=4.000), a5j1(d=15,p=0.146,G_at_completion=12.000); choose a0j1 |
| 10 | queue_snapshot | waiting a1j1, a3j1, a5j1; active {'finish': 11, 'job_id': 'a0j1', 'start': 10} |
| 11 | review_completed | a0j1: replace_filter, applied=True, corrected=False |
| 11 | planning_decision | eligible a3j1(d=15,p=0.146,G_at_completion=4.000), a5j1(d=15,p=0.146,G_at_completion=11.000); choose a5j1 |
| 11 | queue_snapshot | waiting a1j1, a3j1; active {'finish': 12, 'job_id': 'a5j1', 'start': 11} |
| 12 | review_completed | a5j1: replace_filter, applied=True, corrected=False |
| 12 | job_closed | a2j1: correct=True, job loss=0 |
| 12 | planning_decision | eligible a3j1(d=15,p=0.146,G_at_completion=4.000); choose a3j1 |
| 12 | queue_snapshot | waiting a1j1; active {'finish': 13, 'job_id': 'a3j1', 'start': 12} |
| 13 | review_completed | a3j1: replace_filter, applied=True, corrected=False |
| 13 | job_closed | a0j1: correct=True, job loss=0 |
| 13 | planning_decision | eligible ; choose None |
| 13 | queue_snapshot | waiting a1j1; active None |
| 14 | request_expired | a1j1: zero_value |
| 14 | job_closed | a1j1: correct=True, job loss=0 |
| 14 | planning_decision | eligible ; choose None |
| 14 | queue_snapshot | waiting ; active None |
| 15 | job_closed | a3j1: correct=True, job loss=0 |
| 15 | job_closed | a4j1: correct=True, job loss=0 |
| 15 | job_closed | a5j1: correct=True, job loss=0 |
| 15 | planning_decision | eligible ; choose None |
| 15 | queue_snapshot | waiting ; active None |
| 16 | proposal | a2j2: clues filter/filter; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 22; c=1; K=0 |
| 16 | proposal | a5j2: clues sensor/sensor; first reset_sensor; second reset_sensor; initial wrong (offline label); p=0.1461; deadline 22; c=0; K=4 |
| 16 | planning_decision | eligible a2j2(d=22,p=0.146,G_at_completion=5.000), a5j2(d=22,p=0.146,G_at_completion=4.000); choose a2j2 |
| 16 | queue_snapshot | waiting a5j2; active {'finish': 17, 'job_id': 'a2j2', 'start': 16} |
| 17 | review_completed | a2j2: replace_filter, applied=True, corrected=False |
| 17 | proposal | a0j2: clues filter/filter; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 23; c=3; K=8 |
| 17 | proposal | a1j2: clues filter/sensor; first replace_filter; second replace_filter; initial wrong (offline label); p=0.1461; deadline 19; c=3; K=12 |
| 17 | proposal | a3j2: clues filter/sensor; first replace_filter; second replace_filter; initial correct (offline label); p=0.1461; deadline 19; c=0; K=4 |
| 17 | proposal | a4j2: clues sensor/filter; first reset_sensor; second reset_sensor; initial correct (offline label); p=0.1461; deadline 23; c=1; K=4 |
| 17 | planning_decision | eligible a5j2(d=22,p=0.146,G_at_completion=4.000), a0j2(d=23,p=0.146,G_at_completion=23.000), a1j2(d=19,p=0.146,G_at_completion=15.000), a3j2(d=19,p=0.146,G_at_completion=4.000), a4j2(d=23,p=0.146,G_at_completion=9.000); choose a0j2 |
| 17 | queue_snapshot | waiting a1j2, a3j2, a4j2, a5j2; active {'finish': 18, 'job_id': 'a0j2', 'start': 17} |
| 18 | review_completed | a0j2: reset_sensor, applied=True, corrected=True |
| 18 | planning_decision | eligible a5j2(d=22,p=0.146,G_at_completion=4.000), a1j2(d=19,p=0.146,G_at_completion=12.000), a3j2(d=19,p=0.146,G_at_completion=4.000), a4j2(d=23,p=0.146,G_at_completion=8.000); choose a1j2 |
| 18 | queue_snapshot | waiting a3j2, a4j2, a5j2; active {'finish': 19, 'job_id': 'a1j2', 'start': 18} |
| 19 | review_completed | a1j2: reset_sensor, applied=True, corrected=True |
| 19 | job_closed | a1j2: correct=True, job loss=6 |
| 19 | request_expired | a3j2: opportunity_lost_while_waiting |
| 19 | job_closed | a3j2: correct=True, job loss=0 |
| 19 | planning_decision | eligible a5j2(d=22,p=0.146,G_at_completion=4.000), a4j2(d=23,p=0.146,G_at_completion=7.000); choose a4j2 |
| 19 | queue_snapshot | waiting a5j2; active {'finish': 20, 'job_id': 'a4j2', 'start': 19} |
| 20 | review_completed | a4j2: reset_sensor, applied=True, corrected=False |
| 20 | planning_decision | eligible a5j2(d=22,p=0.146,G_at_completion=4.000); choose a5j2 |
| 20 | queue_snapshot | waiting ; active {'finish': 21, 'job_id': 'a5j2', 'start': 20} |
| 21 | review_completed | a5j2: replace_filter, applied=True, corrected=True |
| 21 | planning_decision | eligible ; choose None |
| 21 | queue_snapshot | waiting ; active None |
| 22 | job_closed | a2j2: correct=True, job loss=0 |
| 22 | job_closed | a5j2: correct=True, job loss=0 |
| 22 | planning_decision | eligible ; choose None |
| 22 | queue_snapshot | waiting ; active None |
| 23 | job_closed | a0j2: correct=True, job loss=3 |
| 23 | job_closed | a4j2: correct=True, job loss=0 |
| 23 | planning_decision | eligible ; choose None |
| 23 | queue_snapshot | waiting ; active None |
| 24 | queue_snapshot | waiting ; active None |
