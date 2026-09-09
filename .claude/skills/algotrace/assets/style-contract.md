# algotrace Style Contract

Every algotrace response — in every mode — follows this contract. It exists so output reads like a clean, hand-drawn study guide, not AI slop.

## PAGE STRUCTURE

1. **Tag line first.** Open with a bracketed navigation line of pattern/topic tags:

   `[sliding window, hash map, O(n)]`

2. **ALL-CAPS subheadings** segment the response. Use only the ones you need, in roughly this order:

   `DEFINITION · INTUITION · TRACE · COMPLEXITY · PITFALLS`

   Modes may add their own (e.g., `THE BUG`, `HINT 2 OF 5`, `RUBRIC`) — always ALL-CAPS.

3. **Definitions live in blockquotes** with **key terms bolded**:

   > A **sliding window** maintains a contiguous range `[left, right]` over a sequence and moves both ends **monotonically forward**, so each element enters and leaves the window at most once.

4. **Comparisons and characteristics go in standard Markdown tables** — never paragraphs of prose comparing things.

5. Prose stays tight: 1–3 sentence paragraphs. No filler, no pep talk, no emoji.

## COLOR SEMANTICS (non-negotiable)

Minimal, flat, muted. Four meanings, four colors, used SPARSELY — most elements stay ink-on-paper.

| Meaning | Color | Hex |
|---|---|---|
| correct / added / found / in-window | green | `#16a34a` |
| wrong / removed / eliminated / out-of-bounds | red | `#dc2626` |
| current pointer / active element / cursor | blue | `#2563eb` |
| inert / already-processed | gray | `#94a3b8` |
| text / strokes | ink | `#1e293b` |
| background | paper | `#f8fafc` |

Banned: pastels, gradients, glows, shadows everywhere, neon, decorative icons, "dashboard" chrome. If a cell has no semantic state, it gets NO color.

## INLINE MODE (default)

Render diagrams directly in chat as clean **inline SVG** or **Markdown tables**, stepping frame by frame.

Array frame as a table (indices always shown; states named in a state row):

| idx | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| val | 2 | 5 | 8 | 12 | 16 |
| state | gray | gray | **blue: mid** | — | — |

Array frame as inline SVG: flat rectangles (`fill="#f8fafc"`, `stroke="#1e293b"`), index labels below cells, pointer labels/arrows above cells in blue, eliminated cells tinted red at low opacity (`fill="#dc2626" fill-opacity="0.15"` + red stroke), processed cells in gray, found cell in green. Trees/graphs: circles with straight edges, same palette. No filters, no gradients, no shadows.

Show **one frame per step** with a one-line caption: what changed and why.

## ARTIFACT MODE (full walkthroughs)

For a complete problem walkthrough (≥ ~6 frames, or when the user wants to "play" the algorithm), emit ONE self-contained interactive HTML file based on `assets/visualizer-template.html`:

- Single file, no external dependencies. (Exception: Chart.js from CDN is OPTIONALLY allowed when plotting complexity curves.)
- **Prev / Next / Play** controls stepping through the same green/red/blue/gray states.
- Flat, minimal design matching this palette. System font stack. No shadow-everywhere AI look.
- MUST NOT use `localStorage` or `sessionStorage` — keep all state in JS variables.
- Every frame has a caption; the current step number is always visible.

## WHICH RENDERING TO PICK

| Situation | Render as |
|---|---|
| Concept snippet, 1–5 frames, quick trace | Inline (SVG or table) |
| Full problem walkthrough, ≥6 frames, "let me play with it" | HTML artifact |
| Diff of buggy vs. fixed line | Inline `diff` code block (red `-`, green `+`) |
| Pattern comparison | Markdown table |
