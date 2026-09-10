# Episode trace

Evidence: **live_gpu**, policy **delay**, scenario seed 222.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 2, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j0", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 1, "deadline": 2, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 0}}` |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j0", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 5, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 0}}` |
| 0 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 0, "deadline": 2, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}], "selected": "a0j0"}` |
| 0 | review_started | `{"finish": 2, "job_id": "a0j0", "start": 0}` |
| 0 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a0j0", "start": 0}, "pending": ["a1j0", "a2j0"]}` |
| 0 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 1 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a0j0", "start": 0}, "pending": ["a1j0", "a2j0"]}` |
| 1 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 2 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a0j0", "late": false}` |
| 2 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a0j0", "job_loss": 0, "terminal_loss": 0}` |
| 2 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a1j0"}` |
| 2 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a1j0", "job_loss": 0, "terminal_loss": 0}` |
| 2 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 2 | queue_snapshot | `{"busy": null, "pending": ["a2j0"]}` |
| 2 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 3 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 3 | queue_snapshot | `{"busy": null, "pending": ["a2j0"]}` |
| 3 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 4 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 4 | queue_snapshot | `{"busy": null, "pending": ["a2j0"]}` |
| 4 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 5 | request_expired | `{"category": "zero_value", "initial_proposal_wrong": false, "job_id": "a2j0"}` |
| 5 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j0", "job_loss": 0, "terminal_loss": 0}` |
| 5 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | proposal | `{"agreement": false, "evidence": "live_gpu", "job_id": "a1j1", "p_error": 0.1836734693877551, "primary": "reset_sensor", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 3, "deadline": 7, "job_id": "a1j1", "p_error": 0.1836734693877551, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}}` |
| 6 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 6 | queue_snapshot | `{"busy": null, "pending": ["a1j1"]}` |
| 6 | interval_scored | `{"job_id": "a1j1", "loss": 3}` |
| 7 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": true, "job_id": "a1j1"}` |
| 7 | job_closed | `{"action": "reset_sensor", "correct": false, "job_id": "a1j1", "job_loss": 11, "terminal_loss": 8}` |
| 7 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j1", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 7 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 9, "job_id": "a0j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 7, "review_ticks": 2, "terminal_cost": 8}}` |
| 7 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j1", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 7 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 12, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 7, "review_ticks": 2, "terminal_cost": 8}}` |
| 7 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 0, "deadline": 9, "job_id": "a0j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 7, "review_ticks": 2, "terminal_cost": 8}, {"agent_id": 2, "cost_per_tick": 0, "deadline": 12, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 7, "review_ticks": 2, "terminal_cost": 8}], "selected": "a0j1"}` |
| 7 | review_started | `{"finish": 9, "job_id": "a0j1", "start": 7}` |
| 7 | queue_snapshot | `{"busy": {"finish": 9, "job_id": "a0j1", "start": 7}, "pending": ["a2j1"]}` |
| 7 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 8 | queue_snapshot | `{"busy": {"finish": 9, "job_id": "a0j1", "start": 7}, "pending": ["a2j1"]}` |
| 8 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 8 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 9 | review_completed | `{"applied": true, "changed": false, "instructed_action": "reset_sensor", "job_id": "a0j1", "late": false}` |
| 9 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a0j1", "job_loss": 0, "terminal_loss": 0}` |
| 9 | dispatch_considered | `{"eligible": [{"agent_id": 2, "cost_per_tick": 0, "deadline": 12, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 7, "review_ticks": 2, "terminal_cost": 8}], "selected": "a2j1"}` |
| 9 | review_started | `{"finish": 11, "job_id": "a2j1", "start": 9}` |
| 9 | queue_snapshot | `{"busy": {"finish": 11, "job_id": "a2j1", "start": 9}, "pending": []}` |
| 9 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 10 | queue_snapshot | `{"busy": {"finish": 11, "job_id": "a2j1", "start": 9}, "pending": []}` |
| 10 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 11 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a2j1", "late": false}` |
| 11 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 11 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 12 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a2j1", "job_loss": 0, "terminal_loss": 0}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 11, "attempts": 12, "completion_tokens": 84, "correct_jobs": 5, "corrections": 0, "episode_wall_seconds": 2.171696, "error": null, "evidence": "live_gpu", "expired_requests": 3, "incomplete_service": null, "jobs_closed": 6, "late_returns": 0, "loss_upper_bound": 37, "planned_calls": 12, "policy": "delay", "prompt_tokens": 2510, "request_wall_seconds": 1.6592108774930239, "review_busy_ticks": 6, "reviews_completed": 3, "reviews_started": 3, "scenario_hash": "7ed5a28f2968f2ffdd714c816e527463b82963bc1ec04409cf4bb8ad542beee6", "scheduled_calls": 12, "seed": 222, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 11, "unknown_token_attempts": 0}` |
