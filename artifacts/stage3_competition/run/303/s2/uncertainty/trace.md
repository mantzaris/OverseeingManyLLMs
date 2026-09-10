# Episode trace

Evidence: **live_gpu**, policy **uncertainty**, scenario seed 303.

Scoring/diagnostic artifact; not an agent observation.

| Tick | Event | Details |
| --- | --- | --- |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 5, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 4}}` |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 2, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}}` |
| 0 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j0", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 0 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 4, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 12}}` |
| 0 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 0, "deadline": 5, "job_id": "a0j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 4}, {"agent_id": 1, "cost_per_tick": 0, "deadline": 2, "job_id": "a1j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 8}, {"agent_id": 2, "cost_per_tick": 0, "deadline": 4, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 12}], "selected": "a0j0"}` |
| 0 | review_started | `{"finish": 2, "job_id": "a0j0", "start": 0}` |
| 0 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a0j0", "start": 0}, "pending": ["a1j0", "a2j0"]}` |
| 0 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 0 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 1 | queue_snapshot | `{"busy": {"finish": 2, "job_id": "a0j0", "start": 0}, "pending": ["a1j0", "a2j0"]}` |
| 1 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a1j0", "loss": 0}` |
| 1 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 2 | review_completed | `{"applied": true, "changed": true, "instructed_action": "reset_sensor", "job_id": "a0j0", "late": false}` |
| 2 | request_expired | `{"category": "opportunity_lost_while_waiting", "initial_proposal_wrong": true, "job_id": "a1j0"}` |
| 2 | job_closed | `{"action": "replace_filter", "correct": false, "job_id": "a1j0", "job_loss": 8, "terminal_loss": 8}` |
| 2 | dispatch_considered | `{"eligible": [{"agent_id": 2, "cost_per_tick": 0, "deadline": 4, "job_id": "a2j0", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 0, "review_ticks": 2, "terminal_cost": 12}], "selected": "a2j0"}` |
| 2 | review_started | `{"finish": 4, "job_id": "a2j0", "start": 2}` |
| 2 | queue_snapshot | `{"busy": {"finish": 4, "job_id": "a2j0", "start": 2}, "pending": []}` |
| 2 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 2 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 3 | queue_snapshot | `{"busy": {"finish": 4, "job_id": "a2j0", "start": 2}, "pending": []}` |
| 3 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 3 | interval_scored | `{"job_id": "a2j0", "loss": 0}` |
| 4 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a2j0", "late": false}` |
| 4 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a2j0", "job_loss": 0, "terminal_loss": 0}` |
| 4 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 4 | queue_snapshot | `{"busy": null, "pending": []}` |
| 4 | interval_scored | `{"job_id": "a0j0", "loss": 0}` |
| 5 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a0j0", "job_loss": 0, "terminal_loss": 0}` |
| 5 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 5 | queue_snapshot | `{"busy": null, "pending": []}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a0j1", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 0, "cost_per_tick": 0, "deadline": 10, "job_id": "a0j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 4}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a1j1", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 1, "cost_per_tick": 0, "deadline": 8, "job_id": "a1j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}}` |
| 6 | proposal | `{"agreement": true, "evidence": "live_gpu", "job_id": "a2j1", "p_error": 0.14606741573033707, "primary": "replace_filter", "secondary": "replace_filter"}` |
| 6 | request_queued | `{"request": {"agent_id": 2, "cost_per_tick": 0, "deadline": 11, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 12}}` |
| 6 | dispatch_considered | `{"eligible": [{"agent_id": 0, "cost_per_tick": 0, "deadline": 10, "job_id": "a0j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 4}, {"agent_id": 1, "cost_per_tick": 0, "deadline": 8, "job_id": "a1j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 8}, {"agent_id": 2, "cost_per_tick": 0, "deadline": 11, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 12}], "selected": "a0j1"}` |
| 6 | review_started | `{"finish": 8, "job_id": "a0j1", "start": 6}` |
| 6 | queue_snapshot | `{"busy": {"finish": 8, "job_id": "a0j1", "start": 6}, "pending": ["a1j1", "a2j1"]}` |
| 6 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 6 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 7 | queue_snapshot | `{"busy": {"finish": 8, "job_id": "a0j1", "start": 6}, "pending": ["a1j1", "a2j1"]}` |
| 7 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a1j1", "loss": 0}` |
| 7 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 8 | review_completed | `{"applied": true, "changed": false, "instructed_action": "replace_filter", "job_id": "a0j1", "late": false}` |
| 8 | request_expired | `{"category": "opportunity_lost_while_waiting", "initial_proposal_wrong": false, "job_id": "a1j1"}` |
| 8 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a1j1", "job_loss": 0, "terminal_loss": 0}` |
| 8 | dispatch_considered | `{"eligible": [{"agent_id": 2, "cost_per_tick": 0, "deadline": 11, "job_id": "a2j1", "p_error": 0.14606741573033707, "proposal": "replace_filter", "requested_at": 6, "review_ticks": 2, "terminal_cost": 12}], "selected": "a2j1"}` |
| 8 | review_started | `{"finish": 10, "job_id": "a2j1", "start": 8}` |
| 8 | queue_snapshot | `{"busy": {"finish": 10, "job_id": "a2j1", "start": 8}, "pending": []}` |
| 8 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 8 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 9 | queue_snapshot | `{"busy": {"finish": 10, "job_id": "a2j1", "start": 8}, "pending": []}` |
| 9 | interval_scored | `{"job_id": "a0j1", "loss": 0}` |
| 9 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 10 | review_completed | `{"applied": true, "changed": true, "instructed_action": "reset_sensor", "job_id": "a2j1", "late": false}` |
| 10 | job_closed | `{"action": "replace_filter", "correct": true, "job_id": "a0j1", "job_loss": 0, "terminal_loss": 0}` |
| 10 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 10 | queue_snapshot | `{"busy": null, "pending": []}` |
| 10 | interval_scored | `{"job_id": "a2j1", "loss": 0}` |
| 11 | job_closed | `{"action": "reset_sensor", "correct": true, "job_id": "a2j1", "job_loss": 0, "terminal_loss": 0}` |
| 11 | dispatch_considered | `{"eligible": [], "selected": null}` |
| 11 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | queue_snapshot | `{"busy": null, "pending": []}` |
| 12 | episode_finished | `{"accrued_loss": 8, "attempts": 12, "completion_tokens": 84, "correct_jobs": 5, "corrections": 2, "episode_wall_seconds": 3.807796, "error": null, "evidence": "live_gpu", "expired_requests": 2, "incomplete_service": null, "jobs_closed": 6, "late_returns": 0, "loss_upper_bound": 48, "planned_calls": 12, "policy": "uncertainty", "prompt_tokens": 2570, "request_wall_seconds": 1.6772955507040024, "review_busy_ticks": 8, "reviews_completed": 4, "reviews_started": 4, "scenario_hash": "b83eacc3f07791bb2f4ea5979fb2b7423a3a62e6c3d6e1970f50f9d41459ecdf", "scheduled_calls": 12, "seed": 303, "simulated_ticks_completed": 12, "status": "completed", "total_loss": 8, "unknown_token_attempts": 0}` |
