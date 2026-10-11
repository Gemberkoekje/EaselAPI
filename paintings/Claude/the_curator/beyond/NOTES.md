# The room seen through the doorway

*One of the nine pieces of [The Curator](../README.md)'s interim art. How the set was painted,
filed and checked is in [`../FILING.md`](../FILING.md); the painter's verdict on the tool is
[`../verdict.md`](../verdict.md). The painter left no notes of its own for each piece; these
are the filer's.*

| | |
|---|---|
| Script | [`beyond_doorway.py`](beyond_doorway.py), as committed in the game at `76122c4e` |
| Session | `Session(560, 600, texture="linen", ground="toned_grey", seed=11, budget=150, out_dir=".")` |
| Its reason | *the wall beyond the arch, brightening toward a window out of sight on the left* |
| Spent | 123 of 150 strokes |
| Rebuilt | `python beyond_doorway.py 99` writes `painting.png`'s export again, within one level on another machine ([`../FILING.md`](../FILING.md)) |
| Files | `painting.png`, the export as the painter's run left it; `painting.gif`, the time-lapse, recorded by the filer's re-run on 2026-10-11; `scratch/`, its drawing and swatch tests |

What `s.checklist()` measured at the end, re-run (all of it in [`../reports.txt`](../reports.txt)):

- `values: 0.26-0.66 of a box that reaches 0.13-0.96, clusters at 0.32, 0.44, 0.63; a clear light, mid and dark`
- `ground: 5.61% of the canvas is still bare ground`
