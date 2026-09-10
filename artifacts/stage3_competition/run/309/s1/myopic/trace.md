# Episode trace

Evidence: **live_gpu**, policy **myopic**, scenario seed 309.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j0", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 5, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 1, "terminal_cost": 4}}` |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j0", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 0 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 4, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 1, "terminal_cost": 8}}` |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 2, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 1, "terminal_cost": 12}}` |
| 0 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 0, "deadline": 5, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 1, "terminal_cost": 4}, {"agent_id": 1, "cost_per_tick": 0, "deadline": 4, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 1, "terminal_cost": 8}, {"agent_id": 2, "cost_per_tick": 0, "deadline": 2, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 1, "terminal_cost": 12}], "selected": "a2j0"}` |
| 0 | review_started | `{"finish": 1, "job_id": "a2j0", "start": 0}` |
| 0 | queue_snapshot | `{"busy": {"finish": 1, "job_id": "a2j0", "start": 0}, "pending": ["a0j0", "a1j0"]}` |
| 0 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 1 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a2j0", "late": false}` |
| 1 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 0, "deadline": 5, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 1, "terminal_cost": 4}, {"agent_id": 1, "cost_per_tick": 0, "deadline": 4, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 1, "terminal_cost": 8}], "selected": "a1j0"}` |
| 1 | review_started | `{"finish": 2, "job_id": "a1j0", "start": 1}` |
| 1 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a1j0", "start": 1}, "pending": ["a0j0"]}` |
| 1 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 2 | review_completed | `{"applied": true, "changed": false, "instructed_action": "reset_sensor", "job_id": "a1j0", "late": false}` |
| 2 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a2j0", "job_loss": 0, "terminal_loss": 0}` |
| 2 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 0, "deadline": 5, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 0, "review_ticks": 1, "terminal_cost": 4}], "selected": "a0j0"}` |
| 2 | review_started | `{"finish": 3, "job_id": "a0j0", "start": 2}` |
| 2 | queue_snapshot | `{"busy": {"finish": 3, "job_id": "a0j0", "start": 2}, "pending": []}` |
| 2 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 2 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 3 | review_completed | `{"applied": true, "changed": false, "instructed_action": "reset_sensor", "job_id": "a0j0", "late": false}` |
| 3 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 3 | queue_snapshot | `{"busy": null, "pending": []}` |
| 3 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 3 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 4 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a1j0", "job_loss": 0, "terminal_loss": 0}` |
| 4 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 5 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a0j0", "job_loss": 0, "terminal_loss": 0}` |
| 5 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j1", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 6 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 10, "job_id": "a0j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 1, "terminal_cost": 12}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j1", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 6 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 11, "job_id": "a1j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 1, "terminal_cost": 8}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j1", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 6 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 8, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 1, "terminal_cost": 4}}` |
| 6 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 0, "deadline": 10, "job_id": "a0j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 1, "terminal_cost": 12}, {"agent_id": 1, "cost_per_tick": 0, "deadline": 11, "job_id": "a1j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 1, "terminal_cost": 8}, {"agent_id": 2, "cost_per_tick": 0, "deadline": 8, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 1, "terminal_cost": 4}], "selected": "a0j1"}` |
| 6 | review_started | `{"finish": 7, "job_id": "a0j1", "start": 6}` |
| 6 | queue_snapshot | `{"busy": {"finish": 7, "job_id": "a0j1", "start": 6}, "pending": ["a1j1", "a2j1"]}` |
| 6 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 7 | review_completed | `{"applied": true, "changed": false, "instructed_action": "reset_sensor", "job_id": "a0j1", "late": false}` |
| 7 | dispatch_considered | `{"eligible": [{"agent_id": 1, "cost_per_tick": 0, "deadline": 11, "job_id": "a1j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 1, "terminal_cost": 8}, {"agent_id": 2, "cost_per_tick": 0, "deadline": 8, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 1, "terminal_cost": 4}], "selected": "a1j1"}` |
| 7 | review_started | `{"finish": 8, "job_id": "a1j1", "start": 7}` |
| 7 | queue_snapshot | `{"busy": {"finish": 8, "job_id": "a1j1", "start": 7}, "pending": ["a2j1"]}` |
| 7 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 8 | review_completed | `{"applied": true, "changed": false, "instructed_action": "reset_sensor", "job_id": "a1j1", "late": false}` |
| 8 | request_expired | `{"category": "opportunity_lost_while_waiting", "initial_proposal_wrong": false, "job_id": "a2j1"}` |
| 8 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j1", "job_loss": 0, "terminal_loss": 0}` |
| 8 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 8 | queue_snapshot | `{"busy": null, "pending": []}` |
| 8 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 8 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 9 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 9 | queue_snapshot | `{"busy": null, "pending": []}` |
| 9 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 9 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 10 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a0j1", "job_loss": 0, "terminal_loss": 0}` |
| 10 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 11 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a1j1", "job_loss": 0, "terminal_loss": 0}` |
| 11 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 0, "attempts": 12, "completion_tokens": 84, "correct_jobs": 6, "corrections": 0, "episode_wall_seconds": 2.311646, "error": null, "evidence": "live_gpu", "expired_requests": 1, "incomplete_service": null, "jobs_closed": 6, "late_returns": 0, "loss_upper_bound": 48, "planned_calls": 12, "policy": "myopic", "prompt_tokens": 2624, "request_wall_seconds": 1.6740057859569788, "review_busy_ticks": 5, "reviews_completed": 5, "reviews_started": 5, "scenario_hash": "0d7d5ad3af2f381873bf076a5d698b70db0787fa77cbc6bf590a6cc8200c09e4", "scheduled_calls": 12, "seed": 309, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 0, "unknown_token_attempts": 0}` |
