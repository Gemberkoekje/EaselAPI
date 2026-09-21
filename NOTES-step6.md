# Step 6 of `PLAN-0.6.0.md`, part two: `spill` (D1)

**To understand this, start by reading `_spill` and `_spill_over` in
[`src/easel/session.py`](src/easel/session.py) — the prediction, and the two gates in
front of it — then `_check_mass_spill` and `_check_band_spill`, which are the two places
it is said, then *Paint that lands outside the place* in
[`CALIBRATION.md`](CALIBRATION.md), which holds every number below, then the four tests
after the staircase ones in [`tests/test_requests.py`](tests/test_requests.py).**

Branch: `d1-spill`, off `main` at `ad4d947`. It also carries the three rulings the step
notes left for the owner, settled on 2026-09-21 — a separate change, recorded in the
plan's decisions table and in the *Open* sections of `NOTES-step7.md`, `-step8.md` and
`-step9.md`.

Part one of step 6 was `chisel-staircase` (#60). It left no notes file — its commit
message is its record — and no `CHANGELOG.md` entry, which the entry this step writes
covers for both D1 checks.

---

## What this step was for

Finding 8 and B17: *`scumble` and `cover` land well outside the place they were given* —
a water scumble covered part of the sky, a repair laid a flat patch in front of a tower —
and, checked while planning, a band crossed at 60 degrees paints 3.5x its own area with
nothing able to say so. The guide has named the mass half of this since shapes existed
(*the most expensive first mistake with shapes*, 72 strokes and one `undo`), and no
painter who hit it had read the paragraph.

## What landed

| | |
|---|---|
| `spill` at the call | a ragged `block_in` at `1.6x` its place (never inside `cover()`), and a banded `scumble` at `2.0x` unless the ends check already spoke; a planned band says it when `cost()` walks it |
| `_spill` | the prediction: the call's passes walked on a trial copy, each laid as a strip as far past its line as that tip's paint reaches, on a coarse pixel grid clipped to the canvas and to every hold |
| `_SPILL_REACH` | how far each tip's paint reaches, fitted on a bench of 150 calls painted for the purpose |
| three guide blocks | the value scale, the swatch strip and the per-stroke overrides example, which were all painting their neighbours |
| `PAINTING.md` | the spill paragraph is one line naming the code; the three answers stay |
| `CALIBRATION.md` | *Paint that lands outside the place*: the reach table, the pixel floor, the threshold, the three blocks, `cover()`, and B17's cap measured and declined |
| the probe | fires where the engine speaks, and goes on measuring the paint beside it |

## Decisions and gotchas

**1. The prototype measured the paint; the engine cannot.** Step 2's `spill` fired on
what a call *had* covered, read off the canvas after it. A check at the call has only the
passes, so it had to predict the same multiple — and a prediction nobody has held against
the paint is a number the tool would be making up. So a bench came first
(`spill_lab.py` in the session scratchpad, not committed): 150 masses, bands and burials
on three canvases, painted, measured exactly as the corpus replay measures a call, and set
against the passes each actually laid. Four families of tip fell out, each with its own
reach. The engine's raster was written separately from the bench's, and lands within half
a percentage point of the fit on every family.

**2. The plan's rule of thumb would have fired on the guide's first mass.** *A brush over
a fifth of the shorter extent* is what `PAINTING.md` says, and `PAINTER.md`'s first
`block_in` lays a brush 60% of its shape — and lands 1.48x of it. `mass-is-a-stroke` died
in step 2 of exactly this. The fraction does not paint the neighbours; the multiple does,
and the multiple depends on the overhang, the direction, the density and the canvas edge
as much as on the brush.

**3. Under twelve pixels the prediction is fiction.** The first fit's worst misses were
all tiny brushes: a 7 px `flat` predicted at 1.68x came back at 0.65x, a 10 px comb at
1.65x came back at 0.47x. A comb that narrow is a few streaks and a chisel lays next to
nothing (`chisel-blank`), so the paint never reaches its own outline, never mind past it.
Past the floor, the fit tightened from 11% to 5% on the comb.

**4. A comb that runs dry reaches less far than a solid one.** `0.90` of a half-brush in a
`block_in` at the preset's own load, `1.05` in a banded `scumble`, which has laid solid
since step 8. The solid figure was fitted on bands and borrowed for `solid=True` masses,
so it was checked on 90 more of those — 1.7% on average, 6.5% at worst.

**5. `cover()` is exempt, by `_call_verb`, and F1 is not decided here.** Its docstring
says it outright: *there is no warning on the plain form, because the overrun is the
recipe working*. The prototype fired on `PAINTER.md`'s own `cover(cell("D5"))` at 4.42x,
which is that rule firing on the canonical call. `block_in`'s checks run before its own
`_one_call`, so inside a burial `self._call_verb` is still `"cover"` — no signature moved.
The plan tied F1 (`cover()` to `edge="hard"`) to this step: *do it with the spill notice or
not at all*. The notice exists and is silent there by design, so F1 is now a clean
decision about the default alone, and it is the owner's.

**6. B17's open question is answered by measurement, and the answer is no cap.** Capping
the auto brush at the band's own depth leaves 2.22x at 30 degrees and 2.04x at 60; at half
the depth the passes stop overlapping and 3.2% and 15.8% of the band comes back bare.
The angle is the painter's and the gradient runs along it, so the remedy that keeps both
is the hold, and `edge="hard"` is named first.

**7. A band gets its own line, `2.0`, and the suite is what said so.** The first build
used the prototype's `1.6` for both, and the full suite failed three tests — all on bands
laid along their own axis with the verb's own brush, the case two of them assert is the
one to copy. A band's brush is three of its steps and breaks past the band by design, and
off-square the step is taken in the canvas's height while the brush is sized against its
long side, so in pixels it is more than three: the tuning band covers 1.69x at 320×240,
and a square in six passes 2.29x. Mapping bands by prediction (seven canvases, seven
places, six pass counts) put those laid along their axis at a median of 1.63x and the same
bands crossed at 30 to 60 degrees near 3x; `2.0` keeps three in four of the first silent
and tells 85% of the second. The quarter it still tells are squares given four to six
passes, which do lay a smear twice their size. A rule on the mechanism — *the brush is
wider than the band is deep* — was tried and missed angled squares at 3.2x–3.5x.

The third failure was `test_mcp.py`'s price-parity test reading the quote's first line as
the price: a quote puts what the walk said above the price, and the six-pass square now
says something. The test finds the price line wherever it is, which any later check that
speaks in a quote would have needed too.

**8. One notice per bloom.** At 60 degrees every pass is shorter than the brush and
`scumble-dabs` already says the paint blooms past the band. `_check_scumble_ends` now
returns whether it spoke, and `spill` stands aside when it did — two notices for one fault
is the noise the round is budgeted against.

**9. Rule 2 found three blocks, and the fixes were chosen on numbers, cheapest first.**

- *The value scale* laid `size=0.06` across bands `1/9` of a 900 px canvas and covered
  2.00x each: every band painted half of the one before it. Four fixes were measured.
  `direction="axis"` runs the passes along each tall band and lands 1.36x — and costs
  **27 strokes where the old block cost 189**, because horizontal passes on a canvas
  that is not square step in fractions of the *height* while the brush is sized against
  the long side (`CALIBRATION.md`, *Spacing, depth and how many passes*: *`block_in` has
  always mixed the two units the same way*). On 900×200 that put the passes 6.7 px apart
  under a 54 px brush. That mixing is untouched here — changing it would move every
  painting — but the exercise no longer pays for it.
- *The swatch strip* is laid solid, and running its passes vertically tripped `holes`:
  correctly spaced passes expose the tapered ends a chisel leaves, where the over-dense
  horizontal ones had buried them. `size=0.04`, a fifth of each swatch's width, lands
  1.45x with nothing said.
- *Per-stroke overrides* filled `cell("D5")` with a `flat` wider than the cell, 2.79x.
  The mass was incidental to the point of the block, and `span("C4", "F6")` lands 1.38x.

`edge="hard"` would have silenced all three for free, and was not used: the plan's risk
table warns that the remedies push towards cut-outs, and a worked example is an
instruction.

**10. What it costs.** Walking the passes takes a trial session — a copy of the canvas
channels — so nothing is walked unless the brush is over the pixel floor and the place's
box, grown by the furthest any pass of that brush can reach, is itself over 1.6x the
place. That bound is generous and an ordinary mass often passes it; the grid is then at
most 256 cells across, whatever the size of the mass. Timed on 1024×768, with a corpus
replay running beside it: a sky screened out costs nothing measurable, and a mass that
is walked — silent or told — about 6.5–7 ms, against the seconds its passes take to
paint.

## Open, and for the owner to rule on

**F1** — `cover()` to `edge="hard"` by default. Nothing in the engine waits for it now.
The probe question the plan wrote for it is unchanged and unmeasured: *does a hard-edged
repair read as a cut-out patch on a worked passage?*

**The inset remedy can be told off.** The check sees the place it was handed, and
`Polygon.inset()` keeps no record of the shape it came from, so a mass inset by half a
brush that is itself a large share of the mass is measured against the inset shape. At
the guide's own numbers it is silent (1.44x), and a test holds that; a much larger brush
inset the same way would be told it spills onto the outline it was inset to reach.
Fixing it would mean a field on `Polygon`, which rides in the log.

**`Region.inset` works in canvas fractions on each axis**, so *inset the place by half the
brush* is exact only on a square canvas; off it, the short axis is inset a little less
than half a brush. The notice keeps the guide's words rather than a second rule.

## What step 6 did *not* touch

D2 (`glaze-far`, `smudge-across`, `smudge-long`) and D3 (`radiating`, `one-loop`,
`buried`) are not started, nor the tier-3 rows. `inset-lost` is still unbuilt, so the
`inset` paragraph under *Masses that are not rectangles* stays whole.

## File map

| File | What changed |
|---|---|
| `src/easel/session.py` | `_SPILL_RATIO`, `_SPILL_RATIO_BAND`, `_SPILL_MIN_PX`, `_SPILL_REACH`; `_spill_reach`, `_spill`, `_spill_over`, `_shorter_side`, `_check_mass_spill`, `_check_band_spill`; `block_in` says it outside `cover()`; `_scumble_paths` takes `held=` and says it unless the ends check did; `cost()` hands a planned band its hold; `_check_scumble_ends` returns whether it spoke |
| `src/easel/notices.py` | the `spill` code |
| `tests/test_requests.py` | four tests: the band, the planned band, the mass and its three answers, and the cases that must stay silent |
| `tests/test_mcp.py` | the price-parity test finds the price line below whatever the walk said |
| `REFERENCE.md` | the `spill` row in *What the tool will tell you* |
| `CALIBRATION.md` | *Paint that lands outside the place* |
| `PAINTING.md` | the spill paragraph cut to one line; the overrides example fills `span("C4", "F6")` |
| `PAINTER.md` | exercise 1 runs its passes along the bands; exercise 9 lays `size=0.04` |
| `scripts/probe_cohort_session.py` | `spill` fires where the engine spoke and keeps measuring the paint; the noise table knows the notice |
| `CHANGELOG.md` | *Two checks at the call, off the geometry of the passes*, for both D1 checks |
| `SUGGESTIONS.md` | finding 8's row gains what landed |
| `PLAN-0.6.0.md` | status; B17 settled in section 8; the migration and F1 rows |
