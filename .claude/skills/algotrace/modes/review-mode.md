# Review Mode — spaced repetition and recall

Turn solved problems into retained patterns. This mode owns the progress log and the redo schedule. Follow `assets/style-contract.md`.

## WHEN THIS MODE FIRES

"what should I revise", "review day", "quiz me", "recall drill", "log this session", "what am I weak on", "schedule my redos", or the day-6 step of the study plan.

## THE PROGRESS LOG

A single Markdown file the user keeps in their project: `.algotrace/progress.md`. Created on first use. One table, append-only:

| date | problem | pattern | mode used | hints | bug class | next review |
|---|---|---|---|---|---|---|
| 2026-07-14 | LC 3 longest substring | sliding window | hint (to L4) | 4 | - | 2026-07-17 |
| 2026-07-15 | max sum size k | sliding window | debug | - | off-by-one | 2026-07-18 |

Rules:

- **Offer, never nag.** At the end of a debug, hint, or interview session, offer once: "Log this to your progress file?" If yes, append one row. If the file does not exist, create it.
- **Next review** follows expanding intervals from the solve date: +3 days, then +7, then +21. A clean recall (no hints, correct invariant stated) advances the interval; a failed recall resets to +3.
- The log is the user's file in their repo. Never overwrite existing rows; only append or update the `next review` column of the row being reviewed.

## RECALL DRILLS

When the user asks to review, read the log, pick rows where `next review` is due (oldest first), and drill ONE problem per turn:

1. `RECALL` — restate the problem from the log in one line. Do not name the pattern.
2. Ask for three things, in order, waiting for each answer:
   - the pattern and why it applies (checks recognition)
   - the invariant in one sentence (checks understanding)
   - the complexity with justification (checks analysis)
3. `VERDICT` — a 3-frame visual check: show a small input and ask the user to state what the state looks like at frame 2. Their answer against the true frame (green if right, red where it diverges) is the evidence, debug-mode style.
4. Update the row: clean recall advances the interval, misses reset it. Say which happened and when the problem returns.

## WEAKNESS REPORT

On "what am I weak on": aggregate the log into two tables, nothing else.

| pattern | attempts | avg hints | failed recalls |
|---|---|---|---|

| bug class | count | last seen |
|---|---|---|

Then ONE recommendation: the single pattern or bug class with the worst ratio, and which mode to attack it with. One, not a list.

## GUARDRAILS

- Recall drills never turn into teaching. A missed recall gets the failing frame shown, the row reset, and a pointer to tutor mode — not an inline lecture.
- Never fabricate log history. If the log is empty or missing, say so and offer to start it with the current session.
- One problem per turn keeps recall honest; batch-reviewing five problems in one message defeats the format.
