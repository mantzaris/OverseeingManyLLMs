# Episode trace

Evidence: **live_gpu**, policy **fcfs**, scenario seed 203.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j0", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 1, "job_id": "a0j0", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j0", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 3, "deadline": 2, "job_id": "a1j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | dispatch_considered | `{"eligible": [{"agent_id": 1, "cost_per_tick": 3, "deadline": 2, "job_id": "a1j0", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}], "selected": "a1j0"}` |
| 0 | review_started | `{"finish": 2, "job_id": "a1j0", "start": 0}` |
| 0 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a1j0", "start": 0}, "pending": ["a0j0"]}` |
| 0 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 1 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": true, "job_id": "a0j0"}` |
| 1 | job_closed | `{"action": "reset_sensor", "correct": false, "job_id": "a0j0", "job_loss": 8, "terminal_loss": 8}` |
| 1 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j0", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 1 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 3, "deadline": 3, "job_id": "a2j0", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 1, "review_ticks": 2, "terminal_cost": 0}}` |
| 1 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a1j0", "start": 0}, "pending": ["a2j0"]}` |
| 1 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 2 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a1j0", "late": false}` |
| 2 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a1j0", "job_loss": 0, "terminal_loss": 0}` |
| 2 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 2 | queue_snapshot | `{"busy": null, "pending": ["a2j0"]}` |
| 2 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 3 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a2j0"}` |
| 3 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j0", "job_loss": 0, "terminal_loss": 0}` |
| 3 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 3 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 5 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j1", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 3, "deadline": 7, "job_id": "a0j1", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 0}}` |
| 6 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 6 | queue_snapshot | `{"busy": null, "pending": ["a0j1"]}` |
| 6 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 7 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": false, "job_id": "a0j1"}` |
| 7 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a0j1", "job_loss": 0, "terminal_loss": 0}` |
| 7 | proposal | `{"agreement": false, "evidence": "live_gpu", "job_id": "a1j1", "p_error": 0.5, "primary": "replace_filter", "secondary": "reset_sensor"}` |
| 7 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 9, "job_id": "a1j1", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 7, "review_ticks": 2, "terminal_cost": 8}}` |
| 7 | proposal | `{"agreement": false, "evidence": "live_gpu", "job_id": "a2j1", "p_error": 0.5, "primary": "reset_sensor", "secondary": "replace_filter"}` |
| 7 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 1, "deadline": 9, "job_id": "a2j1", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 7, "review_ticks": 2, "terminal_cost": 8}}` |
| 7 | dispatch_considered | `{"eligible": [{"agent_id": 1, "cost_per_tick": 0, "deadline": 9, "job_id": "a1j1", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 7, "review_ticks": 2, "terminal_cost": 8}, {"agent_id": 2, "cost_per_tick": 1, "deadline": 9, "job_id": "a2j1", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 7, "review_ticks": 2, "terminal_cost": 8}], "selected": "a1j1"}` |
| 7 | review_started | `{"finish": 9, "job_id": "a1j1", "start": 7}` |
| 7 | queue_snapshot | `{"busy": {"finish": 9, "job_id": "a1j1", "start": 7}, "pending": ["a2j1"]}` |
| 7 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 8 | queue_snapshot | `{"busy": {"finish": 9, "job_id": "a1j1", "start": 7}, "pending": ["a2j1"]}` |
| 8 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 8 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 9 | review_completed | `{"applied": true, "changed": true, "instructed_action": "reset_sensor", "job_id": "a1j1", "late": false}` |
| 9 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a1j1", "job_loss": 0, "terminal_loss": 0}` |
| 9 | request_expired | `{"category": "opportunity_lost_while_waiting", "initial_proposal_wrong": false, "job_id": "a2j1"}` |
| 9 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j1", "job_loss": 0, "terminal_loss": 0}` |
| 9 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 9 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 11 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 8, "attempts": 12, "completion_tokens": 84, "correct_jobs": 5, "corrections": 1, "episode_wall_seconds": 2.213755, "error": null, "evidence": "live_gpu", "expired_requests": 4, "incomplete_service": null, "jobs_closed": 6, "late_returns": 0, "loss_upper_bound": 49, "planned_calls": 12, "policy": "fcfs", "prompt_tokens": 2508, "request_wall_seconds": 1.684391489252448, "review_busy_ticks": 4, "reviews_completed": 2, "reviews_started": 2, "scenario_hash": "f813b9bea89d2c6b9c515f8620a2d6f28b246600b81688e61e58c51e40df0f80", "scheduled_calls": 12, "seed": 203, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 8, "unknown_token_attempts": 0}` |
