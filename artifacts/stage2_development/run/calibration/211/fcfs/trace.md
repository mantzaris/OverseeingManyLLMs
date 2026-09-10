# Episode trace

Evidence: **live_gpu**, policy **fcfs**, scenario seed 211.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j0", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 1, "deadline": 2, "job_id": "a2j0", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | dispatch_considered | `{"eligible": [{"agent_id": 2, "cost_per_tick": 1, "deadline": 2, "job_id": "a2j0", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}], "selected": "a2j0"}` |
| 0 | review_started | `{"finish": 2, "job_id": "a2j0", "start": 0}` |
| 0 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a2j0", "start": 0}, "pending": []}` |
| 0 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j0", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 1 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 3, "deadline": 6, "job_id": "a0j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 1, "review_ticks": 2, "terminal_cost": 8}}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j0", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 1 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 3, "deadline": 2, "job_id": "a1j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 1, "review_ticks": 2, "terminal_cost": 8}}` |
| 1 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a2j0", "start": 0}, "pending": ["a0j0", "a1j0"]}` |
| 1 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 2 | review_completed | `{"applied": true, "changed": false, "instructed_action": "reset_sensor", "job_id": "a2j0", "late": false}` |
| 2 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a1j0"}` |
| 2 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a1j0", "job_loss": 0, "terminal_loss": 0}` |
| 2 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j0", "job_loss": 0, "terminal_loss": 0}` |
| 2 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 3, "deadline": 6, "job_id": "a0j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 1, "review_ticks": 2, "terminal_cost": 8}], "selected": "a0j0"}` |
| 2 | review_started | `{"finish": 4, "job_id": "a0j0", "start": 2}` |
| 2 | queue_snapshot | `{"busy": {"finish": 4, "job_id": "a0j0", "start": 2}, "pending": []}` |
| 2 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 3 | queue_snapshot | `{"busy": {"finish": 4, "job_id": "a0j0", "start": 2}, "pending": []}` |
| 3 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 4 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a0j0", "late": false}` |
| 4 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 5 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 5 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 6 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a0j0", "job_loss": 0, "terminal_loss": 0}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j1", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 6 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 3, "deadline": 11, "job_id": "a0j1", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 0}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j1", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 6 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 3, "deadline": 7, "job_id": "a1j1", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j1", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 6 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 11, "job_id": "a2j1", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}}` |
| 6 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 3, "deadline": 11, "job_id": "a0j1", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 0}, {"agent_id": 2, "cost_per_tick": 0, "deadline": 11, "job_id": "a2j1", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}], "selected": "a0j1"}` |
| 6 | review_started | `{"finish": 8, "job_id": "a0j1", "start": 6}` |
| 6 | queue_snapshot | `{"busy": {"finish": 8, "job_id": "a0j1", "start": 6}, "pending": ["a1j1", "a2j1"]}` |
| 6 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 7 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a1j1"}` |
| 7 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a1j1", "job_loss": 0, "terminal_loss": 0}` |
| 7 | queue_snapshot | `{"busy": {"finish": 8, "job_id": "a0j1", "start": 6}, "pending": ["a2j1"]}` |
| 7 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 8 | review_completed | `{"applied": true, "changed": false, "instructed_action": "reset_sensor", "job_id": "a0j1", "late": false}` |
| 8 | dispatch_considered | `{"eligible": [{"agent_id": 2, "cost_per_tick": 0, "deadline": 11, "job_id": "a2j1", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}], "selected": "a2j1"}` |
| 8 | review_started | `{"finish": 10, "job_id": "a2j1", "start": 8}` |
| 8 | queue_snapshot | `{"busy": {"finish": 10, "job_id": "a2j1", "start": 8}, "pending": []}` |
| 8 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 8 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 9 | queue_snapshot | `{"busy": {"finish": 10, "job_id": "a2j1", "start": 8}, "pending": []}` |
| 9 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 9 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 10 | review_completed | `{"applied": true, "changed": false, "instructed_action": "reset_sensor", "job_id": "a2j1", "late": false}` |
| 10 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 10 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 11 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a0j1", "job_loss": 0, "terminal_loss": 0}` |
| 11 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j1", "job_loss": 0, "terminal_loss": 0}` |
| 11 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 0, "attempts": 12, "completion_tokens": 84, "correct_jobs": 6, "corrections": 0, "episode_wall_seconds": 2.593744, "error": null, "evidence": "live_gpu", "expired_requests": 2, "incomplete_service": null, "jobs_closed": 6, "late_returns": 0, "loss_upper_bound": 78, "planned_calls": 12, "policy": "fcfs", "prompt_tokens": 2566, "request_wall_seconds": 1.685040621086955, "review_busy_ticks": 8, "reviews_completed": 4, "reviews_started": 4, "scenario_hash": "f04b137ccdf98a6c8504acb1ff412c1bda50021635d0f6890379b989144f7ae7", "scheduled_calls": 12, "seed": 211, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 0, "unknown_token_attempts": 0}` |
