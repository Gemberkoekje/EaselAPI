# The doorway wall, the arch cut out

*One of the nine pieces of [The Curator](../README.md)'s interim art. How the set was painted,
filed and checked is in [`../FILING.md`](../FILING.md); the painter's verdict on the tool is
[`../verdict.md`](../verdict.md). The painter left no notes of its own for each piece; these
are the filer's.*

| | |
|---|---|
| Script | [`doorway_wall.py`](doorway_wall.py), as committed in the game at `76122c4e` |
| Session | `Session(W, H, texture="linen", ground="umber_wash", seed=23, budget=320, out_dir=".")` |
| Its reason | *the arch stones catch the light coming through from the room beyond; the wall round them sinks into shade* |
| Spent | 245 of 320 strokes |
| Rebuilt | `python doorway_wall.py 99 && python cut_arch.py doorway_wall_rgb.png doorway_wall.png` writes `painting.png`'s export again, within one level on another machine ([`../FILING.md`](../FILING.md)) |
| Files | `painting.png`, the export as the painter's run left it; `painting.gif`, the time-lapse, recorded by the filer's re-run on 2026-10-11; `doorway_wall.png`, the arch cut out by `cut_arch.py` |

What `s.checklist()` measured at the end, re-run (all of it in [`../reports.txt`](../reports.txt)):

- `values: 0.18-0.40 of a box that reaches 0.13-0.96, clusters at 0.19, 0.28, 0.39; no clear light -- nothing above 0.40, and the box's own middle is 0.54`
- `ground: 7.27% of the canvas is still bare ground`
