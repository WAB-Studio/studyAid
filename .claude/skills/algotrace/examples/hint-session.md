# Example session: hint mode

The five-level ladder on LeetCode 3, Longest Substring Without Repeating Characters. One level per message, nothing skipped.

---

**User:** stuck on longest substring without repeating characters. do NOT spoil it.

**algotrace:**

HINT 1 OF 5, OBSERVATION

Any valid answer is a contiguous stretch. Extending a stretch can only add duplicates, never remove them. What does that tell you about when shrinking is ever useful?

Say **hint** for level 2, or paste your attempt any time.

---

**User:** hint

**algotrace:**

HINT 2 OF 5, PATTERN

This is a **variable-size sliding window**: grow until invalid, shrink until valid again. The signal was in level 1: validity is monotonic in both directions.

---

**User:** ok i get the window idea but my left pointer logic is a mess. hint

**algotrace:**

HINT 3 OF 5, INVARIANT

The window `[left, right]` must always contain no repeats.

| s | a | b | c | b |
|---|---|---|---|---|
| state | gray | green | green | red |

The red `b` just broke the invariant. Everything at or before the first `b` can never be in a valid window with it. Where must `left` land, at minimum?

---

**User:** left jumps past the old b. but how do i find where the old b was fast?

**algotrace:**

HINT 4 OF 5, TECHNIQUE

A hash map from character to its last seen index. When `s[right]` is already in the map at position `p >= left`, set `left = p + 1` in one jump. Each pointer only moves forward, so the whole pass is O(n).

That is everything except the code. Try writing it; paste your attempt if it misbehaves.

---

The user wrote it themselves after level 4. Level 5 (the skeleton with blanks) exists but most ladders end before it, which is the point.
