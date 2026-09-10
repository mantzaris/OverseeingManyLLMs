# Episode trace

Evidence: **live_gpu**, policy **fcfs**, scenario seed 205.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 0 | queue_snapshot | `{"busy": null, "pending": []}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j0", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 1 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 1, "deadline": 3, "job_id": "a0j0", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 1, "review_ticks": 2, "terminal_cost": 0}}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j0", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 1 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 1, "deadline": 3, "job_id": "a1j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 1, "review_ticks": 2, "terminal_cost": 0}}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j0", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 1 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 3, "deadline": 3, "job_id": "a2j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 1, "review_ticks": 2, "terminal_cost": 8}}` |
| 1 | dispatch_considered | `{"eligible": [{"agent_id": 2, "cost_per_tick": 3, "deadline": 3, "job_id": "a2j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 1, "review_ticks": 2, "terminal_cost": 8}], "selected": "a2j0"}` |
| 1 | review_started | `{"finish": 3, "job_id": "a2j0", "start": 1}` |
| 1 | queue_snapshot | `{"busy": {"finish": 3, "job_id": "a2j0", "start": 1}, "pending": ["a0j0", "a1j0"]}` |
| 1 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a2j0", "loss": 3}` |
| 2 | queue_snapshot | `{"busy": {"finish": 3, "job_id": "a2j0", "start": 1}, "pending": ["a0j0", "a1j0"]}` |
| 2 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 2 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 2 | interval_scored | `{"job_id": "a2j0", "loss": 3}` |
| 3 | review_completed | `{"applied": true, "changed": true, "instructed_action": "reset_sensor", "job_id": "a2j0", "late": false}` |
| 3 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a0j0"}` |
| 3 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a0j0", "job_loss": 0, "terminal_loss": 0}` |
| 3 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a1j0"}` |
| 3 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a1j0", "job_loss": 0, "terminal_loss": 0}` |
| 3 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j0", "job_loss": 6, "terminal_loss": 0}` |
| 3 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 3 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 5 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j1", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 3, "deadline": 7, "job_id": "a0j1", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 0}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j1", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 8, "job_id": "a1j1", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 0}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j1", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 3, "deadline": 7, "job_id": "a2j1", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}}` |
| 6 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 6 | queue_snapshot | `{"busy": null, "pending": ["a0j1", "a1j1", "a2j1"]}` |
| 6 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 7 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a0j1"}` |
| 7 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a0j1", "job_loss": 0, "terminal_loss": 0}` |
| 7 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a2j1"}` |
| 7 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a2j1", "job_loss": 0, "terminal_loss": 0}` |
| 7 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 7 | queue_snapshot | `{"busy": null, "pending": ["a1j1"]}` |
| 7 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 8 | request_expired | `{"category": "zero_value", "initial_proposal_wrong": false, "job_id": "a1j1"}` |
| 8 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a1j1", "job_loss": 0, "terminal_loss": 0}` |
| 8 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 8 | queue_snapshot | `{"busy": null, "pending": []}` |
| 9 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 9 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 11 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 6, "attempts": 12, "completion_tokens": 84, "correct_jobs": 6, "corrections": 1, "episode_wall_seconds": 2.153423, "error": null, "evidence": "live_gpu", "expired_requests": 5, "incomplete_service": null, "jobs_closed": 6, "late_returns": 0, "loss_upper_bound": 32, "planned_calls": 12, "policy": "fcfs", "prompt_tokens": 2508, "request_wall_seconds": 1.6899690050631762, "review_busy_ticks": 2, "reviews_completed": 1, "reviews_started": 1, "scenario_hash": "3515383c2933c6ceb03d991da007d9e9111041bb2237d10646def4403030c640", "scheduled_calls": 12, "seed": 205, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 6, "unknown_token_attempts": 0}` |
