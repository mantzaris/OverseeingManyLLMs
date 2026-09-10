# Episode trace

Evidence: **live_gpu**, policy **myopic**, scenario seed 220.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 1, "deadline": 2, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 0}}` |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 1, "deadline": 5, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | dispatch_considered | `{"eligible": [{"agent_id": 1, "cost_per_tick": 1, "deadline": 5, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}], "selected": "a1j0"}` |
| 0 | review_started | `{"finish": 2, "job_id": "a1j0", "start": 0}` |
| 0 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a1j0", "start": 0}, "pending": ["a0j0"]}` |
| 0 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j0", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 1 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 3, "deadline": 6, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 1, "review_ticks": 2, "terminal_cost": 0}}` |
| 1 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a1j0", "start": 0}, "pending": ["a0j0", "a2j0"]}` |
| 1 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 2 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a1j0", "late": false}` |
| 2 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a0j0"}` |
| 2 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a0j0", "job_loss": 0, "terminal_loss": 0}` |
| 2 | dispatch_considered | `{"eligible": [{"agent_id": 2, "cost_per_tick": 3, "deadline": 6, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 1, "review_ticks": 2, "terminal_cost": 0}], "selected": "a2j0"}` |
| 2 | review_started | `{"finish": 4, "job_id": "a2j0", "start": 2}` |
| 2 | queue_snapshot | `{"busy": {"finish": 4, "job_id": "a2j0", "start": 2}, "pending": []}` |
| 2 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 2 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 3 | queue_snapshot | `{"busy": {"finish": 4, "job_id": "a2j0", "start": 2}, "pending": []}` |
| 3 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 3 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 4 | review_completed | `{"applied": true, "changed": false, "instructed_action": "reset_sensor", "job_id": "a2j0", "late": false}` |
| 4 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 4 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 5 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a1j0", "job_loss": 0, "terminal_loss": 0}` |
| 5 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 5 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 6 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j0", "job_loss": 0, "terminal_loss": 0}` |
| 6 | proposal | `{"agreement": false, "evidence": "live_gpu", "job_id": "a1j1", "p_error": 0.1836734693877551, "primary": "reset_sensor", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 7, "job_id": "a1j1", "p_error": 0.1836734693877551, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 0}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j1", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 3, "deadline": 7, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}}` |
| 6 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 6 | queue_snapshot | `{"busy": null, "pending": ["a1j1", "a2j1"]}` |
| 6 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 7 | request_expired | `{"category": "zero_value", "initial_proposal_wrong": false, "job_id": "a1j1"}` |
| 7 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a1j1", "job_loss": 0, "terminal_loss": 0}` |
| 7 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a2j1"}` |
| 7 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a2j1", "job_loss": 0, "terminal_loss": 0}` |
| 7 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j1", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 7 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 1, "deadline": 9, "job_id": "a0j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 7, "review_ticks": 2, "terminal_cost": 0}}` |
| 7 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 7 | queue_snapshot | `{"busy": null, "pending": ["a0j1"]}` |
| 7 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 8 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 8 | queue_snapshot | `{"busy": null, "pending": ["a0j1"]}` |
| 8 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 9 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a0j1"}` |
| 9 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a0j1", "job_loss": 0, "terminal_loss": 0}` |
| 9 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 9 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 11 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 0, "attempts": 12, "completion_tokens": 84, "correct_jobs": 6, "corrections": 0, "episode_wall_seconds": 2.157445, "error": null, "evidence": "live_gpu", "expired_requests": 4, "incomplete_service": null, "jobs_closed": 6, "late_returns": 0, "loss_upper_bound": 43, "planned_calls": 12, "policy": "myopic", "prompt_tokens": 2562, "request_wall_seconds": 1.6681247483938932, "review_busy_ticks": 4, "reviews_completed": 2, "reviews_started": 2, "scenario_hash": "c986429270cd0b18dcf4468dd430d53aedb624c6695a3fb92ea0ff725a9b5ebf", "scheduled_calls": 12, "seed": 220, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 0, "unknown_token_attempts": 0}` |
