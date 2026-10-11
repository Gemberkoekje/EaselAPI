# The right bookcase

*One of the nine pieces of [The Curator](../README.md)'s interim art. How the set was painted,
filed and checked is in [`../FILING.md`](../FILING.md); the painter's verdict on the tool is
[`../verdict.md`](../verdict.md). The painter left no notes of its own for each piece; these
are the filer's.*

| | |
|---|---|
| Script | [`shelves.py`](shelves.py), as committed in the game at `76122c4e` |
| Session | `Session(640, 720, texture="linen", ground="umber_wash", seed=SEED, budget=460, out_dir=".")` |
| Its reason | *a wall of old books, every spine its own, oak shelves catching the window's light* |
| Spent | 388 of 460 strokes |
| Rebuilt | `python shelves.py right 99` writes `painting.png`'s export again, within one level on another machine ([`../FILING.md`](../FILING.md)) |
| Files | `painting.png`, the export as the painter's run left it; `painting.gif`, the time-lapse, recorded by the filer's re-run on 2026-10-11 |

What `s.checklist()` measured at the end, re-run (all of it in [`../reports.txt`](../reports.txt)):

- `values: 0.15-0.32 of a box that reaches 0.13-0.96, clusters at 0.16, 0.23, 0.29; no clear light -- nothing above 0.32, and the box's own middle is 0.54`
- `ground: 0.00% of the canvas is still bare ground -- under 0.5%, and the checklist asks for some`
