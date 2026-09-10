# Episode trace

Evidence: **stipulated_mechanics_only**, policy **delay**, scenario seed -5.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "stipulated_mechanics_only", "job_id": "B", "p_error": 0.2, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 2, "job_id": "B", "p_error": 0.2, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 2, "terminal_cost": 12}}` |
| 0 | proposal | `{"agreement": true, "evidence": "stipulated_mechanics_only", "job_id": "A", "p_error": 0.5, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 2, "job_id": "A", "p_error": 0.5, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | review_started | `{"finish": 2, "job_id": "A", "start": 0}` |
| 0 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "A", "start": 0}, "pending": ["B"]}` |
| 0 | interval_scored | `{"job_id": "B", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "A", "loss": 0}` |
| 1 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "A", "start": 0}, "pending": ["B"]}` |
| 1 | interval_scored | `{"job_id": "B", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "A", "loss": 0}` |
| 2 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "A", "late": false}` |
| 2 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "A", "job_loss": 0, "terminal_loss": 0}` |
| 2 | request_expired | `{"category": "opportunity_lost_while_waiting", "initial_proposal_wrong": true, "job_id": "B"}` |
| 2 | job_closed | `{"action": "reset_sensor", "correct": false, "job_id": "B", "job_loss": 12, "terminal_loss": 12}` |
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
| 12 | episode_finished | `{"accrued_loss": 12, "attempts": 0, "completion_tokens": 0, "correct_jobs": 1, "corrections": 0, "episode_wall_seconds": 0.129214, "error": null, "evidence": "stipulated_mechanics_only", "expired_requests": 1, "incomplete_service": null, "jobs_closed": 2, "late_returns": 0, "loss_upper_bound": 20, "planned_calls": 0, "policy": "delay", "prompt_tokens": 0, "request_wall_seconds": 0.0, "review_busy_ticks": 2, "reviews_completed": 1, "reviews_started": 1, "scenario_hash": "63b38c723ffb639b1456a38b73f76fa45afe65b98c35f9f60549e7d93c94c874", "scheduled_calls": 0, "seed": -5, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 12, "unknown_token_attempts": 0}` |
