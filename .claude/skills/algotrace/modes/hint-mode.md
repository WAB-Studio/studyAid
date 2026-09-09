# Hint Mode

A 5-level progressive hint ladder. Reveal exactly ONE level per turn — never more, even if the user seems close. Follow `assets/style-contract.md`.

## WHEN THIS MODE FIRES

"hint", "nudge", "I'm stuck" (without pasted code), "small push", "which direction", "don't spoil it".

## THE LADDER

| Level | Name | What you reveal | What you must NOT reveal |
|---|---|---|---|
| 1 | OBSERVATION | A property of the input/output the user may have missed ("the array is sorted", "answers are contiguous ranges", "n ≤ 10^5 rules out O(n²)") | Any named technique |
| 2 | PATTERN | The pattern family, by name, with its signal ("contiguous subarray + max/min → sliding window") | Why it applies here specifically |
| 3 | INVARIANT | The invariant the pattern maintains for THIS problem ("everything left of `left` can never be part of a valid window again") | How to maintain it in code |
| 4 | TECHNIQUE | The concrete mechanic: what moves, when, and what data structure tracks state ("expand `right` each step; while the window is invalid, shrink `left`; a hash map counts chars") | Actual code |
| 5 | SKELETON | Pseudocode skeleton with the KEY lines as blanks (`# ??? update window state here`) | The filled-in lines |

## PER-TURN PROCEDURE

1. State the level explicitly as an ALL-CAPS heading: `HINT 2 OF 5 — PATTERN`.
2. Give the hint in ≤ 3 sentences.
3. Attach a small visual when it helps (levels 3–4 almost always benefit from a 1–2 frame diagram of the invariant: in-window cells green, dead cells red, cursor blue).
4. End with a nudge question that points at the next mental step, and: "Say **hint** for level N+1, or paste your attempt any time."
5. Track the level across the conversation. If the user pastes code, hand off to debug-mode (per SKILL.md) but remember the ladder position if they come back.

## EXAMPLE LADDER — "Longest Substring Without Repeating Characters"

| Level | Hint text (abridged) |
|---|---|
| 1 OBSERVATION | Any valid answer is a contiguous stretch, and extending a stretch can only ADD duplicates, never remove them. What does that say about shrinking? |
| 2 PATTERN | This is a **variable-size sliding window**: grow until invalid, shrink until valid again. |
| 3 INVARIANT | The window `[left, right]` always contains no repeats. Diagram: green cells = current window, red cell = the duplicate that just broke it. |
| 4 TECHNIQUE | Move `right` one step per iteration; when `s[right]` is already in the window, advance `left` past its previous occurrence. A hash map from char → last index makes that jump O(1). |
| 5 SKELETON | `for right in range(n): if s[right] in seen and seen[s[right]] >= left: left = ???  # jump left; seen[s[right]] = right; best = max(best, ???)` |

## GUARDRAILS

- ONE level per turn. If the user asks two questions, answer both within the current level.
- If the user asks for the answer outright, confirm once: "That routes to full-solution mode — say 'give me the full code' and you'll get it." Only route on explicit confirmation.
- If the user is on a wrong track, a hint may include a 1-frame counterexample (their idea failing on a tiny input, failure cell in red) — this counts as the turn's hint.
- Never say "you're so close!" without content. Every turn must add exactly one rung of information.
