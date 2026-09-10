# Episode trace

Evidence: **stipulated_mechanics_only**, policy **myopic**, scenario seed -3.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "stipulated_mechanics_only", "job_id": "A", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 2, "job_id": "A", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | proposal | `{"agreement": true, "evidence": "stipulated_mechanics_only", "job_id": "B", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 5, "job_id": "B", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 12}}` |
| 0 | review_started | `{"finish": 2, "job_id": "B", "start": 0}` |
| 0 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "B", "start": 0}, "pending": ["A"]}` |
| 0 | interval_scored | `{"job_id": "A", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "B", "loss": 0}` |
| 1 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "B", "start": 0}, "pending": ["A"]}` |
| 1 | interval_scored | `{"job_id": "A", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "B", "loss": 0}` |
| 2 | review_completed | `{"applied": true, "changed": true, "instructed_action": "replace_filter", "job_id": "B", "late": false}` |
| 2 | request_expired | `{"category": "opportunity_lost_while_waiting", "initial_proposal_wrong": true, "job_id": "A"}` |
| 2 | job_closed | `{"action": "reset_sensor", "correct": false, "job_id": "A", "job_loss": 8, "terminal_loss": 8}` |
| 2 | queue_snapshot | `{"busy": null, "pending": []}` |
| 2 | interval_scored | `{"job_id": "B", "loss": 0}` |
| 3 | queue_snapshot | `{"busy": null, "pending": []}` |
| 3 | interval_scored | `{"job_id": "B", "loss": 0}` |
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
| 12 | episode_finished | `{"accrued_loss": 8, "attempts": 0, "completion_tokens": 0, "correct_jobs": 1, "corrections": 1, "episode_wall_seconds": 0.134215, "error": null, "evidence": "stipulated_mechanics_only", "expired_requests": 1, "incomplete_service": null, "jobs_closed": 2, "late_returns": 0, "loss_upper_bound": 20, "planned_calls": 0, "policy": "myopic", "prompt_tokens": 0, "request_wall_seconds": 0.0, "review_busy_ticks": 2, "reviews_completed": 1, "reviews_started": 1, "scenario_hash": "711d26d35fef192cba117f5e66fd0f1686a21a6c2e930434860896dac46fb8c4", "scheduled_calls": 0, "seed": -3, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 8, "unknown_token_attempts": 0}` |
