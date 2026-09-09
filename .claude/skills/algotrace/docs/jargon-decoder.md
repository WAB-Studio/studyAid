# Jargon decoder

Every term below in one plain sentence. When algotrace is asked to "say it simply", it speaks at this level. No term on the left may appear in a simple-mode explanation without its right-side meaning attached.

| Term | What it actually means |
|---|---|
| invariant | A promise that stays true the whole time your loop runs, no matter what. |
| in-place | You rearrange the stuff you were given instead of making a copy. |
| amortized O(1) | Usually instant; once in a while it does a big cleanup, and averaged out it is still cheap. |
| monotonic | Only ever moves one direction: always up, or always down, never both. |
| contiguous | Touching neighbors, no gaps. "Contiguous subarray" = a stretch of the array. |
| subarray vs subsequence | Subarray keeps elements touching. Subsequence keeps their order but can skip. |
| two pointers | Two fingers on the data that only move forward, so you never re-read what a finger passed. |
| sliding window | A stretch between two fingers; the right one grows it, the left one shrinks it. |
| pivot | The element you compare everything else against this round. |
| stable sort | Equal items keep the order they arrived in. |
| hash map | A magic notebook: ask for any name, get its note instantly. |
| collision | Two names land on the same notebook page and share it. |
| heap / priority queue | A bag that always hands you the smallest (or biggest) thing when you reach in. |
| stack | A pile of plates: the last one you put down is the first one you pick up. |
| queue | A line at a shop: first in, first served. |
| deque | A line you can join or leave from both ends. |
| BFS | Explore in rings: everything 1 step away, then everything 2 steps away. |
| DFS | Follow one path to its dead end, back up one step, try the next path. |
| backtracking | DFS where you undo your choice on the way back so the next try starts clean. |
| memoization | Write down answers you already computed so you never compute them twice. |
| tabulation | Fill a table from the smallest case up, so every answer is ready before it is needed. |
| recurrence | The sentence "the answer for n is built from answers for smaller n, like this". |
| base case | The smallest version of the problem you can answer without thinking. |
| greedy | Always grab the best-looking option right now and never look back. |
| divide and conquer | Split the problem in half, solve halves, stitch them together. |
| topological order | A to-do list order where every task comes after the tasks it depends on. |
| union-find | A club-membership tracker: instantly answer "same club?" and merge clubs. |
| trie | A tree where each path from the root spells a word letter by letter. |
| adjacency list | For each node, the plain list of its neighbors. |
| directed / undirected | One-way streets vs two-way streets. |
| cycle | A route that comes back to where it started. |
| overflow | The number got too big for its box and wrapped around to garbage. |
| off-by-one | Your loop stops one step too early or runs one step too far. |
| TLE | Your answer is right but too slow; the judge gave up waiting. |
| edge case | The weird inputs: empty, one element, all same, biggest allowed. |
| asymptotic / Big-O | How the cost grows when the input gets huge, ignoring small change. |
| O(log n) | Every step throws away half of what is left. |
| O(n log n) | The cost of sorting; you touch everything, log-many times. |
| amortized vs worst case | Average over many operations vs the single slowest one. |
