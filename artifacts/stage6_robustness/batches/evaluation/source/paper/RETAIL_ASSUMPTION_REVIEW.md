# Retail assumption review

Source-based methodological review, 2026-09-10. This is not independent human
expert validation. No retailer, customer, or expert was contacted. Stage 5 is
preserved at commit `189cf517dc06f4bf3008281c0d2966dbceba928b`.

The review distinguishes three kinds of support. **Upstream** means the pinned
τ-bench implementation and policy. **Operational documentation** describes what
a named platform supports, not universal retailer practice. **Constructed** means
our simulation choice, which needs sensitivity analysis rather than a claim of
external validation.

## Assumption and interpretation table

| Assumption | Current implementation | Evidence or rationale | Limitation and implication |
|---|---|---|---|
| Stage before commitment | `RetailWorkflow.step` validates a mutation on a copy, stores a proposal, and leaves committed account state unchanged. `simulation.commit` invokes the mutation at completed review or cutoff. | Upstream tools mutate local state immediately. Our extra staging layer is a coherent service architecture if mutation dispatch can be gated. Platform return workflows distinguish a request from approval and later processing [S4,S5]. | Staging is our adapter, not native τ-bench or evidence that all operations can be delayed. The experiment ends at transaction posting, not physical shipment, receipt, refund settlement, or actual fulfillment. |
| Full corrective authority | Only a completed perfect review replaces a proposal with the annotated target. Automatic upstream guards run again. | Restoring recorded intent is a useful idealized upper authority condition. The source task provides the target only to offline scoring and completed review. | This includes choice of item, reason and payment destination. It assumes authority and customer compliance beyond approval. It can turn an unresolved task into a correct one without further agent work. Stage 6 separates this from approve-or-block authority. |
| Renewed confirmation | The agent must obtain exact-argument confirmation before staging. The reviewer replacement does not obtain a new confirmation. | The pinned policy requires explicit confirmation of consequential action details [S1]. Order edits can entail a changed invoice or refund [S2]. | Prior confirmation of a wrong transaction does not automatically establish consent to a different full transaction. The corrected target is within original intent, but this does not substitute for actual renewed consent. Stage 5 remains an idealized correction condition. Restricted review approves unchanged correct proposals or blocks wrong proposals without changing their arguments. |
| Cancellation cutoff | A proposal can be corrected through an abstract deadline, then cancellation posts. | τ-bench permits cancellation only while pending [S1]. Shopify cancellation depends on fulfillment and may require coordination with a fulfillment service [S3]. | Our cutoff is a deadline for dispatching the cancellation transaction, not a measured latest moment before a real shipment. Upstream status is not autonomously advanced by the clock. Missing the cutoff does not simulate a shipment, it commits the original proposal and incurs declared consequence points. |
| Modification cutoff | Same 2/4/5 relative windows as other families. | τ-bench item modification is one-shot and prevents subsequent modification or cancellation. Real platform editing has fulfillment/payment restrictions [S1,S2]. | The common deadline distribution does not estimate modification lead times. One-shot tool semantics give intervention timing a rationale, but not its numerical values. |
| Return/exchange cutoff | Same abstract posting deadline; wrong return/exchange request can incur loss. | Upstream sets `return requested` or `exchange requested`, not physical completion [S1]. Real return processing may follow receipt and inspection, with intermediate approval and processing states [S4,S5]. | Returns often have distinct stages and time scales. A wrong request is not necessarily irreversible physical harm. Here the incurred quantity is a posting/rework consequence that cannot be retroactively erased within the episode. No empirical return-window claim is made. |
| Review duration | Every request occupies one reviewer for 1 or 2 abstract ticks. | Fixed duration isolates capacity. Item selection and variant comparison can require more checks than a single cancellation; upstream requires collecting all items before modification/exchange [S1]. | No review times are measured. Stage 6 adds one tick when a public staged proposal lists at least two items. This is a simple complexity sensitivity, not an estimated labor model. Wrong omission can reduce observed complexity and review time, a limitation we retain. |
| Consequence weights | Four points per unresolved request plus 4/8/12 if a wrong proposal posts, independently permuted over slots. | Separates failure to provide service from extra processing consequences. The weights define an explicit scheduling objective. | Points are neither dollars nor measured severity. A wrong cancellation reason and an incorrect product variant may have different real consequences. Review labor is a capacity constraint rather than an added monetary loss. Lower weighted loss need not imply more completed tasks. |
| Exact state equality | Hash final account database using the upstream recursive list-order-sensitive equality rule. | Matches the retained benchmark validator. Source audits check target execution, unique item mappings and named return multiplicities. | Exact annotation agreement can be stricter than operational equivalence. Different reason fields, payment destinations or item ordering can matter to the hash. Stage 6 retains this measure to isolate authority/time, reports error classes, and makes no claim that all unequal states are equally harmful. |
| Preparation failure scope | No staged proposal means no reviewer request. The service remains unresolved with loss four. | The modeled reviewer gates an executable transaction; authentication loops, exhausted context/output budget, unfinished confirmation, or no valid mutation occur earlier. | Perfect transaction review cannot rescue these failures. Model/task completion and reviewer allocation must be reported separately. An upstream transfer-to-human workflow would require a different intervention boundary and is outside this follow-up. |
| Reviewer diagnosis | A completed review recognizes whether the staged state differs from target with accuracy one. | Controlled oracle assumption separates timing/authority from diagnostic noise. | Detection is still idealized under approve-or-block. No diagnosis is revealed before completion; no hidden state enters scheduler requests. No measured human-performance claim follows. |

## Consequence for Stage 6

Use the Stage 5 correction condition as a reference at both capacities. Change
one factor at a time. In the **restricted-authority** condition a completed
review commits the original proposal if correct, and blocks it if wrong. A block
leaves the account unchanged and the service unresolved. It removes the proposal
from the queue and prevents later automatic posting; it does not count as task
completion or correction. Detection remains perfect. If the wrong transaction
would incur service cost S and processing cost W, correction prevents S+W while
blocking prevents only W. Thus the respective expected timely benefits are
`p * (S + W)` and `p * W`. This is not a common rescaling because W varies and S
is fixed. Even when orders coincide, task completion can differ mechanically.

The second one-factor condition retains correction authority and changes review
time to `base duration + 1` for a proposal whose public `item_ids` list contains
at least two entries. Cancellation and single-item proposals retain base time.
The underlying arrivals, cutoffs, costs, risk estimator, prompts and preparations
stay fixed. No authority-by-complexity interaction is evaluated.

No-review outcomes are mathematically invariant across these conditions. Under
perfect blocking, total correct tasks equal the initially correct staged tasks
for every policy: blocking does not complete an initially wrong or unstaged
request. These are implementation consequences, not empirical discoveries.

## Primary sources checked

- **S1:** [Pinned τ-bench retail policy](https://github.com/sierra-research/tau-bench/blob/59a200c6d575d595120f1cb70fea53cef0632f6b/tau_bench/envs/retail/wiki.md), [tools](https://github.com/sierra-research/tau-bench/tree/59a200c6d575d595120f1cb70fea53cef0632f6b/tau_bench/envs/retail/tools), and [validator](https://github.com/sierra-research/tau-bench/blob/59a200c6d575d595120f1cb70fea53cef0632f6b/tau_bench/envs/base.py). Unmodified local copies and hashes are under `third_party/tau_bench/`.
- **S2:** Shopify, [Editing orders](https://help.shopify.com/en/manual/fulfillment/managing-orders/editing-orders) and [Considerations](https://help.shopify.com/en/manual/fulfillment/managing-orders/editing-orders/considerations). Checked 2026-09-10.
- **S3:** Shopify, [Canceling orders](https://help.shopify.com/en/manual/fulfillment/managing-orders/canceling-orders). Checked 2026-09-10.
- **S4:** Shopify, [Understanding order statuses](https://help.shopify.com/en/manual/fulfillment/managing-orders/order-status). Checked 2026-09-10.
- **S5:** Shopify, [Processing and managing returns](https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/processing-returns) and [Return-management APIs](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-return-management). Checked 2026-09-10.

These sources support distinctions between requests, approval, processing and
fulfillment. They do not validate our numerical cutoffs, loss weights, diagnostic
accuracy, reviewer times or full corrective authority. Legal consumer-rights
claims are outside this review. Independent domain assessment remains absent.
