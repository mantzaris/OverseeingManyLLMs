# Review-queue timeline

Evidence: **stipulated mechanics; NOT GPU inference**.

Snapshots are after completion, closure, arrivals and dispatch; before interval loss.

| Run | Tick | In service (completion tick) | Pending |
| --- | --- | --- | --- |
| competition/myopic | 0 | B (2) | A |
| competition/myopic | 1 | B (2) | A |
| competition/myopic | 2 | — | — |
| competition/myopic | 3 | — | — |
| competition/myopic | 4 | — | — |
| competition/myopic | 5 | — | — |
| competition/myopic | 6 | — | — |
| competition/myopic | 7 | — | — |
| competition/myopic | 8 | — | — |
| competition/myopic | 9 | — | — |
| competition/myopic | 10 | — | — |
| competition/myopic | 11 | — | — |
| competition/myopic | 12 | — | — |
| competition/delay | 0 | A (2) | B |
| competition/delay | 1 | A (2) | B |
| competition/delay | 2 | B (4) | — |
| competition/delay | 3 | B (4) | — |
| competition/delay | 4 | — | — |
| competition/delay | 5 | — | — |
| competition/delay | 6 | — | — |
| competition/delay | 7 | — | — |
| competition/delay | 8 | — | — |
| competition/delay | 9 | — | — |
| competition/delay | 10 | — | — |
| competition/delay | 11 | — | — |
| competition/delay | 12 | — | — |
