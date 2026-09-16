# Painting notes — landscape with mountains at sunset

## Why this subject

A mountain landscape at sunset: three values in one scene (dark ridge, flat
foreground, warm sky) that test the graded-field recipe, and a horizon that
breaks the horizontal bands instead of stacking them.

## Order of work (back to front)

1. Graphite underdrawing: three closed outlines (far mountain, near mountain,
   foreground hill) on a toned-grey ground.
2. Sky, as a graded field in three scumbles: deep blue at the top grading to
   warm orange at the horizon, plus two starved cross-strokes so the field is
   not a band.
3. Far mountain mass, `mountain_dark`, swept along its own axis.
4. Near mountain mass, `mountain_mid`, swept at -15 degrees, plus a sun-lit
   slope blocked in with a hard edge.
5. Foreground hill (`ground`) and a lit foreground patch.
6. Sun dab + soft glow.
7. Edge work: two smudges along the ridgelines.
8. Highlights: two small dabs and one warm bristle pass.

## Budget split

- Planned: 120 strokes.
- Spent: 50 of 120 (42%): ~10 drawing-free anchors invisible to the budget,
  12 sky, ~12 mountains, ~10 foreground, ~6 accents.
- 70 strokes remain. The weakest passage would want them (see below).

## Values

- Sky light: ~0.7 (near the sun). 
- Mountain mid: dark.
- Foreground: mid-dark.
- Clear light / clear mid / clear dark were the aim; the greyscale controls
  (`s.look(values=True)`) were used between passes.

## What went wrong / what the check said

`report()` over the whole painting, 50 marks:

- **Stack of bars**: 30 of 44 long marks run within 6 degrees of horizontal,
  from 10 calls. The sky scumbles ran at 4/3/2 degrees (fine), but the block-in
  passes and cross-strokes drifted nearly horizontal. Fix would be steeper
  `direction=` per mass — the sky scumbles, in particular, want a few degrees
  off the frame.
- **Bare ground**: 31.94% of the canvas is still bare ground. Density was left
  at 0.5 on the sun-lit and foreground patches deliberately, but the mountains
  at 0.85 left more tooth showing than intended.

## Honest assessment

Painted blind: the painter (an LLM) could not open `out/look_*.png` between
passes, so "look every 5 to 15 strokes" was obeyed in spirit but not in fact.
The composition followed the method and the graded-field recipe, but the value
bands and the mountain edges were guesses. The tool's own check catches a real
fault — the near-horizontal passes — that a painter with eyes would have caught
much earlier.

## Assets

- `sunset_paint.py` — the painting script (deterministic from `seed=42`).
- `sunset.easel` — the session; repaint it and `timelapse_gif` reproduces the GIF.
- `painting.png` — final export.
- `painting.gif` — the timelapse (8 fps).
- `out/` — progress looks (`look_001..009.png`).

To understand the painting, start by reading `sunset_paint.py`, then poke at
`sunset.easel` with `easel look sunset.easel --grid`.