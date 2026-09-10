# Review-queue timeline

Evidence: **stipulated competition mechanics; zero model calls**.

Snapshots are after completion, closure, arrivals and dispatch; before interval loss.

| Run | Tick | In service (completion tick) | Pending |
| --- | --- | --- | --- |
| fcfs | 0 | A (2) | B |
| fcfs | 1 | A (2) | B |
| fcfs | 2 | B (4) | — |
| fcfs | 3 | B (4) | — |
| fcfs | 4 | — | — |
| fcfs | 5 | — | — |
| fcfs | 6 | — | — |
| fcfs | 7 | — | — |
| fcfs | 8 | — | — |
| fcfs | 9 | — | — |
| fcfs | 10 | — | — |
| fcfs | 11 | — | — |
| fcfs | 12 | — | — |
| uncertainty | 0 | A (2) | B |
| uncertainty | 1 | A (2) | B |
| uncertainty | 2 | B (4) | — |
| uncertainty | 3 | B (4) | — |
| uncertainty | 4 | — | — |
| uncertainty | 5 | — | — |
| uncertainty | 6 | — | — |
| uncertainty | 7 | — | — |
| uncertainty | 8 | — | — |
| uncertainty | 9 | — | — |
| uncertainty | 10 | — | — |
| uncertainty | 11 | — | — |
| uncertainty | 12 | — | — |
| myopic | 0 | B (2) | A |
| myopic | 1 | B (2) | A |
| myopic | 2 | — | — |
| myopic | 3 | — | — |
| myopic | 4 | — | — |
| myopic | 5 | — | — |
| myopic | 6 | — | — |
| myopic | 7 | — | — |
| myopic | 8 | — | — |
| myopic | 9 | — | — |
| myopic | 10 | — | — |
| myopic | 11 | — | — |
| myopic | 12 | — | — |
| greedy | 0 | B (2) | A |
| greedy | 1 | B (2) | A |
| greedy | 2 | — | — |
| greedy | 3 | — | — |
| greedy | 4 | — | — |
| greedy | 5 | — | — |
| greedy | 6 | — | — |
| greedy | 7 | — | — |
| greedy | 8 | — | — |
| greedy | 9 | — | — |
| greedy | 10 | — | — |
| greedy | 11 | — | — |
| greedy | 12 | — | — |
| delay | 0 | A (2) | B |
| delay | 1 | A (2) | B |
| delay | 2 | B (4) | — |
| delay | 3 | B (4) | — |
| delay | 4 | — | — |
| delay | 5 | — | — |
| delay | 6 | — | — |
| delay | 7 | — | — |
| delay | 8 | — | — |
| delay | 9 | — | — |
| delay | 10 | — | — |
| delay | 11 | — | — |
| delay | 12 | — | — |
