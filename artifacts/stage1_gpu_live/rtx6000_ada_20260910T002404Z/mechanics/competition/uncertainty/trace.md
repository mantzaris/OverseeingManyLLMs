# Episode trace

Evidence: **stipulated_mechanics_only**, policy **uncertainty**, scenario seed -3.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "stipulated_mechanics_only", "job_id": "A", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 2, "job_id": "A", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | proposal | `{"agreement": true, "evidence": "stipulated_mechanics_only", "job_id": "B", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 5, "job_id": "B", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 12}}` |
| 0 | review_started | `{"finish": 2, "job_id": "A", "start": 0}` |
| 0 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "A", "start": 0}, "pending": ["B"]}` |
| 0 | interval_scored | `{"job_id": "A", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "B", "loss": 0}` |
| 1 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "A", "start": 0}, "pending": ["B"]}` |
| 1 | interval_scored | `{"job_id": "A", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "B", "loss": 0}` |
| 2 | review_completed | `{"applied": true, "changed": true, "instructed_action": "replace_filter", "job_id": "A", "late": false}` |
| 2 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "A", "job_loss": 0, "terminal_loss": 0}` |
| 2 | review_started | `{"finish": 4, "job_id": "B", "start": 2}` |
| 2 | queue_snapshot | `{"busy": {"finish": 4, "job_id": "B", "start": 2}, "pending": []}` |
| 2 | interval_scored | `{"job_id": "B", "loss": 0}` |
| 3 | queue_snapshot | `{"busy": {"finish": 4, "job_id": "B", "start": 2}, "pending": []}` |
| 3 | interval_scored | `{"job_id": "B", "loss": 0}` |
| 4 | review_completed | `{"applied": true, "changed": true, "instructed_action": "replace_filter", "job_id": "B", "late": false}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | interval_scored | `{"job_id": "B", "loss": 0}` |
| 5 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "B", "job_loss": 0, "terminal_loss": 0}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | queue_snapshot | `{"busy": null, "pending": []}` |
| 7 | queue_snapshot | `{"busy": null, "pending": []}` |
| 8 | queue_snapshot | `{"busy": null, "pending": []}` |
| 9 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 0, "attempts": 0, "completion_tokens": 0, "correct_jobs": 2, "corrections": 2, "episode_wall_seconds": 0.138924, "error": null, "evidence": "stipulated_mechanics_only", "expired_requests": 0, "incomplete_service": null, "jobs_closed": 2, "late_returns": 0, "loss_upper_bound": 20, "planned_calls": 0, "policy": "uncertainty", "prompt_tokens": 0, "request_wall_seconds": 0.0, "review_busy_ticks": 4, "reviews_completed": 2, "reviews_started": 2, "scenario_hash": "711d26d35fef192cba117f5e66fd0f1686a21a6c2e930434860896dac46fb8c4", "scheduled_calls": 0, "seed": -3, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 0, "unknown_token_attempts": 0}` |
