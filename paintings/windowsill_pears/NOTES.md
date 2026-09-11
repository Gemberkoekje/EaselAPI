# Three pears on a kitchen windowsill

A painting made from `PAINTER.md` alone, with no reference photograph. The subject was
chosen before the guide was read: three ripe pears on a kitchen windowsill in
late-afternoon light, a chipped blue enamel mug behind them, a half-drawn curtain at
the right, the sun coming in low through the window.

- Canvas 1024×768, linen, `toned_warm_grey` ground, seed 11.
- **224 strokes**, plus two signature marks that did not count.
- Final painting: `painting.png`. Time-lapse: `painting.gif`.
- The scripts `p0_plan.py` … `p16_finish.py` are the whole painting in order; run them
  against a fresh `easel new painting.easel --size 1024x768 --texture linen --ground
  toned_warm_grey --seed 11` to regenerate it. `pears.py` builds the pear silhouettes
  and the shading recipe; `helpers.py` mixes a colour to a planned value.

## No assisted modes

There was no reference, so `prepare`, `sketch`, `ref_shape` and `ref_outline` were not
used. Every outline is a polygon built from two circles and a waist (`pears.py`), a
rectangle, or points chosen by hand. `preview`, `rehearse` and `cost` were used before
the pears went on; nothing else was traced.

## The plan, and what it cost

Values were planned as numbers first (`p0_plan.py`): window 0.82, curtain 0.70, sill
0.62, wall 0.48, wall below the sill 0.30, pears 0.34 with a rim at 0.63, mug 0.36.
The greyscale looks kept those five steps separated all the way through.

The split written down before the first stroke was: surroundings up to 80 strokes,
subject about 130, refinement and highlights the rest. What was spent:

| Stage | Strokes | Share |
|---|---|---|
| Block-in of window, walls, curtain, sill, shadows, and their corrections | 96 | 43% |
| Subject: mug 14, pears 66 | 80 | 36% |
| Surroundings again: sun in the pane, curtain folds, sill light, shadow tails | 37 | 16% |
| Edges, highlights, the curtain's shadow on the sill | 11 | 5% |

The subject was reached at stroke 91 with two thirds of the budget in hand. The
surroundings overran their share because five masses were repainted while nothing stood
on them yet, which is the cheap moment the guide describes: the curtain (a stripy
saturated yellow, redone quiet and grey with a flat brush), the sill (too orange, then
its top edge, twice), the cast shadows (black slugs at 0.30, redone at 0.45), and the sun
in the pane (four hard-edged diagonal bars, buried and redone as one soft-edged region).

## What went right

- Back to front throughout. Every edge on the pears and the mug is where their paint
  stops and the pane or sill still shows; nothing was cut around anything.
- The mug's opening was painted as three depths, far lip, dark inside, near lip, and
  reads as a hollow.
- Pear 1 was painted once as a mid-value mass with a dark stroke and a yellow stroke
  laid on it, which read as marks on a mask. Two rehearsals later the recipe became a
  body in shadow, a soft reflected light underneath, a narrow rim on the window side,
  and one sweep of the body colour round the outline to smooth the scalloped edge.
  That recipe painted all three pears.

## What still bothers me

- The three rims are three similar yellow stripes. Varying the lying pear's rim helped
  less than hoped.
- A spray of dark dots sits outside the pears' contours on the pane; a cleanup stroke
  nicked pear 1's shoulder and had to be filled.
- The curtain folds are dotty bristle bands, and the lit patch on the left of the sill
  still shows the bands it was laid in.

## The signature

Two marks in the lower-right corner, a step lighter than the wall they sit on: a short
chevron laid with a `lift_off` pressure, and a dot. The chevron is a stroke that lands
and lifts, which is the one thing about a mark this guide kept coming back to; the dot
is the smallest mark the engine makes. Neither is a name, and neither is a repair.
