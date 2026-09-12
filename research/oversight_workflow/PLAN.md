# Oversight workflow: stage authorization and development plan

Started 2026-09-12 10:57:11 UTC on main at 8ee8f5a2. This is a separately
authorized three-hour stage. Deadline 13:57:11 UTC; new inference stops by
13:12:11 UTC. Historical clocks and the original 36-hour overrun remain intact.
No new paid resources, server replacement, participant recruitment or push.

Question: how can one person inspect competing actionable requests while
retaining unfinished work and controlling exact output versions released?

1. Reuse source cards, bounded GPU transport and official scoring. Review the
   closest interface systems and current ICAART requirements, bounded to 20 minutes.
2. Implement one event protocol with stable active review, explicit per-output
   decisions, deferral, versions, admission control and replay. Configure separate
   conversations, a central conventional queue and optional source sessions.
3. Use old TAT-QA development material for interface and throughput checks.
   Freeze 24 fresh source-order contexts and two answer replicas if forecast fits.
   No selection by answers or model errors. Preserve every original question.
4. Collect real GPU answers through asynchronous workers. Record one live
   integration with arrivals during an active review and actual model revisions.
   Compare interface configurations with identical saved outputs and schedules.
5. Measure software reliability, accounting, response latency and useful releases
   under explicitly scripted actions. Prepare a prospective human study. Render
   figures, screenshots and a separate conference-format draft, then verify and commit.

The primary comparison is central queue versus optional user-controlled sessions.
All configurations share approval/version/source semantics. No optimizer is added.
Scripted review does not estimate human speed, cognitive load or efficacy. A
mechanical tie is acceptable. A software-complete study without participants is
likely best framed as a position paper with a prospective effectiveness study.

Resource ceiling: 400 scheduled calls, 450 attempts, at most one retry per call,
60-second attempt timeout. One GPU uses existing BF16 Qwen2.5-7B weights without
CPU offload. Task workers are independently prompted jobs using the same model.
The transport serializes GPU requests; the queue and UI remain asynchronous.
