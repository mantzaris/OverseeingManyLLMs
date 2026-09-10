# Episode trace

Evidence: **live_gpu**, policy **uncertainty**, scenario seed 304.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 2, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 5, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 4}}` |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 4, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 12}}` |
| 0 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 0, "deadline": 2, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}, {"agent_id": 1, "cost_per_tick": 0, "deadline": 5, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 4}, {"agent_id": 2, "cost_per_tick": 0, "deadline": 4, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 12}], "selected": "a0j0"}` |
| 0 | review_started | `{"finish": 2, "job_id": "a0j0", "start": 0}` |
| 0 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a0j0", "start": 0}, "pending": ["a1j0", "a2j0"]}` |
| 0 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 1 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a0j0", "start": 0}, "pending": ["a1j0", "a2j0"]}` |
| 1 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 2 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a0j0", "late": false}` |
| 2 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a0j0", "job_loss": 0, "terminal_loss": 0}` |
| 2 | dispatch_considered | `{"eligible": [{"agent_id": 1, "cost_per_tick": 0, "deadline": 5, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 4}, {"agent_id": 2, "cost_per_tick": 0, "deadline": 4, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 12}], "selected": "a1j0"}` |
| 2 | review_started | `{"finish": 4, "job_id": "a1j0", "start": 2}` |
| 2 | queue_snapshot | `{"busy": {"finish": 4, "job_id": "a1j0", "start": 2}, "pending": ["a2j0"]}` |
| 2 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 2 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 3 | queue_snapshot | `{"busy": {"finish": 4, "job_id": "a1j0", "start": 2}, "pending": ["a2j0"]}` |
| 3 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 3 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 4 | review_completed | `{"applied": true, "changed": true, "instructed_action": "reset_sensor", "job_id": "a1j0", "late": false}` |
| 4 | request_expired | `{"category": "opportunity_lost_while_waiting", "initial_proposal_wrong": false, "job_id": "a2j0"}` |
| 4 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a2j0", "job_loss": 0, "terminal_loss": 0}` |
| 4 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 5 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a1j0", "job_loss": 0, "terminal_loss": 0}` |
| 5 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j1", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 10, "job_id": "a0j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 12}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j1", "p_error": 0.14606741573033707, "primary": "reset_sensor", "secondary": "reset_sensor"}` |
| 6 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 8, "job_id": "a1j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j1", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 11, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 4}}` |
| 6 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 0, "deadline": 10, "job_id": "a0j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 12}, {"agent_id": 1, "cost_per_tick": 0, "deadline": 8, "job_id": "a1j1", "p_error": 0.14606741573033707, "proposal": "reset_sensor", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}, {"agent_id": 2, "cost_per_tick": 0, "deadline": 11, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 4}], "selected": "a0j1"}` |
| 6 | review_started | `{"finish": 8, "job_id": "a0j1", "start": 6}` |
| 6 | queue_snapshot | `{"busy": {"finish": 8, "job_id": "a0j1", "start": 6}, "pending": ["a1j1", "a2j1"]}` |
| 6 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 7 | queue_snapshot | `{"busy": {"finish": 8, "job_id": "a0j1", "start": 6}, "pending": ["a1j1", "a2j1"]}` |
| 7 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 8 | review_completed | `{"applied": true, "changed": true, "instructed_action": "reset_sensor", "job_id": "a0j1", "late": false}` |
| 8 | request_expired | `{"category": "opportunity_lost_while_waiting", "initial_proposal_wrong": true, "job_id": "a1j1"}` |
| 8 | job_closed | `{"action": "reset_sensor", "correct": false, "job_id": "a1j1", "job_loss": 8, "terminal_loss": 8}` |
| 8 | dispatch_considered | `{"eligible": [{"agent_id": 2, "cost_per_tick": 0, "deadline": 11, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 4}], "selected": "a2j1"}` |
| 8 | review_started | `{"finish": 10, "job_id": "a2j1", "start": 8}` |
| 8 | queue_snapshot | `{"busy": {"finish": 10, "job_id": "a2j1", "start": 8}, "pending": []}` |
| 8 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 8 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 9 | queue_snapshot | `{"busy": {"finish": 10, "job_id": "a2j1", "start": 8}, "pending": []}` |
| 9 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 9 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 10 | review_completed | `{"applied": true, "changed": true, "instructed_action": "reset_sensor", "job_id": "a2j1", "late": false}` |
| 10 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a0j1", "job_loss": 0, "terminal_loss": 0}` |
| 10 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 11 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j1", "job_loss": 0, "terminal_loss": 0}` |
| 11 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 8, "attempts": 12, "completion_tokens": 84, "correct_jobs": 5, "corrections": 3, "episode_wall_seconds": 2.239841, "error": null, "evidence": "live_gpu", "expired_requests": 2, "incomplete_service": null, "jobs_closed": 6, "late_returns": 0, "loss_upper_bound": 48, "planned_calls": 12, "policy": "uncertainty", "prompt_tokens": 2570, "request_wall_seconds": 1.6671506818383932, "review_busy_ticks": 8, "reviews_completed": 4, "reviews_started": 4, "scenario_hash": "a81cceb92dcb078054c398795cb98e97b94a5c678b0272b5036654960f08a38f", "scheduled_calls": 12, "seed": 304, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 8, "unknown_token_attempts": 0}` |
