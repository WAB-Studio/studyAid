# Eight-week placement prep plan

A schedule that pairs each week with the skill modes that do the most work at that stage. Assumes roughly 90 minutes a day, six days a week. Problem counts are floors, not targets; quality of review beats volume.

The weekly rhythm, regardless of topic:

| Day | Focus |
|---|---|
| 1-2 | Learn or refresh the pattern (tutor mode, then the cheatsheet template) |
| 3-5 | Solve. Get stuck properly before asking for hint level 1 |
| 6 | Review day: run review mode's recall drills on everything due, then blank-editor redos of what you missed |

## WEEK 1 — arrays, hashing, two pointers

Foundation week. Ask tutor mode for two pointers with a trace before touching problems.

- 12-15 easy/medium: two sum variants, remove duplicates, container with most water, 3sum
- Habit to build: before coding, write the invariant in a comment. Debug mode will hold you to it later.

## WEEK 2 — sliding window, prefix sums

- 10-12 medium: max sum size k, longest substring without repeating, minimum window substring, subarray sum equals k
- The off-by-one in fixed-size windows is the most common bug this week. When you hit it, let debug mode trace it rather than eyeballing.

## WEEK 3 — binary search, sorting

- 10-12 problems: first/last position, rotated array, koko eating bananas, capacity to ship packages
- Learn binary search on the answer this week, not later. Signal: "minimize the maximum" or "can we do it with x".

## WEEK 4 — linked lists, stacks, monotonic stack

- 10-12 problems: reverse in k groups, LRU cache, daily temperatures, largest rectangle in histogram
- Monotonic stack deserves a full tutor session with frames; it never sticks from prose alone.

## WEEK 5 — trees, BST, tries

- 12-15 problems: traversals without recursion, lowest common ancestor, validate BST, word search II
- Use visualize mode on every recursion you cannot hold in your head. Recursion is the topic where frames pay off most.

## WEEK 6 — graphs, BFS/DFS, union-find

- 12-15 problems: number of islands, course schedule, rotting oranges, accounts merge
- Interview mode once this week: graphs, medium, full time. Grade yourself on the rubric before reading its scores.

## WEEK 7 — dynamic programming

- 12-15 problems: climbing stairs through house robber, coin change, LIS, edit distance, knapsack shapes
- Rule for the week: no DP problem is done until you can state the recurrence in one sentence. Tutor mode's check questions are built for this.

## WEEK 8 — heaps, greedy, mixed review, mocks

- 8-10 new problems: merge k lists, top k frequent, jump game, gas station
- Three full interview-mode sessions on mixed topics. Treat the rubric trend, not any single score, as the signal.
- Redo the ten problems that cost you the most hints across all weeks.

## Using the modes without cheating yourself

The ladder exists so you always do the maximum you can do alone.

1. Stuck less than 20 minutes: stay off the skill entirely.
2. Stuck at 20-30 minutes: hint level 1 or 2. Go back to solving.
3. Wrong answer on a hidden test: generate edge cases with `scripts/testgen.py` first. If you still cannot find it, paste the code into debug mode.
4. Solved but slow: ask tutor mode why your complexity is what it is, then look for the pattern that removes the bottleneck.
5. Full solution: only after a genuine attempt, and always followed by a blank-editor redo the same week.

Log every session you needed help on; review mode schedules the redos so you do not have to. Interview follow-through: after every interview-mode session, take the single NEXT drill it gives you and do it before starting new material. One drill actually done beats a list of ten saved for later.
