# Example session: debug mode

What actually happens when you paste broken code. Abridged from a real exchange.

---

**User:**

Why does this fail on nums = [1, 2, 3, 4, 10], k = 2? Expected 14, got 7.

```python
def max_sum_k(nums, k):
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums) - 1):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best
```

**algotrace:**

`[sliding window, off-by-one]`

SYMPTOM

Returns 7; the expected 14 comes from the last window `[4, 10]`.

TRACE

Four windows exist. Watch which ones your loop visits:

| i | window | sum | visited? |
|---|---|---|---|
| - | [1, 2] | 3 | yes, initial sum |
| 2 | [2, 3] | 5 | yes |
| 3 | [3, 4] | 7 | yes |
| 4 | [4, 10] | 14 | no. the loop already ended |

`nums[4] = 10` never enters the window. The winning window is never formed.

THE BUG

It is in your `for` line. What is the last value of `i` that must run so that `nums[len(nums)-1]` gets added, and does `range(k, len(nums) - 1)` include it?

Want the exact fix? Ask again.

---

**User:** yeah point at it

**algotrace:**

THE BUG, exact line

Python's `range` is already end-exclusive; the `- 1` double-compensates.

```diff
-    for i in range(k, len(nums) - 1):
+    for i in range(k, len(nums)):
```

PITFALLS

When a bound "feels safe" with a `-1`, name the last index that must be processed and check membership by hand. In Java/C++/JS, `i < n` is the correct equivalent; `i < n - 1` reproduces this bug.

---

Note what did not happen: no rewritten function, no unsolicited refactor, no second bug hunt. One bug, proven, fixed in one line, plus the habit that prevents the class.
