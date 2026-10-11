# The Curator: how this was filed

*The filer's account of the set. The painter left no notes of its own beyond
[`README.md`](README.md), which is filed as it wrote it for its game's repository; its
paths (`game/art/easel/`, `game/art/painted/`, `docs/QUESTIONS.md`, and the scripts under
`tools/easel/`) are that repository's. **Each piece is a painting of its own here**, in its
own folder with its script, `painting.png` (its export), `painting.gif` (a time-lapse the
filer's re-run recorded) and a short `NOTES.md`, because the corpus probe replays one
canvas per painting.*

## What this is

Nine pieces of interim art for the owner's own game, *The Curator*, painted against 0.8.0
on 2026-10-11 between 01:52 and 04:12 UTC by `claude-opus-5-5` at max effort, in a cloud
session of the game's repository. They stand in until the designer's photographed oils
arrive. Each piece is one script, seeded, with a stage argument; stage 99 writes the
shipped PNG.

| piece | script | canvas | budget | spent |
|---|---|---|---|---|
| the room seen through the doorway | `beyond_doorway.py` | 560×600 | 150 | 123 |
| the desk | `desk.py` | 1920×720 | 170 | 103 |
| the counter | `counter.py` | 1920×360 | 120 | 78 |
| the left bookcase | `shelves.py left` | 640×720 | 460 | 410 |
| the right bookcase | `shelves.py right` | 640×720 | 460 | 388 |
| the locked case | `locked_shelf.py` | 300×460 | 240 | 211 |
| the doorway wall, the arch cut out | `doorway_wall.py`, then `cut_arch.py` | 1920×720 | 320 | 245 |
| the hooded patron, cut out | `patron_default.py`, then `cut_outline.py` | 400×620 | 160 | 95 |
| the candle, cut out | `candle.py`, then `cut_outline.py` | 120×300 | 110 | 47 |

1,700 strokes over the nine, of 2,190 budgeted. Every checklist is in
[`reports.txt`](reports.txt). `set.png` is the nine together
on a grey ground, for `PAINTINGS.md`. Each folder's `painting.png` is the export as the
painter's run left it; the three cut-outs' shipped files sit beside theirs
(`wall/doorway_wall.png`, `patron/patron_default.png`, `candle/candle.png`), with the alpha
channel the painter's own scripts cut. The wall's export is the copy from its repaint after
the review: the working copy left in its scratch folder is the earlier run, 86 pixels
from what shipped.

## The evidence, and what is missing

- **The painting session's transcript is not here.** The session ran in the cloud, and
  asked for its evidence it pushed a branch to the game's repository with everything its
  scratch folder held and a manifest, but declined to copy its transcripts. So, unlike the
  last rounds, nothing here was recovered from the session's own words: what it read and
  what it ran come from its manifest, and the versions it threw away do not exist (it
  edited each script in place).
- **Its manifest, in short.** It read `easel guide` (the card, 119 lines) and most of
  `easel guide --full` (`PAINTER.md`, 767 lines; lines 1-119 only by grep); parts of
  `RECIPES.md` (lines 35-92, 271-301, 572-620, 735-787, 852-895); and `REFERENCE.md` for
  the lines matching *direction* only. It read `block_in`, `scumble`, `sweep`, `cover`
  and `glaze`'s signatures from `session.py`, and `ribbon`, `polygon`,
  `PRESSURE_PROFILES`, `PIGMENTS` and `catmull_rom` through `inspect`. It never opened
  `PAINTING.md`, `CALIBRATION.md` or `DIAGNOSIS.md`. **It called `s.checklist()` at
  stage 99 of every script and never called `s.report()`, `cost()`, `easel run` or
  `easel check`**: it painted without rehearsal, the check, or the price, by re-running
  each script and looking at the stage images.
- **Its run logs were lost on the way**: the game's repository ignores `*.log`, so the 16
  logs its manifest lists never reached the branch. The scripts are seeded, so
  [`reports.txt`](reports.txt) is the checklists re-run here.
- **`beyond/scratch/`** holds the drawing and swatch tests its manifest lists for the first piece
  (`p0.py`, `swatch.py`, with what they drew). **`evidence/`** holds two of the crops it
  made to check the desk's knots and the candle.

## What filing found

Measured on 2026-10-11 on this checkout, whose engine is `v0.8.0`'s.

- **The pieces rebuild, but not to the pixel here.** Every script re-run at stage 99 comes
  back within one level of the shipped PNG, and differs in 12 (the candle) to 2,508 (the
  wall) pixels, each by exactly one level. The painter's machine was Linux, this one
  Windows; `tests/test_golden.py` already allows a numpy build to round a few pixels ±1,
  and no document a painter reads says so.
- **Six of the nine say *no clear light*** (the counter, the wall, the locked case, the
  patron, both bookcases). Every one names a light in its plan and none declares a key.
  None of the six has a light standing clear of the rest (from -0.01 to +0.07 by the
  shipped PNGs), so 0.9.0's planned line naming a planned light would stay silent; but all
  six keep their top twentieth under the box's middle, `0.54`, so `plan(key="low")` would
  have said *low-key, as the plan says*.
- **The candle's checklist reads the part the cut throws away**: 67% of its canvas still
  bare ground, *detail before the masses are down*, five discs at the flame. The patron's
  reads 25% bare ground.
- **The candle's shading was a brush under its landing width**, not an opacity. On the
  120×300 canvas, the sprite's own size, `size=0.009` is 2.7 px; one wax-light stroke at
  opacity 0.6 moved its pixels a mean 6 levels, 14 at 0.9 laid twice. The same stroke at
  four times the canvas is 10.8 px and moves 17 levels at 0.6, once.
- **Umber and ultramarine cross neutral into violet.** Burnt umber alone is hue 17°; with
  10 to 18% ultramarine the mix stays a red-brown, at 25% it is a neutral leaning magenta,
  at 35% violet (276° to 320°), its chroma falling all the way. `at_value` re-solves the
  value whatever white was mixed first, so *lightened with white* returns the same hex.
  The committed stones carry yellow ochre and 4 to 6% ultramarine: the fix it found.
- **The reference it asked for exists.** `REFERENCE.md` gives `ribbon()`'s width (line
  24), the pressure profiles' names (203), `density` as *spacing, not coverage* (126),
  `solid` (127), `opacity` as per-dab strength (135) and a brush table (183); `easel guide
  --reference` prints it. The card mentions `REFERENCE.md` once, for the plan, and never as
  the place for signatures and units.
- **The engine spoke at the call on three pieces**, as warnings on every run: a pressure
  list on a bristle (the room beyond), a mass spilling 40% and 62% of its paint outside
  its place (the desk's and the counter's grain), a planned pair reading as one, and a
  solid comb twice (the patron). Six pieces ran with nothing said at the call.
- **The messages it praised are the engine's**: the floor with a hex and a hue
  (`palette.py`), and `press`, documented as *for a one-point mark*.
