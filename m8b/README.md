# M8b — the wet-blend reflectance floor

Item 11 of `painting-api-brief.md`, the phase between M8 and the server. The
Kubelka-Munk reflectance floor from `REVIEW.md` finding 5 was being applied to the
*answer* as well as to the arithmetic. `REVIEW.md` finding 35 is the write-up; this
directory is the evidence.

```
probe_floor.py       both halves of the defect, as numbers. `--label` names the run.
paint_the_dark.py    one composition painted by both engines, and the sheet.
before.png           that composition, pre-M8b
after.png            the same composition, post-M8b
compared.png         the two side by side, with the dark mass and the yellow enlarged
```

## What was wrong

`blend_wet()` clipped both colours into `[0.01, 1 - 1e-4]` on the way into K/S space
and never took the clip back off, so the floor decided two things it had no business
deciding.

**A pixel nothing was being painted onto still moved.** `Canvas.stamp` blends a dab's
whole *square* bounding box; a round tip's corners have an alpha of exactly zero. A
black pixel in one of those corners came away at sRGB 25 — from a dab whose mask value
at that pixel was `0.00000000`. Under one `round_soft` dab on a black canvas, 625
pixels moved off zero where the tip only reaches 437.

**A colour below the floor could not be laid as written.** At any opacity. This half
was self-concealing: the canvas could never *get* below the floor either, so the first
half looked unreachable — which is what the M6b re-measurement concluded.

| | before | after |
|---|---|---|
| black pixel under a dab that misses it | sRGB 25 | **0** |
| the same, at a hundredth of a dab | sRGB 26 | **1** |
| `cadmium_yellow` laid opaque (swatch says blue 18) | blue 25 | **18** |
| a literal `#000000` laid opaque | grey 25 | **0** |
| `mix("cadmium_yellow", anything, 0.0)` | (255, 192, 25) | **(255, 192, 18)** |

## The fix

The clip stays on the K/S arithmetic, where finding 5 needs it, and comes back off the
mixture weighted by how much of each ingredient is actually in it. So `amount = 0`
returns the canvas and `amount = 1` lays the colour, both to the eighth bit of the
export, and a colour outside the band is carried through a mixture in proportion to
how much of it is there.

Two things this cost, both found by measuring rather than by reasoning:

* **Measuring the offset against `np.clip` is not good enough.** The K/S round trip
  lands a hair below its own input, so an offset that ignored it left a constant
  1.7e-6 gap in one direction on *every* blend. Sub-floor pixels leaked downward and a
  near-black went 23 levels adrift over 5000 dabs — a slow-motion version of the bug
  being fixed. The offset is measured against `_solo()`, what the round trip actually
  returns, so the two cancel.
* **The correction is skipped where the clip does not bite** (`_outside_band`). Not an
  optimisation for its own sake: computing it unconditionally cost 20% of the time to
  paint a picture, and it also made in-band work differ from pre-M8b by a few parts in
  a million, which would have moved images for no reason anyone could see. Gated, the
  common path is ~5% *faster* than before, because the incoming colour's K/S is now
  worked out on the `(3,)` colour instead of on a broadcast copy of the whole dab.

## Judged on the sampler and a real painting

The brief asks for both, looked at, before any golden moves. The first result is that
**nothing in the existing corpus moves at all** — the change is a strict no-op for any
colour inside the band, and every pigment but `cadmium_yellow` is inside it:

| | |
|---|---|
| the seven golden images | identical, no hash regenerated |
| `samples/brushes.png` (1802×2708) | byte for byte identical |
| `samples/shapes.png` | byte for byte identical |
| `m7/repaint.py` — the 295-stroke copy | byte for byte identical |
| `m7/repaint.py --own` — the 120-stroke painting | byte for byte identical |

`tests/test_floor.py::test_work_inside_the_band_is_bit_for_bit_what_it_was` keeps that
true, against the pre-M8b formula written out in full. To re-check the corpus by hand:

```
python scripts/make_brush_sampler.py     # then compare samples/brushes.png
python m7/repaint.py out.png             # and again with the change reverted
```

That settles what the change breaks — nothing — and says nothing about what it buys,
so `paint_the_dark.py` is a controlled pair *in the range the fix opens up*: the same
five masses as `m8/paint_two_ways.py`, same seed and same order of work, with a
painter-supplied `#060606` for the dark mass and cadmium yellow for the lit one.

```
  before   51 marks   darkest pixel sRGB  23   pixels at or under sRGB 16:  0.00%
  after    51 marks   darkest pixel sRGB   6   pixels at or under sRGB 16: 22.31%

  Inside the dark mass (31.9% of the picture):
    before  range  23- 40    18 distinct levels   at the old floor's value: 39.8%   local contrast 4.55
    after   range   6- 37    32 distinct levels   at the old floor's value:  2.9%   local contrast 6.06
```

**Looked at** (`compared.png`), and the gain is not that the dark is darker. It is that
the dark has a *surface*. Two fifths of that mass used to be pinned to one value, which
is what a hole looks like; the bristle comb's streaks and the linen tooth were being
crushed flat against the floor. They survive now — 18 levels become 32, local contrast
up a third — and the soft accents sit on the dark instead of in a grey fog of their own
bounding boxes. The cadmium yellow is a hair cleaner and, at seven levels of blue in a
colour whose red is 255, that half is nearly invisible; it is in the sheet because it is
the pigment the palette's own rule was written around, not because it is worth looking at.

## What this leaves for the guide

The floor used to be quoted as an engine limit — *"nothing in this engine reflects less
than `0.01` linear"* — in both `PAINTER.md` and `CALIBRATION.md`. That is no longer
true, and it was two claims wearing one coat: the box's mixtures bottom out around
`0.13` because of what is in the box, and the engine will lay whatever colour it is
handed. Only the first is a painting lesson. Both files now say so, and the advice they
give is unchanged: mix your darks, do not reach for a tube of black. `palette.py`'s rule
that a dark swatch must be written at or above the floor was a workaround for this
defect and is gone; what replaces it is `tests/test_floor.py` checking every pigment
against what the canvas actually receives.
