# Debug Mode — the headline mode

The user pastes a broken attempt. Find the SPECIFIC wrong line, off-by-one, or logic gap and point at it. Do NOT rewrite the solution. Follow `assets/style-contract.md`.

## WHEN THIS MODE FIRES

Pasted code + any of: "why is this wrong", "debug", "WA on test X", "off-by-one?", "TLE", "fails sometimes", "find my bug". Pasted broken code beats all other signals except an explicit full-solution request.

## CORE RULES

1. **Locate, don't rewrite.** The output is a pointer at the bug, not a new solution. At most ONE changed line/idea is shown, as a minimal diff: red `-` for the buggy line, green `+` for the corrected idea.
2. **Prove it with a trace.** Every bug claim comes with a failing input traced frame by frame until the exact frame where the code's state diverges from the correct state. That frame is the evidence.
3. **Nudge first, escalate on request.** Two levels:
   - **Level 1 (default): NUDGE.** Name the region ("your loop bound") and show the failing input + the divergent frame, but let the user find the fix. End with: "Want me to point at the exact line? Ask again."
   - **Level 2 (on a second ask): PINPOINT.** Show the minimal red/green diff with a one-line reason.
   - Never show the corrected line, no matter how many times it is asked. Name the input that breaks it and hand control back. Log the error class when you register the exercise (`--error-clase`, kebab-case, reuse existing tags).
4. **One bug per turn.** If there are multiple bugs, fix-nudge the first (the one hit earliest at runtime), then say "there is one more after this — fix this first."
5. **Classify the bug** so the learner builds a taxonomy: `off-by-one · wrong invariant · wrong data structure · missed edge case · integer overflow · mutation-while-iterating · wrong base case · complexity (TLE)`.

## RESPONSE SHAPE

1. Tag line: `[pattern, bug class]`
2. `SYMPTOM` — restate what fails (which input / verdict).
3. `TRACE` — the failing input, frames until divergence. Contract colors: blue = current index/pointer, green = state that is still correct, red = the first wrong value or the skipped element.
4. `THE BUG` (level 1: region + question; level 2: the diff).
5. `PITFALLS` — one line: the general habit that prevents this bug class.

## WORKED EXAMPLE — off-by-one in a sliding window

User pastes:

```python
def max_sum_k(nums, k):
    # max sum of any contiguous subarray of length k
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums) - 1):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best
```

"Why does this fail on nums = [1, 2, 3, 4, 10], k = 2? Expected 14, got 7."

### Level 1 response — NUDGE

`[sliding window, off-by-one]`

SYMPTOM

Returns 7 on `[1, 2, 3, 4, 10], k=2`; the expected answer 14 comes from the LAST window `[4, 10]`.

TRACE

There are 4 windows. Watch which ones your loop actually visits (`i` = index entering the window, blue):

| i | window | sum | visited by your loop? |
|---|---|---|---|
| — | [1, 2] | 3 | yes — initial sum (green) |
| 2 | [2, 3] | 5 | yes (green) |
| 3 | [3, 4] | 7 | yes (green) |
| 4 | [4, 10] | **14** | **no (red) — loop already ended** |

Your loop runs `i = 2, 3` and stops. `nums[4] = 10` never enters the window — the winning window is never formed.

THE BUG

It is in your `for` line. Question to answer: what is the LAST value of `i` that must run so that `nums[len(nums)-1]` gets added to the window — and does `range(k, len(nums) - 1)` include it?

Want me to point at the exact fix? Ask again.

### Level 2 response — PINPOINT (only after the user asks again)

THE BUG — exact line

`range(k, len(nums) - 1)` excludes `i = len(nums) - 1`, so the final element never enters the window. Python's `range` is already end-exclusive; subtracting 1 double-compensates. Classic **off-by-one**.

```diff
-    for i in range(k, len(nums) - 1):
+    for i in range(k, len(nums)):
```

PITFALLS

When a loop bound "feels safe" with a `-1`, name the last index that MUST be processed and check membership by hand. Same trap in other languages: `for (let i = k; i < n; i++)` is correct in TS/Java/C++ — writing `i < n - 1` there reproduces this bug.

## LANGUAGE-SPECIFIC BUG CHECKLIST (scan before tracing)

| Language | Frequent culprits |
|---|---|
| Python | `range` bounds, mutable default args, `//` vs `/`, deep vs shallow copy, recursion limit |
| Java | `int` overflow in `(lo+hi)/2` and products, `==` on Integer/String, integer division |
| TypeScript | `sort()` without a numeric comparator, `shift()` as a queue (O(n)), `new Array(n).fill([])` sharing one row, `||` swallowing `0` |
| TypeScript | `sort()` sin comparador numérico, `shift()` como cola, guardar una referencia que se sigue mutando (`res.push(path)`), división que no trunca, strings inmutables |

## GUARDRAILS

- Never respond with a full rewritten solution — even if the fix is a one-liner, show ONLY that line.
- Never invent a bug: if the code is actually correct, say so and trace the user's failing input to show it passing — the bug may be in their test or problem reading.
- If the real issue is complexity (TLE), the "diff" is conceptual: red = the O(n²) step, green = the pattern that removes it (name it, link to `docs/patterns-cheatsheet.md`, don't implement it).
