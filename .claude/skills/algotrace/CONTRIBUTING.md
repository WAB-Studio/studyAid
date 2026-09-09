# Contributing

Thanks for the interest. This project is a Claude skill, so most contributions are Markdown, not code.

## What helps most

- New worked examples inside the mode files. Debug mode especially: real bugs from real attempts, with the failing input and the trace to the divergent step. One bug per example.
- New baked demos in `demos/`. Copy `assets/visualizer-template.html`, replace the `VIZ` object, update the static first frame, keep everything else untouched.
- Corrections to the patterns cheatsheet, particularly complexity edge cases and language-specific traps.
- Additions to the language bug checklist in `modes/debug-mode.md`.

## Ground rules

- Every visual follows `assets/style-contract.md`. Four colors, fixed meanings, no decoration.
- No emojis anywhere in the repo.
- Prose stays tight. If a table can say it, a table says it.
- Demos must be single-file, dependency-free, and render something without JavaScript (bake the first frame into static HTML).

## Testing a change

Run `python -m unittest discover -s scripts` for the generator tests. The skill itself is prompts, so mode changes are checked by hand: To sanity-check a mode change, load the skill in Claude Code and run the trigger phrases listed at the top of the mode file. For demo changes, open the file in a browser with JavaScript disabled first, then enabled.

Open an issue before large restructures.
