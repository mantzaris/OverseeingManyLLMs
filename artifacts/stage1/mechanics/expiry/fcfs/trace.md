# Episode trace

Evidence: **stipulated_mechanics_only**, policy **fcfs**, scenario seed -4.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "stipulated_mechanics_only", "job_id": "expiry", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 1, "deadline": 1, "job_id": "expiry", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | queue_snapshot | `{"busy": null, "pending": ["expiry"]}` |
| 0 | interval_scored | `{"job_id": "expiry", "loss": 1}` |
| 1 | request_expired | `{"category": "infeasible_at_arrival", "initial_proposal_wrong": true, "job_id": "expiry"}` |
| 1 | job_closed | `{"action": "reset_sensor", "correct": false, "job_id": "expiry", "job_loss": 9, "terminal_loss": 8}` |
| 1 | queue_snapshot | `{"busy": null, "pending": []}` |
| 2 | queue_snapshot | `{"busy": null, "pending": []}` |
| 3 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | queue_snapshot | `{"busy": null, "pending": []}` |
| 7 | queue_snapshot | `{"busy": null, "pending": []}` |
| 8 | queue_snapshot | `{"busy": null, "pending": []}` |
| 9 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 9, "attempts": 0, "completion_tokens": 0, "correct_jobs": 0, "corrections": 0, "episode_wall_seconds": 0.001222, "error": null, "evidence": "stipulated_mechanics_only", "expired_requests": 1, "incomplete_service": null, "jobs_closed": 1, "late_returns": 0, "loss_upper_bound": 9, "planned_calls": 0, "policy": "fcfs", "prompt_tokens": 0, "request_wall_seconds": 0.0, "review_busy_ticks": 0, "reviews_completed": 0, "reviews_started": 0, "scenario_hash": "05e2040b338e05026efaa9e1da9166805604ef02ca205bff5c655f905706dfc2", "scheduled_calls": 0, "seed": -4, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 9, "unknown_token_attempts": 0}` |
