# The rings, frame by frame

Seven frames out of GLM's own working folder, copied in because a painting's `out/` is
not committed and these seven are the evidence for the one finding of its round that
nobody has got right yet: **the concentric rings on the wall right of the monitor.**

The painter's own account, in [`../NOTES.md`](../NOTES.md) and
[`../verdict.md`](../verdict.md), is *six crossing glazes laid wet, then a block-in on
top*. It cost the session's one `undo`, back to the bare masses. What replaced it is the
`pass1b.py` that is committed — take three, one tight low-contrast inward scumble. **The
calls that made the rings are gone**: the first takes of `pass1b.py` and `pass2.py` were
overwritten and their marks undone, so these frames are all that is left of them.

The frames are in the order they were written, and they are here to be argued with. What
follows each one is the reading the 0.6.0 round took from it, which is not the painter's
and is not yet checked: a probe that rebuilds pass 2's first take is what settles it, and
it is right when it reproduces frame 4's dark band.

| Frame | What it is | What it shows |
|---|---|---|
| [1](ring_1_look_005.png) | `look_005`, the whole canvas, after the six glazes and before pass 2 | The glow is in, the wall is clean. Faint straight bands, no rings anywhere. |
| [2](ring_2_look_006.png) | `look_006`, the wall right of the bezel, same moment | The same wall at the crop the rings will land on, still clean. **Frames 1 and 2 are why the six crossing glazes are not the cause.** |
| [3](ring_3_rehearse_012.png) | `rehearse_012`, the last rehearsal of pass 2's first take | The rings, on a copy, before a mark was paid for. |
| [4](ring_4_look_007.png) | `look_007`, the committed pass | The same rings, in the same places. **The rehearsal showed them and *what you rehearse is what lands* held** — the painter did not look, or looked and did not see them. |
| [5](ring_5_noimp.png) | `noimp.png`, the crop again with `impasto=False` | The rings are still there with the relief switched off, so they are paint and not surface. One band is as dark as the bezel. |
| [6](ring_6_noimp2.png) | `noimp2.png`, the monitor in values, no relief | What they actually are: **wobbly closed loops concentric with a blob-shaped patch**, lying over the bezel's right edge and out onto the wall — the patch overshoots the glass. |
| [7](ring_7_bisect30.png) | `bisect30.png`, the crop in values at record 30 | The painter bisecting its own log with `replay(upto=30)`. The rings read as value steps, which is the number a check would have to measure. |

**The round's reading**, from frames 2, 6 and 7: this is an inward `scumble`'s own
contour rings — the failure `RECIPES.md` already names as *visible concentric rings* and
the pool painting called *a contour map* — laid after the bezel around a patch that
overshoots the glass, and possibly darkened where it picked up the wet bezel under it.
Wetness is `alpha x brush.wetness` and alpha carries the opacity, so a film at
`opacity=0.15` leaves about 0.13 rather than 0.90, and it had twenty-odd strokes at
about 6% a stroke to fade: a wet film at full wetness is not available as an explanation
either. The painter's own cure fits the reading — a far lower-contrast inward scumble at
`n=10`, and `dry()` before the bezel.

**Three accounts of these rings have been written and at least two are wrong**, which is
why the frames are committed rather than the conclusion. See `SUGGESTIONS.md`, the 0.5.0
cohort's round, B18.
