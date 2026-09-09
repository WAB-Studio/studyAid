# Reading constraints before reading the problem

The constraints block tells you the intended complexity before you understand a single word of the story. Most online judges allow roughly 10^8 simple operations per second-limit. Work backwards from n.

| n up to | Slowest acceptable | What that usually means |
|---|---|---|
| 10-12 | O(n!) | Permutations, brute force everything |
| 20-25 | O(2^n) | Bitmask, subsets, meet in the middle |
| 100 | O(n^4) | Small DP with two nested state loops |
| 500 | O(n^3) | Floyd-Warshall, interval DP |
| 5 000 | O(n^2) | Quadratic DP, all-pairs on small graphs |
| 100 000 | O(n log n) | Sort, heap, binary search on answer, sweep |
| 1 000 000 | O(n) | One or two passes; sliding window, two pointers, hash map |
| 10^9 or more | O(log n) or O(1) | Math, binary search on value space, digit tricks |

How to use it:

1. Read the constraint. Write the ceiling row down.
2. Cross out every pattern in `patterns-cheatsheet.md` that is too slow. Usually 2-3 remain.
3. Only now read the story and pick between the survivors.

Second-order signals:

| You see | Suspect |
|---|---|
| "sorted" anywhere | binary search or two pointers |
| "contiguous", "substring" | sliding window |
| "k-th largest / smallest" | heap or quickselect |
| "number of ways", "minimum cost" | DP |
| "shortest path", unweighted | BFS |
| "connected", "groups", "merge accounts" | union-find or DFS |
| "next greater / smaller" | monotonic stack |
| "prefix", "starts with" | trie |
| values up to 10^9 but n small | coordinate compression, or the value is binary-searchable |
| "at most k changes / picks" | window with a budget, or DP with k as a state |

One habit: when your solution TLEs, do not optimize constants. Come back to this table, find your row, and switch patterns.
