# Visualize Mode

Animate a data structure or algorithm step by step. The visualization IS the deliverable. Follow `assets/style-contract.md` exactly.

## WHEN THIS MODE FIRES

"visualize", "simulate", "animate", "show me step by step", "trace / dry run", "draw the array/tree/graph", "how do the pointers move".

## PROCEDURE

1. **Tag line** — open with `[pattern, data structure, complexity]`.
2. **Pick the rendering:**

| Condition | Choice |
|---|---|
| ≤ 5 frames, single concept, quick question | Inline SVG or Markdown-table frames in chat |
| ≥ 6 frames, full problem, user wants to replay/scrub | Interactive HTML artifact from `assets/visualizer-template.html` |
| User explicitly asks for one format | That format |

3. **Build the frame sequence.** One frame = one algorithmic decision (a comparison, a pointer move, an elimination). Never merge two decisions into one frame. Each frame gets a one-line caption: what changed and WHY.
4. **Apply color semantics** from the style contract: blue = pointers/cursor, red = eliminated/out-of-bounds, gray = processed/inert, green = found/in-window/correct. No other colors.
5. **Close with COMPLEXITY** (time + space, one-line justification) and, if useful, one PITFALLS line.

For the HTML artifact: copy `assets/visualizer-template.html`, replace the `VIZ` object (title, data, frames) with the new trace, keep everything else untouched. Frames support `pointers`, `states`, `vars`, `caption`, and optional raw `svg` for trees/graphs.

## FRAME DESIGN RULES

- Arrays: cells with values, index row underneath, pointer labels above in blue.
- Trees/graphs: circles + straight edges; the node being visited is blue, visited set gray, target/result green, pruned subtrees red-tinted.
- Windows/ranges: tint the in-window cells green at low opacity; a shrinking window turns the departed cell gray.
- State variables (`lo`, `hi`, `best`, window sum, etc.) shown per frame in a small table or the artifact's VARS strip.

## WORKED EXAMPLE — binary search on a sorted array

User: "Visualize binary search for 23 in [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]."

Response shape (inline; ≤ 6 frames so no artifact needed):

---

`[binary search, sorted array, O(log n)]`

DEFINITION

> **Binary search** keeps an **invariant**: if the target exists, it lies inside `[lo, hi]`. Each probe of **mid** eliminates half of that range.

TRACE — target = 23

Frame 1 — initialize. `lo=0` (blue), `hi=9` (blue). Everything is still possible.

| idx | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| val | 2 | 5 | 8 | 12 | 16 | 23 | 38 | 56 | 72 | 91 |
| ptr | lo |  |  |  |  |  |  |  |  | hi |

Frame 2 — probe `mid = (0+9)//2 = 4` (blue). `arr[4] = 16 < 23`, so the answer cannot be at index ≤ 4.

| idx | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| val | 2 | 5 | 8 | 12 | **16** | 23 | 38 | 56 | 72 | 91 |
| ptr | lo |  |  |  | mid (blue) |  |  |  |  | hi |

Frame 3 — eliminate the left half (red): indices 0–4 are out. `lo = mid + 1 = 5`.

| idx | ~~0~~ | ~~1~~ | ~~2~~ | ~~3~~ | ~~4~~ | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| val | red | red | red | red | red | 23 | 38 | 56 | 72 | 91 |
| ptr |  |  |  |  |  | lo |  |  |  | hi |

Frame 4 — probe `mid = (5+9)//2 = 7`. `arr[7] = 56 > 23`, so indices ≥ 7 are out (red). `hi = mid − 1 = 6`.

| idx | ~~0–4~~ | 5 | 6 | ~~7~~ | ~~8~~ | ~~9~~ |
|---|---|---|---|---|---|---|
| val | red | 23 | 38 | red | red | red |
| ptr |  | lo | hi |  |  |  |

Frame 5 — probe `mid = (5+6)//2 = 5`. `arr[5] = 23` — **found** (green) at index 5.

| idx | ~~0–4~~ | 5 | 6 | ~~7–9~~ |
|---|---|---|---|---|
| val | red | **23 (green)** | 38 | red |

Equivalent inline SVG for a single frame (Frame 2), matching the contract:

```svg
<svg viewBox="0 0 560 110" xmlns="http://www.w3.org/2000/svg" font-family="system-ui" font-size="13">
  <!-- pointer labels -->
  <text x="28"  y="18" fill="#2563eb" text-anchor="middle">lo</text>
  <text x="252" y="18" fill="#2563eb" text-anchor="middle">mid</text>
  <text x="532" y="18" fill="#2563eb" text-anchor="middle">hi</text>
  <!-- cells: x = 4 + i*56 -->
  <g stroke="#1e293b" fill="#f8fafc">
    <rect x="4"   y="26" width="48" height="40"/><rect x="60"  y="26" width="48" height="40"/>
    <rect x="116" y="26" width="48" height="40"/><rect x="172" y="26" width="48" height="40"/>
    <rect x="228" y="26" width="48" height="40" stroke="#2563eb" stroke-width="2.5"/>
    <rect x="284" y="26" width="48" height="40"/><rect x="340" y="26" width="48" height="40"/>
    <rect x="396" y="26" width="48" height="40"/><rect x="452" y="26" width="48" height="40"/>
    <rect x="508" y="26" width="48" height="40"/>
  </g>
  <g fill="#1e293b" text-anchor="middle">
    <text x="28" y="51">2</text><text x="84" y="51">5</text><text x="140" y="51">8</text>
    <text x="196" y="51">12</text><text x="252" y="51">16</text><text x="308" y="51">23</text>
    <text x="364" y="51">38</text><text x="420" y="51">56</text><text x="476" y="51">72</text>
    <text x="532" y="51">91</text>
  </g>
  <g fill="#94a3b8" text-anchor="middle" font-size="11">
    <text x="28" y="82">0</text><text x="84" y="82">1</text><text x="140" y="82">2</text>
    <text x="196" y="82">3</text><text x="252" y="82">4</text><text x="308" y="82">5</text>
    <text x="364" y="82">6</text><text x="420" y="82">7</text><text x="476" y="82">8</text>
    <text x="532" y="82">9</text>
  </g>
  <text x="4" y="104" fill="#1e293b">arr[mid]=16 &lt; 23 → eliminate left half next</text>
</svg>
```

COMPLEXITY

O(log n) time — the candidate range halves every frame (10 → 5 → 2 → 1). O(1) space — three integers.

PITFALLS

`mid = (lo + hi) // 2` overflows in Java/C++ for large indices; use `lo + (hi - lo) / 2`.

---

## GUARDRAILS

- Do not attach full solution code in this mode; the trace may reference pseudocode lines but the deliverable is the visualization. If the user then asks for code, route per SKILL.md.
- Never skip frames to save space; if there are too many, switch to the HTML artifact instead.
