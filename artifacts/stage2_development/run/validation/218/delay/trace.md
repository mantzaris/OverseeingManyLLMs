# Episode trace

Evidence: **live_gpu**, policy **delay**, scenario seed 218.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 0 | queue_snapshot | `{"busy": null, "pending": []}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 1 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 1, "deadline": 3, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 1, "review_ticks": 2, "terminal_cost": 0}}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j0", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 1 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 1, "deadline": 3, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 1, "review_ticks": 2, "terminal_cost": 0}}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 1 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 1, "deadline": 2, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 1, "review_ticks": 2, "terminal_cost": 0}}` |
| 1 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 1 | queue_snapshot | `{"busy": null, "pending": ["a0j0", "a1j0", "a2j0"]}` |
| 1 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 2 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a2j0"}` |
| 2 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a2j0", "job_loss": 0, "terminal_loss": 0}` |
| 2 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 2 | queue_snapshot | `{"busy": null, "pending": ["a0j0", "a1j0"]}` |
| 2 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 2 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 3 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a0j0"}` |
| 3 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a0j0", "job_loss": 0, "terminal_loss": 0}` |
| 3 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a1j0"}` |
| 3 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a1j0", "job_loss": 0, "terminal_loss": 0}` |
| 3 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 3 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 5 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j1", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 6 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 11, "job_id": "a0j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 0}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j1", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 1, "deadline": 11, "job_id": "a1j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j1", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 6 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 7, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}}` |
| 6 | dispatch_considered | `{"eligible": [{"agent_id": 1, "cost_per_tick": 1, "deadline": 11, "job_id": "a1j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}], "selected": "a1j1"}` |
| 6 | review_started | `{"finish": 8, "job_id": "a1j1", "start": 6}` |
| 6 | queue_snapshot | `{"busy": {"finish": 8, "job_id": "a1j1", "start": 6}, "pending": ["a0j1", "a2j1"]}` |
| 6 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 7 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a2j1"}` |
| 7 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j1", "job_loss": 0, "terminal_loss": 0}` |
| 7 | queue_snapshot | `{"busy": {"finish": 8, "job_id": "a1j1", "start": 6}, "pending": ["a0j1"]}` |
| 7 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 8 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a1j1", "late": false}` |
| 8 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 8 | queue_snapshot | `{"busy": null, "pending": ["a0j1"]}` |
| 8 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 8 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 9 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 9 | queue_snapshot | `{"busy": null, "pending": ["a0j1"]}` |
| 9 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 9 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 10 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 10 | queue_snapshot | `{"busy": null, "pending": ["a0j1"]}` |
| 10 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 10 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 11 | request_expired | `{"category": "zero_value", "initial_proposal_wrong": false, "job_id": "a0j1"}` |
| 11 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a0j1", "job_loss": 0, "terminal_loss": 0}` |
| 11 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a1j1", "job_loss": 0, "terminal_loss": 0}` |
| 11 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 0, "attempts": 12, "completion_tokens": 84, "correct_jobs": 6, "corrections": 0, "episode_wall_seconds": 2.203984, "error": null, "evidence": "live_gpu", "expired_requests": 5, "incomplete_service": null, "jobs_closed": 6, "late_returns": 0, "loss_upper_bound": 26, "planned_calls": 12, "policy": "delay", "prompt_tokens": 2458, "request_wall_seconds": 1.653924746438861, "review_busy_ticks": 2, "reviews_completed": 1, "reviews_started": 1, "scenario_hash": "4b7cc93f1fec65f6a0e9437ccb25792b11e34e11adc920d8d68a409e8c8a8646", "scheduled_calls": 12, "seed": 218, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 0, "unknown_token_attempts": 0}` |
