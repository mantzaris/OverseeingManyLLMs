# Focused literature and novelty assessment

Verified 12 September 2026. This update was bounded to approximately 20 minutes;
prior detailed reading remains in `research/attention_sessions/LITERATURE.md` and
its human-study protocol. No system below is claimed as a reproduced baseline.
A/B/C are controlled configurations of our own application.

| Closest system | Established mechanism and evidence | Difference tested here |
|---|---|---|
| [AgentGUI](https://arxiv.org/html/2607.26300v1), Zhao, Sohn, Zheng and Moor, 2026 preprint | Sections 3.1-3.4 describe concurrent desks, activity/source previews, saved sessions, intervention and manager audits. Section 4.1 compares trace comprehension with Hermes Dashboard using eight participants and counterbalanced traces. Section 4.2 separately tests automated steering. | Our endpoint is accounting and version-specific release under asynchronous actionable requests. We do not reproduce its human comprehension result or establish superiority to its interface. |
| [AGDebugger](https://arxiv.org/html/2503.02068v1), Epperson et al., CHI 2025, DOI 10.1145/3706598.3713581 | Sections 5.1-5.3 provide message queues, pause/step controls, history, edits and checkpoint forks. Section 6 uses six participants for error identification and eight others for steering. Only two of the latter eight reach exact correct answers. | Our task is deciding which independent output/version may be released, with unfinished-work accounting. Editing history, dashboards and queues are already established. |
| [Chien et al., 2018](https://doi.org/10.1016/j.ijhcs.2018.03.005), IJHCS 117:30-44 | Compares an open queue of robot conditions with a single-request shortest-job-first display in human multi-robot supervision. | Directly precedes queue-versus-open-work presentation. We use financial QA task workers, not robots, and make no claim to new attention scheduling. Publisher abstract/metadata verified; author PDF and CORE mirror returned HTTP 403 in this bounded update, so detailed findings are not inferred here. |
| [Horvitz, Apacible and Subramani, notification deferral](https://www.microsoft.com/en-us/research/publication/balancing-awareness-interruption-investigation-notification-deferral-policies/) and [Iqbal and Horvitz, 2007](https://www.erichorvitz.com/CHI_2007_Iqbal_Horvitz.pdf) | Prior repository review covers bounded interruption deferral and recovery from disruption. | Stable focus and saved resumption context instantiate established principles. Queue length and events are not cognitive-load measures. |
| Prior repository studies and verified HiLSVA/AgentLens/One Human, N Agents comparisons | Auditing budgets, agent observability, explicit handoffs and review sessions already have close precedents. Our sessions did not beat sticky EDF; uncertain correction reuse did not beat simpler correction consistently. | We retain simple ordering, directly display source evidence and require separate output decisions. Prior null results motivate design choices but do not validate this interface. |

The author repositories [AgentGUI](https://github.com/eth-medical-ai-lab/agent-gui)
and [AGDebugger](https://github.com/microsoft/AGDebugger) are public MIT releases.
Their verified current commits are recorded under `artifacts/oversight_workflow/sources/`.
The exact AgentGUI here is *An Interface for Observing and Steering Long-Running
AI Agents*, arXiv 2607.26300, not unrelated packages with similar names.

**Candidate contribution.** A specified output-review lifecycle connecting live
workers, a stable active evidence view, individually scoped release decisions,
visible outstanding work and deterministic interaction replay, plus a real-data
software evaluation and a prospective human comparison. This is a systems and
protocol contribution, not a novel queueing algorithm or the first oversight UI.
The strongest competing explanation is that ordinary well-engineered queue and
version controls already suffice. B versus C keeps those controls common; an
identical scripted outcome does not support a session advantage. Human evidence
is necessary before claiming better review quality or effort.

**Venue.** Official [ICAART 2027 guidelines](https://icaart.scitevents.org/Guidelines.aspx?y=2027)
and [template page](https://icaart.scitevents.org/Templates.aspx?y=2027) were checked.
Position submissions allow 8,000-40,000 non-whitespace characters and an eight-page
ordinary proceedings limit. Regular review submissions allow 10,000-50,000
characters. Double-blind review and AI-assistance disclosure apply. We use the
unchanged official SCITEPRESS files already preserved in `paper/template/`.
No regular-paper supplementary-upload entitlement was found. This stage does not
submit, push or publicly post a manuscript. The pending human study makes a
position-paper framing the conservative recommendation.
