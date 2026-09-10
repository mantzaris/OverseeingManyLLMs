# Episode trace

Evidence: **live_gpu**, policy **fcfs**, scenario seed 208.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j0", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 5, "job_id": "a2j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 0}}` |
| 0 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 0 | queue_snapshot | `{"busy": null, "pending": ["a2j0"]}` |
| 0 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j0", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 1 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 3, "deadline": 3, "job_id": "a0j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 1, "review_ticks": 2, "terminal_cost": 8}}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j0", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 1 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 3, "deadline": 2, "job_id": "a1j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 1, "review_ticks": 2, "terminal_cost": 0}}` |
| 1 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 3, "deadline": 3, "job_id": "a0j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 1, "review_ticks": 2, "terminal_cost": 8}], "selected": "a0j0"}` |
| 1 | review_started | `{"finish": 3, "job_id": "a0j0", "start": 1}` |
| 1 | queue_snapshot | `{"busy": {"finish": 3, "job_id": "a0j0", "start": 1}, "pending": ["a1j0", "a2j0"]}` |
| 1 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a1j0", "loss": 3}` |
| 2 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": true, "job_id": "a1j0"}` |
| 2 | job_closed | `{"action": "replace_filter", "correct": false, "job_id": "a1j0", "job_loss": 3, "terminal_loss": 0}` |
| 2 | queue_snapshot | `{"busy": {"finish": 3, "job_id": "a0j0", "start": 1}, "pending": ["a2j0"]}` |
| 2 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 2 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 3 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a0j0", "late": false}` |
| 3 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a0j0", "job_loss": 0, "terminal_loss": 0}` |
| 3 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 3 | queue_snapshot | `{"busy": null, "pending": ["a2j0"]}` |
| 3 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 4 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 4 | queue_snapshot | `{"busy": null, "pending": ["a2j0"]}` |
| 4 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 5 | request_expired | `{"category": "zero_value", "initial_proposal_wrong": false, "job_id": "a2j0"}` |
| 5 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a2j0", "job_loss": 0, "terminal_loss": 0}` |
| 5 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 6 | queue_snapshot | `{"busy": null, "pending": []}` |
| 7 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j1", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 7 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 1, "deadline": 8, "job_id": "a0j1", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 7, "review_ticks": 2, "terminal_cost": 0}}` |
| 7 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j1", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 7 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 9, "job_id": "a1j1", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 7, "review_ticks": 2, "terminal_cost": 0}}` |
| 7 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j1", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 7 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 3, "deadline": 8, "job_id": "a2j1", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 7, "review_ticks": 2, "terminal_cost": 8}}` |
| 7 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 7 | queue_snapshot | `{"busy": null, "pending": ["a0j1", "a1j1", "a2j1"]}` |
| 7 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 8 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a0j1"}` |
| 8 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a0j1", "job_loss": 0, "terminal_loss": 0}` |
| 8 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a2j1"}` |
| 8 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j1", "job_loss": 0, "terminal_loss": 0}` |
| 8 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 8 | queue_snapshot | `{"busy": null, "pending": ["a1j1"]}` |
| 8 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 9 | request_expired | `{"category": "zero_value", "initial_proposal_wrong": false, "job_id": "a1j1"}` |
| 9 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a1j1", "job_loss": 0, "terminal_loss": 0}` |
| 9 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 9 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 11 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 3, "attempts": 12, "completion_tokens": 84, "correct_jobs": 5, "corrections": 0, "episode_wall_seconds": 2.231064, "error": null, "evidence": "live_gpu", "expired_requests": 5, "incomplete_service": null, "jobs_closed": 6, "late_returns": 0, "loss_upper_bound": 29, "planned_calls": 12, "policy": "fcfs", "prompt_tokens": 2508, "request_wall_seconds": 1.6818787921220064, "review_busy_ticks": 2, "reviews_completed": 1, "reviews_started": 1, "scenario_hash": "84d2f74bed0d9c879fc461dcd18e089c4dbee88ba5c6ac8ed1ada1debcf9b114", "scheduled_calls": 12, "seed": 208, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 3, "unknown_token_attempts": 0}` |
