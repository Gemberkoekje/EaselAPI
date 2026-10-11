# The hooded patron, cut out

*One of the nine pieces of [The Curator](../README.md)'s interim art. How the set was painted,
filed and checked is in [`../FILING.md`](../FILING.md); the painter's verdict on the tool is
[`../verdict.md`](../verdict.md). The painter left no notes of its own for each piece; these
are the filer's.*

| | |
|---|---|
| Script | [`patron_default.py`](patron_default.py), as committed in the game at `76122c4e` |
| Session | `Session(W, H, texture="linen", ground="toned_grey", seed=41, budget=160, out_dir=".")` |
| Its reason | *a figure against the bright doorway: all shadow, with the light behind just catching hood and shoulders* |
| Spent | 95 of 160 strokes |
| Rebuilt | `python patron_default.py 99 && python cut_outline.py patron_rgb.png outline.json patron_default.png` writes `painting.png`'s export again, within one level on another machine ([`../FILING.md`](../FILING.md)) |
| Files | `painting.png`, the export as the painter's run left it; `painting.gif`, the time-lapse, recorded by the filer's re-run on 2026-10-11; `patron_default.png`, cut out by `cut_outline.py` |

What `s.checklist()` measured at the end, re-run (all of it in [`../reports.txt`](../reports.txt)):

- `values: 0.09-0.54 of a box that reaches 0.13-0.96, clusters at 0.09, 0.28, 0.53; no clear light -- nothing above 0.54, and the box's own middle is 0.54`
- `ground: 25.28% of the canvas is still bare ground`
