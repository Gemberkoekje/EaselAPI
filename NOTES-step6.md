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
| over the corpus | 18 calls in 13 of the 325 painted passes, **4%** — the prototype's own share — and none of the guide's 71 runnable blocks; the median pass still prints nothing |

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

**Four of the corpus's eighteen fires measured under the line.** Where `spill` spoke, the
paint measured a median of 1.71x, but on four calls 1.23x–1.58x — two in the sonnet's
beam, the greenhouse floor's band (predicted 2.2x, measured 1.23x), a pier mass. The
replay counts a pixel as painted when its value moved by more than `0.004`, so paint laid
on paint of its own value is invisible to it and the measured multiple is a floor. That
those four are such cases is a reading, not checked call by call. If they are, the
question is whether a spill onto paint of its own value is worth saying at all — which
needs the canvas under the footprint, and is D2's to ask, not D1's.

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

---

# Step 6 of `PLAN-0.6.0.md`, part three: the canvas under the mark (D2)

**To understand this, start by reading `_smudge_samples`, `_smudge_crossing` and
`_check_smudge_path` in [`src/easel/session.py`](src/easel/session.py) — one reading of
the canvas along the path, and the two things said from it — then `_film_shift` and
`_check_glaze_far` beside them, then the fix at `tasted` in
[`src/easel/stroke.py`](src/easel/stroke.py), then *Across a boundary, and along a long
one* and *A film far from what it lands on* in [`CALIBRATION.md`](CALIBRATION.md), then
the D2 tests after the `spill` ones in [`tests/test_requests.py`](tests/test_requests.py).**

Branch: `d2-canvas-checks`, off `main` at `54d0d7d`.

---

## What this step was for

Workstream D2: the three checks step 2 left standing that read the canvas a mark meets.
`smudge-across` and `smudge-long` for finding 3 and the winter greenhouse's strips,
`glaze-far` for finding 4. `wet-under` and `ring-rim` were dropped in step 2 and
`smudge-again` is tier 3; none of them is built here.

## What landed

| | |
|---|---|
| **fixed: a smudge started loaded with white** | `paint_stroke` gives a pure smudge nothing of its own to carry until its first dab has tasted the canvas; the three `marks` goldens and the brush sampler moved with it, looked at and regenerated |
| `smudge-across` (fact) | a path crossing a step of `0.10` or more, arriving from one mass and going on into the other; 11 of the corpus's 37 smudges, 9 of 325 passes, no guide block |
| `smudge-long` (habit) | a path following a step of `0.05` or more for more than `0.10` of the canvas; 14 smudges, 11 passes, no guide block |
| `glaze-far` (fact) | a film that moved the value `0.08` or more (not said about `to_value=`), or was mixed `0.07` or more from what it lands on in Oklab *a/b*; 38 of 222 films, 17 passes, no guide block |
| the guide | `PAINTER.md` step 6's three rules about `smudge` are one paragraph naming the codes; the edge-study exercise shows the three edges it promises; `RECIPES.md`'s strip paragraph is a line and its block smudges a stretch; `PAINTING.md`'s glaze table is a line and its example is mixed from its field |
| `CALIBRATION.md` | the two new subsections; the finding-3 claim row and two older `smudge` bullets corrected |
| the probe | the three prototypes fire where the engine spoke and go on measuring their own numbers beside it; the thumbprint probe says what it used to measure |

## Decisions and gotchas

**1. Half of finding 3 was the engine, and it was found by looking.** Crops of every
smudge in the corpus, before and after, showed a light cap at one end of nearly all of
them — including two passes run down the middle of a *uniform* dark pile, where there
was no light mass to drag. A smudge's carried colour began as its nominal
`titanium_white` and mixed only 45% of the canvas in per dab. **The round's own probe had
measured that bug as the fault**: `probe_smudge_thumbprint` runs its *across* pass from
inside the dark and counts light lifted in the dark, and got `4.1` brushes — the cap,
laid from the first dab on. It reproduces exactly without the fix and reads `0.5` with
it. The measurement was right; it was measuring the engine. `CALIBRATION.md`'s first
`smudge` bullet (*it pulls the lighter mass into the darker more than the reverse*) does
not reproduce either — `0.49` brushes each way on a dried step, on 0.5.0's engine as well
— and it recorded no conditions, so it now says what was measured.

**2. The prototype `smudge-across` was wrong in both directions.** It compared the range
of every value under the path with the mean step across it, which fired on both heron
necks — passes run *along* a lit edge striped with short marks, where the range is the
stripes — and missed the one pass that dragged a dark hull out into the water. The
engine locates each crossing instead: where the step runs along the path, is bigger
than the step across it, and has path on both sides.

**3. Where the line is had to be found between samples, and a test caught it twice.**
A step shows in every sample within half a brush of it, so neither *the first sample to
see it* nor *the middle of the run* nor *the steepest pair* is the boundary — the second
and third were each one sample off with the 5 px blur, and one sample was the whole
margin of the *stopping on the line* test. The line is where the value on the path
passes halfway between the two masses, read half a brush behind and ahead of the run's
strongest sample; a symmetric blur of a step crosses its halfway value on the edge. The
margins — half a brush before, a quarter after — are what the hull needed and what a
pass that only stops on the line does not have.

**4. `smudge-long` on bare length was a rule against smudging.** The corpus's median
smudge is `0.168` long and the prototype fired on most of them. What leaves a band is a
long pass *along a boundary*, so that is what it counts; and the band reads at a much
smaller value step than a grey step suggests, because a join between two colours `0.07`
apart still leaves a strip of a third colour — hence a follow step of `0.05`, half the
`0.10`. The `0.10` of length stayed: along a hard step the strip is a pill at `0.05` and
a drawn line from `0.10`, rendered and looked at.

**5. The guide's own examples ran the smudges the rule is about, and the edge study showed
neither of its edges.** `RECIPES.md` smudged half the canvas directly above its paragraph
saying a tenth; `PAINTER.md` step 6, a third. Both smudge a stretch now, one as a slice of
a shape's own outline (`mass.closed[3:5]`, one side, `0.08` on the guide's `mass`). The
guide-block run could not find either — a blank canvas has no boundary to follow — so
they were found by reading the blocks against the rule, which is finding 1's lesson again.
Exercise 5 was worse: its *soft* edge was a smudge 20 px inside the light panel (the
bristle mass spills past its region), and its *hard* edge a line in the panel's own
colour, so it rendered one boundary and a lost edge. It now lays the light panel with
`edge="hard"`, the hard line across the dark panel, and a short smudge on the boundary.

**6. For a film, the distance is in the mixing and not in the result.** The value shift
alone missed both films the cohort described — the harbour's searchlight moved the value
`0.020`, and the corpus's worst bloom, an orange glow on a violet sky, `0.061`. Measured
next was how far a film moves the *hue*, and it does not separate: the lit-air recipe's
own film moves it `0.018` and the searchlight `0.026`, and the guide's own table explains
why — the far film moves it `0.034` at the opacity the table calls *already neutral* and
`0.057` where it calls it *warm*. What is wrong at every opacity is where the film was
mixed. The recipes mix their films `0.031`-`0.051` from the field; every bloom is `0.080`
or over.

**7. `to_value=` answers one line and not the other.** An aimed film asked for its value
shift, so the value line is not said about it. The mix line is: the search lands a value,
and the colour is still the film's. The corpus's thirteen aimed films are all mixed
`0.033` or closer, so this costs nothing today.

**8. The solver's films needed a flag of their own.** `glaze(to_value=)` lays up to twelve
films on trial copies; each is a hand-laid glaze on a session whose notices are thrown
away but whose warnings are not. `Session._solving` keeps them quiet. Replays needed
nothing: they lay inside `_one_call`, where no hand-laid check runs.

**9. A guide example must not sit on its own threshold.** `PAINTING.md`'s rewritten glaze
first mixed 30% alizarin into its field, which moved the value `0.079` against `0.08`.
It mixes 15% (`0.045`, mixed `0.028`).

**10. The goldens moved and were looked at before regenerating** (`LESSONS.md` trap 2).
The fix's effect is confined to each smudge's box: in the `marks` cases a whitish patch
at the smudge's start becomes the ochre that is there; in the sampler the caps were white
on white and barely show. `scripts/make_golden.py` writes `hashes.json` with CRLF on
Windows, which git normalises and warns about; it was converted by hand.

**11. A smudge's no-effect size is a pixel width, so no size floor was added.** The
calibration's *does nothing below about `0.014`* was measured on 640x480; the
laundromat's `0.011` on 1024 wide moved 1,337 px, and `smudge-long` is right to speak
there.

## Open, and for the owner to rule on

**The replay promise.** The smudge fix moves the first brush-width of every smudge,
including one already saved in an `.easel` file, and `CHANGELOG.md`'s preamble says a
saved file *always replays as it was painted*. The entry says so; the preamble is
unchanged. An exception for a stroke the engine laid wrongly, or a 0.5.0 file replaying
its smudges the old way, is the owner's call, and it is in the plan's *Still open*.

**`wet-under`'s fact line** — step 2's *what is left is a fact line at the call* — is not
built here and nothing in the plan owns it now.

## What step 6 part three did *not* touch

D3 (`radiating`, `one-loop`, `buried`) is not started. `smudge-again` is tier 3, so
`PAINTER.md`'s *one pass, not three* stays. The golden fixtures' own raw-pigment glazes
now warn in the test output, as their pinned `0.06` smudge already would unfiltered.

## File map

| File | What changed |
|---|---|
| `src/easel/stroke.py` | a pure smudge carries nothing of its own until its first dab (`tasted`) |
| `src/easel/session.py` | `_SMUDGE_STEP`, `_SMUDGE_LONG`, `_SMUDGE_FOLLOW`, `_box_mean`, `_SmudgeRead`, `_smudge_samples`, `_smudge_crossing`, `_check_smudge_path`; `_FILM_FOOTPRINT`, `_FILM_NEW_MASS`, `_FILM_FAR`, `_film_shift`, `_check_glaze_far`; `smudge()` reads its path first; `stroke()` keeps a film's box and measures it; `glaze()` says it is the caller and whether it was aimed; `_film_call` and `_solving` on sessions and trial copies |
| `src/easel/notices.py` | `smudge-across`, `smudge-long`, `glaze-far` |
| `tests/test_requests.py` | five tests after the `spill` ones: the fix, both smudge checks, the film and the two films it leaves alone |
| `tests/golden/*`, `samples/brushes.png` | the three `marks` cases and the sampler, regenerated after looking |
| `REFERENCE.md` | three rows in *What the tool will tell you* |
| `CALIBRATION.md` | *Across a boundary, and along a long one*; *A film far from what it lands on*; the asymmetry and across bullets; the finding-3 claim row |
| `PAINTER.md` | step 6's smudge rules as one paragraph and a stretch; the edge-study exercise |
| `PAINTING.md` | the glaze table as a line; the example mixed from its field |
| `RECIPES.md` | *An edge that is actually lost*: a stretch, and the strip paragraph as a line |
| `scripts/probe_cohort_session.py` | the D2 prototypes fire where the engine spoke; `_RULES` knows the three; the thumbprint probe's reading |
| `CHANGELOG.md` | *Three checks that read the canvas under the mark, and a smudge that lays nothing of its own* |
| `SUGGESTIONS.md` | findings 3 and 4 gain what landed |
| `PLAN-0.6.0.md` | status; the three D2 rows; three migration-map rows and the stale `spill` one; the replay question in *Still open* |
