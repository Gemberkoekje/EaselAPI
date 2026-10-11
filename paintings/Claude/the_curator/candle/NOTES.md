# The candle, cut out

*One of the nine pieces of [The Curator](../README.md)'s interim art. How the set was painted,
filed and checked is in [`../FILING.md`](../FILING.md); the painter's verdict on the tool is
[`../verdict.md`](../verdict.md). The painter left no notes of its own for each piece; these
are the filer's.*

| | |
|---|---|
| Script | [`candle.py`](candle.py), as committed in the game at `76122c4e` |
| Session | `Session(W, H, texture="linen", ground="toned_warm_grey", seed=61, budget=110, out_dir=".")` |
| Its reason | *a tallow candle in a brass dish, lit from its own flame above, the wax brightest near the top* |
| Spent | 47 of 110 strokes |
| Rebuilt | `python candle.py 99 && python cut_outline.py candle_rgb.png outline.json candle.png` writes `painting.png`'s export again, within one level on another machine ([`../FILING.md`](../FILING.md)) |
| Files | `painting.png`, the export as the painter's run left it; `painting.gif`, the time-lapse, recorded by the filer's re-run on 2026-10-11; `candle.png`, cut out by `cut_outline.py` |

What `s.checklist()` measured at the end, re-run (all of it in [`../reports.txt`](../reports.txt)):

- `values: 0.37-0.80 of a box that reaches 0.13-0.96, clusters at 0.35, 0.54, 0.78; a clear light, mid and dark`
- `ground: 67.14% of the canvas is still bare ground`
