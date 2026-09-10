# Review-queue timeline

Evidence: **live GPU only if verified in manifest**.

Snapshots are after completion, closure, arrivals and dispatch; before interval loss.

| Run | Tick | In service (completion tick) | Pending |
| --- | --- | --- | --- |
| fcfs | 0 | a0j0 (2) | a1j0 |
| fcfs | 1 | a0j0 (2) | a2j0 |
| fcfs | 2 | — | — |
| fcfs | 3 | — | — |
| fcfs | 4 | — | — |
| fcfs | 5 | — | — |
| fcfs | 6 | — | a1j1 |
| fcfs | 7 | — | a0j1, a2j1 |
| fcfs | 8 | — | a0j1 |
| fcfs | 9 | — | — |
| fcfs | 10 | — | — |
| fcfs | 11 | — | — |
| fcfs | 12 | — | — |
| uncertainty | 0 | a0j0 (2) | a1j0 |
| uncertainty | 1 | a0j0 (2) | a2j0 |
| uncertainty | 2 | — | — |
| uncertainty | 3 | — | — |
| uncertainty | 4 | — | — |
| uncertainty | 5 | — | — |
| uncertainty | 6 | — | a1j1 |
| uncertainty | 7 | — | a0j1, a2j1 |
| uncertainty | 8 | — | a0j1 |
| uncertainty | 9 | — | — |
| uncertainty | 10 | — | — |
| uncertainty | 11 | — | — |
| uncertainty | 12 | — | — |
| myopic | 0 | a0j0 (2) | a1j0 |
| myopic | 1 | a0j0 (2) | a2j0 |
| myopic | 2 | — | — |
| myopic | 3 | — | — |
| myopic | 4 | — | — |
| myopic | 5 | — | — |
| myopic | 6 | — | a1j1 |
| myopic | 7 | — | a0j1, a2j1 |
| myopic | 8 | — | a0j1 |
| myopic | 9 | — | — |
| myopic | 10 | — | — |
| myopic | 11 | — | — |
| myopic | 12 | — | — |
| delay | 0 | a0j0 (2) | a1j0 |
| delay | 1 | a0j0 (2) | a2j0 |
| delay | 2 | — | — |
| delay | 3 | — | — |
| delay | 4 | — | — |
| delay | 5 | — | — |
| delay | 6 | — | a1j1 |
| delay | 7 | — | a0j1, a2j1 |
| delay | 8 | — | a0j1 |
| delay | 9 | — | — |
| delay | 10 | — | — |
| delay | 11 | — | — |
| delay | 12 | — | — |
