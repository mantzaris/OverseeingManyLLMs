# Review-queue timeline

Evidence: **live GPU constructed competition; see per-episode completion status**.

Snapshots are after completion, closure, arrivals and dispatch; before interval loss.

| Run | Tick | In service (completion tick) | Pending |
| --- | --- | --- | --- |
| 300/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 300/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 300/s1/fcfs | 2 | a2j0 (3) | — |
| 300/s1/fcfs | 3 | — | — |
| 300/s1/fcfs | 4 | — | — |
| 300/s1/fcfs | 5 | — | — |
| 300/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 300/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 300/s1/fcfs | 8 | a2j1 (9) | — |
| 300/s1/fcfs | 9 | — | — |
| 300/s1/fcfs | 10 | — | — |
| 300/s1/fcfs | 11 | — | — |
| 300/s1/fcfs | 12 | — | — |
| 300/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 300/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 300/s1/uncertainty | 2 | a2j0 (3) | — |
| 300/s1/uncertainty | 3 | — | — |
| 300/s1/uncertainty | 4 | — | — |
| 300/s1/uncertainty | 5 | — | — |
| 300/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 300/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 300/s1/uncertainty | 8 | a2j1 (9) | — |
| 300/s1/uncertainty | 9 | — | — |
| 300/s1/uncertainty | 10 | — | — |
| 300/s1/uncertainty | 11 | — | — |
| 300/s1/uncertainty | 12 | — | — |
| 300/s1/myopic | 0 | a1j0 (1) | a0j0, a2j0 |
| 300/s1/myopic | 1 | a0j0 (2) | a2j0 |
| 300/s1/myopic | 2 | a2j0 (3) | — |
| 300/s1/myopic | 3 | — | — |
| 300/s1/myopic | 4 | — | — |
| 300/s1/myopic | 5 | — | — |
| 300/s1/myopic | 6 | a0j1 (7) | a1j1, a2j1 |
| 300/s1/myopic | 7 | a1j1 (8) | a2j1 |
| 300/s1/myopic | 8 | a2j1 (9) | — |
| 300/s1/myopic | 9 | — | — |
| 300/s1/myopic | 10 | — | — |
| 300/s1/myopic | 11 | — | — |
| 300/s1/myopic | 12 | — | — |
| 300/s1/greedy | 0 | a1j0 (1) | a0j0, a2j0 |
| 300/s1/greedy | 1 | a0j0 (2) | a2j0 |
| 300/s1/greedy | 2 | a2j0 (3) | — |
| 300/s1/greedy | 3 | — | — |
| 300/s1/greedy | 4 | — | — |
| 300/s1/greedy | 5 | — | — |
| 300/s1/greedy | 6 | a0j1 (7) | a1j1, a2j1 |
| 300/s1/greedy | 7 | a1j1 (8) | a2j1 |
| 300/s1/greedy | 8 | a2j1 (9) | — |
| 300/s1/greedy | 9 | — | — |
| 300/s1/greedy | 10 | — | — |
| 300/s1/greedy | 11 | — | — |
| 300/s1/greedy | 12 | — | — |
| 300/s1/edf | 0 | a1j0 (1) | a0j0, a2j0 |
| 300/s1/edf | 1 | a0j0 (2) | a2j0 |
| 300/s1/edf | 2 | a2j0 (3) | — |
| 300/s1/edf | 3 | — | — |
| 300/s1/edf | 4 | — | — |
| 300/s1/edf | 5 | — | — |
| 300/s1/edf | 6 | a0j1 (7) | a1j1, a2j1 |
| 300/s1/edf | 7 | a1j1 (8) | a2j1 |
| 300/s1/edf | 8 | a2j1 (9) | — |
| 300/s1/edf | 9 | — | — |
| 300/s1/edf | 10 | — | — |
| 300/s1/edf | 11 | — | — |
| 300/s1/edf | 12 | — | — |
| 300/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 300/s1/delay | 1 | a1j0 (2) | a2j0 |
| 300/s1/delay | 2 | a2j0 (3) | — |
| 300/s1/delay | 3 | — | — |
| 300/s1/delay | 4 | — | — |
| 300/s1/delay | 5 | — | — |
| 300/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 300/s1/delay | 7 | a1j1 (8) | a2j1 |
| 300/s1/delay | 8 | a2j1 (9) | — |
| 300/s1/delay | 9 | — | — |
| 300/s1/delay | 10 | — | — |
| 300/s1/delay | 11 | — | — |
| 300/s1/delay | 12 | — | — |
| 300/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 300/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 300/s2/uncertainty | 2 | a2j0 (4) | — |
| 300/s2/uncertainty | 3 | a2j0 (4) | — |
| 300/s2/uncertainty | 4 | — | — |
| 300/s2/uncertainty | 5 | — | — |
| 300/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/uncertainty | 8 | a1j1 (10) | a2j1 |
| 300/s2/uncertainty | 9 | a1j1 (10) | a2j1 |
| 300/s2/uncertainty | 10 | — | a2j1 |
| 300/s2/uncertainty | 11 | — | — |
| 300/s2/uncertainty | 12 | — | — |
| 300/s2/myopic | 0 | a1j0 (2) | a0j0, a2j0 |
| 300/s2/myopic | 1 | a1j0 (2) | a0j0, a2j0 |
| 300/s2/myopic | 2 | a0j0 (4) | a2j0 |
| 300/s2/myopic | 3 | a0j0 (4) | a2j0 |
| 300/s2/myopic | 4 | — | a2j0 |
| 300/s2/myopic | 5 | — | — |
| 300/s2/myopic | 6 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/myopic | 7 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/myopic | 8 | a1j1 (10) | a2j1 |
| 300/s2/myopic | 9 | a1j1 (10) | a2j1 |
| 300/s2/myopic | 10 | — | a2j1 |
| 300/s2/myopic | 11 | — | — |
| 300/s2/myopic | 12 | — | — |
| 300/s2/greedy | 0 | a1j0 (2) | a0j0, a2j0 |
| 300/s2/greedy | 1 | a1j0 (2) | a0j0, a2j0 |
| 300/s2/greedy | 2 | a0j0 (4) | a2j0 |
| 300/s2/greedy | 3 | a0j0 (4) | a2j0 |
| 300/s2/greedy | 4 | — | a2j0 |
| 300/s2/greedy | 5 | — | — |
| 300/s2/greedy | 6 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/greedy | 7 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/greedy | 8 | a1j1 (10) | a2j1 |
| 300/s2/greedy | 9 | a1j1 (10) | a2j1 |
| 300/s2/greedy | 10 | — | a2j1 |
| 300/s2/greedy | 11 | — | — |
| 300/s2/greedy | 12 | — | — |
| 300/s2/edf | 0 | a1j0 (2) | a0j0, a2j0 |
| 300/s2/edf | 1 | a1j0 (2) | a0j0, a2j0 |
| 300/s2/edf | 2 | a0j0 (4) | a2j0 |
| 300/s2/edf | 3 | a0j0 (4) | a2j0 |
| 300/s2/edf | 4 | — | a2j0 |
| 300/s2/edf | 5 | — | — |
| 300/s2/edf | 6 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/edf | 7 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/edf | 8 | a1j1 (10) | a2j1 |
| 300/s2/edf | 9 | a1j1 (10) | a2j1 |
| 300/s2/edf | 10 | — | a2j1 |
| 300/s2/edf | 11 | — | — |
| 300/s2/edf | 12 | — | — |
| 300/s2/delay | 0 | a1j0 (2) | a0j0, a2j0 |
| 300/s2/delay | 1 | a1j0 (2) | a0j0, a2j0 |
| 300/s2/delay | 2 | a0j0 (4) | a2j0 |
| 300/s2/delay | 3 | a0j0 (4) | a2j0 |
| 300/s2/delay | 4 | — | a2j0 |
| 300/s2/delay | 5 | — | — |
| 300/s2/delay | 6 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/delay | 7 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/delay | 8 | a1j1 (10) | a2j1 |
| 300/s2/delay | 9 | a1j1 (10) | a2j1 |
| 300/s2/delay | 10 | — | a2j1 |
| 300/s2/delay | 11 | — | — |
| 300/s2/delay | 12 | — | — |
| 300/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 300/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 300/s2/fcfs | 2 | a2j0 (4) | — |
| 300/s2/fcfs | 3 | a2j0 (4) | — |
| 300/s2/fcfs | 4 | — | — |
| 300/s2/fcfs | 5 | — | — |
| 300/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 300/s2/fcfs | 8 | a1j1 (10) | a2j1 |
| 300/s2/fcfs | 9 | a1j1 (10) | a2j1 |
| 300/s2/fcfs | 10 | — | a2j1 |
| 300/s2/fcfs | 11 | — | — |
| 300/s2/fcfs | 12 | — | — |
| 301/s2/myopic | 0 | a0j0 (2) | a1j0, a2j0 |
| 301/s2/myopic | 1 | a0j0 (2) | a1j0, a2j0 |
| 301/s2/myopic | 2 | a1j0 (4) | — |
| 301/s2/myopic | 3 | a1j0 (4) | — |
| 301/s2/myopic | 4 | — | — |
| 301/s2/myopic | 5 | — | — |
| 301/s2/myopic | 6 | a2j1 (8) | a0j1, a1j1 |
| 301/s2/myopic | 7 | a2j1 (8) | a0j1, a1j1 |
| 301/s2/myopic | 8 | a0j1 (10) | — |
| 301/s2/myopic | 9 | a0j1 (10) | — |
| 301/s2/myopic | 10 | — | — |
| 301/s2/myopic | 11 | — | — |
| 301/s2/myopic | 12 | — | — |
| 301/s2/greedy | 0 | a0j0 (2) | a1j0, a2j0 |
| 301/s2/greedy | 1 | a0j0 (2) | a1j0, a2j0 |
| 301/s2/greedy | 2 | a1j0 (4) | — |
| 301/s2/greedy | 3 | a1j0 (4) | — |
| 301/s2/greedy | 4 | — | — |
| 301/s2/greedy | 5 | — | — |
| 301/s2/greedy | 6 | a2j1 (8) | a0j1, a1j1 |
| 301/s2/greedy | 7 | a2j1 (8) | a0j1, a1j1 |
| 301/s2/greedy | 8 | a0j1 (10) | — |
| 301/s2/greedy | 9 | a0j1 (10) | — |
| 301/s2/greedy | 10 | — | — |
| 301/s2/greedy | 11 | — | — |
| 301/s2/greedy | 12 | — | — |
| 301/s2/edf | 0 | a2j0 (2) | a0j0, a1j0 |
| 301/s2/edf | 1 | a2j0 (2) | a0j0, a1j0 |
| 301/s2/edf | 2 | a1j0 (4) | a0j0 |
| 301/s2/edf | 3 | a1j0 (4) | a0j0 |
| 301/s2/edf | 4 | — | a0j0 |
| 301/s2/edf | 5 | — | — |
| 301/s2/edf | 6 | a1j1 (8) | a0j1, a2j1 |
| 301/s2/edf | 7 | a1j1 (8) | a0j1, a2j1 |
| 301/s2/edf | 8 | a2j1 (10) | a0j1 |
| 301/s2/edf | 9 | a2j1 (10) | a0j1 |
| 301/s2/edf | 10 | — | a0j1 |
| 301/s2/edf | 11 | — | — |
| 301/s2/edf | 12 | — | — |
| 301/s2/delay | 0 | a2j0 (2) | a0j0, a1j0 |
| 301/s2/delay | 1 | a2j0 (2) | a0j0, a1j0 |
| 301/s2/delay | 2 | a0j0 (4) | a1j0 |
| 301/s2/delay | 3 | a0j0 (4) | a1j0 |
| 301/s2/delay | 4 | — | — |
| 301/s2/delay | 5 | — | — |
| 301/s2/delay | 6 | a1j1 (8) | a0j1, a2j1 |
| 301/s2/delay | 7 | a1j1 (8) | a0j1, a2j1 |
| 301/s2/delay | 8 | a2j1 (10) | a0j1 |
| 301/s2/delay | 9 | a2j1 (10) | a0j1 |
| 301/s2/delay | 10 | — | a0j1 |
| 301/s2/delay | 11 | — | — |
| 301/s2/delay | 12 | — | — |
| 301/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 301/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 301/s2/fcfs | 2 | a1j0 (4) | — |
| 301/s2/fcfs | 3 | a1j0 (4) | — |
| 301/s2/fcfs | 4 | — | — |
| 301/s2/fcfs | 5 | — | — |
| 301/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 301/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 301/s2/fcfs | 8 | a2j1 (10) | — |
| 301/s2/fcfs | 9 | a2j1 (10) | — |
| 301/s2/fcfs | 10 | — | — |
| 301/s2/fcfs | 11 | — | — |
| 301/s2/fcfs | 12 | — | — |
| 301/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 301/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 301/s2/uncertainty | 2 | a1j0 (4) | — |
| 301/s2/uncertainty | 3 | a1j0 (4) | — |
| 301/s2/uncertainty | 4 | — | — |
| 301/s2/uncertainty | 5 | — | — |
| 301/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 301/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 301/s2/uncertainty | 8 | a2j1 (10) | — |
| 301/s2/uncertainty | 9 | a2j1 (10) | — |
| 301/s2/uncertainty | 10 | — | — |
| 301/s2/uncertainty | 11 | — | — |
| 301/s2/uncertainty | 12 | — | — |
| 301/s1/greedy | 0 | a0j0 (1) | a1j0, a2j0 |
| 301/s1/greedy | 1 | a2j0 (2) | a1j0 |
| 301/s1/greedy | 2 | a1j0 (3) | — |
| 301/s1/greedy | 3 | — | — |
| 301/s1/greedy | 4 | — | — |
| 301/s1/greedy | 5 | — | — |
| 301/s1/greedy | 6 | a2j1 (7) | a0j1, a1j1 |
| 301/s1/greedy | 7 | a1j1 (8) | a0j1 |
| 301/s1/greedy | 8 | a0j1 (9) | — |
| 301/s1/greedy | 9 | — | — |
| 301/s1/greedy | 10 | — | — |
| 301/s1/greedy | 11 | — | — |
| 301/s1/greedy | 12 | — | — |
| 301/s1/edf | 0 | a2j0 (1) | a0j0, a1j0 |
| 301/s1/edf | 1 | a1j0 (2) | a0j0 |
| 301/s1/edf | 2 | a0j0 (3) | — |
| 301/s1/edf | 3 | — | — |
| 301/s1/edf | 4 | — | — |
| 301/s1/edf | 5 | — | — |
| 301/s1/edf | 6 | a1j1 (7) | a0j1, a2j1 |
| 301/s1/edf | 7 | a2j1 (8) | a0j1 |
| 301/s1/edf | 8 | a0j1 (9) | — |
| 301/s1/edf | 9 | — | — |
| 301/s1/edf | 10 | — | — |
| 301/s1/edf | 11 | — | — |
| 301/s1/edf | 12 | — | — |
| 301/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 301/s1/delay | 1 | a2j0 (2) | a1j0 |
| 301/s1/delay | 2 | a1j0 (3) | — |
| 301/s1/delay | 3 | — | — |
| 301/s1/delay | 4 | — | — |
| 301/s1/delay | 5 | — | — |
| 301/s1/delay | 6 | a1j1 (7) | a0j1, a2j1 |
| 301/s1/delay | 7 | a0j1 (8) | a2j1 |
| 301/s1/delay | 8 | a2j1 (9) | — |
| 301/s1/delay | 9 | — | — |
| 301/s1/delay | 10 | — | — |
| 301/s1/delay | 11 | — | — |
| 301/s1/delay | 12 | — | — |
| 301/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 301/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 301/s1/fcfs | 2 | — | — |
| 301/s1/fcfs | 3 | — | — |
| 301/s1/fcfs | 4 | — | — |
| 301/s1/fcfs | 5 | — | — |
| 301/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 301/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 301/s1/fcfs | 8 | a2j1 (9) | — |
| 301/s1/fcfs | 9 | — | — |
| 301/s1/fcfs | 10 | — | — |
| 301/s1/fcfs | 11 | — | — |
| 301/s1/fcfs | 12 | — | — |
| 301/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 301/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 301/s1/uncertainty | 2 | — | — |
| 301/s1/uncertainty | 3 | — | — |
| 301/s1/uncertainty | 4 | — | — |
| 301/s1/uncertainty | 5 | — | — |
| 301/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 301/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 301/s1/uncertainty | 8 | a2j1 (9) | — |
| 301/s1/uncertainty | 9 | — | — |
| 301/s1/uncertainty | 10 | — | — |
| 301/s1/uncertainty | 11 | — | — |
| 301/s1/uncertainty | 12 | — | — |
| 301/s1/myopic | 0 | a0j0 (1) | a1j0, a2j0 |
| 301/s1/myopic | 1 | a2j0 (2) | a1j0 |
| 301/s1/myopic | 2 | a1j0 (3) | — |
| 301/s1/myopic | 3 | — | — |
| 301/s1/myopic | 4 | — | — |
| 301/s1/myopic | 5 | — | — |
| 301/s1/myopic | 6 | a2j1 (7) | a0j1, a1j1 |
| 301/s1/myopic | 7 | a1j1 (8) | a0j1 |
| 301/s1/myopic | 8 | a0j1 (9) | — |
| 301/s1/myopic | 9 | — | — |
| 301/s1/myopic | 10 | — | — |
| 301/s1/myopic | 11 | — | — |
| 301/s1/myopic | 12 | — | — |
| 302/s1/edf | 0 | a1j0 (1) | a0j0, a2j0 |
| 302/s1/edf | 1 | a2j0 (2) | a0j0 |
| 302/s1/edf | 2 | a0j0 (3) | — |
| 302/s1/edf | 3 | — | — |
| 302/s1/edf | 4 | — | — |
| 302/s1/edf | 5 | — | — |
| 302/s1/edf | 6 | a2j1 (7) | a0j1, a1j1 |
| 302/s1/edf | 7 | a1j1 (8) | a0j1 |
| 302/s1/edf | 8 | a0j1 (9) | — |
| 302/s1/edf | 9 | — | — |
| 302/s1/edf | 10 | — | — |
| 302/s1/edf | 11 | — | — |
| 302/s1/edf | 12 | — | — |
| 302/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 302/s1/delay | 1 | a1j0 (2) | a2j0 |
| 302/s1/delay | 2 | a2j0 (3) | — |
| 302/s1/delay | 3 | — | — |
| 302/s1/delay | 4 | — | — |
| 302/s1/delay | 5 | — | — |
| 302/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 302/s1/delay | 7 | a2j1 (8) | a1j1 |
| 302/s1/delay | 8 | a1j1 (9) | — |
| 302/s1/delay | 9 | — | — |
| 302/s1/delay | 10 | — | — |
| 302/s1/delay | 11 | — | — |
| 302/s1/delay | 12 | — | — |
| 302/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 302/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 302/s1/fcfs | 2 | a2j0 (3) | — |
| 302/s1/fcfs | 3 | — | — |
| 302/s1/fcfs | 4 | — | — |
| 302/s1/fcfs | 5 | — | — |
| 302/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 302/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 302/s1/fcfs | 8 | — | — |
| 302/s1/fcfs | 9 | — | — |
| 302/s1/fcfs | 10 | — | — |
| 302/s1/fcfs | 11 | — | — |
| 302/s1/fcfs | 12 | — | — |
| 302/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 302/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 302/s1/uncertainty | 2 | a2j0 (3) | — |
| 302/s1/uncertainty | 3 | — | — |
| 302/s1/uncertainty | 4 | — | — |
| 302/s1/uncertainty | 5 | — | — |
| 302/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 302/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 302/s1/uncertainty | 8 | — | — |
| 302/s1/uncertainty | 9 | — | — |
| 302/s1/uncertainty | 10 | — | — |
| 302/s1/uncertainty | 11 | — | — |
| 302/s1/uncertainty | 12 | — | — |
| 302/s1/myopic | 0 | a1j0 (1) | a0j0, a2j0 |
| 302/s1/myopic | 1 | a0j0 (2) | a2j0 |
| 302/s1/myopic | 2 | a2j0 (3) | — |
| 302/s1/myopic | 3 | — | — |
| 302/s1/myopic | 4 | — | — |
| 302/s1/myopic | 5 | — | — |
| 302/s1/myopic | 6 | a1j1 (7) | a0j1, a2j1 |
| 302/s1/myopic | 7 | a0j1 (8) | a2j1 |
| 302/s1/myopic | 8 | — | — |
| 302/s1/myopic | 9 | — | — |
| 302/s1/myopic | 10 | — | — |
| 302/s1/myopic | 11 | — | — |
| 302/s1/myopic | 12 | — | — |
| 302/s1/greedy | 0 | a1j0 (1) | a0j0, a2j0 |
| 302/s1/greedy | 1 | a0j0 (2) | a2j0 |
| 302/s1/greedy | 2 | a2j0 (3) | — |
| 302/s1/greedy | 3 | — | — |
| 302/s1/greedy | 4 | — | — |
| 302/s1/greedy | 5 | — | — |
| 302/s1/greedy | 6 | a1j1 (7) | a0j1, a2j1 |
| 302/s1/greedy | 7 | a0j1 (8) | a2j1 |
| 302/s1/greedy | 8 | — | — |
| 302/s1/greedy | 9 | — | — |
| 302/s1/greedy | 10 | — | — |
| 302/s1/greedy | 11 | — | — |
| 302/s1/greedy | 12 | — | — |
| 302/s2/delay | 0 | a1j0 (2) | a0j0, a2j0 |
| 302/s2/delay | 1 | a1j0 (2) | a0j0, a2j0 |
| 302/s2/delay | 2 | a0j0 (4) | a2j0 |
| 302/s2/delay | 3 | a0j0 (4) | a2j0 |
| 302/s2/delay | 4 | — | — |
| 302/s2/delay | 5 | — | — |
| 302/s2/delay | 6 | a0j1 (8) | a1j1, a2j1 |
| 302/s2/delay | 7 | a0j1 (8) | a1j1, a2j1 |
| 302/s2/delay | 8 | a1j1 (10) | — |
| 302/s2/delay | 9 | a1j1 (10) | — |
| 302/s2/delay | 10 | — | — |
| 302/s2/delay | 11 | — | — |
| 302/s2/delay | 12 | — | — |
| 302/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 302/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 302/s2/fcfs | 2 | a2j0 (4) | — |
| 302/s2/fcfs | 3 | a2j0 (4) | — |
| 302/s2/fcfs | 4 | — | — |
| 302/s2/fcfs | 5 | — | — |
| 302/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 302/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 302/s2/fcfs | 8 | a1j1 (10) | — |
| 302/s2/fcfs | 9 | a1j1 (10) | — |
| 302/s2/fcfs | 10 | — | — |
| 302/s2/fcfs | 11 | — | — |
| 302/s2/fcfs | 12 | — | — |
| 302/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 302/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 302/s2/uncertainty | 2 | a2j0 (4) | — |
| 302/s2/uncertainty | 3 | a2j0 (4) | — |
| 302/s2/uncertainty | 4 | — | — |
| 302/s2/uncertainty | 5 | — | — |
| 302/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 302/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 302/s2/uncertainty | 8 | a1j1 (10) | — |
| 302/s2/uncertainty | 9 | a1j1 (10) | — |
| 302/s2/uncertainty | 10 | — | — |
| 302/s2/uncertainty | 11 | — | — |
| 302/s2/uncertainty | 12 | — | — |
| 302/s2/myopic | 0 | a1j0 (2) | a0j0, a2j0 |
| 302/s2/myopic | 1 | a1j0 (2) | a0j0, a2j0 |
| 302/s2/myopic | 2 | a0j0 (4) | a2j0 |
| 302/s2/myopic | 3 | a0j0 (4) | a2j0 |
| 302/s2/myopic | 4 | — | — |
| 302/s2/myopic | 5 | — | — |
| 302/s2/myopic | 6 | a1j1 (8) | a0j1, a2j1 |
| 302/s2/myopic | 7 | a1j1 (8) | a0j1, a2j1 |
| 302/s2/myopic | 8 | a0j1 (10) | — |
| 302/s2/myopic | 9 | a0j1 (10) | — |
| 302/s2/myopic | 10 | — | — |
| 302/s2/myopic | 11 | — | — |
| 302/s2/myopic | 12 | — | — |
| 302/s2/greedy | 0 | a1j0 (2) | a0j0, a2j0 |
| 302/s2/greedy | 1 | a1j0 (2) | a0j0, a2j0 |
| 302/s2/greedy | 2 | a0j0 (4) | a2j0 |
| 302/s2/greedy | 3 | a0j0 (4) | a2j0 |
| 302/s2/greedy | 4 | — | — |
| 302/s2/greedy | 5 | — | — |
| 302/s2/greedy | 6 | a1j1 (8) | a0j1, a2j1 |
| 302/s2/greedy | 7 | a1j1 (8) | a0j1, a2j1 |
| 302/s2/greedy | 8 | a0j1 (10) | — |
| 302/s2/greedy | 9 | a0j1 (10) | — |
| 302/s2/greedy | 10 | — | — |
| 302/s2/greedy | 11 | — | — |
| 302/s2/greedy | 12 | — | — |
| 302/s2/edf | 0 | a1j0 (2) | a0j0, a2j0 |
| 302/s2/edf | 1 | a1j0 (2) | a0j0, a2j0 |
| 302/s2/edf | 2 | a2j0 (4) | a0j0 |
| 302/s2/edf | 3 | a2j0 (4) | a0j0 |
| 302/s2/edf | 4 | — | a0j0 |
| 302/s2/edf | 5 | — | — |
| 302/s2/edf | 6 | a2j1 (8) | a0j1, a1j1 |
| 302/s2/edf | 7 | a2j1 (8) | a0j1, a1j1 |
| 302/s2/edf | 8 | a1j1 (10) | a0j1 |
| 302/s2/edf | 9 | a1j1 (10) | a0j1 |
| 302/s2/edf | 10 | — | a0j1 |
| 302/s2/edf | 11 | — | — |
| 302/s2/edf | 12 | — | — |
| 303/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 303/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 303/s2/fcfs | 2 | a2j0 (4) | — |
| 303/s2/fcfs | 3 | a2j0 (4) | — |
| 303/s2/fcfs | 4 | — | — |
| 303/s2/fcfs | 5 | — | — |
| 303/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 303/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 303/s2/fcfs | 8 | a2j1 (10) | — |
| 303/s2/fcfs | 9 | a2j1 (10) | — |
| 303/s2/fcfs | 10 | — | — |
| 303/s2/fcfs | 11 | — | — |
| 303/s2/fcfs | 12 | — | — |
| 303/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 303/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 303/s2/uncertainty | 2 | a2j0 (4) | — |
| 303/s2/uncertainty | 3 | a2j0 (4) | — |
| 303/s2/uncertainty | 4 | — | — |
| 303/s2/uncertainty | 5 | — | — |
| 303/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 303/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 303/s2/uncertainty | 8 | a2j1 (10) | — |
| 303/s2/uncertainty | 9 | a2j1 (10) | — |
| 303/s2/uncertainty | 10 | — | — |
| 303/s2/uncertainty | 11 | — | — |
| 303/s2/uncertainty | 12 | — | — |
| 303/s2/myopic | 0 | a2j0 (2) | a0j0, a1j0 |
| 303/s2/myopic | 1 | a2j0 (2) | a0j0, a1j0 |
| 303/s2/myopic | 2 | a0j0 (4) | — |
| 303/s2/myopic | 3 | a0j0 (4) | — |
| 303/s2/myopic | 4 | — | — |
| 303/s2/myopic | 5 | — | — |
| 303/s2/myopic | 6 | a2j1 (8) | a0j1, a1j1 |
| 303/s2/myopic | 7 | a2j1 (8) | a0j1, a1j1 |
| 303/s2/myopic | 8 | a0j1 (10) | — |
| 303/s2/myopic | 9 | a0j1 (10) | — |
| 303/s2/myopic | 10 | — | — |
| 303/s2/myopic | 11 | — | — |
| 303/s2/myopic | 12 | — | — |
| 303/s2/greedy | 0 | a2j0 (2) | a0j0, a1j0 |
| 303/s2/greedy | 1 | a2j0 (2) | a0j0, a1j0 |
| 303/s2/greedy | 2 | a0j0 (4) | — |
| 303/s2/greedy | 3 | a0j0 (4) | — |
| 303/s2/greedy | 4 | — | — |
| 303/s2/greedy | 5 | — | — |
| 303/s2/greedy | 6 | a2j1 (8) | a0j1, a1j1 |
| 303/s2/greedy | 7 | a2j1 (8) | a0j1, a1j1 |
| 303/s2/greedy | 8 | a0j1 (10) | — |
| 303/s2/greedy | 9 | a0j1 (10) | — |
| 303/s2/greedy | 10 | — | — |
| 303/s2/greedy | 11 | — | — |
| 303/s2/greedy | 12 | — | — |
| 303/s2/edf | 0 | a1j0 (2) | a0j0, a2j0 |
| 303/s2/edf | 1 | a1j0 (2) | a0j0, a2j0 |
| 303/s2/edf | 2 | a2j0 (4) | a0j0 |
| 303/s2/edf | 3 | a2j0 (4) | a0j0 |
| 303/s2/edf | 4 | — | a0j0 |
| 303/s2/edf | 5 | — | — |
| 303/s2/edf | 6 | a1j1 (8) | a0j1, a2j1 |
| 303/s2/edf | 7 | a1j1 (8) | a0j1, a2j1 |
| 303/s2/edf | 8 | a0j1 (10) | a2j1 |
| 303/s2/edf | 9 | a0j1 (10) | a2j1 |
| 303/s2/edf | 10 | — | a2j1 |
| 303/s2/edf | 11 | — | — |
| 303/s2/edf | 12 | — | — |
| 303/s2/delay | 0 | a1j0 (2) | a0j0, a2j0 |
| 303/s2/delay | 1 | a1j0 (2) | a0j0, a2j0 |
| 303/s2/delay | 2 | a2j0 (4) | a0j0 |
| 303/s2/delay | 3 | a2j0 (4) | a0j0 |
| 303/s2/delay | 4 | — | a0j0 |
| 303/s2/delay | 5 | — | — |
| 303/s2/delay | 6 | a1j1 (8) | a0j1, a2j1 |
| 303/s2/delay | 7 | a1j1 (8) | a0j1, a2j1 |
| 303/s2/delay | 8 | a2j1 (10) | a0j1 |
| 303/s2/delay | 9 | a2j1 (10) | a0j1 |
| 303/s2/delay | 10 | — | — |
| 303/s2/delay | 11 | — | — |
| 303/s2/delay | 12 | — | — |
| 303/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 303/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 303/s1/uncertainty | 2 | a2j0 (3) | — |
| 303/s1/uncertainty | 3 | — | — |
| 303/s1/uncertainty | 4 | — | — |
| 303/s1/uncertainty | 5 | — | — |
| 303/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 303/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 303/s1/uncertainty | 8 | a2j1 (9) | — |
| 303/s1/uncertainty | 9 | — | — |
| 303/s1/uncertainty | 10 | — | — |
| 303/s1/uncertainty | 11 | — | — |
| 303/s1/uncertainty | 12 | — | — |
| 303/s1/myopic | 0 | a2j0 (1) | a0j0, a1j0 |
| 303/s1/myopic | 1 | a1j0 (2) | a0j0 |
| 303/s1/myopic | 2 | a0j0 (3) | — |
| 303/s1/myopic | 3 | — | — |
| 303/s1/myopic | 4 | — | — |
| 303/s1/myopic | 5 | — | — |
| 303/s1/myopic | 6 | a2j1 (7) | a0j1, a1j1 |
| 303/s1/myopic | 7 | a1j1 (8) | a0j1 |
| 303/s1/myopic | 8 | a0j1 (9) | — |
| 303/s1/myopic | 9 | — | — |
| 303/s1/myopic | 10 | — | — |
| 303/s1/myopic | 11 | — | — |
| 303/s1/myopic | 12 | — | — |
| 303/s1/greedy | 0 | a2j0 (1) | a0j0, a1j0 |
| 303/s1/greedy | 1 | a1j0 (2) | a0j0 |
| 303/s1/greedy | 2 | a0j0 (3) | — |
| 303/s1/greedy | 3 | — | — |
| 303/s1/greedy | 4 | — | — |
| 303/s1/greedy | 5 | — | — |
| 303/s1/greedy | 6 | a2j1 (7) | a0j1, a1j1 |
| 303/s1/greedy | 7 | a1j1 (8) | a0j1 |
| 303/s1/greedy | 8 | a0j1 (9) | — |
| 303/s1/greedy | 9 | — | — |
| 303/s1/greedy | 10 | — | — |
| 303/s1/greedy | 11 | — | — |
| 303/s1/greedy | 12 | — | — |
| 303/s1/edf | 0 | a1j0 (1) | a0j0, a2j0 |
| 303/s1/edf | 1 | a2j0 (2) | a0j0 |
| 303/s1/edf | 2 | a0j0 (3) | — |
| 303/s1/edf | 3 | — | — |
| 303/s1/edf | 4 | — | — |
| 303/s1/edf | 5 | — | — |
| 303/s1/edf | 6 | a1j1 (7) | a0j1, a2j1 |
| 303/s1/edf | 7 | a0j1 (8) | a2j1 |
| 303/s1/edf | 8 | a2j1 (9) | — |
| 303/s1/edf | 9 | — | — |
| 303/s1/edf | 10 | — | — |
| 303/s1/edf | 11 | — | — |
| 303/s1/edf | 12 | — | — |
| 303/s1/delay | 0 | a1j0 (1) | a0j0, a2j0 |
| 303/s1/delay | 1 | a0j0 (2) | a2j0 |
| 303/s1/delay | 2 | a2j0 (3) | — |
| 303/s1/delay | 3 | — | — |
| 303/s1/delay | 4 | — | — |
| 303/s1/delay | 5 | — | — |
| 303/s1/delay | 6 | a1j1 (7) | a0j1, a2j1 |
| 303/s1/delay | 7 | a0j1 (8) | a2j1 |
| 303/s1/delay | 8 | a2j1 (9) | — |
| 303/s1/delay | 9 | — | — |
| 303/s1/delay | 10 | — | — |
| 303/s1/delay | 11 | — | — |
| 303/s1/delay | 12 | — | — |
| 303/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 303/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 303/s1/fcfs | 2 | a2j0 (3) | — |
| 303/s1/fcfs | 3 | — | — |
| 303/s1/fcfs | 4 | — | — |
| 303/s1/fcfs | 5 | — | — |
| 303/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 303/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 303/s1/fcfs | 8 | a2j1 (9) | — |
| 303/s1/fcfs | 9 | — | — |
| 303/s1/fcfs | 10 | — | — |
| 303/s1/fcfs | 11 | — | — |
| 303/s1/fcfs | 12 | — | — |
| 304/s1/myopic | 0 | a2j0 (1) | a0j0, a1j0 |
| 304/s1/myopic | 1 | a0j0 (2) | a1j0 |
| 304/s1/myopic | 2 | a1j0 (3) | — |
| 304/s1/myopic | 3 | — | — |
| 304/s1/myopic | 4 | — | — |
| 304/s1/myopic | 5 | — | — |
| 304/s1/myopic | 6 | a0j1 (7) | a1j1, a2j1 |
| 304/s1/myopic | 7 | a1j1 (8) | a2j1 |
| 304/s1/myopic | 8 | a2j1 (9) | — |
| 304/s1/myopic | 9 | — | — |
| 304/s1/myopic | 10 | — | — |
| 304/s1/myopic | 11 | — | — |
| 304/s1/myopic | 12 | — | — |
| 304/s1/greedy | 0 | a2j0 (1) | a0j0, a1j0 |
| 304/s1/greedy | 1 | a0j0 (2) | a1j0 |
| 304/s1/greedy | 2 | a1j0 (3) | — |
| 304/s1/greedy | 3 | — | — |
| 304/s1/greedy | 4 | — | — |
| 304/s1/greedy | 5 | — | — |
| 304/s1/greedy | 6 | a0j1 (7) | a1j1, a2j1 |
| 304/s1/greedy | 7 | a1j1 (8) | a2j1 |
| 304/s1/greedy | 8 | a2j1 (9) | — |
| 304/s1/greedy | 9 | — | — |
| 304/s1/greedy | 10 | — | — |
| 304/s1/greedy | 11 | — | — |
| 304/s1/greedy | 12 | — | — |
| 304/s1/edf | 0 | a0j0 (1) | a1j0, a2j0 |
| 304/s1/edf | 1 | a2j0 (2) | a1j0 |
| 304/s1/edf | 2 | a1j0 (3) | — |
| 304/s1/edf | 3 | — | — |
| 304/s1/edf | 4 | — | — |
| 304/s1/edf | 5 | — | — |
| 304/s1/edf | 6 | a1j1 (7) | a0j1, a2j1 |
| 304/s1/edf | 7 | a0j1 (8) | a2j1 |
| 304/s1/edf | 8 | a2j1 (9) | — |
| 304/s1/edf | 9 | — | — |
| 304/s1/edf | 10 | — | — |
| 304/s1/edf | 11 | — | — |
| 304/s1/edf | 12 | — | — |
| 304/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 304/s1/delay | 1 | a1j0 (2) | a2j0 |
| 304/s1/delay | 2 | a2j0 (3) | — |
| 304/s1/delay | 3 | — | — |
| 304/s1/delay | 4 | — | — |
| 304/s1/delay | 5 | — | — |
| 304/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 304/s1/delay | 7 | a1j1 (8) | a2j1 |
| 304/s1/delay | 8 | a2j1 (9) | — |
| 304/s1/delay | 9 | — | — |
| 304/s1/delay | 10 | — | — |
| 304/s1/delay | 11 | — | — |
| 304/s1/delay | 12 | — | — |
| 304/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 304/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 304/s1/fcfs | 2 | a2j0 (3) | — |
| 304/s1/fcfs | 3 | — | — |
| 304/s1/fcfs | 4 | — | — |
| 304/s1/fcfs | 5 | — | — |
| 304/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 304/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 304/s1/fcfs | 8 | a2j1 (9) | — |
| 304/s1/fcfs | 9 | — | — |
| 304/s1/fcfs | 10 | — | — |
| 304/s1/fcfs | 11 | — | — |
| 304/s1/fcfs | 12 | — | — |
| 304/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 304/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 304/s1/uncertainty | 2 | a2j0 (3) | — |
| 304/s1/uncertainty | 3 | — | — |
| 304/s1/uncertainty | 4 | — | — |
| 304/s1/uncertainty | 5 | — | — |
| 304/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 304/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 304/s1/uncertainty | 8 | a2j1 (9) | — |
| 304/s1/uncertainty | 9 | — | — |
| 304/s1/uncertainty | 10 | — | — |
| 304/s1/uncertainty | 11 | — | — |
| 304/s1/uncertainty | 12 | — | — |
| 304/s2/greedy | 0 | a2j0 (2) | a0j0, a1j0 |
| 304/s2/greedy | 1 | a2j0 (2) | a0j0, a1j0 |
| 304/s2/greedy | 2 | a1j0 (4) | — |
| 304/s2/greedy | 3 | a1j0 (4) | — |
| 304/s2/greedy | 4 | — | — |
| 304/s2/greedy | 5 | — | — |
| 304/s2/greedy | 6 | a0j1 (8) | a1j1, a2j1 |
| 304/s2/greedy | 7 | a0j1 (8) | a1j1, a2j1 |
| 304/s2/greedy | 8 | a2j1 (10) | — |
| 304/s2/greedy | 9 | a2j1 (10) | — |
| 304/s2/greedy | 10 | — | — |
| 304/s2/greedy | 11 | — | — |
| 304/s2/greedy | 12 | — | — |
| 304/s2/edf | 0 | a0j0 (2) | a1j0, a2j0 |
| 304/s2/edf | 1 | a0j0 (2) | a1j0, a2j0 |
| 304/s2/edf | 2 | a2j0 (4) | a1j0 |
| 304/s2/edf | 3 | a2j0 (4) | a1j0 |
| 304/s2/edf | 4 | — | a1j0 |
| 304/s2/edf | 5 | — | — |
| 304/s2/edf | 6 | a1j1 (8) | a0j1, a2j1 |
| 304/s2/edf | 7 | a1j1 (8) | a0j1, a2j1 |
| 304/s2/edf | 8 | a0j1 (10) | a2j1 |
| 304/s2/edf | 9 | a0j1 (10) | a2j1 |
| 304/s2/edf | 10 | — | a2j1 |
| 304/s2/edf | 11 | — | — |
| 304/s2/edf | 12 | — | — |
| 304/s2/delay | 0 | a0j0 (2) | a1j0, a2j0 |
| 304/s2/delay | 1 | a0j0 (2) | a1j0, a2j0 |
| 304/s2/delay | 2 | a2j0 (4) | a1j0 |
| 304/s2/delay | 3 | a2j0 (4) | a1j0 |
| 304/s2/delay | 4 | — | a1j0 |
| 304/s2/delay | 5 | — | — |
| 304/s2/delay | 6 | a1j1 (8) | a0j1, a2j1 |
| 304/s2/delay | 7 | a1j1 (8) | a0j1, a2j1 |
| 304/s2/delay | 8 | a0j1 (10) | a2j1 |
| 304/s2/delay | 9 | a0j1 (10) | a2j1 |
| 304/s2/delay | 10 | — | a2j1 |
| 304/s2/delay | 11 | — | — |
| 304/s2/delay | 12 | — | — |
| 304/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 304/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 304/s2/fcfs | 2 | a1j0 (4) | a2j0 |
| 304/s2/fcfs | 3 | a1j0 (4) | a2j0 |
| 304/s2/fcfs | 4 | — | — |
| 304/s2/fcfs | 5 | — | — |
| 304/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 304/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 304/s2/fcfs | 8 | a2j1 (10) | — |
| 304/s2/fcfs | 9 | a2j1 (10) | — |
| 304/s2/fcfs | 10 | — | — |
| 304/s2/fcfs | 11 | — | — |
| 304/s2/fcfs | 12 | — | — |
| 304/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 304/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 304/s2/uncertainty | 2 | a1j0 (4) | a2j0 |
| 304/s2/uncertainty | 3 | a1j0 (4) | a2j0 |
| 304/s2/uncertainty | 4 | — | — |
| 304/s2/uncertainty | 5 | — | — |
| 304/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 304/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 304/s2/uncertainty | 8 | a2j1 (10) | — |
| 304/s2/uncertainty | 9 | a2j1 (10) | — |
| 304/s2/uncertainty | 10 | — | — |
| 304/s2/uncertainty | 11 | — | — |
| 304/s2/uncertainty | 12 | — | — |
| 304/s2/myopic | 0 | a2j0 (2) | a0j0, a1j0 |
| 304/s2/myopic | 1 | a2j0 (2) | a0j0, a1j0 |
| 304/s2/myopic | 2 | a1j0 (4) | — |
| 304/s2/myopic | 3 | a1j0 (4) | — |
| 304/s2/myopic | 4 | — | — |
| 304/s2/myopic | 5 | — | — |
| 304/s2/myopic | 6 | a0j1 (8) | a1j1, a2j1 |
| 304/s2/myopic | 7 | a0j1 (8) | a1j1, a2j1 |
| 304/s2/myopic | 8 | a2j1 (10) | — |
| 304/s2/myopic | 9 | a2j1 (10) | — |
| 304/s2/myopic | 10 | — | — |
| 304/s2/myopic | 11 | — | — |
| 304/s2/myopic | 12 | — | — |
| 305/s2/edf | 0 | a2j0 (2) | a0j0, a1j0 |
| 305/s2/edf | 1 | a2j0 (2) | a0j0, a1j0 |
| 305/s2/edf | 2 | a0j0 (4) | a1j0 |
| 305/s2/edf | 3 | a0j0 (4) | a1j0 |
| 305/s2/edf | 4 | — | a1j0 |
| 305/s2/edf | 5 | — | — |
| 305/s2/edf | 6 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/edf | 7 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/edf | 8 | a2j1 (10) | a1j1 |
| 305/s2/edf | 9 | a2j1 (10) | a1j1 |
| 305/s2/edf | 10 | — | a1j1 |
| 305/s2/edf | 11 | — | — |
| 305/s2/edf | 12 | — | — |
| 305/s2/delay | 0 | a0j0 (2) | a1j0, a2j0 |
| 305/s2/delay | 1 | a0j0 (2) | a1j0, a2j0 |
| 305/s2/delay | 2 | a1j0 (4) | — |
| 305/s2/delay | 3 | a1j0 (4) | — |
| 305/s2/delay | 4 | — | — |
| 305/s2/delay | 5 | — | — |
| 305/s2/delay | 6 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/delay | 7 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/delay | 8 | a2j1 (10) | a1j1 |
| 305/s2/delay | 9 | a2j1 (10) | a1j1 |
| 305/s2/delay | 10 | — | a1j1 |
| 305/s2/delay | 11 | — | — |
| 305/s2/delay | 12 | — | — |
| 305/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 305/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 305/s2/fcfs | 2 | a1j0 (4) | — |
| 305/s2/fcfs | 3 | a1j0 (4) | — |
| 305/s2/fcfs | 4 | — | — |
| 305/s2/fcfs | 5 | — | — |
| 305/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/fcfs | 8 | a1j1 (10) | a2j1 |
| 305/s2/fcfs | 9 | a1j1 (10) | a2j1 |
| 305/s2/fcfs | 10 | — | — |
| 305/s2/fcfs | 11 | — | — |
| 305/s2/fcfs | 12 | — | — |
| 305/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 305/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 305/s2/uncertainty | 2 | a1j0 (4) | — |
| 305/s2/uncertainty | 3 | a1j0 (4) | — |
| 305/s2/uncertainty | 4 | — | — |
| 305/s2/uncertainty | 5 | — | — |
| 305/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/uncertainty | 8 | a1j1 (10) | a2j1 |
| 305/s2/uncertainty | 9 | a1j1 (10) | a2j1 |
| 305/s2/uncertainty | 10 | — | — |
| 305/s2/uncertainty | 11 | — | — |
| 305/s2/uncertainty | 12 | — | — |
| 305/s2/myopic | 0 | a1j0 (2) | a0j0, a2j0 |
| 305/s2/myopic | 1 | a1j0 (2) | a0j0, a2j0 |
| 305/s2/myopic | 2 | a0j0 (4) | — |
| 305/s2/myopic | 3 | a0j0 (4) | — |
| 305/s2/myopic | 4 | — | — |
| 305/s2/myopic | 5 | — | — |
| 305/s2/myopic | 6 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/myopic | 7 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/myopic | 8 | a2j1 (10) | a1j1 |
| 305/s2/myopic | 9 | a2j1 (10) | a1j1 |
| 305/s2/myopic | 10 | — | a1j1 |
| 305/s2/myopic | 11 | — | — |
| 305/s2/myopic | 12 | — | — |
| 305/s2/greedy | 0 | a1j0 (2) | a0j0, a2j0 |
| 305/s2/greedy | 1 | a1j0 (2) | a0j0, a2j0 |
| 305/s2/greedy | 2 | a0j0 (4) | — |
| 305/s2/greedy | 3 | a0j0 (4) | — |
| 305/s2/greedy | 4 | — | — |
| 305/s2/greedy | 5 | — | — |
| 305/s2/greedy | 6 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/greedy | 7 | a0j1 (8) | a1j1, a2j1 |
| 305/s2/greedy | 8 | a2j1 (10) | a1j1 |
| 305/s2/greedy | 9 | a2j1 (10) | a1j1 |
| 305/s2/greedy | 10 | — | a1j1 |
| 305/s2/greedy | 11 | — | — |
| 305/s2/greedy | 12 | — | — |
| 305/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 305/s1/delay | 1 | a2j0 (2) | a1j0 |
| 305/s1/delay | 2 | a1j0 (3) | — |
| 305/s1/delay | 3 | — | — |
| 305/s1/delay | 4 | — | — |
| 305/s1/delay | 5 | — | — |
| 305/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 305/s1/delay | 7 | a1j1 (8) | a2j1 |
| 305/s1/delay | 8 | a2j1 (9) | — |
| 305/s1/delay | 9 | — | — |
| 305/s1/delay | 10 | — | — |
| 305/s1/delay | 11 | — | — |
| 305/s1/delay | 12 | — | — |
| 305/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 305/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 305/s1/fcfs | 2 | — | — |
| 305/s1/fcfs | 3 | — | — |
| 305/s1/fcfs | 4 | — | — |
| 305/s1/fcfs | 5 | — | — |
| 305/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 305/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 305/s1/fcfs | 8 | a2j1 (9) | — |
| 305/s1/fcfs | 9 | — | — |
| 305/s1/fcfs | 10 | — | — |
| 305/s1/fcfs | 11 | — | — |
| 305/s1/fcfs | 12 | — | — |
| 305/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 305/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 305/s1/uncertainty | 2 | — | — |
| 305/s1/uncertainty | 3 | — | — |
| 305/s1/uncertainty | 4 | — | — |
| 305/s1/uncertainty | 5 | — | — |
| 305/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 305/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 305/s1/uncertainty | 8 | a2j1 (9) | — |
| 305/s1/uncertainty | 9 | — | — |
| 305/s1/uncertainty | 10 | — | — |
| 305/s1/uncertainty | 11 | — | — |
| 305/s1/uncertainty | 12 | — | — |
| 305/s1/myopic | 0 | a1j0 (1) | a0j0, a2j0 |
| 305/s1/myopic | 1 | a0j0 (2) | a2j0 |
| 305/s1/myopic | 2 | — | — |
| 305/s1/myopic | 3 | — | — |
| 305/s1/myopic | 4 | — | — |
| 305/s1/myopic | 5 | — | — |
| 305/s1/myopic | 6 | a0j1 (7) | a1j1, a2j1 |
| 305/s1/myopic | 7 | a2j1 (8) | a1j1 |
| 305/s1/myopic | 8 | a1j1 (9) | — |
| 305/s1/myopic | 9 | — | — |
| 305/s1/myopic | 10 | — | — |
| 305/s1/myopic | 11 | — | — |
| 305/s1/myopic | 12 | — | — |
| 305/s1/greedy | 0 | a1j0 (1) | a0j0, a2j0 |
| 305/s1/greedy | 1 | a0j0 (2) | a2j0 |
| 305/s1/greedy | 2 | — | — |
| 305/s1/greedy | 3 | — | — |
| 305/s1/greedy | 4 | — | — |
| 305/s1/greedy | 5 | — | — |
| 305/s1/greedy | 6 | a0j1 (7) | a1j1, a2j1 |
| 305/s1/greedy | 7 | a2j1 (8) | a1j1 |
| 305/s1/greedy | 8 | a1j1 (9) | — |
| 305/s1/greedy | 9 | — | — |
| 305/s1/greedy | 10 | — | — |
| 305/s1/greedy | 11 | — | — |
| 305/s1/greedy | 12 | — | — |
| 305/s1/edf | 0 | a2j0 (1) | a0j0, a1j0 |
| 305/s1/edf | 1 | a0j0 (2) | a1j0 |
| 305/s1/edf | 2 | a1j0 (3) | — |
| 305/s1/edf | 3 | — | — |
| 305/s1/edf | 4 | — | — |
| 305/s1/edf | 5 | — | — |
| 305/s1/edf | 6 | a0j1 (7) | a1j1, a2j1 |
| 305/s1/edf | 7 | a2j1 (8) | a1j1 |
| 305/s1/edf | 8 | a1j1 (9) | — |
| 305/s1/edf | 9 | — | — |
| 305/s1/edf | 10 | — | — |
| 305/s1/edf | 11 | — | — |
| 305/s1/edf | 12 | — | — |
| 306/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 306/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 306/s1/fcfs | 2 | a2j0 (3) | — |
| 306/s1/fcfs | 3 | — | — |
| 306/s1/fcfs | 4 | — | — |
| 306/s1/fcfs | 5 | — | — |
| 306/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 306/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 306/s1/fcfs | 8 | a2j1 (9) | — |
| 306/s1/fcfs | 9 | — | — |
| 306/s1/fcfs | 10 | — | — |
| 306/s1/fcfs | 11 | — | — |
| 306/s1/fcfs | 12 | — | — |
| 306/s1/uncertainty | 0 | a2j0 (1) | a0j0, a1j0 |
| 306/s1/uncertainty | 1 | a0j0 (2) | a1j0 |
| 306/s1/uncertainty | 2 | a1j0 (3) | — |
| 306/s1/uncertainty | 3 | — | — |
| 306/s1/uncertainty | 4 | — | — |
| 306/s1/uncertainty | 5 | — | — |
| 306/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 306/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 306/s1/uncertainty | 8 | a2j1 (9) | — |
| 306/s1/uncertainty | 9 | — | — |
| 306/s1/uncertainty | 10 | — | — |
| 306/s1/uncertainty | 11 | — | — |
| 306/s1/uncertainty | 12 | — | — |
| 306/s1/myopic | 0 | a1j0 (1) | a0j0, a2j0 |
| 306/s1/myopic | 1 | a0j0 (2) | a2j0 |
| 306/s1/myopic | 2 | a2j0 (3) | — |
| 306/s1/myopic | 3 | — | — |
| 306/s1/myopic | 4 | — | — |
| 306/s1/myopic | 5 | — | — |
| 306/s1/myopic | 6 | a0j1 (7) | a1j1, a2j1 |
| 306/s1/myopic | 7 | a1j1 (8) | a2j1 |
| 306/s1/myopic | 8 | a2j1 (9) | — |
| 306/s1/myopic | 9 | — | — |
| 306/s1/myopic | 10 | — | — |
| 306/s1/myopic | 11 | — | — |
| 306/s1/myopic | 12 | — | — |
| 306/s1/greedy | 0 | a1j0 (1) | a0j0, a2j0 |
| 306/s1/greedy | 1 | a0j0 (2) | a2j0 |
| 306/s1/greedy | 2 | a2j0 (3) | — |
| 306/s1/greedy | 3 | — | — |
| 306/s1/greedy | 4 | — | — |
| 306/s1/greedy | 5 | — | — |
| 306/s1/greedy | 6 | a0j1 (7) | a1j1, a2j1 |
| 306/s1/greedy | 7 | a1j1 (8) | a2j1 |
| 306/s1/greedy | 8 | a2j1 (9) | — |
| 306/s1/greedy | 9 | — | — |
| 306/s1/greedy | 10 | — | — |
| 306/s1/greedy | 11 | — | — |
| 306/s1/greedy | 12 | — | — |
| 306/s1/edf | 0 | a0j0 (1) | a1j0, a2j0 |
| 306/s1/edf | 1 | a1j0 (2) | a2j0 |
| 306/s1/edf | 2 | a2j0 (3) | — |
| 306/s1/edf | 3 | — | — |
| 306/s1/edf | 4 | — | — |
| 306/s1/edf | 5 | — | — |
| 306/s1/edf | 6 | a1j1 (7) | a0j1, a2j1 |
| 306/s1/edf | 7 | a2j1 (8) | a0j1 |
| 306/s1/edf | 8 | a0j1 (9) | — |
| 306/s1/edf | 9 | — | — |
| 306/s1/edf | 10 | — | — |
| 306/s1/edf | 11 | — | — |
| 306/s1/edf | 12 | — | — |
| 306/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 306/s1/delay | 1 | a1j0 (2) | a2j0 |
| 306/s1/delay | 2 | a2j0 (3) | — |
| 306/s1/delay | 3 | — | — |
| 306/s1/delay | 4 | — | — |
| 306/s1/delay | 5 | — | — |
| 306/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 306/s1/delay | 7 | a1j1 (8) | a2j1 |
| 306/s1/delay | 8 | a2j1 (9) | — |
| 306/s1/delay | 9 | — | — |
| 306/s1/delay | 10 | — | — |
| 306/s1/delay | 11 | — | — |
| 306/s1/delay | 12 | — | — |
| 306/s2/uncertainty | 0 | a2j0 (2) | a0j0, a1j0 |
| 306/s2/uncertainty | 1 | a2j0 (2) | a0j0, a1j0 |
| 306/s2/uncertainty | 2 | a1j0 (4) | — |
| 306/s2/uncertainty | 3 | a1j0 (4) | — |
| 306/s2/uncertainty | 4 | — | — |
| 306/s2/uncertainty | 5 | — | — |
| 306/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 306/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 306/s2/uncertainty | 8 | a2j1 (10) | — |
| 306/s2/uncertainty | 9 | a2j1 (10) | — |
| 306/s2/uncertainty | 10 | — | — |
| 306/s2/uncertainty | 11 | — | — |
| 306/s2/uncertainty | 12 | — | — |
| 306/s2/myopic | 0 | a1j0 (2) | a0j0, a2j0 |
| 306/s2/myopic | 1 | a1j0 (2) | a0j0, a2j0 |
| 306/s2/myopic | 2 | a2j0 (4) | — |
| 306/s2/myopic | 3 | a2j0 (4) | — |
| 306/s2/myopic | 4 | — | — |
| 306/s2/myopic | 5 | — | — |
| 306/s2/myopic | 6 | a0j1 (8) | a1j1, a2j1 |
| 306/s2/myopic | 7 | a0j1 (8) | a1j1, a2j1 |
| 306/s2/myopic | 8 | a2j1 (10) | — |
| 306/s2/myopic | 9 | a2j1 (10) | — |
| 306/s2/myopic | 10 | — | — |
| 306/s2/myopic | 11 | — | — |
| 306/s2/myopic | 12 | — | — |
| 306/s2/greedy | 0 | a1j0 (2) | a0j0, a2j0 |
| 306/s2/greedy | 1 | a1j0 (2) | a0j0, a2j0 |
| 306/s2/greedy | 2 | a2j0 (4) | — |
| 306/s2/greedy | 3 | a2j0 (4) | — |
| 306/s2/greedy | 4 | — | — |
| 306/s2/greedy | 5 | — | — |
| 306/s2/greedy | 6 | a0j1 (8) | a1j1, a2j1 |
| 306/s2/greedy | 7 | a0j1 (8) | a1j1, a2j1 |
| 306/s2/greedy | 8 | a2j1 (10) | — |
| 306/s2/greedy | 9 | a2j1 (10) | — |
| 306/s2/greedy | 10 | — | — |
| 306/s2/greedy | 11 | — | — |
| 306/s2/greedy | 12 | — | — |
| 306/s2/edf | 0 | a0j0 (2) | a1j0, a2j0 |
| 306/s2/edf | 1 | a0j0 (2) | a1j0, a2j0 |
| 306/s2/edf | 2 | a1j0 (4) | a2j0 |
| 306/s2/edf | 3 | a1j0 (4) | a2j0 |
| 306/s2/edf | 4 | — | a2j0 |
| 306/s2/edf | 5 | — | — |
| 306/s2/edf | 6 | a1j1 (8) | a0j1, a2j1 |
| 306/s2/edf | 7 | a1j1 (8) | a0j1, a2j1 |
| 306/s2/edf | 8 | a2j1 (10) | a0j1 |
| 306/s2/edf | 9 | a2j1 (10) | a0j1 |
| 306/s2/edf | 10 | — | a0j1 |
| 306/s2/edf | 11 | — | — |
| 306/s2/edf | 12 | — | — |
| 306/s2/delay | 0 | a0j0 (2) | a1j0, a2j0 |
| 306/s2/delay | 1 | a0j0 (2) | a1j0, a2j0 |
| 306/s2/delay | 2 | a1j0 (4) | a2j0 |
| 306/s2/delay | 3 | a1j0 (4) | a2j0 |
| 306/s2/delay | 4 | — | a2j0 |
| 306/s2/delay | 5 | — | — |
| 306/s2/delay | 6 | a1j1 (8) | a0j1, a2j1 |
| 306/s2/delay | 7 | a1j1 (8) | a0j1, a2j1 |
| 306/s2/delay | 8 | a0j1 (10) | a2j1 |
| 306/s2/delay | 9 | a0j1 (10) | a2j1 |
| 306/s2/delay | 10 | — | — |
| 306/s2/delay | 11 | — | — |
| 306/s2/delay | 12 | — | — |
| 306/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 306/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 306/s2/fcfs | 2 | a1j0 (4) | a2j0 |
| 306/s2/fcfs | 3 | a1j0 (4) | a2j0 |
| 306/s2/fcfs | 4 | — | a2j0 |
| 306/s2/fcfs | 5 | — | — |
| 306/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 306/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 306/s2/fcfs | 8 | a2j1 (10) | — |
| 306/s2/fcfs | 9 | a2j1 (10) | — |
| 306/s2/fcfs | 10 | — | — |
| 306/s2/fcfs | 11 | — | — |
| 306/s2/fcfs | 12 | — | — |
| 307/s2/myopic | 0 | a2j0 (2) | a0j0, a1j0 |
| 307/s2/myopic | 1 | a2j0 (2) | a0j0, a1j0 |
| 307/s2/myopic | 2 | a0j0 (4) | — |
| 307/s2/myopic | 3 | a0j0 (4) | — |
| 307/s2/myopic | 4 | — | — |
| 307/s2/myopic | 5 | — | — |
| 307/s2/myopic | 6 | a1j1 (8) | a0j1, a2j1 |
| 307/s2/myopic | 7 | a1j1 (8) | a0j1, a2j1 |
| 307/s2/myopic | 8 | a2j1 (10) | — |
| 307/s2/myopic | 9 | a2j1 (10) | — |
| 307/s2/myopic | 10 | — | — |
| 307/s2/myopic | 11 | — | — |
| 307/s2/myopic | 12 | — | — |
| 307/s2/greedy | 0 | a2j0 (2) | a0j0, a1j0 |
| 307/s2/greedy | 1 | a2j0 (2) | a0j0, a1j0 |
| 307/s2/greedy | 2 | a0j0 (4) | — |
| 307/s2/greedy | 3 | a0j0 (4) | — |
| 307/s2/greedy | 4 | — | — |
| 307/s2/greedy | 5 | — | — |
| 307/s2/greedy | 6 | a1j1 (8) | a0j1, a2j1 |
| 307/s2/greedy | 7 | a1j1 (8) | a0j1, a2j1 |
| 307/s2/greedy | 8 | a2j1 (10) | — |
| 307/s2/greedy | 9 | a2j1 (10) | — |
| 307/s2/greedy | 10 | — | — |
| 307/s2/greedy | 11 | — | — |
| 307/s2/greedy | 12 | — | — |
| 307/s2/edf | 0 | a1j0 (2) | a0j0, a2j0 |
| 307/s2/edf | 1 | a1j0 (2) | a0j0, a2j0 |
| 307/s2/edf | 2 | a0j0 (4) | a2j0 |
| 307/s2/edf | 3 | a0j0 (4) | a2j0 |
| 307/s2/edf | 4 | — | a2j0 |
| 307/s2/edf | 5 | — | — |
| 307/s2/edf | 6 | a0j1 (8) | a1j1, a2j1 |
| 307/s2/edf | 7 | a0j1 (8) | a1j1, a2j1 |
| 307/s2/edf | 8 | a2j1 (10) | a1j1 |
| 307/s2/edf | 9 | a2j1 (10) | a1j1 |
| 307/s2/edf | 10 | — | a1j1 |
| 307/s2/edf | 11 | — | — |
| 307/s2/edf | 12 | — | — |
| 307/s2/delay | 0 | a1j0 (2) | a0j0, a2j0 |
| 307/s2/delay | 1 | a1j0 (2) | a0j0, a2j0 |
| 307/s2/delay | 2 | a2j0 (4) | a0j0 |
| 307/s2/delay | 3 | a2j0 (4) | a0j0 |
| 307/s2/delay | 4 | — | — |
| 307/s2/delay | 5 | — | — |
| 307/s2/delay | 6 | a0j1 (8) | a1j1, a2j1 |
| 307/s2/delay | 7 | a0j1 (8) | a1j1, a2j1 |
| 307/s2/delay | 8 | a1j1 (10) | a2j1 |
| 307/s2/delay | 9 | a1j1 (10) | a2j1 |
| 307/s2/delay | 10 | — | — |
| 307/s2/delay | 11 | — | — |
| 307/s2/delay | 12 | — | — |
| 307/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 307/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 307/s2/fcfs | 2 | a2j0 (4) | — |
| 307/s2/fcfs | 3 | a2j0 (4) | — |
| 307/s2/fcfs | 4 | — | — |
| 307/s2/fcfs | 5 | — | — |
| 307/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 307/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 307/s2/fcfs | 8 | a1j1 (10) | a2j1 |
| 307/s2/fcfs | 9 | a1j1 (10) | a2j1 |
| 307/s2/fcfs | 10 | — | — |
| 307/s2/fcfs | 11 | — | — |
| 307/s2/fcfs | 12 | — | — |
| 307/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 307/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 307/s2/uncertainty | 2 | a2j0 (4) | — |
| 307/s2/uncertainty | 3 | a2j0 (4) | — |
| 307/s2/uncertainty | 4 | — | — |
| 307/s2/uncertainty | 5 | — | — |
| 307/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 307/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 307/s2/uncertainty | 8 | a1j1 (10) | a2j1 |
| 307/s2/uncertainty | 9 | a1j1 (10) | a2j1 |
| 307/s2/uncertainty | 10 | — | — |
| 307/s2/uncertainty | 11 | — | — |
| 307/s2/uncertainty | 12 | — | — |
| 307/s1/greedy | 0 | a2j0 (1) | a0j0, a1j0 |
| 307/s1/greedy | 1 | a1j0 (2) | a0j0 |
| 307/s1/greedy | 2 | a0j0 (3) | — |
| 307/s1/greedy | 3 | — | — |
| 307/s1/greedy | 4 | — | — |
| 307/s1/greedy | 5 | — | — |
| 307/s1/greedy | 6 | a1j1 (7) | a0j1, a2j1 |
| 307/s1/greedy | 7 | a0j1 (8) | a2j1 |
| 307/s1/greedy | 8 | a2j1 (9) | — |
| 307/s1/greedy | 9 | — | — |
| 307/s1/greedy | 10 | — | — |
| 307/s1/greedy | 11 | — | — |
| 307/s1/greedy | 12 | — | — |
| 307/s1/edf | 0 | a1j0 (1) | a0j0, a2j0 |
| 307/s1/edf | 1 | a0j0 (2) | a2j0 |
| 307/s1/edf | 2 | a2j0 (3) | — |
| 307/s1/edf | 3 | — | — |
| 307/s1/edf | 4 | — | — |
| 307/s1/edf | 5 | — | — |
| 307/s1/edf | 6 | a0j1 (7) | a1j1, a2j1 |
| 307/s1/edf | 7 | a2j1 (8) | a1j1 |
| 307/s1/edf | 8 | a1j1 (9) | — |
| 307/s1/edf | 9 | — | — |
| 307/s1/edf | 10 | — | — |
| 307/s1/edf | 11 | — | — |
| 307/s1/edf | 12 | — | — |
| 307/s1/delay | 0 | a1j0 (1) | a0j0, a2j0 |
| 307/s1/delay | 1 | a0j0 (2) | a2j0 |
| 307/s1/delay | 2 | a2j0 (3) | — |
| 307/s1/delay | 3 | — | — |
| 307/s1/delay | 4 | — | — |
| 307/s1/delay | 5 | — | — |
| 307/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 307/s1/delay | 7 | a1j1 (8) | a2j1 |
| 307/s1/delay | 8 | a2j1 (9) | — |
| 307/s1/delay | 9 | — | — |
| 307/s1/delay | 10 | — | — |
| 307/s1/delay | 11 | — | — |
| 307/s1/delay | 12 | — | — |
| 307/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 307/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 307/s1/fcfs | 2 | a2j0 (3) | — |
| 307/s1/fcfs | 3 | — | — |
| 307/s1/fcfs | 4 | — | — |
| 307/s1/fcfs | 5 | — | — |
| 307/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 307/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 307/s1/fcfs | 8 | a2j1 (9) | — |
| 307/s1/fcfs | 9 | — | — |
| 307/s1/fcfs | 10 | — | — |
| 307/s1/fcfs | 11 | — | — |
| 307/s1/fcfs | 12 | — | — |
| 307/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 307/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 307/s1/uncertainty | 2 | a2j0 (3) | — |
| 307/s1/uncertainty | 3 | — | — |
| 307/s1/uncertainty | 4 | — | — |
| 307/s1/uncertainty | 5 | — | — |
| 307/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 307/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 307/s1/uncertainty | 8 | a2j1 (9) | — |
| 307/s1/uncertainty | 9 | — | — |
| 307/s1/uncertainty | 10 | — | — |
| 307/s1/uncertainty | 11 | — | — |
| 307/s1/uncertainty | 12 | — | — |
| 307/s1/myopic | 0 | a2j0 (1) | a0j0, a1j0 |
| 307/s1/myopic | 1 | a1j0 (2) | a0j0 |
| 307/s1/myopic | 2 | a0j0 (3) | — |
| 307/s1/myopic | 3 | — | — |
| 307/s1/myopic | 4 | — | — |
| 307/s1/myopic | 5 | — | — |
| 307/s1/myopic | 6 | a1j1 (7) | a0j1, a2j1 |
| 307/s1/myopic | 7 | a0j1 (8) | a2j1 |
| 307/s1/myopic | 8 | a2j1 (9) | — |
| 307/s1/myopic | 9 | — | — |
| 307/s1/myopic | 10 | — | — |
| 307/s1/myopic | 11 | — | — |
| 307/s1/myopic | 12 | — | — |
| 308/s1/edf | 0 | a2j0 (1) | a0j0, a1j0 |
| 308/s1/edf | 1 | a0j0 (2) | a1j0 |
| 308/s1/edf | 2 | a1j0 (3) | — |
| 308/s1/edf | 3 | — | — |
| 308/s1/edf | 4 | — | — |
| 308/s1/edf | 5 | — | — |
| 308/s1/edf | 6 | a2j1 (7) | a0j1, a1j1 |
| 308/s1/edf | 7 | a0j1 (8) | a1j1 |
| 308/s1/edf | 8 | a1j1 (9) | — |
| 308/s1/edf | 9 | — | — |
| 308/s1/edf | 10 | — | — |
| 308/s1/edf | 11 | — | — |
| 308/s1/edf | 12 | — | — |
| 308/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 308/s1/delay | 1 | a2j0 (2) | a1j0 |
| 308/s1/delay | 2 | a1j0 (3) | — |
| 308/s1/delay | 3 | — | — |
| 308/s1/delay | 4 | — | — |
| 308/s1/delay | 5 | — | — |
| 308/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 308/s1/delay | 7 | a2j1 (8) | a1j1 |
| 308/s1/delay | 8 | a1j1 (9) | — |
| 308/s1/delay | 9 | — | — |
| 308/s1/delay | 10 | — | — |
| 308/s1/delay | 11 | — | — |
| 308/s1/delay | 12 | — | — |
| 308/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 308/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 308/s1/fcfs | 2 | — | — |
| 308/s1/fcfs | 3 | — | — |
| 308/s1/fcfs | 4 | — | — |
| 308/s1/fcfs | 5 | — | — |
| 308/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 308/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 308/s1/fcfs | 8 | — | — |
| 308/s1/fcfs | 9 | — | — |
| 308/s1/fcfs | 10 | — | — |
| 308/s1/fcfs | 11 | — | — |
| 308/s1/fcfs | 12 | — | — |
| 308/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 308/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 308/s1/uncertainty | 2 | — | — |
| 308/s1/uncertainty | 3 | — | — |
| 308/s1/uncertainty | 4 | — | — |
| 308/s1/uncertainty | 5 | — | — |
| 308/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 308/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 308/s1/uncertainty | 8 | — | — |
| 308/s1/uncertainty | 9 | — | — |
| 308/s1/uncertainty | 10 | — | — |
| 308/s1/uncertainty | 11 | — | — |
| 308/s1/uncertainty | 12 | — | — |
| 308/s1/myopic | 0 | a0j0 (1) | a1j0, a2j0 |
| 308/s1/myopic | 1 | a2j0 (2) | a1j0 |
| 308/s1/myopic | 2 | a1j0 (3) | — |
| 308/s1/myopic | 3 | — | — |
| 308/s1/myopic | 4 | — | — |
| 308/s1/myopic | 5 | — | — |
| 308/s1/myopic | 6 | a0j1 (7) | a1j1, a2j1 |
| 308/s1/myopic | 7 | a2j1 (8) | a1j1 |
| 308/s1/myopic | 8 | a1j1 (9) | — |
| 308/s1/myopic | 9 | — | — |
| 308/s1/myopic | 10 | — | — |
| 308/s1/myopic | 11 | — | — |
| 308/s1/myopic | 12 | — | — |
| 308/s1/greedy | 0 | a0j0 (1) | a1j0, a2j0 |
| 308/s1/greedy | 1 | a2j0 (2) | a1j0 |
| 308/s1/greedy | 2 | a1j0 (3) | — |
| 308/s1/greedy | 3 | — | — |
| 308/s1/greedy | 4 | — | — |
| 308/s1/greedy | 5 | — | — |
| 308/s1/greedy | 6 | a0j1 (7) | a1j1, a2j1 |
| 308/s1/greedy | 7 | a2j1 (8) | a1j1 |
| 308/s1/greedy | 8 | a1j1 (9) | — |
| 308/s1/greedy | 9 | — | — |
| 308/s1/greedy | 10 | — | — |
| 308/s1/greedy | 11 | — | — |
| 308/s1/greedy | 12 | — | — |
| 308/s2/delay | 0 | a2j0 (2) | a0j0, a1j0 |
| 308/s2/delay | 1 | a2j0 (2) | a0j0, a1j0 |
| 308/s2/delay | 2 | a0j0 (4) | a1j0 |
| 308/s2/delay | 3 | a0j0 (4) | a1j0 |
| 308/s2/delay | 4 | — | a1j0 |
| 308/s2/delay | 5 | — | — |
| 308/s2/delay | 6 | a2j1 (8) | a0j1, a1j1 |
| 308/s2/delay | 7 | a2j1 (8) | a0j1, a1j1 |
| 308/s2/delay | 8 | a0j1 (10) | a1j1 |
| 308/s2/delay | 9 | a0j1 (10) | a1j1 |
| 308/s2/delay | 10 | — | a1j1 |
| 308/s2/delay | 11 | — | — |
| 308/s2/delay | 12 | — | — |
| 308/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 308/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 308/s2/fcfs | 2 | a1j0 (4) | — |
| 308/s2/fcfs | 3 | a1j0 (4) | — |
| 308/s2/fcfs | 4 | — | — |
| 308/s2/fcfs | 5 | — | — |
| 308/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 308/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 308/s2/fcfs | 8 | a1j1 (10) | — |
| 308/s2/fcfs | 9 | a1j1 (10) | — |
| 308/s2/fcfs | 10 | — | — |
| 308/s2/fcfs | 11 | — | — |
| 308/s2/fcfs | 12 | — | — |
| 308/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 308/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 308/s2/uncertainty | 2 | a1j0 (4) | — |
| 308/s2/uncertainty | 3 | a1j0 (4) | — |
| 308/s2/uncertainty | 4 | — | — |
| 308/s2/uncertainty | 5 | — | — |
| 308/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 308/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 308/s2/uncertainty | 8 | a1j1 (10) | — |
| 308/s2/uncertainty | 9 | a1j1 (10) | — |
| 308/s2/uncertainty | 10 | — | — |
| 308/s2/uncertainty | 11 | — | — |
| 308/s2/uncertainty | 12 | — | — |
| 308/s2/myopic | 0 | a0j0 (2) | a1j0, a2j0 |
| 308/s2/myopic | 1 | a0j0 (2) | a1j0, a2j0 |
| 308/s2/myopic | 2 | a1j0 (4) | — |
| 308/s2/myopic | 3 | a1j0 (4) | — |
| 308/s2/myopic | 4 | — | — |
| 308/s2/myopic | 5 | — | — |
| 308/s2/myopic | 6 | a0j1 (8) | a1j1, a2j1 |
| 308/s2/myopic | 7 | a0j1 (8) | a1j1, a2j1 |
| 308/s2/myopic | 8 | a1j1 (10) | — |
| 308/s2/myopic | 9 | a1j1 (10) | — |
| 308/s2/myopic | 10 | — | — |
| 308/s2/myopic | 11 | — | — |
| 308/s2/myopic | 12 | — | — |
| 308/s2/greedy | 0 | a0j0 (2) | a1j0, a2j0 |
| 308/s2/greedy | 1 | a0j0 (2) | a1j0, a2j0 |
| 308/s2/greedy | 2 | a1j0 (4) | — |
| 308/s2/greedy | 3 | a1j0 (4) | — |
| 308/s2/greedy | 4 | — | — |
| 308/s2/greedy | 5 | — | — |
| 308/s2/greedy | 6 | a0j1 (8) | a1j1, a2j1 |
| 308/s2/greedy | 7 | a0j1 (8) | a1j1, a2j1 |
| 308/s2/greedy | 8 | a1j1 (10) | — |
| 308/s2/greedy | 9 | a1j1 (10) | — |
| 308/s2/greedy | 10 | — | — |
| 308/s2/greedy | 11 | — | — |
| 308/s2/greedy | 12 | — | — |
| 308/s2/edf | 0 | a2j0 (2) | a0j0, a1j0 |
| 308/s2/edf | 1 | a2j0 (2) | a0j0, a1j0 |
| 308/s2/edf | 2 | a0j0 (4) | a1j0 |
| 308/s2/edf | 3 | a0j0 (4) | a1j0 |
| 308/s2/edf | 4 | — | a1j0 |
| 308/s2/edf | 5 | — | — |
| 308/s2/edf | 6 | a2j1 (8) | a0j1, a1j1 |
| 308/s2/edf | 7 | a2j1 (8) | a0j1, a1j1 |
| 308/s2/edf | 8 | a0j1 (10) | a1j1 |
| 308/s2/edf | 9 | a0j1 (10) | a1j1 |
| 308/s2/edf | 10 | — | a1j1 |
| 308/s2/edf | 11 | — | — |
| 308/s2/edf | 12 | — | — |
| 309/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 309/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 309/s2/fcfs | 2 | a1j0 (4) | — |
| 309/s2/fcfs | 3 | a1j0 (4) | — |
| 309/s2/fcfs | 4 | — | — |
| 309/s2/fcfs | 5 | — | — |
| 309/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 309/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 309/s2/fcfs | 8 | a1j1 (10) | — |
| 309/s2/fcfs | 9 | a1j1 (10) | — |
| 309/s2/fcfs | 10 | — | — |
| 309/s2/fcfs | 11 | — | — |
| 309/s2/fcfs | 12 | — | — |
| 309/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 309/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 309/s2/uncertainty | 2 | a1j0 (4) | — |
| 309/s2/uncertainty | 3 | a1j0 (4) | — |
| 309/s2/uncertainty | 4 | — | — |
| 309/s2/uncertainty | 5 | — | — |
| 309/s2/uncertainty | 6 | a2j1 (8) | a0j1, a1j1 |
| 309/s2/uncertainty | 7 | a2j1 (8) | a0j1, a1j1 |
| 309/s2/uncertainty | 8 | a0j1 (10) | a1j1 |
| 309/s2/uncertainty | 9 | a0j1 (10) | a1j1 |
| 309/s2/uncertainty | 10 | — | a1j1 |
| 309/s2/uncertainty | 11 | — | — |
| 309/s2/uncertainty | 12 | — | — |
| 309/s2/myopic | 0 | a2j0 (2) | a0j0, a1j0 |
| 309/s2/myopic | 1 | a2j0 (2) | a0j0, a1j0 |
| 309/s2/myopic | 2 | a1j0 (4) | a0j0 |
| 309/s2/myopic | 3 | a1j0 (4) | a0j0 |
| 309/s2/myopic | 4 | — | a0j0 |
| 309/s2/myopic | 5 | — | — |
| 309/s2/myopic | 6 | a0j1 (8) | a1j1, a2j1 |
| 309/s2/myopic | 7 | a0j1 (8) | a1j1, a2j1 |
| 309/s2/myopic | 8 | a1j1 (10) | — |
| 309/s2/myopic | 9 | a1j1 (10) | — |
| 309/s2/myopic | 10 | — | — |
| 309/s2/myopic | 11 | — | — |
| 309/s2/myopic | 12 | — | — |
| 309/s2/greedy | 0 | a2j0 (2) | a0j0, a1j0 |
| 309/s2/greedy | 1 | a2j0 (2) | a0j0, a1j0 |
| 309/s2/greedy | 2 | a1j0 (4) | a0j0 |
| 309/s2/greedy | 3 | a1j0 (4) | a0j0 |
| 309/s2/greedy | 4 | — | a0j0 |
| 309/s2/greedy | 5 | — | — |
| 309/s2/greedy | 6 | a0j1 (8) | a1j1, a2j1 |
| 309/s2/greedy | 7 | a0j1 (8) | a1j1, a2j1 |
| 309/s2/greedy | 8 | a1j1 (10) | — |
| 309/s2/greedy | 9 | a1j1 (10) | — |
| 309/s2/greedy | 10 | — | — |
| 309/s2/greedy | 11 | — | — |
| 309/s2/greedy | 12 | — | — |
| 309/s2/edf | 0 | a2j0 (2) | a0j0, a1j0 |
| 309/s2/edf | 1 | a2j0 (2) | a0j0, a1j0 |
| 309/s2/edf | 2 | a1j0 (4) | a0j0 |
| 309/s2/edf | 3 | a1j0 (4) | a0j0 |
| 309/s2/edf | 4 | — | a0j0 |
| 309/s2/edf | 5 | — | — |
| 309/s2/edf | 6 | a2j1 (8) | a0j1, a1j1 |
| 309/s2/edf | 7 | a2j1 (8) | a0j1, a1j1 |
| 309/s2/edf | 8 | a0j1 (10) | a1j1 |
| 309/s2/edf | 9 | a0j1 (10) | a1j1 |
| 309/s2/edf | 10 | — | a1j1 |
| 309/s2/edf | 11 | — | — |
| 309/s2/edf | 12 | — | — |
| 309/s2/delay | 0 | a2j0 (2) | a0j0, a1j0 |
| 309/s2/delay | 1 | a2j0 (2) | a0j0, a1j0 |
| 309/s2/delay | 2 | a1j0 (4) | a0j0 |
| 309/s2/delay | 3 | a1j0 (4) | a0j0 |
| 309/s2/delay | 4 | — | a0j0 |
| 309/s2/delay | 5 | — | — |
| 309/s2/delay | 6 | a0j1 (8) | a1j1, a2j1 |
| 309/s2/delay | 7 | a0j1 (8) | a1j1, a2j1 |
| 309/s2/delay | 8 | a1j1 (10) | — |
| 309/s2/delay | 9 | a1j1 (10) | — |
| 309/s2/delay | 10 | — | — |
| 309/s2/delay | 11 | — | — |
| 309/s2/delay | 12 | — | — |
| 309/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 309/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 309/s1/uncertainty | 2 | — | — |
| 309/s1/uncertainty | 3 | — | — |
| 309/s1/uncertainty | 4 | — | — |
| 309/s1/uncertainty | 5 | — | — |
| 309/s1/uncertainty | 6 | a2j1 (7) | a0j1, a1j1 |
| 309/s1/uncertainty | 7 | a0j1 (8) | a1j1 |
| 309/s1/uncertainty | 8 | a1j1 (9) | — |
| 309/s1/uncertainty | 9 | — | — |
| 309/s1/uncertainty | 10 | — | — |
| 309/s1/uncertainty | 11 | — | — |
| 309/s1/uncertainty | 12 | — | — |
| 309/s1/myopic | 0 | a2j0 (1) | a0j0, a1j0 |
| 309/s1/myopic | 1 | a1j0 (2) | a0j0 |
| 309/s1/myopic | 2 | a0j0 (3) | — |
| 309/s1/myopic | 3 | — | — |
| 309/s1/myopic | 4 | — | — |
| 309/s1/myopic | 5 | — | — |
| 309/s1/myopic | 6 | a0j1 (7) | a1j1, a2j1 |
| 309/s1/myopic | 7 | a1j1 (8) | a2j1 |
| 309/s1/myopic | 8 | — | — |
| 309/s1/myopic | 9 | — | — |
| 309/s1/myopic | 10 | — | — |
| 309/s1/myopic | 11 | — | — |
| 309/s1/myopic | 12 | — | — |
| 309/s1/greedy | 0 | a2j0 (1) | a0j0, a1j0 |
| 309/s1/greedy | 1 | a1j0 (2) | a0j0 |
| 309/s1/greedy | 2 | a0j0 (3) | — |
| 309/s1/greedy | 3 | — | — |
| 309/s1/greedy | 4 | — | — |
| 309/s1/greedy | 5 | — | — |
| 309/s1/greedy | 6 | a0j1 (7) | a1j1, a2j1 |
| 309/s1/greedy | 7 | a1j1 (8) | a2j1 |
| 309/s1/greedy | 8 | — | — |
| 309/s1/greedy | 9 | — | — |
| 309/s1/greedy | 10 | — | — |
| 309/s1/greedy | 11 | — | — |
| 309/s1/greedy | 12 | — | — |
| 309/s1/edf | 0 | a2j0 (1) | a0j0, a1j0 |
| 309/s1/edf | 1 | a1j0 (2) | a0j0 |
| 309/s1/edf | 2 | a0j0 (3) | — |
| 309/s1/edf | 3 | — | — |
| 309/s1/edf | 4 | — | — |
| 309/s1/edf | 5 | — | — |
| 309/s1/edf | 6 | a2j1 (7) | a0j1, a1j1 |
| 309/s1/edf | 7 | a0j1 (8) | a1j1 |
| 309/s1/edf | 8 | a1j1 (9) | — |
| 309/s1/edf | 9 | — | — |
| 309/s1/edf | 10 | — | — |
| 309/s1/edf | 11 | — | — |
| 309/s1/edf | 12 | — | — |
| 309/s1/delay | 0 | a1j0 (1) | a0j0, a2j0 |
| 309/s1/delay | 1 | a2j0 (2) | a0j0 |
| 309/s1/delay | 2 | a0j0 (3) | — |
| 309/s1/delay | 3 | — | — |
| 309/s1/delay | 4 | — | — |
| 309/s1/delay | 5 | — | — |
| 309/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 309/s1/delay | 7 | a2j1 (8) | a1j1 |
| 309/s1/delay | 8 | a1j1 (9) | — |
| 309/s1/delay | 9 | — | — |
| 309/s1/delay | 10 | — | — |
| 309/s1/delay | 11 | — | — |
| 309/s1/delay | 12 | — | — |
| 309/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 309/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 309/s1/fcfs | 2 | — | — |
| 309/s1/fcfs | 3 | — | — |
| 309/s1/fcfs | 4 | — | — |
| 309/s1/fcfs | 5 | — | — |
| 309/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 309/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 309/s1/fcfs | 8 | — | — |
| 309/s1/fcfs | 9 | — | — |
| 309/s1/fcfs | 10 | — | — |
| 309/s1/fcfs | 11 | — | — |
| 309/s1/fcfs | 12 | — | — |
| 310/s1/myopic | 0 | a1j0 (1) | a0j0, a2j0 |
| 310/s1/myopic | 1 | a2j0 (2) | a0j0 |
| 310/s1/myopic | 2 | a0j0 (3) | — |
| 310/s1/myopic | 3 | — | — |
| 310/s1/myopic | 4 | — | — |
| 310/s1/myopic | 5 | — | — |
| 310/s1/myopic | 6 | a0j1 (7) | a1j1, a2j1 |
| 310/s1/myopic | 7 | a1j1 (8) | a2j1 |
| 310/s1/myopic | 8 | a2j1 (9) | — |
| 310/s1/myopic | 9 | — | — |
| 310/s1/myopic | 10 | — | — |
| 310/s1/myopic | 11 | — | — |
| 310/s1/myopic | 12 | — | — |
| 310/s1/greedy | 0 | a1j0 (1) | a0j0, a2j0 |
| 310/s1/greedy | 1 | a2j0 (2) | a0j0 |
| 310/s1/greedy | 2 | a0j0 (3) | — |
| 310/s1/greedy | 3 | — | — |
| 310/s1/greedy | 4 | — | — |
| 310/s1/greedy | 5 | — | — |
| 310/s1/greedy | 6 | a0j1 (7) | a1j1, a2j1 |
| 310/s1/greedy | 7 | a1j1 (8) | a2j1 |
| 310/s1/greedy | 8 | a2j1 (9) | — |
| 310/s1/greedy | 9 | — | — |
| 310/s1/greedy | 10 | — | — |
| 310/s1/greedy | 11 | — | — |
| 310/s1/greedy | 12 | — | — |
| 310/s1/edf | 0 | a2j0 (1) | a0j0, a1j0 |
| 310/s1/edf | 1 | a1j0 (2) | a0j0 |
| 310/s1/edf | 2 | a0j0 (3) | — |
| 310/s1/edf | 3 | — | — |
| 310/s1/edf | 4 | — | — |
| 310/s1/edf | 5 | — | — |
| 310/s1/edf | 6 | a1j1 (7) | a0j1, a2j1 |
| 310/s1/edf | 7 | a0j1 (8) | a2j1 |
| 310/s1/edf | 8 | a2j1 (9) | — |
| 310/s1/edf | 9 | — | — |
| 310/s1/edf | 10 | — | — |
| 310/s1/edf | 11 | — | — |
| 310/s1/edf | 12 | — | — |
| 310/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 310/s1/delay | 1 | a2j0 (2) | a1j0 |
| 310/s1/delay | 2 | a1j0 (3) | — |
| 310/s1/delay | 3 | — | — |
| 310/s1/delay | 4 | — | — |
| 310/s1/delay | 5 | — | — |
| 310/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 310/s1/delay | 7 | a1j1 (8) | a2j1 |
| 310/s1/delay | 8 | a2j1 (9) | — |
| 310/s1/delay | 9 | — | — |
| 310/s1/delay | 10 | — | — |
| 310/s1/delay | 11 | — | — |
| 310/s1/delay | 12 | — | — |
| 310/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 310/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 310/s1/fcfs | 2 | — | — |
| 310/s1/fcfs | 3 | — | — |
| 310/s1/fcfs | 4 | — | — |
| 310/s1/fcfs | 5 | — | — |
| 310/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 310/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 310/s1/fcfs | 8 | a2j1 (9) | — |
| 310/s1/fcfs | 9 | — | — |
| 310/s1/fcfs | 10 | — | — |
| 310/s1/fcfs | 11 | — | — |
| 310/s1/fcfs | 12 | — | — |
| 310/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 310/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 310/s1/uncertainty | 2 | — | — |
| 310/s1/uncertainty | 3 | — | — |
| 310/s1/uncertainty | 4 | — | — |
| 310/s1/uncertainty | 5 | — | — |
| 310/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 310/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 310/s1/uncertainty | 8 | a2j1 (9) | — |
| 310/s1/uncertainty | 9 | — | — |
| 310/s1/uncertainty | 10 | — | — |
| 310/s1/uncertainty | 11 | — | — |
| 310/s1/uncertainty | 12 | — | — |
| 310/s2/greedy | 0 | a1j0 (2) | a0j0, a2j0 |
| 310/s2/greedy | 1 | a1j0 (2) | a0j0, a2j0 |
| 310/s2/greedy | 2 | a0j0 (4) | — |
| 310/s2/greedy | 3 | a0j0 (4) | — |
| 310/s2/greedy | 4 | — | — |
| 310/s2/greedy | 5 | — | — |
| 310/s2/greedy | 6 | a0j1 (8) | a1j1, a2j1 |
| 310/s2/greedy | 7 | a0j1 (8) | a1j1, a2j1 |
| 310/s2/greedy | 8 | a2j1 (10) | — |
| 310/s2/greedy | 9 | a2j1 (10) | — |
| 310/s2/greedy | 10 | — | — |
| 310/s2/greedy | 11 | — | — |
| 310/s2/greedy | 12 | — | — |
| 310/s2/edf | 0 | a2j0 (2) | a0j0, a1j0 |
| 310/s2/edf | 1 | a2j0 (2) | a0j0, a1j0 |
| 310/s2/edf | 2 | a1j0 (4) | a0j0 |
| 310/s2/edf | 3 | a1j0 (4) | a0j0 |
| 310/s2/edf | 4 | — | a0j0 |
| 310/s2/edf | 5 | — | — |
| 310/s2/edf | 6 | a1j1 (8) | a0j1, a2j1 |
| 310/s2/edf | 7 | a1j1 (8) | a0j1, a2j1 |
| 310/s2/edf | 8 | a0j1 (10) | a2j1 |
| 310/s2/edf | 9 | a0j1 (10) | a2j1 |
| 310/s2/edf | 10 | — | a2j1 |
| 310/s2/edf | 11 | — | — |
| 310/s2/edf | 12 | — | — |
| 310/s2/delay | 0 | a2j0 (2) | a0j0, a1j0 |
| 310/s2/delay | 1 | a2j0 (2) | a0j0, a1j0 |
| 310/s2/delay | 2 | a1j0 (4) | a0j0 |
| 310/s2/delay | 3 | a1j0 (4) | a0j0 |
| 310/s2/delay | 4 | — | a0j0 |
| 310/s2/delay | 5 | — | — |
| 310/s2/delay | 6 | a1j1 (8) | a0j1, a2j1 |
| 310/s2/delay | 7 | a1j1 (8) | a0j1, a2j1 |
| 310/s2/delay | 8 | a0j1 (10) | a2j1 |
| 310/s2/delay | 9 | a0j1 (10) | a2j1 |
| 310/s2/delay | 10 | — | a2j1 |
| 310/s2/delay | 11 | — | — |
| 310/s2/delay | 12 | — | — |
| 310/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 310/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 310/s2/fcfs | 2 | a1j0 (4) | — |
| 310/s2/fcfs | 3 | a1j0 (4) | — |
| 310/s2/fcfs | 4 | — | — |
| 310/s2/fcfs | 5 | — | — |
| 310/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 310/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 310/s2/fcfs | 8 | a2j1 (10) | — |
| 310/s2/fcfs | 9 | a2j1 (10) | — |
| 310/s2/fcfs | 10 | — | — |
| 310/s2/fcfs | 11 | — | — |
| 310/s2/fcfs | 12 | — | — |
| 310/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 310/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 310/s2/uncertainty | 2 | a1j0 (4) | — |
| 310/s2/uncertainty | 3 | a1j0 (4) | — |
| 310/s2/uncertainty | 4 | — | — |
| 310/s2/uncertainty | 5 | — | — |
| 310/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 310/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 310/s2/uncertainty | 8 | a2j1 (10) | — |
| 310/s2/uncertainty | 9 | a2j1 (10) | — |
| 310/s2/uncertainty | 10 | — | — |
| 310/s2/uncertainty | 11 | — | — |
| 310/s2/uncertainty | 12 | — | — |
| 310/s2/myopic | 0 | a1j0 (2) | a0j0, a2j0 |
| 310/s2/myopic | 1 | a1j0 (2) | a0j0, a2j0 |
| 310/s2/myopic | 2 | a0j0 (4) | — |
| 310/s2/myopic | 3 | a0j0 (4) | — |
| 310/s2/myopic | 4 | — | — |
| 310/s2/myopic | 5 | — | — |
| 310/s2/myopic | 6 | a0j1 (8) | a1j1, a2j1 |
| 310/s2/myopic | 7 | a0j1 (8) | a1j1, a2j1 |
| 310/s2/myopic | 8 | a2j1 (10) | — |
| 310/s2/myopic | 9 | a2j1 (10) | — |
| 310/s2/myopic | 10 | — | — |
| 310/s2/myopic | 11 | — | — |
| 310/s2/myopic | 12 | — | — |
| 311/s2/edf | 0 | a1j0 (2) | a0j0, a2j0 |
| 311/s2/edf | 1 | a1j0 (2) | a0j0, a2j0 |
| 311/s2/edf | 2 | a0j0 (4) | a2j0 |
| 311/s2/edf | 3 | a0j0 (4) | a2j0 |
| 311/s2/edf | 4 | — | a2j0 |
| 311/s2/edf | 5 | — | — |
| 311/s2/edf | 6 | a2j1 (8) | a0j1, a1j1 |
| 311/s2/edf | 7 | a2j1 (8) | a0j1, a1j1 |
| 311/s2/edf | 8 | a0j1 (10) | a1j1 |
| 311/s2/edf | 9 | a0j1 (10) | a1j1 |
| 311/s2/edf | 10 | — | a1j1 |
| 311/s2/edf | 11 | — | — |
| 311/s2/edf | 12 | — | — |
| 311/s2/delay | 0 | a1j0 (2) | a0j0, a2j0 |
| 311/s2/delay | 1 | a1j0 (2) | a0j0, a2j0 |
| 311/s2/delay | 2 | a2j0 (4) | a0j0 |
| 311/s2/delay | 3 | a2j0 (4) | a0j0 |
| 311/s2/delay | 4 | — | — |
| 311/s2/delay | 5 | — | — |
| 311/s2/delay | 6 | a2j1 (8) | a0j1, a1j1 |
| 311/s2/delay | 7 | a2j1 (8) | a0j1, a1j1 |
| 311/s2/delay | 8 | a1j1 (10) | a0j1 |
| 311/s2/delay | 9 | a1j1 (10) | a0j1 |
| 311/s2/delay | 10 | — | — |
| 311/s2/delay | 11 | — | — |
| 311/s2/delay | 12 | — | — |
| 311/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 311/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 311/s2/fcfs | 2 | a2j0 (4) | — |
| 311/s2/fcfs | 3 | a2j0 (4) | — |
| 311/s2/fcfs | 4 | — | — |
| 311/s2/fcfs | 5 | — | — |
| 311/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 311/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 311/s2/fcfs | 8 | a1j1 (10) | — |
| 311/s2/fcfs | 9 | a1j1 (10) | — |
| 311/s2/fcfs | 10 | — | — |
| 311/s2/fcfs | 11 | — | — |
| 311/s2/fcfs | 12 | — | — |
| 311/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 311/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 311/s2/uncertainty | 2 | a2j0 (4) | — |
| 311/s2/uncertainty | 3 | a2j0 (4) | — |
| 311/s2/uncertainty | 4 | — | — |
| 311/s2/uncertainty | 5 | — | — |
| 311/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 311/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 311/s2/uncertainty | 8 | a1j1 (10) | — |
| 311/s2/uncertainty | 9 | a1j1 (10) | — |
| 311/s2/uncertainty | 10 | — | — |
| 311/s2/uncertainty | 11 | — | — |
| 311/s2/uncertainty | 12 | — | — |
| 311/s2/myopic | 0 | a2j0 (2) | a0j0, a1j0 |
| 311/s2/myopic | 1 | a2j0 (2) | a0j0, a1j0 |
| 311/s2/myopic | 2 | a0j0 (4) | — |
| 311/s2/myopic | 3 | a0j0 (4) | — |
| 311/s2/myopic | 4 | — | — |
| 311/s2/myopic | 5 | — | — |
| 311/s2/myopic | 6 | a2j1 (8) | a0j1, a1j1 |
| 311/s2/myopic | 7 | a2j1 (8) | a0j1, a1j1 |
| 311/s2/myopic | 8 | a1j1 (10) | a0j1 |
| 311/s2/myopic | 9 | a1j1 (10) | a0j1 |
| 311/s2/myopic | 10 | — | — |
| 311/s2/myopic | 11 | — | — |
| 311/s2/myopic | 12 | — | — |
| 311/s2/greedy | 0 | a2j0 (2) | a0j0, a1j0 |
| 311/s2/greedy | 1 | a2j0 (2) | a0j0, a1j0 |
| 311/s2/greedy | 2 | a0j0 (4) | — |
| 311/s2/greedy | 3 | a0j0 (4) | — |
| 311/s2/greedy | 4 | — | — |
| 311/s2/greedy | 5 | — | — |
| 311/s2/greedy | 6 | a2j1 (8) | a0j1, a1j1 |
| 311/s2/greedy | 7 | a2j1 (8) | a0j1, a1j1 |
| 311/s2/greedy | 8 | a1j1 (10) | a0j1 |
| 311/s2/greedy | 9 | a1j1 (10) | a0j1 |
| 311/s2/greedy | 10 | — | — |
| 311/s2/greedy | 11 | — | — |
| 311/s2/greedy | 12 | — | — |
| 311/s1/delay | 0 | a1j0 (1) | a0j0, a2j0 |
| 311/s1/delay | 1 | a0j0 (2) | a2j0 |
| 311/s1/delay | 2 | a2j0 (3) | — |
| 311/s1/delay | 3 | — | — |
| 311/s1/delay | 4 | — | — |
| 311/s1/delay | 5 | — | — |
| 311/s1/delay | 6 | a1j1 (7) | a0j1, a2j1 |
| 311/s1/delay | 7 | a2j1 (8) | a0j1 |
| 311/s1/delay | 8 | a0j1 (9) | — |
| 311/s1/delay | 9 | — | — |
| 311/s1/delay | 10 | — | — |
| 311/s1/delay | 11 | — | — |
| 311/s1/delay | 12 | — | — |
| 311/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 311/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 311/s1/fcfs | 2 | a2j0 (3) | — |
| 311/s1/fcfs | 3 | — | — |
| 311/s1/fcfs | 4 | — | — |
| 311/s1/fcfs | 5 | — | — |
| 311/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 311/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 311/s1/fcfs | 8 | — | — |
| 311/s1/fcfs | 9 | — | — |
| 311/s1/fcfs | 10 | — | — |
| 311/s1/fcfs | 11 | — | — |
| 311/s1/fcfs | 12 | — | — |
| 311/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 311/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 311/s1/uncertainty | 2 | a2j0 (3) | — |
| 311/s1/uncertainty | 3 | — | — |
| 311/s1/uncertainty | 4 | — | — |
| 311/s1/uncertainty | 5 | — | — |
| 311/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 311/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 311/s1/uncertainty | 8 | — | — |
| 311/s1/uncertainty | 9 | — | — |
| 311/s1/uncertainty | 10 | — | — |
| 311/s1/uncertainty | 11 | — | — |
| 311/s1/uncertainty | 12 | — | — |
| 311/s1/myopic | 0 | a2j0 (1) | a0j0, a1j0 |
| 311/s1/myopic | 1 | a1j0 (2) | a0j0 |
| 311/s1/myopic | 2 | a0j0 (3) | — |
| 311/s1/myopic | 3 | — | — |
| 311/s1/myopic | 4 | — | — |
| 311/s1/myopic | 5 | — | — |
| 311/s1/myopic | 6 | a2j1 (7) | a0j1, a1j1 |
| 311/s1/myopic | 7 | a1j1 (8) | a0j1 |
| 311/s1/myopic | 8 | a0j1 (9) | — |
| 311/s1/myopic | 9 | — | — |
| 311/s1/myopic | 10 | — | — |
| 311/s1/myopic | 11 | — | — |
| 311/s1/myopic | 12 | — | — |
| 311/s1/greedy | 0 | a2j0 (1) | a0j0, a1j0 |
| 311/s1/greedy | 1 | a1j0 (2) | a0j0 |
| 311/s1/greedy | 2 | a0j0 (3) | — |
| 311/s1/greedy | 3 | — | — |
| 311/s1/greedy | 4 | — | — |
| 311/s1/greedy | 5 | — | — |
| 311/s1/greedy | 6 | a2j1 (7) | a0j1, a1j1 |
| 311/s1/greedy | 7 | a1j1 (8) | a0j1 |
| 311/s1/greedy | 8 | a0j1 (9) | — |
| 311/s1/greedy | 9 | — | — |
| 311/s1/greedy | 10 | — | — |
| 311/s1/greedy | 11 | — | — |
| 311/s1/greedy | 12 | — | — |
| 311/s1/edf | 0 | a1j0 (1) | a0j0, a2j0 |
| 311/s1/edf | 1 | a0j0 (2) | a2j0 |
| 311/s1/edf | 2 | a2j0 (3) | — |
| 311/s1/edf | 3 | — | — |
| 311/s1/edf | 4 | — | — |
| 311/s1/edf | 5 | — | — |
| 311/s1/edf | 6 | a2j1 (7) | a0j1, a1j1 |
| 311/s1/edf | 7 | a0j1 (8) | a1j1 |
| 311/s1/edf | 8 | a1j1 (9) | — |
| 311/s1/edf | 9 | — | — |
| 311/s1/edf | 10 | — | — |
| 311/s1/edf | 11 | — | — |
| 311/s1/edf | 12 | — | — |
| 312/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 312/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 312/s1/fcfs | 2 | — | — |
| 312/s1/fcfs | 3 | — | — |
| 312/s1/fcfs | 4 | — | — |
| 312/s1/fcfs | 5 | — | — |
| 312/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 312/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 312/s1/fcfs | 8 | a2j1 (9) | — |
| 312/s1/fcfs | 9 | — | — |
| 312/s1/fcfs | 10 | — | — |
| 312/s1/fcfs | 11 | — | — |
| 312/s1/fcfs | 12 | — | — |
| 312/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 312/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 312/s1/uncertainty | 2 | — | — |
| 312/s1/uncertainty | 3 | — | — |
| 312/s1/uncertainty | 4 | — | — |
| 312/s1/uncertainty | 5 | — | — |
| 312/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 312/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 312/s1/uncertainty | 8 | a2j1 (9) | — |
| 312/s1/uncertainty | 9 | — | — |
| 312/s1/uncertainty | 10 | — | — |
| 312/s1/uncertainty | 11 | — | — |
| 312/s1/uncertainty | 12 | — | — |
| 312/s1/myopic | 0 | a0j0 (1) | a1j0, a2j0 |
| 312/s1/myopic | 1 | a1j0 (2) | a2j0 |
| 312/s1/myopic | 2 | — | — |
| 312/s1/myopic | 3 | — | — |
| 312/s1/myopic | 4 | — | — |
| 312/s1/myopic | 5 | — | — |
| 312/s1/myopic | 6 | a1j1 (7) | a0j1, a2j1 |
| 312/s1/myopic | 7 | a0j1 (8) | a2j1 |
| 312/s1/myopic | 8 | a2j1 (9) | — |
| 312/s1/myopic | 9 | — | — |
| 312/s1/myopic | 10 | — | — |
| 312/s1/myopic | 11 | — | — |
| 312/s1/myopic | 12 | — | — |
| 312/s1/greedy | 0 | a0j0 (1) | a1j0, a2j0 |
| 312/s1/greedy | 1 | a1j0 (2) | a2j0 |
| 312/s1/greedy | 2 | — | — |
| 312/s1/greedy | 3 | — | — |
| 312/s1/greedy | 4 | — | — |
| 312/s1/greedy | 5 | — | — |
| 312/s1/greedy | 6 | a1j1 (7) | a0j1, a2j1 |
| 312/s1/greedy | 7 | a0j1 (8) | a2j1 |
| 312/s1/greedy | 8 | a2j1 (9) | — |
| 312/s1/greedy | 9 | — | — |
| 312/s1/greedy | 10 | — | — |
| 312/s1/greedy | 11 | — | — |
| 312/s1/greedy | 12 | — | — |
| 312/s1/edf | 0 | a2j0 (1) | a0j0, a1j0 |
| 312/s1/edf | 1 | a1j0 (2) | a0j0 |
| 312/s1/edf | 2 | a0j0 (3) | — |
| 312/s1/edf | 3 | — | — |
| 312/s1/edf | 4 | — | — |
| 312/s1/edf | 5 | — | — |
| 312/s1/edf | 6 | a0j1 (7) | a1j1, a2j1 |
| 312/s1/edf | 7 | a1j1 (8) | a2j1 |
| 312/s1/edf | 8 | a2j1 (9) | — |
| 312/s1/edf | 9 | — | — |
| 312/s1/edf | 10 | — | — |
| 312/s1/edf | 11 | — | — |
| 312/s1/edf | 12 | — | — |
| 312/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 312/s1/delay | 1 | a2j0 (2) | a1j0 |
| 312/s1/delay | 2 | a1j0 (3) | — |
| 312/s1/delay | 3 | — | — |
| 312/s1/delay | 4 | — | — |
| 312/s1/delay | 5 | — | — |
| 312/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 312/s1/delay | 7 | a1j1 (8) | a2j1 |
| 312/s1/delay | 8 | a2j1 (9) | — |
| 312/s1/delay | 9 | — | — |
| 312/s1/delay | 10 | — | — |
| 312/s1/delay | 11 | — | — |
| 312/s1/delay | 12 | — | — |
| 312/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 312/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 312/s2/uncertainty | 2 | a1j0 (4) | — |
| 312/s2/uncertainty | 3 | a1j0 (4) | — |
| 312/s2/uncertainty | 4 | — | — |
| 312/s2/uncertainty | 5 | — | — |
| 312/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 312/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 312/s2/uncertainty | 8 | a1j1 (10) | a2j1 |
| 312/s2/uncertainty | 9 | a1j1 (10) | a2j1 |
| 312/s2/uncertainty | 10 | — | a2j1 |
| 312/s2/uncertainty | 11 | — | — |
| 312/s2/uncertainty | 12 | — | — |
| 312/s2/myopic | 0 | a0j0 (2) | a1j0, a2j0 |
| 312/s2/myopic | 1 | a0j0 (2) | a1j0, a2j0 |
| 312/s2/myopic | 2 | a1j0 (4) | — |
| 312/s2/myopic | 3 | a1j0 (4) | — |
| 312/s2/myopic | 4 | — | — |
| 312/s2/myopic | 5 | — | — |
| 312/s2/myopic | 6 | a1j1 (8) | a0j1, a2j1 |
| 312/s2/myopic | 7 | a1j1 (8) | a0j1, a2j1 |
| 312/s2/myopic | 8 | a2j1 (10) | — |
| 312/s2/myopic | 9 | a2j1 (10) | — |
| 312/s2/myopic | 10 | — | — |
| 312/s2/myopic | 11 | — | — |
| 312/s2/myopic | 12 | — | — |
| 312/s2/greedy | 0 | a0j0 (2) | a1j0, a2j0 |
| 312/s2/greedy | 1 | a0j0 (2) | a1j0, a2j0 |
| 312/s2/greedy | 2 | a1j0 (4) | — |
| 312/s2/greedy | 3 | a1j0 (4) | — |
| 312/s2/greedy | 4 | — | — |
| 312/s2/greedy | 5 | — | — |
| 312/s2/greedy | 6 | a1j1 (8) | a0j1, a2j1 |
| 312/s2/greedy | 7 | a1j1 (8) | a0j1, a2j1 |
| 312/s2/greedy | 8 | a2j1 (10) | — |
| 312/s2/greedy | 9 | a2j1 (10) | — |
| 312/s2/greedy | 10 | — | — |
| 312/s2/greedy | 11 | — | — |
| 312/s2/greedy | 12 | — | — |
| 312/s2/edf | 0 | a2j0 (2) | a0j0, a1j0 |
| 312/s2/edf | 1 | a2j0 (2) | a0j0, a1j0 |
| 312/s2/edf | 2 | a1j0 (4) | a0j0 |
| 312/s2/edf | 3 | a1j0 (4) | a0j0 |
| 312/s2/edf | 4 | — | a0j0 |
| 312/s2/edf | 5 | — | — |
| 312/s2/edf | 6 | a0j1 (8) | a1j1, a2j1 |
| 312/s2/edf | 7 | a0j1 (8) | a1j1, a2j1 |
| 312/s2/edf | 8 | a1j1 (10) | a2j1 |
| 312/s2/edf | 9 | a1j1 (10) | a2j1 |
| 312/s2/edf | 10 | — | a2j1 |
| 312/s2/edf | 11 | — | — |
| 312/s2/edf | 12 | — | — |
| 312/s2/delay | 0 | a0j0 (2) | a1j0, a2j0 |
| 312/s2/delay | 1 | a0j0 (2) | a1j0, a2j0 |
| 312/s2/delay | 2 | a1j0 (4) | — |
| 312/s2/delay | 3 | a1j0 (4) | — |
| 312/s2/delay | 4 | — | — |
| 312/s2/delay | 5 | — | — |
| 312/s2/delay | 6 | a0j1 (8) | a1j1, a2j1 |
| 312/s2/delay | 7 | a0j1 (8) | a1j1, a2j1 |
| 312/s2/delay | 8 | a1j1 (10) | a2j1 |
| 312/s2/delay | 9 | a1j1 (10) | a2j1 |
| 312/s2/delay | 10 | — | a2j1 |
| 312/s2/delay | 11 | — | — |
| 312/s2/delay | 12 | — | — |
| 312/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 312/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 312/s2/fcfs | 2 | a1j0 (4) | — |
| 312/s2/fcfs | 3 | a1j0 (4) | — |
| 312/s2/fcfs | 4 | — | — |
| 312/s2/fcfs | 5 | — | — |
| 312/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 312/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 312/s2/fcfs | 8 | a1j1 (10) | a2j1 |
| 312/s2/fcfs | 9 | a1j1 (10) | a2j1 |
| 312/s2/fcfs | 10 | — | a2j1 |
| 312/s2/fcfs | 11 | — | — |
| 312/s2/fcfs | 12 | — | — |
| 313/s2/myopic | 0 | a1j0 (2) | a0j0, a2j0 |
| 313/s2/myopic | 1 | a1j0 (2) | a0j0, a2j0 |
| 313/s2/myopic | 2 | a2j0 (4) | — |
| 313/s2/myopic | 3 | a2j0 (4) | — |
| 313/s2/myopic | 4 | — | — |
| 313/s2/myopic | 5 | — | — |
| 313/s2/myopic | 6 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/myopic | 7 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/myopic | 8 | a2j1 (10) | a1j1 |
| 313/s2/myopic | 9 | a2j1 (10) | a1j1 |
| 313/s2/myopic | 10 | — | a1j1 |
| 313/s2/myopic | 11 | — | — |
| 313/s2/myopic | 12 | — | — |
| 313/s2/greedy | 0 | a1j0 (2) | a0j0, a2j0 |
| 313/s2/greedy | 1 | a1j0 (2) | a0j0, a2j0 |
| 313/s2/greedy | 2 | a2j0 (4) | — |
| 313/s2/greedy | 3 | a2j0 (4) | — |
| 313/s2/greedy | 4 | — | — |
| 313/s2/greedy | 5 | — | — |
| 313/s2/greedy | 6 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/greedy | 7 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/greedy | 8 | a2j1 (10) | a1j1 |
| 313/s2/greedy | 9 | a2j1 (10) | a1j1 |
| 313/s2/greedy | 10 | — | a1j1 |
| 313/s2/greedy | 11 | — | — |
| 313/s2/greedy | 12 | — | — |
| 313/s2/edf | 0 | a0j0 (2) | a1j0, a2j0 |
| 313/s2/edf | 1 | a0j0 (2) | a1j0, a2j0 |
| 313/s2/edf | 2 | a1j0 (4) | a2j0 |
| 313/s2/edf | 3 | a1j0 (4) | a2j0 |
| 313/s2/edf | 4 | — | a2j0 |
| 313/s2/edf | 5 | — | — |
| 313/s2/edf | 6 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/edf | 7 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/edf | 8 | a2j1 (10) | a1j1 |
| 313/s2/edf | 9 | a2j1 (10) | a1j1 |
| 313/s2/edf | 10 | — | a1j1 |
| 313/s2/edf | 11 | — | — |
| 313/s2/edf | 12 | — | — |
| 313/s2/delay | 0 | a0j0 (2) | a1j0, a2j0 |
| 313/s2/delay | 1 | a0j0 (2) | a1j0, a2j0 |
| 313/s2/delay | 2 | a1j0 (4) | a2j0 |
| 313/s2/delay | 3 | a1j0 (4) | a2j0 |
| 313/s2/delay | 4 | — | a2j0 |
| 313/s2/delay | 5 | — | — |
| 313/s2/delay | 6 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/delay | 7 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/delay | 8 | a2j1 (10) | a1j1 |
| 313/s2/delay | 9 | a2j1 (10) | a1j1 |
| 313/s2/delay | 10 | — | a1j1 |
| 313/s2/delay | 11 | — | — |
| 313/s2/delay | 12 | — | — |
| 313/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 313/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 313/s2/fcfs | 2 | a1j0 (4) | a2j0 |
| 313/s2/fcfs | 3 | a1j0 (4) | a2j0 |
| 313/s2/fcfs | 4 | — | a2j0 |
| 313/s2/fcfs | 5 | — | — |
| 313/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/fcfs | 8 | a1j1 (10) | a2j1 |
| 313/s2/fcfs | 9 | a1j1 (10) | a2j1 |
| 313/s2/fcfs | 10 | — | — |
| 313/s2/fcfs | 11 | — | — |
| 313/s2/fcfs | 12 | — | — |
| 313/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 313/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 313/s2/uncertainty | 2 | a1j0 (4) | a2j0 |
| 313/s2/uncertainty | 3 | a1j0 (4) | a2j0 |
| 313/s2/uncertainty | 4 | — | a2j0 |
| 313/s2/uncertainty | 5 | — | — |
| 313/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 313/s2/uncertainty | 8 | a1j1 (10) | a2j1 |
| 313/s2/uncertainty | 9 | a1j1 (10) | a2j1 |
| 313/s2/uncertainty | 10 | — | — |
| 313/s2/uncertainty | 11 | — | — |
| 313/s2/uncertainty | 12 | — | — |
| 313/s1/greedy | 0 | a1j0 (1) | a0j0, a2j0 |
| 313/s1/greedy | 1 | a0j0 (2) | a2j0 |
| 313/s1/greedy | 2 | a2j0 (3) | — |
| 313/s1/greedy | 3 | — | — |
| 313/s1/greedy | 4 | — | — |
| 313/s1/greedy | 5 | — | — |
| 313/s1/greedy | 6 | a0j1 (7) | a1j1, a2j1 |
| 313/s1/greedy | 7 | a2j1 (8) | a1j1 |
| 313/s1/greedy | 8 | a1j1 (9) | — |
| 313/s1/greedy | 9 | — | — |
| 313/s1/greedy | 10 | — | — |
| 313/s1/greedy | 11 | — | — |
| 313/s1/greedy | 12 | — | — |
| 313/s1/edf | 0 | a0j0 (1) | a1j0, a2j0 |
| 313/s1/edf | 1 | a1j0 (2) | a2j0 |
| 313/s1/edf | 2 | a2j0 (3) | — |
| 313/s1/edf | 3 | — | — |
| 313/s1/edf | 4 | — | — |
| 313/s1/edf | 5 | — | — |
| 313/s1/edf | 6 | a0j1 (7) | a1j1, a2j1 |
| 313/s1/edf | 7 | a2j1 (8) | a1j1 |
| 313/s1/edf | 8 | a1j1 (9) | — |
| 313/s1/edf | 9 | — | — |
| 313/s1/edf | 10 | — | — |
| 313/s1/edf | 11 | — | — |
| 313/s1/edf | 12 | — | — |
| 313/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 313/s1/delay | 1 | a1j0 (2) | a2j0 |
| 313/s1/delay | 2 | a2j0 (3) | — |
| 313/s1/delay | 3 | — | — |
| 313/s1/delay | 4 | — | — |
| 313/s1/delay | 5 | — | — |
| 313/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 313/s1/delay | 7 | a1j1 (8) | a2j1 |
| 313/s1/delay | 8 | a2j1 (9) | — |
| 313/s1/delay | 9 | — | — |
| 313/s1/delay | 10 | — | — |
| 313/s1/delay | 11 | — | — |
| 313/s1/delay | 12 | — | — |
| 313/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 313/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 313/s1/fcfs | 2 | a2j0 (3) | — |
| 313/s1/fcfs | 3 | — | — |
| 313/s1/fcfs | 4 | — | — |
| 313/s1/fcfs | 5 | — | — |
| 313/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 313/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 313/s1/fcfs | 8 | a2j1 (9) | — |
| 313/s1/fcfs | 9 | — | — |
| 313/s1/fcfs | 10 | — | — |
| 313/s1/fcfs | 11 | — | — |
| 313/s1/fcfs | 12 | — | — |
| 313/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 313/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 313/s1/uncertainty | 2 | a2j0 (3) | — |
| 313/s1/uncertainty | 3 | — | — |
| 313/s1/uncertainty | 4 | — | — |
| 313/s1/uncertainty | 5 | — | — |
| 313/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 313/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 313/s1/uncertainty | 8 | a2j1 (9) | — |
| 313/s1/uncertainty | 9 | — | — |
| 313/s1/uncertainty | 10 | — | — |
| 313/s1/uncertainty | 11 | — | — |
| 313/s1/uncertainty | 12 | — | — |
| 313/s1/myopic | 0 | a1j0 (1) | a0j0, a2j0 |
| 313/s1/myopic | 1 | a0j0 (2) | a2j0 |
| 313/s1/myopic | 2 | a2j0 (3) | — |
| 313/s1/myopic | 3 | — | — |
| 313/s1/myopic | 4 | — | — |
| 313/s1/myopic | 5 | — | — |
| 313/s1/myopic | 6 | a0j1 (7) | a1j1, a2j1 |
| 313/s1/myopic | 7 | a2j1 (8) | a1j1 |
| 313/s1/myopic | 8 | a1j1 (9) | — |
| 313/s1/myopic | 9 | — | — |
| 313/s1/myopic | 10 | — | — |
| 313/s1/myopic | 11 | — | — |
| 313/s1/myopic | 12 | — | — |
| 314/s1/edf | 0 | a2j0 (1) | a0j0, a1j0 |
| 314/s1/edf | 1 | a1j0 (2) | a0j0 |
| 314/s1/edf | 2 | a0j0 (3) | — |
| 314/s1/edf | 3 | — | — |
| 314/s1/edf | 4 | — | — |
| 314/s1/edf | 5 | — | — |
| 314/s1/edf | 6 | a0j1 (7) | a1j1, a2j1 |
| 314/s1/edf | 7 | a2j1 (8) | a1j1 |
| 314/s1/edf | 8 | a1j1 (9) | — |
| 314/s1/edf | 9 | — | — |
| 314/s1/edf | 10 | — | — |
| 314/s1/edf | 11 | — | — |
| 314/s1/edf | 12 | — | — |
| 314/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 314/s1/delay | 1 | a2j0 (2) | a1j0 |
| 314/s1/delay | 2 | a1j0 (3) | — |
| 314/s1/delay | 3 | — | — |
| 314/s1/delay | 4 | — | — |
| 314/s1/delay | 5 | — | — |
| 314/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 314/s1/delay | 7 | a1j1 (8) | a2j1 |
| 314/s1/delay | 8 | a2j1 (9) | — |
| 314/s1/delay | 9 | — | — |
| 314/s1/delay | 10 | — | — |
| 314/s1/delay | 11 | — | — |
| 314/s1/delay | 12 | — | — |
| 314/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 314/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 314/s1/fcfs | 2 | — | — |
| 314/s1/fcfs | 3 | — | — |
| 314/s1/fcfs | 4 | — | — |
| 314/s1/fcfs | 5 | — | — |
| 314/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 314/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 314/s1/fcfs | 8 | a2j1 (9) | — |
| 314/s1/fcfs | 9 | — | — |
| 314/s1/fcfs | 10 | — | — |
| 314/s1/fcfs | 11 | — | — |
| 314/s1/fcfs | 12 | — | — |
| 314/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 314/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 314/s1/uncertainty | 2 | — | — |
| 314/s1/uncertainty | 3 | — | — |
| 314/s1/uncertainty | 4 | — | — |
| 314/s1/uncertainty | 5 | — | — |
| 314/s1/uncertainty | 6 | a0j1 (7) | a1j1, a2j1 |
| 314/s1/uncertainty | 7 | a1j1 (8) | a2j1 |
| 314/s1/uncertainty | 8 | a2j1 (9) | — |
| 314/s1/uncertainty | 9 | — | — |
| 314/s1/uncertainty | 10 | — | — |
| 314/s1/uncertainty | 11 | — | — |
| 314/s1/uncertainty | 12 | — | — |
| 314/s1/myopic | 0 | a0j0 (1) | a1j0, a2j0 |
| 314/s1/myopic | 1 | a2j0 (2) | a1j0 |
| 314/s1/myopic | 2 | a1j0 (3) | — |
| 314/s1/myopic | 3 | — | — |
| 314/s1/myopic | 4 | — | — |
| 314/s1/myopic | 5 | — | — |
| 314/s1/myopic | 6 | a1j1 (7) | a0j1, a2j1 |
| 314/s1/myopic | 7 | a2j1 (8) | a0j1 |
| 314/s1/myopic | 8 | — | — |
| 314/s1/myopic | 9 | — | — |
| 314/s1/myopic | 10 | — | — |
| 314/s1/myopic | 11 | — | — |
| 314/s1/myopic | 12 | — | — |
| 314/s1/greedy | 0 | a0j0 (1) | a1j0, a2j0 |
| 314/s1/greedy | 1 | a2j0 (2) | a1j0 |
| 314/s1/greedy | 2 | a1j0 (3) | — |
| 314/s1/greedy | 3 | — | — |
| 314/s1/greedy | 4 | — | — |
| 314/s1/greedy | 5 | — | — |
| 314/s1/greedy | 6 | a1j1 (7) | a0j1, a2j1 |
| 314/s1/greedy | 7 | a2j1 (8) | a0j1 |
| 314/s1/greedy | 8 | — | — |
| 314/s1/greedy | 9 | — | — |
| 314/s1/greedy | 10 | — | — |
| 314/s1/greedy | 11 | — | — |
| 314/s1/greedy | 12 | — | — |
| 314/s2/delay | 0 | a2j0 (2) | a0j0, a1j0 |
| 314/s2/delay | 1 | a2j0 (2) | a0j0, a1j0 |
| 314/s2/delay | 2 | a0j0 (4) | a1j0 |
| 314/s2/delay | 3 | a0j0 (4) | a1j0 |
| 314/s2/delay | 4 | — | — |
| 314/s2/delay | 5 | — | — |
| 314/s2/delay | 6 | a1j1 (8) | a0j1, a2j1 |
| 314/s2/delay | 7 | a1j1 (8) | a0j1, a2j1 |
| 314/s2/delay | 8 | a2j1 (10) | — |
| 314/s2/delay | 9 | a2j1 (10) | — |
| 314/s2/delay | 10 | — | — |
| 314/s2/delay | 11 | — | — |
| 314/s2/delay | 12 | — | — |
| 314/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 314/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 314/s2/fcfs | 2 | a1j0 (4) | — |
| 314/s2/fcfs | 3 | a1j0 (4) | — |
| 314/s2/fcfs | 4 | — | — |
| 314/s2/fcfs | 5 | — | — |
| 314/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 314/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 314/s2/fcfs | 8 | a1j1 (10) | a2j1 |
| 314/s2/fcfs | 9 | a1j1 (10) | a2j1 |
| 314/s2/fcfs | 10 | — | — |
| 314/s2/fcfs | 11 | — | — |
| 314/s2/fcfs | 12 | — | — |
| 314/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 314/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 314/s2/uncertainty | 2 | a1j0 (4) | — |
| 314/s2/uncertainty | 3 | a1j0 (4) | — |
| 314/s2/uncertainty | 4 | — | — |
| 314/s2/uncertainty | 5 | — | — |
| 314/s2/uncertainty | 6 | a0j1 (8) | a1j1, a2j1 |
| 314/s2/uncertainty | 7 | a0j1 (8) | a1j1, a2j1 |
| 314/s2/uncertainty | 8 | a1j1 (10) | a2j1 |
| 314/s2/uncertainty | 9 | a1j1 (10) | a2j1 |
| 314/s2/uncertainty | 10 | — | — |
| 314/s2/uncertainty | 11 | — | — |
| 314/s2/uncertainty | 12 | — | — |
| 314/s2/myopic | 0 | a0j0 (2) | a1j0, a2j0 |
| 314/s2/myopic | 1 | a0j0 (2) | a1j0, a2j0 |
| 314/s2/myopic | 2 | a1j0 (4) | — |
| 314/s2/myopic | 3 | a1j0 (4) | — |
| 314/s2/myopic | 4 | — | — |
| 314/s2/myopic | 5 | — | — |
| 314/s2/myopic | 6 | a1j1 (8) | a0j1, a2j1 |
| 314/s2/myopic | 7 | a1j1 (8) | a0j1, a2j1 |
| 314/s2/myopic | 8 | a2j1 (10) | — |
| 314/s2/myopic | 9 | a2j1 (10) | — |
| 314/s2/myopic | 10 | — | — |
| 314/s2/myopic | 11 | — | — |
| 314/s2/myopic | 12 | — | — |
| 314/s2/greedy | 0 | a0j0 (2) | a1j0, a2j0 |
| 314/s2/greedy | 1 | a0j0 (2) | a1j0, a2j0 |
| 314/s2/greedy | 2 | a1j0 (4) | — |
| 314/s2/greedy | 3 | a1j0 (4) | — |
| 314/s2/greedy | 4 | — | — |
| 314/s2/greedy | 5 | — | — |
| 314/s2/greedy | 6 | a1j1 (8) | a0j1, a2j1 |
| 314/s2/greedy | 7 | a1j1 (8) | a0j1, a2j1 |
| 314/s2/greedy | 8 | a2j1 (10) | — |
| 314/s2/greedy | 9 | a2j1 (10) | — |
| 314/s2/greedy | 10 | — | — |
| 314/s2/greedy | 11 | — | — |
| 314/s2/greedy | 12 | — | — |
| 314/s2/edf | 0 | a2j0 (2) | a0j0, a1j0 |
| 314/s2/edf | 1 | a2j0 (2) | a0j0, a1j0 |
| 314/s2/edf | 2 | a1j0 (4) | a0j0 |
| 314/s2/edf | 3 | a1j0 (4) | a0j0 |
| 314/s2/edf | 4 | — | a0j0 |
| 314/s2/edf | 5 | — | — |
| 314/s2/edf | 6 | a0j1 (8) | a1j1, a2j1 |
| 314/s2/edf | 7 | a0j1 (8) | a1j1, a2j1 |
| 314/s2/edf | 8 | a2j1 (10) | a1j1 |
| 314/s2/edf | 9 | a2j1 (10) | a1j1 |
| 314/s2/edf | 10 | — | a1j1 |
| 314/s2/edf | 11 | — | — |
| 314/s2/edf | 12 | — | — |
| 315/s2/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| 315/s2/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| 315/s2/fcfs | 2 | a1j0 (4) | a2j0 |
| 315/s2/fcfs | 3 | a1j0 (4) | a2j0 |
| 315/s2/fcfs | 4 | — | — |
| 315/s2/fcfs | 5 | — | — |
| 315/s2/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| 315/s2/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| 315/s2/fcfs | 8 | a2j1 (10) | — |
| 315/s2/fcfs | 9 | a2j1 (10) | — |
| 315/s2/fcfs | 10 | — | — |
| 315/s2/fcfs | 11 | — | — |
| 315/s2/fcfs | 12 | — | — |
| 315/s2/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| 315/s2/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| 315/s2/uncertainty | 2 | a1j0 (4) | a2j0 |
| 315/s2/uncertainty | 3 | a1j0 (4) | a2j0 |
| 315/s2/uncertainty | 4 | — | — |
| 315/s2/uncertainty | 5 | — | — |
| 315/s2/uncertainty | 6 | a1j1 (8) | a0j1, a2j1 |
| 315/s2/uncertainty | 7 | a1j1 (8) | a0j1, a2j1 |
| 315/s2/uncertainty | 8 | a2j1 (10) | a0j1 |
| 315/s2/uncertainty | 9 | a2j1 (10) | a0j1 |
| 315/s2/uncertainty | 10 | — | a0j1 |
| 315/s2/uncertainty | 11 | — | — |
| 315/s2/uncertainty | 12 | — | — |
| 315/s2/myopic | 0 | a2j0 (2) | a0j0, a1j0 |
| 315/s2/myopic | 1 | a2j0 (2) | a0j0, a1j0 |
| 315/s2/myopic | 2 | a1j0 (4) | — |
| 315/s2/myopic | 3 | a1j0 (4) | — |
| 315/s2/myopic | 4 | — | — |
| 315/s2/myopic | 5 | — | — |
| 315/s2/myopic | 6 | a2j1 (8) | a0j1, a1j1 |
| 315/s2/myopic | 7 | a2j1 (8) | a0j1, a1j1 |
| 315/s2/myopic | 8 | a0j1 (10) | — |
| 315/s2/myopic | 9 | a0j1 (10) | — |
| 315/s2/myopic | 10 | — | — |
| 315/s2/myopic | 11 | — | — |
| 315/s2/myopic | 12 | — | — |
| 315/s2/greedy | 0 | a2j0 (2) | a0j0, a1j0 |
| 315/s2/greedy | 1 | a2j0 (2) | a0j0, a1j0 |
| 315/s2/greedy | 2 | a1j0 (4) | — |
| 315/s2/greedy | 3 | a1j0 (4) | — |
| 315/s2/greedy | 4 | — | — |
| 315/s2/greedy | 5 | — | — |
| 315/s2/greedy | 6 | a2j1 (8) | a0j1, a1j1 |
| 315/s2/greedy | 7 | a2j1 (8) | a0j1, a1j1 |
| 315/s2/greedy | 8 | a0j1 (10) | — |
| 315/s2/greedy | 9 | a0j1 (10) | — |
| 315/s2/greedy | 10 | — | — |
| 315/s2/greedy | 11 | — | — |
| 315/s2/greedy | 12 | — | — |
| 315/s2/edf | 0 | a0j0 (2) | a1j0, a2j0 |
| 315/s2/edf | 1 | a0j0 (2) | a1j0, a2j0 |
| 315/s2/edf | 2 | a2j0 (4) | a1j0 |
| 315/s2/edf | 3 | a2j0 (4) | a1j0 |
| 315/s2/edf | 4 | — | a1j0 |
| 315/s2/edf | 5 | — | — |
| 315/s2/edf | 6 | a1j1 (8) | a0j1, a2j1 |
| 315/s2/edf | 7 | a1j1 (8) | a0j1, a2j1 |
| 315/s2/edf | 8 | a2j1 (10) | a0j1 |
| 315/s2/edf | 9 | a2j1 (10) | a0j1 |
| 315/s2/edf | 10 | — | a0j1 |
| 315/s2/edf | 11 | — | — |
| 315/s2/edf | 12 | — | — |
| 315/s2/delay | 0 | a1j0 (2) | a0j0, a2j0 |
| 315/s2/delay | 1 | a1j0 (2) | a0j0, a2j0 |
| 315/s2/delay | 2 | a2j0 (4) | — |
| 315/s2/delay | 3 | a2j0 (4) | — |
| 315/s2/delay | 4 | — | — |
| 315/s2/delay | 5 | — | — |
| 315/s2/delay | 6 | a0j1 (8) | a1j1, a2j1 |
| 315/s2/delay | 7 | a0j1 (8) | a1j1, a2j1 |
| 315/s2/delay | 8 | a2j1 (10) | — |
| 315/s2/delay | 9 | a2j1 (10) | — |
| 315/s2/delay | 10 | — | — |
| 315/s2/delay | 11 | — | — |
| 315/s2/delay | 12 | — | — |
| 315/s1/uncertainty | 0 | a0j0 (1) | a1j0, a2j0 |
| 315/s1/uncertainty | 1 | a1j0 (2) | a2j0 |
| 315/s1/uncertainty | 2 | a2j0 (3) | — |
| 315/s1/uncertainty | 3 | — | — |
| 315/s1/uncertainty | 4 | — | — |
| 315/s1/uncertainty | 5 | — | — |
| 315/s1/uncertainty | 6 | a1j1 (7) | a0j1, a2j1 |
| 315/s1/uncertainty | 7 | a0j1 (8) | a2j1 |
| 315/s1/uncertainty | 8 | a2j1 (9) | — |
| 315/s1/uncertainty | 9 | — | — |
| 315/s1/uncertainty | 10 | — | — |
| 315/s1/uncertainty | 11 | — | — |
| 315/s1/uncertainty | 12 | — | — |
| 315/s1/myopic | 0 | a2j0 (1) | a0j0, a1j0 |
| 315/s1/myopic | 1 | a1j0 (2) | a0j0 |
| 315/s1/myopic | 2 | — | — |
| 315/s1/myopic | 3 | — | — |
| 315/s1/myopic | 4 | — | — |
| 315/s1/myopic | 5 | — | — |
| 315/s1/myopic | 6 | a2j1 (7) | a0j1, a1j1 |
| 315/s1/myopic | 7 | a0j1 (8) | a1j1 |
| 315/s1/myopic | 8 | — | — |
| 315/s1/myopic | 9 | — | — |
| 315/s1/myopic | 10 | — | — |
| 315/s1/myopic | 11 | — | — |
| 315/s1/myopic | 12 | — | — |
| 315/s1/greedy | 0 | a2j0 (1) | a0j0, a1j0 |
| 315/s1/greedy | 1 | a1j0 (2) | a0j0 |
| 315/s1/greedy | 2 | — | — |
| 315/s1/greedy | 3 | — | — |
| 315/s1/greedy | 4 | — | — |
| 315/s1/greedy | 5 | — | — |
| 315/s1/greedy | 6 | a2j1 (7) | a0j1, a1j1 |
| 315/s1/greedy | 7 | a0j1 (8) | a1j1 |
| 315/s1/greedy | 8 | — | — |
| 315/s1/greedy | 9 | — | — |
| 315/s1/greedy | 10 | — | — |
| 315/s1/greedy | 11 | — | — |
| 315/s1/greedy | 12 | — | — |
| 315/s1/edf | 0 | a0j0 (1) | a1j0, a2j0 |
| 315/s1/edf | 1 | a2j0 (2) | a1j0 |
| 315/s1/edf | 2 | a1j0 (3) | — |
| 315/s1/edf | 3 | — | — |
| 315/s1/edf | 4 | — | — |
| 315/s1/edf | 5 | — | — |
| 315/s1/edf | 6 | a1j1 (7) | a0j1, a2j1 |
| 315/s1/edf | 7 | a2j1 (8) | a0j1 |
| 315/s1/edf | 8 | a0j1 (9) | — |
| 315/s1/edf | 9 | — | — |
| 315/s1/edf | 10 | — | — |
| 315/s1/edf | 11 | — | — |
| 315/s1/edf | 12 | — | — |
| 315/s1/delay | 0 | a0j0 (1) | a1j0, a2j0 |
| 315/s1/delay | 1 | a1j0 (2) | a2j0 |
| 315/s1/delay | 2 | a2j0 (3) | — |
| 315/s1/delay | 3 | — | — |
| 315/s1/delay | 4 | — | — |
| 315/s1/delay | 5 | — | — |
| 315/s1/delay | 6 | a0j1 (7) | a1j1, a2j1 |
| 315/s1/delay | 7 | a1j1 (8) | a2j1 |
| 315/s1/delay | 8 | a2j1 (9) | — |
| 315/s1/delay | 9 | — | — |
| 315/s1/delay | 10 | — | — |
| 315/s1/delay | 11 | — | — |
| 315/s1/delay | 12 | — | — |
| 315/s1/fcfs | 0 | a0j0 (1) | a1j0, a2j0 |
| 315/s1/fcfs | 1 | a1j0 (2) | a2j0 |
| 315/s1/fcfs | 2 | a2j0 (3) | — |
| 315/s1/fcfs | 3 | — | — |
| 315/s1/fcfs | 4 | — | — |
| 315/s1/fcfs | 5 | — | — |
| 315/s1/fcfs | 6 | a0j1 (7) | a1j1, a2j1 |
| 315/s1/fcfs | 7 | a1j1 (8) | a2j1 |
| 315/s1/fcfs | 8 | a2j1 (9) | — |
| 315/s1/fcfs | 9 | — | — |
| 315/s1/fcfs | 10 | — | — |
| 315/s1/fcfs | 11 | — | — |
| 315/s1/fcfs | 12 | — | — |
