# Queue example: seed 300, review duration 1

Selected by the predeclared first-seed rule, irrespective of winner. Faults and correctness below are offline scoring annotations; schedulers never receive them.

| Job | Release | Deadline | Penalty | Correct action (offline) |
| --- | ---: | ---: | ---: | --- |
| a0j0 | 0 | 4 | 8 | reset_sensor |
| a1j0 | 0 | 2 | 12 | replace_filter |
| a2j0 | 0 | 5 | 4 | reset_sensor |
| a0j1 | 6 | 8 | 12 | replace_filter |
| a1j1 | 6 | 10 | 8 | replace_filter |
| a2j1 | 6 | 11 | 4 | replace_filter |

## greedy: loss 0

| Tick | Event | Job | Details |
| ---: | --- | --- | --- |
| 0 | proposal | a0j0 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"} |
| 0 | proposal | a1j0 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"} |
| 0 | proposal | a2j0 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"} |
| 0 | review_started | a1j0 | {"finish": 1, "start": 0} |
| 1 | review_completed | a1j0 | {"applied": true, "changed": false, "instructed_action": "replace_filter", "late": false} |
| 1 | review_started | a0j0 | {"finish": 2, "start": 1} |
| 2 | review_completed | a0j0 | {"applied": true, "changed": true, "instructed_action": "reset_sensor", "late": false} |
| 2 | job_closed | a1j0 | {"action": "replace_filter", "correct": true, "job_loss": 0, "terminal_loss": 0} |
| 2 | review_started | a2j0 | {"finish": 3, "start": 2} |
| 3 | review_completed | a2j0 | {"applied": true, "changed": false, "instructed_action": "reset_sensor", "late": false} |
| 4 | job_closed | a0j0 | {"action": "reset_sensor", "correct": true, "job_loss": 0, "terminal_loss": 0} |
| 5 | job_closed | a2j0 | {"action": "reset_sensor", "correct": true, "job_loss": 0, "terminal_loss": 0} |
| 6 | proposal | a0j1 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"} |
| 6 | proposal | a1j1 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"} |
| 6 | proposal | a2j1 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"} |
| 6 | review_started | a0j1 | {"finish": 7, "start": 6} |
| 7 | review_completed | a0j1 | {"applied": true, "changed": false, "instructed_action": "replace_filter", "late": false} |
| 7 | review_started | a1j1 | {"finish": 8, "start": 7} |
| 8 | review_completed | a1j1 | {"applied": true, "changed": false, "instructed_action": "replace_filter", "late": false} |
| 8 | job_closed | a0j1 | {"action": "replace_filter", "correct": true, "job_loss": 0, "terminal_loss": 0} |
| 8 | review_started | a2j1 | {"finish": 9, "start": 8} |
| 9 | review_completed | a2j1 | {"applied": true, "changed": false, "instructed_action": "replace_filter", "late": false} |
| 10 | job_closed | a1j1 | {"action": "replace_filter", "correct": true, "job_loss": 0, "terminal_loss": 0} |
| 11 | job_closed | a2j1 | {"action": "replace_filter", "correct": true, "job_loss": 0, "terminal_loss": 0} |

## delay: loss 0

| Tick | Event | Job | Details |
| ---: | --- | --- | --- |
| 0 | proposal | a0j0 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"} |
| 0 | proposal | a1j0 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"} |
| 0 | proposal | a2j0 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"} |
| 0 | review_started | a0j0 | {"finish": 1, "start": 0} |
| 1 | review_completed | a0j0 | {"applied": true, "changed": true, "instructed_action": "reset_sensor", "late": false} |
| 1 | review_started | a1j0 | {"finish": 2, "start": 1} |
| 2 | review_completed | a1j0 | {"applied": true, "changed": false, "instructed_action": "replace_filter", "late": false} |
| 2 | job_closed | a1j0 | {"action": "replace_filter", "correct": true, "job_loss": 0, "terminal_loss": 0} |
| 2 | review_started | a2j0 | {"finish": 3, "start": 2} |
| 3 | review_completed | a2j0 | {"applied": true, "changed": false, "instructed_action": "reset_sensor", "late": false} |
| 4 | job_closed | a0j0 | {"action": "reset_sensor", "correct": true, "job_loss": 0, "terminal_loss": 0} |
| 5 | job_closed | a2j0 | {"action": "reset_sensor", "correct": true, "job_loss": 0, "terminal_loss": 0} |
| 6 | proposal | a0j1 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"} |
| 6 | proposal | a1j1 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"} |
| 6 | proposal | a2j1 | {"agreement": true, "evidence": "live_gpu", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"} |
| 6 | review_started | a0j1 | {"finish": 7, "start": 6} |
| 7 | review_completed | a0j1 | {"applied": true, "changed": false, "instructed_action": "replace_filter", "late": false} |
| 7 | review_started | a1j1 | {"finish": 8, "start": 7} |
| 8 | review_completed | a1j1 | {"applied": true, "changed": false, "instructed_action": "replace_filter", "late": false} |
| 8 | job_closed | a0j1 | {"action": "replace_filter", "correct": true, "job_loss": 0, "terminal_loss": 0} |
| 8 | review_started | a2j1 | {"finish": 9, "start": 8} |
| 9 | review_completed | a2j1 | {"applied": true, "changed": false, "instructed_action": "replace_filter", "late": false} |
| 10 | job_closed | a1j1 | {"action": "replace_filter", "correct": true, "job_loss": 0, "terminal_loss": 0} |
| 11 | job_closed | a2j1 | {"action": "replace_filter", "correct": true, "job_loss": 0, "terminal_loss": 0} |

A changed review sequence alone does not imply lower realized loss; compare the two observed loss totals.
