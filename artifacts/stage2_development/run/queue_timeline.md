# Review-queue timeline

Evidence: **live GPU development; see per-episode completion status**.

Snapshots are after completion, closure, arrivals and dispatch; before interval loss.

| Run | Tick | In service (completion tick) | Pending |
| --- | --- | --- | --- |
| calibration/200/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| calibration/200/fcfs | 1 | a0j0 (2) | a1j0 |
| calibration/200/fcfs | 2 | — | — |
| calibration/200/fcfs | 3 | — | — |
| calibration/200/fcfs | 4 | — | — |
| calibration/200/fcfs | 5 | — | — |
| calibration/200/fcfs | 6 | — | a2j1 |
| calibration/200/fcfs | 7 | — | a0j1, a1j1, a2j1 |
| calibration/200/fcfs | 8 | — | a0j1, a1j1 |
| calibration/200/fcfs | 9 | — | — |
| calibration/200/fcfs | 10 | — | — |
| calibration/200/fcfs | 11 | — | — |
| calibration/200/fcfs | 12 | — | — |
| calibration/201/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| calibration/201/fcfs | 1 | a0j0 (2) | a2j0 |
| calibration/201/fcfs | 2 | a2j0 (4) | — |
| calibration/201/fcfs | 3 | a2j0 (4) | — |
| calibration/201/fcfs | 4 | — | — |
| calibration/201/fcfs | 5 | — | — |
| calibration/201/fcfs | 6 | a1j1 (8) | — |
| calibration/201/fcfs | 7 | a1j1 (8) | a0j1, a2j1 |
| calibration/201/fcfs | 8 | — | a0j1, a2j1 |
| calibration/201/fcfs | 9 | — | — |
| calibration/201/fcfs | 10 | — | — |
| calibration/201/fcfs | 11 | — | — |
| calibration/201/fcfs | 12 | — | — |
| calibration/202/fcfs | 0 | a1j0 (2) | a2j0 |
| calibration/202/fcfs | 1 | a1j0 (2) | a0j0, a2j0 |
| calibration/202/fcfs | 2 | a0j0 (4) | — |
| calibration/202/fcfs | 3 | a0j0 (4) | — |
| calibration/202/fcfs | 4 | — | — |
| calibration/202/fcfs | 5 | — | — |
| calibration/202/fcfs | 6 | — | a2j1 |
| calibration/202/fcfs | 7 | a0j1 (9) | a1j1 |
| calibration/202/fcfs | 8 | a0j1 (9) | a1j1 |
| calibration/202/fcfs | 9 | a1j1 (11) | — |
| calibration/202/fcfs | 10 | a1j1 (11) | — |
| calibration/202/fcfs | 11 | — | — |
| calibration/202/fcfs | 12 | — | — |
| calibration/203/fcfs | 0 | a1j0 (2) | a0j0 |
| calibration/203/fcfs | 1 | a1j0 (2) | a2j0 |
| calibration/203/fcfs | 2 | — | a2j0 |
| calibration/203/fcfs | 3 | — | — |
| calibration/203/fcfs | 4 | — | — |
| calibration/203/fcfs | 5 | — | — |
| calibration/203/fcfs | 6 | — | a0j1 |
| calibration/203/fcfs | 7 | a1j1 (9) | a2j1 |
| calibration/203/fcfs | 8 | a1j1 (9) | a2j1 |
| calibration/203/fcfs | 9 | — | — |
| calibration/203/fcfs | 10 | — | — |
| calibration/203/fcfs | 11 | — | — |
| calibration/203/fcfs | 12 | — | — |
| calibration/204/fcfs | 0 | — | — |
| calibration/204/fcfs | 1 | a0j0 (3) | a1j0, a2j0 |
| calibration/204/fcfs | 2 | a0j0 (3) | a2j0 |
| calibration/204/fcfs | 3 | a2j0 (5) | — |
| calibration/204/fcfs | 4 | a2j0 (5) | — |
| calibration/204/fcfs | 5 | — | — |
| calibration/204/fcfs | 6 | a0j1 (8) | — |
| calibration/204/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| calibration/204/fcfs | 8 | a1j1 (10) | a2j1 |
| calibration/204/fcfs | 9 | a1j1 (10) | — |
| calibration/204/fcfs | 10 | — | — |
| calibration/204/fcfs | 11 | — | — |
| calibration/204/fcfs | 12 | — | — |
| calibration/205/fcfs | 0 | — | — |
| calibration/205/fcfs | 1 | a2j0 (3) | a0j0, a1j0 |
| calibration/205/fcfs | 2 | a2j0 (3) | a0j0, a1j0 |
| calibration/205/fcfs | 3 | — | — |
| calibration/205/fcfs | 4 | — | — |
| calibration/205/fcfs | 5 | — | — |
| calibration/205/fcfs | 6 | — | a0j1, a1j1, a2j1 |
| calibration/205/fcfs | 7 | — | a1j1 |
| calibration/205/fcfs | 8 | — | — |
| calibration/205/fcfs | 9 | — | — |
| calibration/205/fcfs | 10 | — | — |
| calibration/205/fcfs | 11 | — | — |
| calibration/205/fcfs | 12 | — | — |
| calibration/206/fcfs | 0 | a1j0 (2) | a0j0 |
| calibration/206/fcfs | 1 | a1j0 (2) | a2j0 |
| calibration/206/fcfs | 2 | a2j0 (4) | — |
| calibration/206/fcfs | 3 | a2j0 (4) | — |
| calibration/206/fcfs | 4 | — | — |
| calibration/206/fcfs | 5 | — | — |
| calibration/206/fcfs | 6 | a0j1 (8) | — |
| calibration/206/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| calibration/206/fcfs | 8 | — | a1j1, a2j1 |
| calibration/206/fcfs | 9 | — | a2j1 |
| calibration/206/fcfs | 10 | — | a2j1 |
| calibration/206/fcfs | 11 | — | a2j1 |
| calibration/206/fcfs | 12 | — | — |
| calibration/207/fcfs | 0 | a2j0 (2) | a0j0, a1j0 |
| calibration/207/fcfs | 1 | a2j0 (2) | — |
| calibration/207/fcfs | 2 | — | — |
| calibration/207/fcfs | 3 | — | — |
| calibration/207/fcfs | 4 | — | — |
| calibration/207/fcfs | 5 | — | — |
| calibration/207/fcfs | 6 | a1j1 (8) | a0j1 |
| calibration/207/fcfs | 7 | a1j1 (8) | a2j1 |
| calibration/207/fcfs | 8 | a2j1 (10) | — |
| calibration/207/fcfs | 9 | a2j1 (10) | — |
| calibration/207/fcfs | 10 | — | — |
| calibration/207/fcfs | 11 | — | — |
| calibration/207/fcfs | 12 | — | — |
| calibration/208/fcfs | 0 | — | a2j0 |
| calibration/208/fcfs | 1 | a0j0 (3) | a1j0, a2j0 |
| calibration/208/fcfs | 2 | a0j0 (3) | a2j0 |
| calibration/208/fcfs | 3 | — | a2j0 |
| calibration/208/fcfs | 4 | — | a2j0 |
| calibration/208/fcfs | 5 | — | — |
| calibration/208/fcfs | 6 | — | — |
| calibration/208/fcfs | 7 | — | a0j1, a1j1, a2j1 |
| calibration/208/fcfs | 8 | — | a1j1 |
| calibration/208/fcfs | 9 | — | — |
| calibration/208/fcfs | 10 | — | — |
| calibration/208/fcfs | 11 | — | — |
| calibration/208/fcfs | 12 | — | — |
| calibration/209/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| calibration/209/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| calibration/209/fcfs | 2 | a2j0 (4) | — |
| calibration/209/fcfs | 3 | a2j0 (4) | — |
| calibration/209/fcfs | 4 | — | — |
| calibration/209/fcfs | 5 | — | — |
| calibration/209/fcfs | 6 | a1j1 (8) | a0j1, a2j1 |
| calibration/209/fcfs | 7 | a1j1 (8) | a0j1 |
| calibration/209/fcfs | 8 | — | — |
| calibration/209/fcfs | 9 | — | — |
| calibration/209/fcfs | 10 | — | — |
| calibration/209/fcfs | 11 | — | — |
| calibration/209/fcfs | 12 | — | — |
| calibration/210/fcfs | 0 | — | a1j0 |
| calibration/210/fcfs | 1 | — | a0j0, a2j0 |
| calibration/210/fcfs | 2 | — | a0j0, a2j0 |
| calibration/210/fcfs | 3 | — | — |
| calibration/210/fcfs | 4 | — | — |
| calibration/210/fcfs | 5 | — | — |
| calibration/210/fcfs | 6 | a2j1 (8) | a1j1 |
| calibration/210/fcfs | 7 | a2j1 (8) | a0j1 |
| calibration/210/fcfs | 8 | a0j1 (10) | — |
| calibration/210/fcfs | 9 | a0j1 (10) | — |
| calibration/210/fcfs | 10 | — | — |
| calibration/210/fcfs | 11 | — | — |
| calibration/210/fcfs | 12 | — | — |
| calibration/211/fcfs | 0 | a2j0 (2) | — |
| calibration/211/fcfs | 1 | a2j0 (2) | a0j0, a1j0 |
| calibration/211/fcfs | 2 | a0j0 (4) | — |
| calibration/211/fcfs | 3 | a0j0 (4) | — |
| calibration/211/fcfs | 4 | — | — |
| calibration/211/fcfs | 5 | — | — |
| calibration/211/fcfs | 6 | a0j1 (8) | a1j1, a2j1 |
| calibration/211/fcfs | 7 | a0j1 (8) | a2j1 |
| calibration/211/fcfs | 8 | a2j1 (10) | — |
| calibration/211/fcfs | 9 | a2j1 (10) | — |
| calibration/211/fcfs | 10 | — | — |
| calibration/211/fcfs | 11 | — | — |
| calibration/211/fcfs | 12 | — | — |
| calibration/212/fcfs | 0 | — | a1j0 |
| calibration/212/fcfs | 1 | — | a0j0, a2j0 |
| calibration/212/fcfs | 2 | — | a0j0 |
| calibration/212/fcfs | 3 | — | a0j0 |
| calibration/212/fcfs | 4 | — | a0j0 |
| calibration/212/fcfs | 5 | — | a0j0 |
| calibration/212/fcfs | 6 | a0j1 (8) | a2j1 |
| calibration/212/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| calibration/212/fcfs | 8 | a2j1 (10) | a1j1 |
| calibration/212/fcfs | 9 | a2j1 (10) | — |
| calibration/212/fcfs | 10 | — | — |
| calibration/212/fcfs | 11 | — | — |
| calibration/212/fcfs | 12 | — | — |
| calibration/213/fcfs | 0 | a0j0 (2) | — |
| calibration/213/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| calibration/213/fcfs | 2 | a1j0 (4) | — |
| calibration/213/fcfs | 3 | a1j0 (4) | — |
| calibration/213/fcfs | 4 | — | — |
| calibration/213/fcfs | 5 | — | — |
| calibration/213/fcfs | 6 | a0j1 (8) | — |
| calibration/213/fcfs | 7 | a0j1 (8) | a1j1, a2j1 |
| calibration/213/fcfs | 8 | a1j1 (10) | a2j1 |
| calibration/213/fcfs | 9 | a1j1 (10) | a2j1 |
| calibration/213/fcfs | 10 | a2j1 (12) | — |
| calibration/213/fcfs | 11 | a2j1 (12) | — |
| calibration/213/fcfs | 12 | — | — |
| calibration/214/fcfs | 0 | — | — |
| calibration/214/fcfs | 1 | a0j0 (3) | a1j0, a2j0 |
| calibration/214/fcfs | 2 | a0j0 (3) | a1j0 |
| calibration/214/fcfs | 3 | a1j0 (5) | — |
| calibration/214/fcfs | 4 | a1j0 (5) | — |
| calibration/214/fcfs | 5 | — | — |
| calibration/214/fcfs | 6 | — | a0j1, a1j1 |
| calibration/214/fcfs | 7 | a2j1 (9) | a1j1 |
| calibration/214/fcfs | 8 | a2j1 (9) | — |
| calibration/214/fcfs | 9 | — | — |
| calibration/214/fcfs | 10 | — | — |
| calibration/214/fcfs | 11 | — | — |
| calibration/214/fcfs | 12 | — | — |
| calibration/215/fcfs | 0 | — | a0j0 |
| calibration/215/fcfs | 1 | — | a1j0, a2j0 |
| calibration/215/fcfs | 2 | — | a1j0 |
| calibration/215/fcfs | 3 | — | — |
| calibration/215/fcfs | 4 | — | — |
| calibration/215/fcfs | 5 | — | — |
| calibration/215/fcfs | 6 | — | a2j1 |
| calibration/215/fcfs | 7 | a0j1 (9) | a1j1 |
| calibration/215/fcfs | 8 | a0j1 (9) | a1j1 |
| calibration/215/fcfs | 9 | — | — |
| calibration/215/fcfs | 10 | — | — |
| calibration/215/fcfs | 11 | — | — |
| calibration/215/fcfs | 12 | — | — |
| validation/216/fcfs | 0 | a2j0 (2) | a0j0 |
| validation/216/fcfs | 1 | a2j0 (2) | a0j0, a1j0 |
| validation/216/fcfs | 2 | — | a1j0 |
| validation/216/fcfs | 3 | — | — |
| validation/216/fcfs | 4 | — | — |
| validation/216/fcfs | 5 | — | — |
| validation/216/fcfs | 6 | a1j1 (8) | — |
| validation/216/fcfs | 7 | a1j1 (8) | a0j1, a2j1 |
| validation/216/fcfs | 8 | — | a2j1 |
| validation/216/fcfs | 9 | — | — |
| validation/216/fcfs | 10 | — | — |
| validation/216/fcfs | 11 | — | — |
| validation/216/fcfs | 12 | — | — |
| validation/216/uncertainty | 0 | a2j0 (2) | a0j0 |
| validation/216/uncertainty | 1 | a2j0 (2) | a0j0, a1j0 |
| validation/216/uncertainty | 2 | — | a1j0 |
| validation/216/uncertainty | 3 | — | — |
| validation/216/uncertainty | 4 | — | — |
| validation/216/uncertainty | 5 | — | — |
| validation/216/uncertainty | 6 | a1j1 (8) | — |
| validation/216/uncertainty | 7 | a1j1 (8) | a0j1, a2j1 |
| validation/216/uncertainty | 8 | — | a2j1 |
| validation/216/uncertainty | 9 | — | — |
| validation/216/uncertainty | 10 | — | — |
| validation/216/uncertainty | 11 | — | — |
| validation/216/uncertainty | 12 | — | — |
| validation/216/myopic | 0 | a2j0 (2) | a0j0 |
| validation/216/myopic | 1 | a2j0 (2) | a0j0, a1j0 |
| validation/216/myopic | 2 | — | a1j0 |
| validation/216/myopic | 3 | — | — |
| validation/216/myopic | 4 | — | — |
| validation/216/myopic | 5 | — | — |
| validation/216/myopic | 6 | a1j1 (8) | — |
| validation/216/myopic | 7 | a1j1 (8) | a0j1, a2j1 |
| validation/216/myopic | 8 | — | a2j1 |
| validation/216/myopic | 9 | — | — |
| validation/216/myopic | 10 | — | — |
| validation/216/myopic | 11 | — | — |
| validation/216/myopic | 12 | — | — |
| validation/216/greedy | 0 | a2j0 (2) | a0j0 |
| validation/216/greedy | 1 | a2j0 (2) | a0j0, a1j0 |
| validation/216/greedy | 2 | — | a1j0 |
| validation/216/greedy | 3 | — | — |
| validation/216/greedy | 4 | — | — |
| validation/216/greedy | 5 | — | — |
| validation/216/greedy | 6 | a1j1 (8) | — |
| validation/216/greedy | 7 | a1j1 (8) | a0j1, a2j1 |
| validation/216/greedy | 8 | — | a2j1 |
| validation/216/greedy | 9 | — | — |
| validation/216/greedy | 10 | — | — |
| validation/216/greedy | 11 | — | — |
| validation/216/greedy | 12 | — | — |
| validation/216/delay | 0 | a2j0 (2) | a0j0 |
| validation/216/delay | 1 | a2j0 (2) | a0j0, a1j0 |
| validation/216/delay | 2 | — | a1j0 |
| validation/216/delay | 3 | — | — |
| validation/216/delay | 4 | — | — |
| validation/216/delay | 5 | — | — |
| validation/216/delay | 6 | a1j1 (8) | — |
| validation/216/delay | 7 | a1j1 (8) | a0j1, a2j1 |
| validation/216/delay | 8 | — | a2j1 |
| validation/216/delay | 9 | — | — |
| validation/216/delay | 10 | — | — |
| validation/216/delay | 11 | — | — |
| validation/216/delay | 12 | — | — |
| validation/217/uncertainty | 0 | — | a1j0 |
| validation/217/uncertainty | 1 | — | a0j0, a2j0 |
| validation/217/uncertainty | 2 | — | a2j0 |
| validation/217/uncertainty | 3 | — | — |
| validation/217/uncertainty | 4 | — | — |
| validation/217/uncertainty | 5 | — | — |
| validation/217/uncertainty | 6 | — | a1j1 |
| validation/217/uncertainty | 7 | a0j1 (9) | a2j1 |
| validation/217/uncertainty | 8 | a0j1 (9) | a2j1 |
| validation/217/uncertainty | 9 | — | — |
| validation/217/uncertainty | 10 | — | — |
| validation/217/uncertainty | 11 | — | — |
| validation/217/uncertainty | 12 | — | — |
| validation/217/myopic | 0 | — | a1j0 |
| validation/217/myopic | 1 | — | a0j0, a2j0 |
| validation/217/myopic | 2 | — | a2j0 |
| validation/217/myopic | 3 | — | — |
| validation/217/myopic | 4 | — | — |
| validation/217/myopic | 5 | — | — |
| validation/217/myopic | 6 | — | a1j1 |
| validation/217/myopic | 7 | a0j1 (9) | a2j1 |
| validation/217/myopic | 8 | a0j1 (9) | a2j1 |
| validation/217/myopic | 9 | — | — |
| validation/217/myopic | 10 | — | — |
| validation/217/myopic | 11 | — | — |
| validation/217/myopic | 12 | — | — |
| validation/217/greedy | 0 | — | a1j0 |
| validation/217/greedy | 1 | — | a0j0, a2j0 |
| validation/217/greedy | 2 | — | a2j0 |
| validation/217/greedy | 3 | — | — |
| validation/217/greedy | 4 | — | — |
| validation/217/greedy | 5 | — | — |
| validation/217/greedy | 6 | — | a1j1 |
| validation/217/greedy | 7 | a0j1 (9) | a2j1 |
| validation/217/greedy | 8 | a0j1 (9) | a2j1 |
| validation/217/greedy | 9 | — | — |
| validation/217/greedy | 10 | — | — |
| validation/217/greedy | 11 | — | — |
| validation/217/greedy | 12 | — | — |
| validation/217/delay | 0 | — | a1j0 |
| validation/217/delay | 1 | — | a0j0, a2j0 |
| validation/217/delay | 2 | — | a2j0 |
| validation/217/delay | 3 | — | — |
| validation/217/delay | 4 | — | — |
| validation/217/delay | 5 | — | — |
| validation/217/delay | 6 | — | a1j1 |
| validation/217/delay | 7 | a0j1 (9) | a2j1 |
| validation/217/delay | 8 | a0j1 (9) | a2j1 |
| validation/217/delay | 9 | — | — |
| validation/217/delay | 10 | — | — |
| validation/217/delay | 11 | — | — |
| validation/217/delay | 12 | — | — |
| validation/217/fcfs | 0 | — | a1j0 |
| validation/217/fcfs | 1 | — | a0j0, a2j0 |
| validation/217/fcfs | 2 | — | a2j0 |
| validation/217/fcfs | 3 | — | — |
| validation/217/fcfs | 4 | — | — |
| validation/217/fcfs | 5 | — | — |
| validation/217/fcfs | 6 | — | a1j1 |
| validation/217/fcfs | 7 | a0j1 (9) | a2j1 |
| validation/217/fcfs | 8 | a0j1 (9) | a2j1 |
| validation/217/fcfs | 9 | — | — |
| validation/217/fcfs | 10 | — | — |
| validation/217/fcfs | 11 | — | — |
| validation/217/fcfs | 12 | — | — |
| validation/218/myopic | 0 | — | — |
| validation/218/myopic | 1 | — | a0j0, a1j0, a2j0 |
| validation/218/myopic | 2 | — | a0j0, a1j0 |
| validation/218/myopic | 3 | — | — |
| validation/218/myopic | 4 | — | — |
| validation/218/myopic | 5 | — | — |
| validation/218/myopic | 6 | a1j1 (8) | a0j1, a2j1 |
| validation/218/myopic | 7 | a1j1 (8) | a0j1 |
| validation/218/myopic | 8 | — | a0j1 |
| validation/218/myopic | 9 | — | a0j1 |
| validation/218/myopic | 10 | — | a0j1 |
| validation/218/myopic | 11 | — | — |
| validation/218/myopic | 12 | — | — |
| validation/218/greedy | 0 | — | — |
| validation/218/greedy | 1 | — | a0j0, a1j0, a2j0 |
| validation/218/greedy | 2 | — | a0j0, a1j0 |
| validation/218/greedy | 3 | — | — |
| validation/218/greedy | 4 | — | — |
| validation/218/greedy | 5 | — | — |
| validation/218/greedy | 6 | a1j1 (8) | a0j1, a2j1 |
| validation/218/greedy | 7 | a1j1 (8) | a0j1 |
| validation/218/greedy | 8 | — | a0j1 |
| validation/218/greedy | 9 | — | a0j1 |
| validation/218/greedy | 10 | — | a0j1 |
| validation/218/greedy | 11 | — | — |
| validation/218/greedy | 12 | — | — |
| validation/218/delay | 0 | — | — |
| validation/218/delay | 1 | — | a0j0, a1j0, a2j0 |
| validation/218/delay | 2 | — | a0j0, a1j0 |
| validation/218/delay | 3 | — | — |
| validation/218/delay | 4 | — | — |
| validation/218/delay | 5 | — | — |
| validation/218/delay | 6 | a1j1 (8) | a0j1, a2j1 |
| validation/218/delay | 7 | a1j1 (8) | a0j1 |
| validation/218/delay | 8 | — | a0j1 |
| validation/218/delay | 9 | — | a0j1 |
| validation/218/delay | 10 | — | a0j1 |
| validation/218/delay | 11 | — | — |
| validation/218/delay | 12 | — | — |
| validation/218/fcfs | 0 | — | — |
| validation/218/fcfs | 1 | — | a0j0, a1j0, a2j0 |
| validation/218/fcfs | 2 | — | a0j0, a1j0 |
| validation/218/fcfs | 3 | — | — |
| validation/218/fcfs | 4 | — | — |
| validation/218/fcfs | 5 | — | — |
| validation/218/fcfs | 6 | a1j1 (8) | a0j1, a2j1 |
| validation/218/fcfs | 7 | a1j1 (8) | a0j1 |
| validation/218/fcfs | 8 | — | a0j1 |
| validation/218/fcfs | 9 | — | a0j1 |
| validation/218/fcfs | 10 | — | a0j1 |
| validation/218/fcfs | 11 | — | — |
| validation/218/fcfs | 12 | — | — |
| validation/218/uncertainty | 0 | — | — |
| validation/218/uncertainty | 1 | — | a0j0, a1j0, a2j0 |
| validation/218/uncertainty | 2 | — | a0j0, a1j0 |
| validation/218/uncertainty | 3 | — | — |
| validation/218/uncertainty | 4 | — | — |
| validation/218/uncertainty | 5 | — | — |
| validation/218/uncertainty | 6 | a1j1 (8) | a0j1, a2j1 |
| validation/218/uncertainty | 7 | a1j1 (8) | a0j1 |
| validation/218/uncertainty | 8 | — | a0j1 |
| validation/218/uncertainty | 9 | — | a0j1 |
| validation/218/uncertainty | 10 | — | a0j1 |
| validation/218/uncertainty | 11 | — | — |
| validation/218/uncertainty | 12 | — | — |
| validation/219/greedy | 0 | — | a1j0 |
| validation/219/greedy | 1 | a0j0 (3) | a1j0, a2j0 |
| validation/219/greedy | 2 | a0j0 (3) | a2j0 |
| validation/219/greedy | 3 | — | — |
| validation/219/greedy | 4 | — | — |
| validation/219/greedy | 5 | — | — |
| validation/219/greedy | 6 | a1j1 (8) | a2j1 |
| validation/219/greedy | 7 | a1j1 (8) | a0j1, a2j1 |
| validation/219/greedy | 8 | — | a0j1 |
| validation/219/greedy | 9 | — | — |
| validation/219/greedy | 10 | — | — |
| validation/219/greedy | 11 | — | — |
| validation/219/greedy | 12 | — | — |
| validation/219/delay | 0 | — | a1j0 |
| validation/219/delay | 1 | a0j0 (3) | a1j0, a2j0 |
| validation/219/delay | 2 | a0j0 (3) | a2j0 |
| validation/219/delay | 3 | — | — |
| validation/219/delay | 4 | — | — |
| validation/219/delay | 5 | — | — |
| validation/219/delay | 6 | a1j1 (8) | a2j1 |
| validation/219/delay | 7 | a1j1 (8) | a0j1, a2j1 |
| validation/219/delay | 8 | — | a0j1 |
| validation/219/delay | 9 | — | — |
| validation/219/delay | 10 | — | — |
| validation/219/delay | 11 | — | — |
| validation/219/delay | 12 | — | — |
| validation/219/fcfs | 0 | — | a1j0 |
| validation/219/fcfs | 1 | a0j0 (3) | a1j0, a2j0 |
| validation/219/fcfs | 2 | a0j0 (3) | a2j0 |
| validation/219/fcfs | 3 | — | — |
| validation/219/fcfs | 4 | — | — |
| validation/219/fcfs | 5 | — | — |
| validation/219/fcfs | 6 | a1j1 (8) | a2j1 |
| validation/219/fcfs | 7 | a1j1 (8) | a0j1, a2j1 |
| validation/219/fcfs | 8 | — | a0j1 |
| validation/219/fcfs | 9 | — | — |
| validation/219/fcfs | 10 | — | — |
| validation/219/fcfs | 11 | — | — |
| validation/219/fcfs | 12 | — | — |
| validation/219/uncertainty | 0 | — | a1j0 |
| validation/219/uncertainty | 1 | a0j0 (3) | a1j0, a2j0 |
| validation/219/uncertainty | 2 | a0j0 (3) | a2j0 |
| validation/219/uncertainty | 3 | — | — |
| validation/219/uncertainty | 4 | — | — |
| validation/219/uncertainty | 5 | — | — |
| validation/219/uncertainty | 6 | a1j1 (8) | a2j1 |
| validation/219/uncertainty | 7 | a1j1 (8) | a0j1, a2j1 |
| validation/219/uncertainty | 8 | — | a0j1 |
| validation/219/uncertainty | 9 | — | — |
| validation/219/uncertainty | 10 | — | — |
| validation/219/uncertainty | 11 | — | — |
| validation/219/uncertainty | 12 | — | — |
| validation/219/myopic | 0 | — | a1j0 |
| validation/219/myopic | 1 | a2j0 (3) | a0j0, a1j0 |
| validation/219/myopic | 2 | a2j0 (3) | a0j0 |
| validation/219/myopic | 3 | — | — |
| validation/219/myopic | 4 | — | — |
| validation/219/myopic | 5 | — | — |
| validation/219/myopic | 6 | a1j1 (8) | a2j1 |
| validation/219/myopic | 7 | a1j1 (8) | a0j1, a2j1 |
| validation/219/myopic | 8 | — | a0j1 |
| validation/219/myopic | 9 | — | — |
| validation/219/myopic | 10 | — | — |
| validation/219/myopic | 11 | — | — |
| validation/219/myopic | 12 | — | — |
| validation/220/delay | 0 | a1j0 (2) | a0j0 |
| validation/220/delay | 1 | a1j0 (2) | a0j0, a2j0 |
| validation/220/delay | 2 | a2j0 (4) | — |
| validation/220/delay | 3 | a2j0 (4) | — |
| validation/220/delay | 4 | — | — |
| validation/220/delay | 5 | — | — |
| validation/220/delay | 6 | — | a1j1, a2j1 |
| validation/220/delay | 7 | — | a0j1 |
| validation/220/delay | 8 | — | a0j1 |
| validation/220/delay | 9 | — | — |
| validation/220/delay | 10 | — | — |
| validation/220/delay | 11 | — | — |
| validation/220/delay | 12 | — | — |
| validation/220/fcfs | 0 | a1j0 (2) | a0j0 |
| validation/220/fcfs | 1 | a1j0 (2) | a0j0, a2j0 |
| validation/220/fcfs | 2 | a2j0 (4) | — |
| validation/220/fcfs | 3 | a2j0 (4) | — |
| validation/220/fcfs | 4 | — | — |
| validation/220/fcfs | 5 | — | — |
| validation/220/fcfs | 6 | — | a1j1, a2j1 |
| validation/220/fcfs | 7 | — | a0j1 |
| validation/220/fcfs | 8 | — | a0j1 |
| validation/220/fcfs | 9 | — | — |
| validation/220/fcfs | 10 | — | — |
| validation/220/fcfs | 11 | — | — |
| validation/220/fcfs | 12 | — | — |
| validation/220/uncertainty | 0 | a1j0 (2) | a0j0 |
| validation/220/uncertainty | 1 | a1j0 (2) | a0j0, a2j0 |
| validation/220/uncertainty | 2 | a2j0 (4) | — |
| validation/220/uncertainty | 3 | a2j0 (4) | — |
| validation/220/uncertainty | 4 | — | — |
| validation/220/uncertainty | 5 | — | — |
| validation/220/uncertainty | 6 | — | a1j1, a2j1 |
| validation/220/uncertainty | 7 | — | a0j1 |
| validation/220/uncertainty | 8 | — | a0j1 |
| validation/220/uncertainty | 9 | — | — |
| validation/220/uncertainty | 10 | — | — |
| validation/220/uncertainty | 11 | — | — |
| validation/220/uncertainty | 12 | — | — |
| validation/220/myopic | 0 | a1j0 (2) | a0j0 |
| validation/220/myopic | 1 | a1j0 (2) | a0j0, a2j0 |
| validation/220/myopic | 2 | a2j0 (4) | — |
| validation/220/myopic | 3 | a2j0 (4) | — |
| validation/220/myopic | 4 | — | — |
| validation/220/myopic | 5 | — | — |
| validation/220/myopic | 6 | — | a1j1, a2j1 |
| validation/220/myopic | 7 | — | a0j1 |
| validation/220/myopic | 8 | — | a0j1 |
| validation/220/myopic | 9 | — | — |
| validation/220/myopic | 10 | — | — |
| validation/220/myopic | 11 | — | — |
| validation/220/myopic | 12 | — | — |
| validation/220/greedy | 0 | a1j0 (2) | a0j0 |
| validation/220/greedy | 1 | a1j0 (2) | a0j0, a2j0 |
| validation/220/greedy | 2 | a2j0 (4) | — |
| validation/220/greedy | 3 | a2j0 (4) | — |
| validation/220/greedy | 4 | — | — |
| validation/220/greedy | 5 | — | — |
| validation/220/greedy | 6 | — | a1j1, a2j1 |
| validation/220/greedy | 7 | — | a0j1 |
| validation/220/greedy | 8 | — | a0j1 |
| validation/220/greedy | 9 | — | — |
| validation/220/greedy | 10 | — | — |
| validation/220/greedy | 11 | — | — |
| validation/220/greedy | 12 | — | — |
| validation/221/fcfs | 0 | — | a0j0 |
| validation/221/fcfs | 1 | a2j0 (3) | a1j0 |
| validation/221/fcfs | 2 | a2j0 (3) | — |
| validation/221/fcfs | 3 | — | — |
| validation/221/fcfs | 4 | — | — |
| validation/221/fcfs | 5 | — | — |
| validation/221/fcfs | 6 | a2j1 (8) | a0j1 |
| validation/221/fcfs | 7 | a2j1 (8) | a0j1, a1j1 |
| validation/221/fcfs | 8 | a1j1 (10) | — |
| validation/221/fcfs | 9 | a1j1 (10) | — |
| validation/221/fcfs | 10 | — | — |
| validation/221/fcfs | 11 | — | — |
| validation/221/fcfs | 12 | — | — |
| validation/221/uncertainty | 0 | — | a0j0 |
| validation/221/uncertainty | 1 | a2j0 (3) | a1j0 |
| validation/221/uncertainty | 2 | a2j0 (3) | — |
| validation/221/uncertainty | 3 | — | — |
| validation/221/uncertainty | 4 | — | — |
| validation/221/uncertainty | 5 | — | — |
| validation/221/uncertainty | 6 | a2j1 (8) | a0j1 |
| validation/221/uncertainty | 7 | a2j1 (8) | a0j1, a1j1 |
| validation/221/uncertainty | 8 | a1j1 (10) | — |
| validation/221/uncertainty | 9 | a1j1 (10) | — |
| validation/221/uncertainty | 10 | — | — |
| validation/221/uncertainty | 11 | — | — |
| validation/221/uncertainty | 12 | — | — |
| validation/221/myopic | 0 | — | a0j0 |
| validation/221/myopic | 1 | a2j0 (3) | a1j0 |
| validation/221/myopic | 2 | a2j0 (3) | — |
| validation/221/myopic | 3 | — | — |
| validation/221/myopic | 4 | — | — |
| validation/221/myopic | 5 | — | — |
| validation/221/myopic | 6 | a2j1 (8) | a0j1 |
| validation/221/myopic | 7 | a2j1 (8) | a0j1, a1j1 |
| validation/221/myopic | 8 | a1j1 (10) | — |
| validation/221/myopic | 9 | a1j1 (10) | — |
| validation/221/myopic | 10 | — | — |
| validation/221/myopic | 11 | — | — |
| validation/221/myopic | 12 | — | — |
| validation/221/greedy | 0 | — | a0j0 |
| validation/221/greedy | 1 | a2j0 (3) | a1j0 |
| validation/221/greedy | 2 | a2j0 (3) | — |
| validation/221/greedy | 3 | — | — |
| validation/221/greedy | 4 | — | — |
| validation/221/greedy | 5 | — | — |
| validation/221/greedy | 6 | a2j1 (8) | a0j1 |
| validation/221/greedy | 7 | a2j1 (8) | a0j1, a1j1 |
| validation/221/greedy | 8 | a1j1 (10) | — |
| validation/221/greedy | 9 | a1j1 (10) | — |
| validation/221/greedy | 10 | — | — |
| validation/221/greedy | 11 | — | — |
| validation/221/greedy | 12 | — | — |
| validation/221/delay | 0 | — | a0j0 |
| validation/221/delay | 1 | a2j0 (3) | a1j0 |
| validation/221/delay | 2 | a2j0 (3) | — |
| validation/221/delay | 3 | — | — |
| validation/221/delay | 4 | — | — |
| validation/221/delay | 5 | — | — |
| validation/221/delay | 6 | a2j1 (8) | a0j1 |
| validation/221/delay | 7 | a2j1 (8) | a0j1, a1j1 |
| validation/221/delay | 8 | a1j1 (10) | — |
| validation/221/delay | 9 | a1j1 (10) | — |
| validation/221/delay | 10 | — | — |
| validation/221/delay | 11 | — | — |
| validation/221/delay | 12 | — | — |
| validation/222/uncertainty | 0 | a0j0 (2) | a1j0, a2j0 |
| validation/222/uncertainty | 1 | a0j0 (2) | a1j0, a2j0 |
| validation/222/uncertainty | 2 | — | a2j0 |
| validation/222/uncertainty | 3 | — | a2j0 |
| validation/222/uncertainty | 4 | — | a2j0 |
| validation/222/uncertainty | 5 | — | — |
| validation/222/uncertainty | 6 | — | a1j1 |
| validation/222/uncertainty | 7 | a0j1 (9) | a2j1 |
| validation/222/uncertainty | 8 | a0j1 (9) | a2j1 |
| validation/222/uncertainty | 9 | a2j1 (11) | — |
| validation/222/uncertainty | 10 | a2j1 (11) | — |
| validation/222/uncertainty | 11 | — | — |
| validation/222/uncertainty | 12 | — | — |
| validation/222/myopic | 0 | a0j0 (2) | a1j0, a2j0 |
| validation/222/myopic | 1 | a0j0 (2) | a1j0, a2j0 |
| validation/222/myopic | 2 | — | a2j0 |
| validation/222/myopic | 3 | — | a2j0 |
| validation/222/myopic | 4 | — | a2j0 |
| validation/222/myopic | 5 | — | — |
| validation/222/myopic | 6 | — | a1j1 |
| validation/222/myopic | 7 | a0j1 (9) | a2j1 |
| validation/222/myopic | 8 | a0j1 (9) | a2j1 |
| validation/222/myopic | 9 | a2j1 (11) | — |
| validation/222/myopic | 10 | a2j1 (11) | — |
| validation/222/myopic | 11 | — | — |
| validation/222/myopic | 12 | — | — |
| validation/222/greedy | 0 | a0j0 (2) | a1j0, a2j0 |
| validation/222/greedy | 1 | a0j0 (2) | a1j0, a2j0 |
| validation/222/greedy | 2 | — | a2j0 |
| validation/222/greedy | 3 | — | a2j0 |
| validation/222/greedy | 4 | — | a2j0 |
| validation/222/greedy | 5 | — | — |
| validation/222/greedy | 6 | — | a1j1 |
| validation/222/greedy | 7 | a0j1 (9) | a2j1 |
| validation/222/greedy | 8 | a0j1 (9) | a2j1 |
| validation/222/greedy | 9 | a2j1 (11) | — |
| validation/222/greedy | 10 | a2j1 (11) | — |
| validation/222/greedy | 11 | — | — |
| validation/222/greedy | 12 | — | — |
| validation/222/delay | 0 | a0j0 (2) | a1j0, a2j0 |
| validation/222/delay | 1 | a0j0 (2) | a1j0, a2j0 |
| validation/222/delay | 2 | — | a2j0 |
| validation/222/delay | 3 | — | a2j0 |
| validation/222/delay | 4 | — | a2j0 |
| validation/222/delay | 5 | — | — |
| validation/222/delay | 6 | — | a1j1 |
| validation/222/delay | 7 | a0j1 (9) | a2j1 |
| validation/222/delay | 8 | a0j1 (9) | a2j1 |
| validation/222/delay | 9 | a2j1 (11) | — |
| validation/222/delay | 10 | a2j1 (11) | — |
| validation/222/delay | 11 | — | — |
| validation/222/delay | 12 | — | — |
| validation/222/fcfs | 0 | a0j0 (2) | a1j0, a2j0 |
| validation/222/fcfs | 1 | a0j0 (2) | a1j0, a2j0 |
| validation/222/fcfs | 2 | — | a2j0 |
| validation/222/fcfs | 3 | — | a2j0 |
| validation/222/fcfs | 4 | — | a2j0 |
| validation/222/fcfs | 5 | — | — |
| validation/222/fcfs | 6 | — | a1j1 |
| validation/222/fcfs | 7 | a0j1 (9) | a2j1 |
| validation/222/fcfs | 8 | a0j1 (9) | a2j1 |
| validation/222/fcfs | 9 | a2j1 (11) | — |
| validation/222/fcfs | 10 | a2j1 (11) | — |
| validation/222/fcfs | 11 | — | — |
| validation/222/fcfs | 12 | — | — |
| validation/223/myopic | 0 | — | a2j0 |
| validation/223/myopic | 1 | a0j0 (3) | a1j0, a2j0 |
| validation/223/myopic | 2 | a0j0 (3) | a1j0 |
| validation/223/myopic | 3 | a1j0 (5) | — |
| validation/223/myopic | 4 | a1j0 (5) | — |
| validation/223/myopic | 5 | — | — |
| validation/223/myopic | 6 | — | a0j1 |
| validation/223/myopic | 7 | a2j1 (9) | a1j1 |
| validation/223/myopic | 8 | a2j1 (9) | a1j1 |
| validation/223/myopic | 9 | a1j1 (11) | — |
| validation/223/myopic | 10 | a1j1 (11) | — |
| validation/223/myopic | 11 | — | — |
| validation/223/myopic | 12 | — | — |
| validation/223/greedy | 0 | — | a2j0 |
| validation/223/greedy | 1 | a0j0 (3) | a1j0, a2j0 |
| validation/223/greedy | 2 | a0j0 (3) | a1j0 |
| validation/223/greedy | 3 | a1j0 (5) | — |
| validation/223/greedy | 4 | a1j0 (5) | — |
| validation/223/greedy | 5 | — | — |
| validation/223/greedy | 6 | — | a0j1 |
| validation/223/greedy | 7 | a2j1 (9) | a1j1 |
| validation/223/greedy | 8 | a2j1 (9) | a1j1 |
| validation/223/greedy | 9 | a1j1 (11) | — |
| validation/223/greedy | 10 | a1j1 (11) | — |
| validation/223/greedy | 11 | — | — |
| validation/223/greedy | 12 | — | — |
| validation/223/delay | 0 | — | a2j0 |
| validation/223/delay | 1 | a0j0 (3) | a1j0, a2j0 |
| validation/223/delay | 2 | a0j0 (3) | a1j0 |
| validation/223/delay | 3 | a1j0 (5) | — |
| validation/223/delay | 4 | a1j0 (5) | — |
| validation/223/delay | 5 | — | — |
| validation/223/delay | 6 | — | a0j1 |
| validation/223/delay | 7 | a2j1 (9) | a1j1 |
| validation/223/delay | 8 | a2j1 (9) | a1j1 |
| validation/223/delay | 9 | a1j1 (11) | — |
| validation/223/delay | 10 | a1j1 (11) | — |
| validation/223/delay | 11 | — | — |
| validation/223/delay | 12 | — | — |
| validation/223/fcfs | 0 | — | a2j0 |
| validation/223/fcfs | 1 | a0j0 (3) | a1j0, a2j0 |
| validation/223/fcfs | 2 | a0j0 (3) | a1j0 |
| validation/223/fcfs | 3 | a1j0 (5) | — |
| validation/223/fcfs | 4 | a1j0 (5) | — |
| validation/223/fcfs | 5 | — | — |
| validation/223/fcfs | 6 | — | a0j1 |
| validation/223/fcfs | 7 | a1j1 (9) | a2j1 |
| validation/223/fcfs | 8 | a1j1 (9) | a2j1 |
| validation/223/fcfs | 9 | a2j1 (11) | — |
| validation/223/fcfs | 10 | a2j1 (11) | — |
| validation/223/fcfs | 11 | — | — |
| validation/223/fcfs | 12 | — | — |
| validation/223/uncertainty | 0 | — | a2j0 |
| validation/223/uncertainty | 1 | a0j0 (3) | a1j0, a2j0 |
| validation/223/uncertainty | 2 | a0j0 (3) | a1j0 |
| validation/223/uncertainty | 3 | a1j0 (5) | — |
| validation/223/uncertainty | 4 | a1j0 (5) | — |
| validation/223/uncertainty | 5 | — | — |
| validation/223/uncertainty | 6 | — | a0j1 |
| validation/223/uncertainty | 7 | a1j1 (9) | a2j1 |
| validation/223/uncertainty | 8 | a1j1 (9) | a2j1 |
| validation/223/uncertainty | 9 | a2j1 (11) | — |
| validation/223/uncertainty | 10 | a2j1 (11) | — |
| validation/223/uncertainty | 11 | — | — |
| validation/223/uncertainty | 12 | — | — |
