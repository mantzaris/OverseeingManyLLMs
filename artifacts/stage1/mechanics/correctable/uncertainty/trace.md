# Episode trace

Evidence: **stipulated_mechanics_only**, policy **uncertainty**, scenario seed -2.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "stipulated_mechanics_only", "job_id": "correctable", "p_error": 0.5, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 1, "deadline": 5, "job_id": "correctable", "p_error": 0.5, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | review_started | `{"finish": 2, "job_id": "correctable", "start": 0}` |
| 0 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "correctable", "start": 0}, "pending": []}` |
| 0 | interval_scored | `{"job_id": "correctable", "loss": 1}` |
| 1 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "correctable", "start": 0}, "pending": []}` |
| 1 | interval_scored | `{"job_id": "correctable", "loss": 1}` |
| 2 | review_completed | `{"applied": true, "changed": true, "instructed_action": "replace_filter", "job_id": "correctable", "late": false}` |
| 2 | queue_snapshot | `{"busy": null, "pending": []}` |
| 2 | interval_scored | `{"job_id": "correctable", "loss": 0}` |
| 3 | queue_snapshot | `{"busy": null, "pending": []}` |
| 3 | interval_scored | `{"job_id": "correctable", "loss": 0}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | interval_scored | `{"job_id": "correctable", "loss": 0}` |
| 5 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "correctable", "job_loss": 2, "terminal_loss": 0}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | queue_snapshot | `{"busy": null, "pending": []}` |
| 7 | queue_snapshot | `{"busy": null, "pending": []}` |
| 8 | queue_snapshot | `{"busy": null, "pending": []}` |
| 9 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 2, "attempts": 0, "completion_tokens": 0, "correct_jobs": 1, "corrections": 1, "episode_wall_seconds": 0.001653, "error": null, "evidence": "stipulated_mechanics_only", "expired_requests": 0, "incomplete_service": null, "jobs_closed": 1, "late_returns": 0, "loss_upper_bound": 13, "planned_calls": 0, "policy": "uncertainty", "prompt_tokens": 0, "request_wall_seconds": 0.0, "review_busy_ticks": 2, "reviews_completed": 1, "reviews_started": 1, "scenario_hash": "ec65dc1147c6eac108a8295b5bb92fe9dcaa32e0f11a4101cd226894495ecdc1", "scheduled_calls": 0, "seed": -2, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 2, "unknown_token_attempts": 0}` |
