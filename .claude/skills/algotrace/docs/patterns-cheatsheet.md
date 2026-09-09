# Patterns Cheatsheet

`[two pointers, sliding window, binary search, BFS/DFS, backtracking, DP, monotonic stack, heap, union-find, trie]`

The 10 patterns that cover most LeetCode / OA problems. For each: the signal words in the problem statement, when to use it, the template shape, and complexity. Templates are Python-flavored pseudocode — they translate line for line to Java / C++ / JavaScript.

---

## 1. TWO POINTERS

> Two indices move through a sequence with a **monotonic relationship** (toward each other, or same direction at different speeds), so the pair space is searched in **O(n)** instead of O(n²).

| Signals | "sorted array", "pair/triplet with sum", "remove duplicates in place", "palindrome check", "container/trapping water" |
|---|---|
| Use when | Sorted input, or the answer depends on a pair whose feasibility changes monotonically as pointers move |
| Complexity | O(n) time, O(1) space |

```python
left, right = 0, n - 1
while left < right:
    if condition(a[left], a[right]) is too_small: left += 1
    elif too_big: right -= 1
    else: record(); left += 1; right -= 1
```

Fast/slow variant (cycle detection, middle of linked list): `slow` moves 1, `fast` moves 2; they meet iff a cycle exists.

## 2. SLIDING WINDOW

> A contiguous range `[left, right]` whose ends move **only forward**; each element enters and leaves once.

| Signals | "contiguous subarray/substring", "longest/shortest ... satisfying", "at most k distinct", "max sum of size k" |
|---|---|
| Use when | Answer is a contiguous range AND validity is monotonic (growing can only break it, shrinking can only fix it) |
| Complexity | O(n) time; space = window-state structure (often O(k) or O(charset)) |

```python
left = 0
for right in range(n):
    add(a[right])                 # grow
    while window_invalid():       # shrink until valid
        remove(a[left]); left += 1
    best = max(best, right - left + 1)
```

Fixed-size variant: seed `sum(a[:k])`, then `for i in range(k, n): window += a[i] - a[i-k]`. Off-by-one hotspot: the loop must include `i = n - 1`.

## 3. BINARY SEARCH

> Maintain the invariant that the answer (if any) lies in `[lo, hi]`; each **mid probe eliminates half**.

| Signals | "sorted", "find first/last position", "minimize the maximum / maximize the minimum", "rotated sorted array", monotonic feasibility ("can we do it with capacity x?") |
|---|---|
| Use when | Search space is ordered, or a yes/no predicate is monotonic over a numeric range (binary search ON THE ANSWER) |
| Complexity | O(log n) time (× cost of predicate), O(1) space |

```python
lo, hi = 0, n - 1
while lo <= hi:
    mid = lo + (hi - lo) // 2     # overflow-safe in Java/C++
    if a[mid] == target: return mid
    if a[mid] < target: lo = mid + 1
    else: hi = mid - 1
```

Boundary variant (first true): `while lo < hi: mid = (lo+hi)//2; hi = mid if ok(mid) else (lo := mid+1)`.

## 4. BFS / DFS

> **BFS** explores by distance layers with a queue — first arrival = shortest unweighted path. **DFS** dives with a stack/recursion — natural for exhaustive exploration, components, and ordering.

| Signals | "shortest path / minimum steps" (BFS), "connected components", "islands", "all paths", "cycle detection", "topological order", grids, mazes, word ladders |
|---|---|
| Use when | Any graph/grid/state-space reachability question; BFS for shortest, DFS for existence/structure |
| Complexity | O(V + E) time, O(V) space |

```python
# BFS                                 # DFS (recursive)
queue = deque([start]); seen = {start}
while queue:                          def dfs(u):
    u = queue.popleft()                   seen.add(u)
    for v in neighbors(u):                for v in neighbors(u):
        if v not in seen:                     if v not in seen:
            seen.add(v)                           dfs(v)
            queue.append(v)
```

Mark `seen` when ENQUEUING (BFS), not when popping — the classic double-visit bug.

## 5. BACKTRACKING

> DFS over **partial solutions**: extend a candidate one choice at a time, **undo** the choice on return, prune branches that cannot succeed.

| Signals | "all permutations/combinations/subsets", "N-queens", "sudoku", "generate all valid ...", "word search" |
|---|---|
| Use when | Must enumerate all solutions (or find one) in an exponential space, with pruning available |
| Complexity | Output-sensitive; O(b^d) worst case (b = branching, d = depth) |

```python
def backtrack(path, choices):
    if is_solution(path): results.append(path.copy()); return
    for c in choices:
        if not valid(c, path): continue   # prune
        path.append(c)
        backtrack(path, next_choices)
        path.pop()                        # undo — the step people forget
```

## 6. DYNAMIC PROGRAMMING

> Define the answer to a subproblem as a **state**; if the recurrence has **overlapping subproblems** and **optimal substructure**, cache it.

| Signals | "number of ways", "minimum cost / maximum value", "longest ... subsequence", "can you partition", "climbing stairs", grids with costs, "wildcard/edit distance" |
|---|---|
| Use when | Brute force recursion recomputes the same states; answer composes from smaller prefixes/suffixes/intervals |
| Complexity | O(#states × transition cost); space O(#states), often reducible one dimension |

```python
# top-down                            # bottom-up
@cache                                dp = [base] * (n + 1)
def f(state):                         for i in range(1, n + 1):
    if base(state): return b              dp[i] = best(dp[i-1] + cost,
    return best(f(smaller)                            dp[i-k] + other)
               for smaller in trans)  return dp[n]
```

Recipe: 1) define state in words, 2) write recurrence, 3) base cases, 4) order/memoize, 5) read off the answer. The definition in words is the step that fails silently — do it first.

## 7. MONOTONIC STACK

> A stack kept **sorted** (increasing or decreasing); each element pops everything it dominates, so every element pushes and pops **once**.

| Signals | "next greater/smaller element", "days until warmer", "largest rectangle in histogram", "stock span", "remove k digits" |
|---|---|
| Use when | For each element you need the nearest element to one side that is greater/smaller |
| Complexity | O(n) time, O(n) space |

```python
stack = []                       # holds indices, values decreasing
for i, x in enumerate(a):
    while stack and a[stack[-1]] < x:
        j = stack.pop()
        answer[j] = i - j        # x is j's "next greater"
    stack.append(i)
```

## 8. HEAP / PRIORITY QUEUE

> A tournament bracket over your data: **peek the best in O(1)**, insert/remove in **O(log n)**, no full sort needed.

| Signals | "k largest/smallest/closest/most frequent", "merge k sorted lists", "median of stream", "schedule by earliest deadline", Dijkstra |
|---|---|
| Use when | You repeatedly need the current min/max while the collection changes |
| Complexity | O(n log k) for top-k with a size-k heap; O(log n) per op |

```python
import heapq
heap = nums[:k]; heapq.heapify(heap)      # min-heap of the k largest
for x in nums[k:]:
    if x > heap[0]: heapq.heapreplace(heap, x)
# heap[0] is the k-th largest
```

Python/JS have min-heaps only — negate values for max-heap. Java: `new PriorityQueue<>(Comparator.reverseOrder())`. C++: `priority_queue` is max by default.

## 9. UNION-FIND (DSU)

> Tracks **disjoint sets** under merging: `find` returns a set's representative, `union` merges two sets — near-O(1) amortized with path compression + rank.

| Signals | "connected components with edges arriving over time", "accounts merge", "redundant connection", "number of provinces", Kruskal MST, "friend circles" |
|---|---|
| Use when | Dynamic connectivity — edges only ever added, queries ask "same group?" |
| Complexity | O(α(n)) ≈ O(1) amortized per op; O(n) space |

```python
parent = list(range(n))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb: parent[ra] = rb; return True
    return False                         # already connected → cycle
```

## 10. TRIE (PREFIX TREE)

> A tree keyed by **characters along the path**; all words sharing a prefix share a path, so prefix queries cost **O(prefix length)** regardless of dictionary size.

| Signals | "prefix", "autocomplete", "starts with", "word dictionary with wildcards", "maximum XOR pair" (bitwise trie) |
|---|---|
| Use when | Many string (or bit) queries against a fixed-ish dictionary, keyed by prefixes |
| Complexity | O(L) insert/search per word of length L; space O(total chars × alphabet) |

```python
root = {}
def insert(word):
    node = root
    for ch in word:
        node = node.setdefault(ch, {})
    node['$'] = True                    # end-of-word marker
def starts_with(prefix):
    node = root
    for ch in prefix:
        if ch not in node: return False
        node = node[ch]
    return True
```

---

## PATTERN PICKER (start here when a problem gives no signal)

| Question about the problem | If yes → |
|---|---|
| Contiguous subarray/substring optimization? | sliding window |
| Sorted input, or monotonic yes/no predicate? | binary search / two pointers |
| "Shortest path / fewest steps" on unweighted states? | BFS |
| "All possible ..." with pruning? | backtracking |
| "Count ways / min cost" composing from subproblems? | DP |
| Nearest greater/smaller per element? | monotonic stack |
| Rolling top-k / repeated min-max? | heap |
| Edges added over time + "connected?" queries? | union-find |
| Many prefix/dictionary queries? | trie |
