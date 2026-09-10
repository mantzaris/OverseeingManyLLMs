# Episode trace

Evidence: **live_gpu**, policy **myopic**, scenario seed 221.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j0", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 1, "deadline": 1, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 0 | queue_snapshot | `{"busy": null, "pending": ["a0j0"]}` |
| 0 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 1 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a0j0"}` |
| 1 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a0j0", "job_loss": 0, "terminal_loss": 0}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j0", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 1 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 1, "deadline": 2, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 1, "review_ticks": 2, "terminal_cost": 0}}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j0", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 1 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 3, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 1, "review_ticks": 2, "terminal_cost": 8}}` |
| 1 | dispatch_considered | `{"eligible": [{"agent_id": 2, "cost_per_tick": 0, "deadline": 3, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 1, "review_ticks": 2, "terminal_cost": 8}], "selected": "a2j0"}` |
| 1 | review_started | `{"finish": 3, "job_id": "a2j0", "start": 1}` |
| 1 | queue_snapshot | `{"busy": {"finish": 3, "job_id": "a2j0", "start": 1}, "pending": ["a1j0"]}` |
| 1 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 2 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a1j0"}` |
| 2 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a1j0", "job_loss": 0, "terminal_loss": 0}` |
| 2 | queue_snapshot | `{"busy": {"finish": 3, "job_id": "a2j0", "start": 1}, "pending": []}` |
| 2 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 3 | review_completed | `{"applied": true, "changed": false, "instructed_action": "reset_sensor", "job_id": "a2j0", "late": false}` |
| 3 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j0", "job_loss": 0, "terminal_loss": 0}` |
| 3 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 3 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 5 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j1", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 6 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 3, "deadline": 8, "job_id": "a0j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 0}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j1", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 11, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}}` |
| 6 | dispatch_considered | `{"eligible": [{"agent_id": 2, "cost_per_tick": 0, "deadline": 11, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}], "selected": "a2j1"}` |
| 6 | review_started | `{"finish": 8, "job_id": "a2j1", "start": 6}` |
| 6 | queue_snapshot | `{"busy": {"finish": 8, "job_id": "a2j1", "start": 6}, "pending": ["a0j1"]}` |
| 6 | interval_scored | `{"job_id": "a0j1", "loss": 3}` |
| 6 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 7 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j1", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 7 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 1, "deadline": 12, "job_id": "a1j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 7, "review_ticks": 2, "terminal_cost": 0}}` |
| 7 | queue_snapshot | `{"busy": {"finish": 8, "job_id": "a2j1", "start": 6}, "pending": ["a0j1", "a1j1"]}` |
| 7 | interval_scored | `{"job_id": "a0j1", "loss": 3}` |
| 7 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 8 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a2j1", "late": false}` |
| 8 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": true, "job_id": "a0j1"}` |
| 8 | job_closed | `{"action": "reset_sensor", "correct": false, "job_id": "a0j1", "job_loss": 6, "terminal_loss": 0}` |
| 8 | dispatch_considered | `{"eligible": [{"agent_id": 1, "cost_per_tick": 1, "deadline": 12, "job_id": "a1j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 7, "review_ticks": 2, "terminal_cost": 0}], "selected": "a1j1"}` |
| 8 | review_started | `{"finish": 10, "job_id": "a1j1", "start": 8}` |
| 8 | queue_snapshot | `{"busy": {"finish": 10, "job_id": "a1j1", "start": 8}, "pending": []}` |
| 8 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 8 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 9 | queue_snapshot | `{"busy": {"finish": 10, "job_id": "a1j1", "start": 8}, "pending": []}` |
| 9 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 9 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 10 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a1j1", "late": false}` |
| 10 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 10 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 11 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a2j1", "job_loss": 0, "terminal_loss": 0}` |
| 11 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 11 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 12 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a1j1", "job_loss": 0, "terminal_loss": 0}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 6, "attempts": 12, "completion_tokens": 84, "correct_jobs": 5, "corrections": 0, "episode_wall_seconds": 2.181399, "error": null, "evidence": "live_gpu", "expired_requests": 3, "incomplete_service": null, "jobs_closed": 6, "late_returns": 0, "loss_upper_bound": 37, "planned_calls": 12, "policy": "myopic", "prompt_tokens": 2512, "request_wall_seconds": 1.6778752356767654, "review_busy_ticks": 6, "reviews_completed": 3, "reviews_started": 3, "scenario_hash": "4e37da73fd2728aa92698fd396b037abbe5d2658e9ddc674fedb3a6d6ff55a43", "scheduled_calls": 12, "seed": 221, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 6, "unknown_token_attempts": 0}` |
