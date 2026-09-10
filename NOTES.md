# Phase notes — scaffolding, M4, the M5 rehearsal twice, M6's tools and final pass, M7, M8's shaped masses, and M8b's floor

**To understand this, start by reading `painting-api-brief.md` (the spec), then
`REHEARSAL3.md` (the M6 final pass — the most recent *measurement*, and it says what
is still wrong), then `M7.md` (the most recent *change*: what a mark looks like now),
then `REHEARSAL.md` and `REHEARSAL2.md` (the two M5 rehearsals),
then `PAINTER.md` (what a fresh agent is given) and `CALIBRATION.md` (the measured
numbers the guide no longer carries), then `src/easel/session.py` (the object
everything goes through), then `src/easel/stroke.py` and `src/easel/canvas.py`
(where the marks actually happen).**

Status: **M1–M5 done. M7 done — `M7.md`. M6's tools are built and its protocol has
now been run — three fresh sessions, `REHEARSAL3.md`. M6 is not done: the copy passes
on recognition, stroke budget and rejected marks, and fails the `0.10` number.** Five
of the seven failing cells were the painter's own, all in the same direction, and
the fixes they point at are now in the guide. A guide fix is a hypothesis until a
fresh session paints against it, which is what `REHEARSAL.md` → `REHEARSAL2.md`
established, so **M6 wants one more run on the mug and one narrow question: does the
value error go away?** See *What to do next*.

The final pass also produced three engine changes (`REVIEW.md` 20–22, all additive —
no golden image moved) and two findings from the human that account for more of
what is wrong with these paintings than anything the three sessions reported: every
mass is laid along the canvas's axes, and nothing ever said to paint back to front.
Both are written up in `rehearsal3/HUMAN_NOTES.md` with their probes.

**M7 (marks at detail scale) is done** — `M7.md`. The bristle comb is drawn per
stroke and a bristle has a width of its own rather than the brush's; width follows
pressure on the round tips, so a lid line tapers in one stroke instead of two; and
`dab(press=n)` lands a catchlight in one mark. Judged on the sampler and on the M6
headline painting repainted by both engines, then the goldens regenerated once. The
one thing it makes harder is in `M7.md`'s *The trap, stated plainly*: a lone
`s.dab()` is a light touch and now lands at about half the width asked for.
**M8 (non-rectangular masses) is done** too — a place can now be a shape, and
`block_in` fills one, which is the largest open item the unprompted stage pointed
at; see *M8 — shaped masses* below. It arrived beside M6c, and the two are
complements rather than alternatives: fill a silhouette you can name, sweep a
boundary you have read.

**M8b (the wet-blend reflectance floor) is done**, which closes the last engine item
in front of the server and the last entry in `REVIEW.md`'s *Open, with evidence*. The
floor from finding 5 was clipping the *answer* and not only the mixing arithmetic, so a
pixel with no paint landing on it still moved and a colour under the floor could not be
laid at all; see *M8b — the floor off the answer* below. M9 (MCP) is untouched and
correctly last, and everything before it is now done.

The M5 rehearsal was run twice. The first (`REHEARSAL.md`) was run by the engine's
author: the unprompted painting went well, the **copy did not reach a likeness**,
and the guide was substantially rewritten; four engine defects came out of it
(`REVIEW.md` 15–18). The second (`REHEARSAL2.md`) was the measurement the first
could not be — a fresh session with the revised guide, the same reference and no
source — and its **copy reached the bar**: a recognisable copy of the scene in 253
strokes, though not a portrait likeness. Nine more guide gaps and two small engine
additions (`span()`, enlarged crops) came out of that.

---

## What exists

| Milestone | State |
|---|---|
| M1 Foundation | Done. Canvas, round brushes, curved strokes, `look()`, PNG export, seed, sampler sheet. |
| M2 Painterly | Done. Flat/bristle/knife with direction following, paint load and run-out, texture modulation, wet blending, `dry()`, pigment mixing, palette. |
| M3 Composition | Done. Regions, grid, relative placement, stroke-based block-in, values view, side-by-side, diff, history, time-lapse. |
| M4 CLI and guide | Done. CLI, `PAINTER.md`, install, and the adversarial review the brief asks for after M4 — four defects found and fixed, see `REVIEW.md` findings 11–14. |
| M5 Rehearsal | Done, twice. First run (author): copy fell short, ten guide gaps and four engine defects fixed — `REHEARSAL.md`. Second run (fresh session, revised guide): copy recognisable at 253 strokes, unprompted painting at 133; nine more guide gaps, `span()` and enlarged crops — `REHEARSAL2.md`. |
| M6 Precision | **Tools done, protocol run, not passed.** Golden images first (they found REVIEW 19 on their first run). Then the `sketch` graphite channel, landmarks, matching crops with `grid="fine"`, `preview()`, `rehearse()`, `compare()`, `prepare()`, the `liner` preset, six CLI verbs, the guide's drawing step. `REHEARSAL3.md` ran the protocol three times over: the tools **do** reach below a cell — the sitter has an eye with a lid, an iris and a catchlight where REHEARSAL2 had a smear — and the copy stage still fails on value. Findings 20–22 and eight guide edits came out of it. |
| M6b Darks | **Done.** The six darks are tube masstones now, so the box floors at `0.13` rather than `0.235` and `mix("ultramarine", "burnt_umber", 0.5)` reads `0.137` against the model's own `0.10` (`REVIEW.md` 33 has the before/after table). The mixing exponent moved `0.5` → `0.35` to keep white's tinting where finding 6 set it against the wider range. Exercise 1 mixes to a value instead of a ratio and its nine bands are even to `0.002`. Every golden regenerated once, looked at first. Item 11 re-measured: it does **not** move up. |
| M6c Sweep | **Done.** `s.sweep(edge, ...)`: passes swept along a hand-given boundary and stepped inward, `cross=` for the second set, `closed=True` for a boundary that comes back on itself (`REVIEW.md` 34). Ordinary strokes, so undo and replay came free. Additive: no golden moved, one added — and regenerated once when M6b's darks landed under it, geometry identical. The recipe is out of `CALIBRATION.md`, and it takes a shape as its edge (M8). |
| M7 Marks at detail scale | **Done** — `M7.md`. Comb drawn per stroke (two marks of one brush were identical to the last bit); `BRISTLE_PITCH` gives a bristle a width of its own, 4 at `size=0.02` and 36 at `size=0.18` where it was 22 at every size; width follows pressure on the round tips (14 px at pressure 0.1 against 36 px at 1.0), oriented tips keep their chisel; `dab(press=n)`. Judged on the sampler *and* on `rehearsal3/pass` repainted by both engines — the same 295 marks, and the whole picture's mean value moved by less than a hundredth. Every golden regenerated after looking. |
| M8 Non-rectangular masses | **Done.** `Polygon` is a place beside `Region`, built with `polygon`, `ellipse`, `blob`, `hull` or `ribbon`; `block_in` cuts every pass against the outline, so a shaped mass keeps its silhouette and a concave one keeps its bite. `direction="axis"` sweeps along the mass's own long axis. `dry`, `erase`, `look`, `compare`, `preview`, `rehearse` and `sweep` all take a shape. Additive: no golden moved, one was added. Evidence in `samples/shapes.png` and `m8/`. |
| M8b Wet-blend floor | **Done.** The K/S clip stays on the arithmetic, where finding 5 needs it, and comes back off the mixture weighted by how much of each ingredient is in it: `amount` of 0 returns the canvas and 1 lays the colour. The brief expected this to change every soft dab edge in the engine; it changes nothing inside the K/S band, so both samplers, both real paintings and all seven goldens are byte for byte identical and none was regenerated. What it buys is in `m8b/` — a dark mass built from 32 levels rather than 18, with two fifths of it no longer pinned to one value. `REVIEW.md` 35. |
| Post-M8b adversarial code + general review | **Done.** Fourteen independent readers over every module not code-reviewed since M6 (`regions.py`'s shape/sweep code, the painting-ops half of `session.py`, M7/M8b's `brush.py`/`stroke.py`/`color.py`), plus a general pass beyond the brief's own framing: security/trust boundaries, `.github/workflows/ci.yml`, `pyproject.toml`, and whether the test suite proves what it claims to. 37 of 38 candidate findings survived independent adversarial verification; 34 fixed, 3 left open with the reasoning for why (`REVIEW.md` findings 36–66, and *Open, with evidence*). One rendering change (`draw_pencil`'s sub-pixel anchor, finding 49) judged on the `drawing` golden before regenerating it; the shape sampler's `cross` column bug (finding 66) regenerated and looked at. Every other fix is pure robustness/security/CI/test-coverage — no other golden moved. |
| Pre-M9 engine changes | **Done** — `engine_changes/`. The brief's rule is that anything changing the API lands before the server exposes it, and `ENGINE_CHANGES.md` was that list. `blob(region, radius)` was a 4.9 : 1 horizontal sausage because the point branch and the region branch disagreed; one radius now means a circle wherever the shape is put, which moved no golden and no call in the corpus. `rehearse()` takes a `sweep` (`edge=`) as well as a `block_in` (`shape=`, which M8 had already added and the request did not know about), and the trial session now holds a *copy* of the real stream state, so a rehearsed mass is pixel-identical to the painted one — note 23 above was the thing standing in the way. `inset()`'s 2.7× report reproduces on a star and is correct erosion, documented rather than changed; the concave case underneath it was a real defect — the fold check asked whether a shape contained its own centroid, which a horseshoe does not. Every golden and both samplers byte for byte unmoved. |
| M9 MCP server | Not started, and correctly last. |

## File map

```
src/easel/
  color.py     sRGB/linear, pigment mixing (Kubelka-Munk power mean). Read first —
               the two constants in here decide whether anything looks like paint.
  texture.py   procedural canvas tooth: smooth / linen / rough, seeded.
  canvas.py    the pixel model: linear RGB + wetness + thickness + tooth + grain.
               `stamp()` is the single place paint is deposited.
  brush.py     Brush dataclass, procedural tip masks, presets. Cached per
               (tip, radius, angle, hardness, sub-pixel phase).
  stroke.py    Catmull-Rom paths, pressure profiles, load run-out, wet pickup.
               `paint_stroke()` is the hot loop; `draw_pencil()` is the same walk
               for graphite.
  palette.py   pigments (no black), mixing, named slots.
  regions.py   named regions, A–H/1–8 grid cells, relative placement, and from M8
               `Polygon` — a shaped place — with `polygon`, `ellipse`, `blob`,
               `hull` and `ribbon` to build one without inventing coordinates.
  look.py      the look() renderer: grid, values, crop, side-by-side, diff, and
               from M6 the fine (tenths) grid, matching crops of both panels,
               landmarks and the preview overlay. `_Frame` is the piece to
               understand: it maps normalised coordinates into whichever panel is
               being drawn, so one overlay routine decorates both.
  measure.py   compare(): per-cell value of reference and canvas, the difference,
               and the heat-map sheet. The number that matters is 0.10.
  prepare.py   the reference cut into numbered masses. Oklab k-means, connected
               components, merge-the-small, Moore boundary tracing,
               Douglas-Peucker. No model anywhere in it, by the brief's rule.
  history.py   stroke log, undo snapshots, GIF and contact-sheet time-lapse.
  session.py   the one object a painter holds. Also save/load and replay.
  cli.py       easel new / run / look / compare / prepare / mark / undo / export /
               timelapse / log / brushes.
  __main__.py  so `python -m easel ...` works when `easel` is not on PATH, which
               on Windows is most of the time.

tests/test_engine.py      95 tests: bounds, determinism, undo, replay, colour,
                          paint behaviour, composition, persistence, error messages.
tests/test_marks.py       17 tests for M7: the comb per stroke and against size,
                          width following pressure on the round tips (and not on the
                          oriented ones), and `press`.
tests/test_precision.py   60 tests for M6: the graphite channel and what buries it,
                          landmarks, matching crops, and mostly what the planning
                          tools must *not* do -- preview paints nothing, rehearse
                          commits nothing, neither disturbs the painting after it.
                          The last ten are M6c's: a swept mass keeps its silhouette,
                          the crossing closes it up, and a sweep deeper than its own
                          mass stops rather than scribbling.
tests/test_shapes.py      36 tests for M8: the shape itself, the five builders, and
                          what a shaped block-in must do -- stop at the silhouette,
                          come back in pieces across a concave mass, and log
                          ordinary strokes so undo and replay are right for free.
tests/test_floor.py       34 tests for M8b, and the ones that matter most assert
                          that nothing happens: paint that is not landing must not
                          move the pixel it is not landing on, in-band work is bit
                          for bit what it was, and the identity has to survive being
                          repeated a few thousand times rather than only once.
tests/test_golden.py      visual regression. `tests/golden_cases.py` holds the fixed
                          scripts; `tests/golden/*.png` are the stored renders, and
                          they are there to be *looked at* when a case fails.
scripts/make_golden.py    regenerates them. Only after looking.
scripts/make_brush_sampler.py   regenerates samples/brushes.png — the primary
                          test artefact. Look at it after every engine change.
scripts/make_shape_sampler.py   regenerates samples/shapes.png — every shape
                          builder against every sweep direction, with the box each
                          mass would have been in the last column.
scripts/probe_sweep.py    what `sweep()` costs and what it buys, on one boundary
                          three ways. Writes out/sweep_sheet.png; the numbers behind
                          CALIBRATION's *`sweep`* section.
m8/paint_two_ways.py      M8's other half of the evidence: one composition painted
                          as boxes and as shapes, same seed, same colours, and the
                          axis-alignment number for both.
m8b/probe_floor.py        both halves of the floor defect as numbers, before and
                          after. `--label` names the run.
m8b/paint_the_dark.py     M8b's evidence: one composition painted by both engines,
                          in the range the fix opens up. Writes m8b/compared.png,
                          and measures what the dark mass is *made of* rather than
                          only how dark it got.
engine_changes/           the three engine changes wanted before M9, and the only
                          place to start on them: README.md is the write-up,
                          probe_blob_radii.py / probe_rehearsed_mass.py /
                          probe_inset.py measure each item and draw its picture.
                          Every probe carries the pre-change behaviour in it, so
                          "before" is a function call rather than a git checkout.
examples/exercises.py     the abstract warm-ups from PAINTER.md, runnable. Kept in
                          step with the printed ones -- two were rewritten in M5,
                          and M6 added the seventh (draw, rehearse, paint).
rehearsal/                the first M5 rehearsal: both paintings, their pass scripts,
                          the probes behind REVIEW 15-18, and a script that
                          executes every python block in PAINTER.md.
rehearsal2/               the second M5 rehearsal, by a fresh session: the copy that
                          reached the bar, the unprompted estuary, every look, the
                          probes behind the overshoot and run-out numbers, and a
                          sheet comparing the two copies against the reference.
rehearsal3/unprompted/    the adversarial check on "how unprompted is unprompted":
                          PREREGISTERED.md (buckets and thresholds fixed first),
                          samples.md (32 fresh sessions naming a subject across four
                          conditions), and the two guide variants they were given.
                          Read PREREGISTERED.md before samples.md.
m7/                       M7's evidence: three probes that run against either engine
                          (`PYTHONPATH=<pre-m7>/src python m7/probe_comb.py` for the
                          before), `make_sheets.py` for the four panels of
                          `marks_compared.png`, and `repaint.py`, which replays
                          `rehearsal3/pass` -- 295 strokes of the mug -- on whichever
                          engine is on the path. That is the "real painting" the
                          brief asks for before a golden is regenerated.
rehearsal3/               M6's final pass: three fresh sessions (pass/ the headline
                          mug and its unprompted painting, sitter/ the same
                          photograph REHEARSAL2 painted, assisted/ the machine-laid
                          sketch), HUMAN_NOTES.md with the two notes from the human,
                          and the probes behind every number in REHEARSAL3.md --
                          the palette's value floor, the axis-alignment metric, the
                          tip-angle sheet, and verify_pass.py, which checks the
                          brief's pass criterion from the exported PNGs rather than
                          from what the painters said.
PAINTER.md                the guide a fresh agent is given. The deliverable. No
                          subjects in it, by the brief's rule -- check with a grep
                          before committing a change to it.
CALIBRATION.md            the engine's measured numbers (graphite survival, wetness
                          decay, the value floor, load windows, block_in overhang,
                          the axis-alignment table, what a sweep costs and buys).
                          Split out of the guide after the critique that preceded
                          REHEARSAL4, so the guide states rules and this states
                          measurements. Update it when the engine changes.
REHEARSAL.md              the first M5 rehearsal write-up. Read it before believing
                          the guide works -- it says plainly where it did not.
REHEARSAL2.md             the second: what the fresh session got, what it cost, and
                          the measurements behind each guide fix.
REVIEW.md                 four rounds. M1/M2: ten defects fixed. M4: four more
                          (11–14), plus four things investigated and found *not* to
                          be defects. M5: 15–18. M6: finding 19, the determinism
                          bug the golden images found on their first run -- read
                          that one. Read the M4 "Method" note before reviewing
                          anything else here.
```

## M8 — shaped masses

**What changed.** A place is now either a `Region` (a rectangle, unchanged) or a
`Polygon` (a closed outline). `block_in` fills either: for a shape it sweeps at the
angle asked for and cuts every pass against the outline, so the passes stop at the
silhouette, and a pass crossing a concave mass comes back as the two or three pieces
that are really inside it. Five builders make one without the painter inventing
coordinates — `polygon`, `ellipse`, `blob`, `hull`, `ribbon` — and each takes a
*place* where a centre would do, so `blob(cell("D5"))` is an irregular mass filling
a cell the painter read off a look. `direction="axis"` sweeps along the shape's own
long axis. `dry`, `erase`, `look`, `compare`, `preview` and `rehearse` all take a
shape; the first two act inside the outline (and record it, so they replay), the
rest crop to the rectangle around it.

**It is additive.** Every existing painting replays byte for byte: the rectangle
branches of `_block_paths` are untouched, and the named directions still run their
own hand-written geometry rather than being re-expressed as angles. No golden image
moved; one (`shapes`) was added. The full suite passed unchanged before the new
tests were written, which is the check that matters here.

**Decisions taken.**
- **A shape's default `overhang` is `0`, a rectangle's stays `0.35`.** A rectangle is
  blocked in past its edge so the mass does not look cropped; a shape's edge is the
  drawing. Only the pass *centres* stop at the boundary — the brush still breaks
  about three-quarters of its width past it, which is the ragged spill a block-in has
  always had at its ends. The M6 assisted run lost a whole edge of its subject to the
  rectangle overhang (`rehearsal3/assisted/GOTCHAS.md`, gotcha 10).
- **The traced-copy question is recorded, not decided.** The brief reserves it for
  the human, so the engine does the one thing it can: `s.ref_shape(n)` returns the
  prepared area as a shape *marked traced*, blocking one in appends to `s.assisted`
  and puts `(traced)` in the log, and that list is saved with the session (format 3)
  and printed by `s.log()`. `s.sketch()` records itself the same way. A run that
  uses either cannot leave it out of the write-up by accident. The painter's own way
  — `hull` on three or four verified landmarks, or a `blob` sized to the cells the
  prepared table says an area covers — is what the guide teaches.
- **No `sweep()` here.** Passes swept *along* a boundary and stepped inward is M6c
  and still open; this is the straight sweep, clipped. The `CALIBRATION.md` recipe
  is gone either way: a closed shape is one call now.

**The evidence, both halves.** `samples/shapes.png` is the sampler: five builders
against four sweep directions, with the box each mass would have been in the last
column — that column is the comparison the sheet exists for. `m8/paint_two_ways.py`
is the real painting: one composition, the same five masses, the same colours, seed
and order, laid once as boxes and once as shapes. As boxes it is a stack of
rectangles; as shapes it is a picture. 53 passes against 46, and **17.8% of the
boxed painting's paint landed outside the masses it meant to lay, against 10.7% of
the shaped one** — most of that 10.7% being the brush's own half-width spill past
each silhouette. The axis-alignment probe moves much less, 27.5% → 25.0%: most of
the strong edges in either picture are the bristle comb's streaks along the passes,
not the boundaries of masses, and M7's finer comb made that more true than it was
before this merge (it read 31.4% → 25.2% under the old comb and the old palette).
That probe is the wrong instrument for this question at this scale; the stray-paint
share is the right one, and the pictures are righter still.

**What it does not fix.** The painter still has to *decide* to use a shape. The
vocabulary is no longer all rectangles, but the guide is now the thing under test
again: whether a fresh session reaches for `blob` and `hull` instead of `span`, and
whether the unprompted paintings stop being bands, is a question for a run, not for
this note.

## M8b — the floor off the answer

Brief item 11, `REVIEW.md` finding 35, evidence in `m8b/`. Kubelka-Munk needs a
reflectance floor or a near-zero channel's K/S blows up and swamps every mixture --
that is finding 5, and `0.01` is the smallest floor that keeps red + blue violet. The
defect was that `_to_ks` clipped each ingredient on the way in and the clip was never
taken back off, so the floor decided two things it had no business deciding.

**A pixel with nothing landing on it still moved.** `Canvas.stamp` blends a dab's whole
*square* bounding box and a round tip's corners have an alpha of exactly zero, so a
black pixel in one of those corners came away at sRGB 25 from a dab whose mask value
there was `0.00000000`. **And a colour under the floor could not be laid at all**, at
any opacity: `cadmium_yellow` read blue 25 against its swatch's 18, `#000000` landed at
grey 25, and `mix("cadmium_yellow", x, 0.0)` -- mixing with nothing -- came back seven
levels lighter than cadmium yellow.

The fix is to keep the clip on the arithmetic and take it back off the mixture,
weighted by how much of each ingredient is in it (`_solo` and `_unclip` in `color.py`).
Then `amount` of 0 returns the canvas, 1 lays the colour, and a colour outside the band
is carried through a mixture in proportion to how much of it is there.

### Three things worth knowing next time

**The brief's premise was wrong, and finding that out was most of the work.** Item 11
said the fix "changes the wet-blend formula for every soft dab edge in the engine,
which is most of what this engine paints", and it is on that basis that it waited four
milestones. It does not. The correction is *identically absent* for any colour inside
the K/S band, every pigment but `cadmium_yellow` is inside it, and no reflectance this
model produces falls outside it -- so the seven goldens, both samplers and both real
paintings in `m7/repaint.py` come back byte for byte identical and not one golden was
regenerated. The scary-sounding item was a two-line change to where a clip is applied.

**"Judged on a real painting" had to be re-aimed.** When the change provably moves
nothing in the corpus, rendering the corpus twice proves only that. The judgement has
to happen in the range the fix *opens*, which is what `m8b/paint_the_dark.py` is: the
same five masses as `m8/paint_two_ways.py`, painted with a supplied `#060606`. And the
number worth looking at is not "the darkest pixel went 23 to 6" -- a mass can be darker
and still be a hole. It is that the dark went from 18 distinct levels to 32 and from
39.8% of its pixels pinned at one value to 2.9%, with local contrast up from 4.55 to
6.06. The comb's streaks and the linen tooth were being crushed flat against the floor;
they survive now, and that is what the eye actually sees in `m8b/compared.png`.

**Both of the fix's own costs were found by measuring, not by reasoning.** The first
version measured the clip's offset against `np.clip`, which is the obvious thing and is
wrong: the K/S round trip lands a hair below its own input, so the offset left a
constant `1.7e-6` gap in one direction on every blend and sub-floor pixels leaked
downward forever -- 23 levels over 5000 dabs, the same bug in slow motion. Measuring
against `_solo`, what the round trip actually returns, makes the two cancel. The second
version was correct and 20% slower to paint a picture, and shifted in-band results by a
few parts in a million for no visible reason; gating the correction on whether the clip
bites at all (`_outside_band`) made in-band work bit for bit what it was *and* came out
about 5% faster than before, because the incoming colour's K/S is now worked out on the
`(3,)` colour instead of on a broadcast copy of the whole dab. Neither of those was
visible from reading the code. Both took a probe.

### What it took out of the guide

`PAINTER.md` and `CALIBRATION.md` both said "nothing in this engine reflects less than
`0.01` linear". That was two claims wearing one coat -- the *box* bottoms out around
`0.13` because of the pigments in it, and the *engine* lays whatever it is handed --
and only the first is a painting lesson. This is finding 33's distinction over again,
and it is worth expecting a third instance: **when the guide explains a limit, check
which of the engine and the palette actually imposes it.** Neither file changed its
advice; the box still has no black because mixed darks are alive and tube black is
dead. `palette.py`'s rule that a dark swatch must sit at or above the floor was a
workaround for this defect and is gone -- what replaces it is `tests/test_floor.py`
checking every pigment against what the canvas actually receives, which
`cadmium_yellow` had been failing all along.

## Key decisions, and why

- **A new finding never adds a paragraph to `PAINTER.md`.** It does one of three
  things: **replaces** an existing rule, **becomes a checklist line**, or **goes to
  `CALIBRATION.md` or here**. This is a hard rule and it exists because the guide was
  growing by roughly a paragraph per rehearsal — every finding right, every one added,
  the document turning into a changelog of everything that went wrong once. `PAINTER.md`
  went 8,621 → 10,805 words across a single rehearsal's fixes. The failure mode is not
  that any paragraph is wrong; it is that **a fresh session reads the guide exactly
  once, at the start, when it matters most**, and the tenth rehearsal produces a guide
  nobody finishes. The test for a candidate paragraph: strip the measurement and the
  reasoning out of it and see what is left. If what is left is one line, that line is
  the rule and it goes in the guide; the measurement and the reasoning go to
  `CALIBRATION.md`, which exists for exactly this and which the guide already points
  at. If nothing is left, it was not a rule.
- **Pigment mixing is a power mean of Kubelka-Munk K/S with exponent 0.5**, over a
  reflectance floor of `0.01`. Both constants were chosen against a table of known
  paint mixes, not by taste. The floor stops a channel-zero colour from swamping
  mixtures (without it, red + blue is *green*); the exponent gives white the tinting
  strength it has in reality. See `src/easel/color.py`.
- **Mixbox is an opt-in extra, not a dependency.** It is a better model, but its
  reference implementation is CC BY-NC and this repo is MIT. `pip install -e
  ".[mixbox]"` enables it; `EASEL_DISABLE_MIXBOX=1` forces the built-in model.
- **Dab spacing is measured along the direction of travel**, not against the tip
  diameter. This is the single most consequential brush-engine decision here; see
  REVIEW.md findings 1 and 2.
- **Strokes are seeded per stroke index**, not drawn from one running stream. That is
  what makes `replay()` exact, which in turn is what makes CLI undo possible without
  persisting snapshots.
- **The canvas tooth and grain are derived from the seed**, so a saved session does
  not store them.
- **The tooth gate's threshold is capped at the surface's own tooth ceiling.**
  Textures are all centred near 0.5 but span very different ranges, and an uncapped
  threshold climbs past the highest peak of the narrow ones — which is how a starved
  brush came to deposit *nothing* on linen and smooth while still marking rough.
  `tooth_ceiling()` in `canvas.py`. The cap engages only where the old code produced
  nothing, so the sampler sheet regenerates byte-identical. REVIEW.md finding 11 also
  records the more ambitious fix that was tried and rejected, and why — read it
  before reaching for the same idea.
- **Every mark records how much paint actually landed**, not just how many dabs were
  stamped. Dabs are attempts. A stroke can stamp 278 dabs and change nothing, and
  before this there was no way — from the API or the log — to tell that apart from a
  stroke that worked.
- **Region names are deliberately neutral** (`upper-band`, not `sky-band`). The
  experiment's second stage is meant to be unprompted.
- **Graphite is a channel, and paint buries it by what *landed*, not what was
  aimed at.** `stamp()` does `sketch *= (1 - effective)`, where `effective` is the
  same per-dab alpha the colour blend uses. That one line gives the whole contract
  for free and keeps it consistent with the paint: coverage after `k` dabs of alpha
  `a` is `1 - (1-a)^k`, and the graphite left is exactly `1 - coverage`. A dab the
  tooth refused leaves the drawing untouched, which is why an underdrawing keeps
  working under a scumble and in the ground. Measured, on a pencil line at
  pressure 0.8 under one pass: opacity 0.04 leaves 79% of the graphite, 0.10 leaves
  55%, 0.18 leaves 34%, 0.30 leaves 19%. The burial is destructive, so `snapshot()`
  carries `sketch` or undo would restore the paint and not the drawing under it.
- **Graphite accumulates as a maximum, not a sum.** Dabs along a pencil line
  overlap almost completely and any additive rule turns the line into a solid bar
  within a few dabs. Density is chosen with `pressure`, which is what leaning on a
  pencil does.
- **`prepare()` quantises in Oklab, then labels connected components, then merges
  the small ones.** Quantising straight to the target number of masses gives one
  area per *colour*, and a picture has more masses than colours — two separate
  things the same brown are two masses. The connected-components pass is what turns
  colours into places. Edge hardness is the Oklab gradient along a shared boundary,
  not the value gradient: a warm table against a cool wall at the same value is an
  edge the painter can see, and a value gradient calls it lost.
- **A rehearsal is seeded as the *next* strokes of the real painting**
  (`Session._index_base`), so what you try on the scrap of canvas is what lands
  when you paint it. It gets its own generator, derived from the seed and the
  stroke count, so it cannot consume the session's stream and change the painting
  that follows — there is a test for exactly that.
- **`preview`, `rehearse` and `stroke` take the same argument shape.** A plan is a
  list of `stroke()` kwargs, so what was checked is what gets painted without being
  retyped. A plan that has to be rewritten between checking it and painting it is a
  plan that will drift.
- **`block_in` takes an angle, and the four names are frozen.** `direction=` accepts
  a number of degrees or a sequence of them, but the horizontal / vertical /
  diagonal / cross branches are byte-for-byte what they were and dispatch happens
  before them. That is what let this land in the middle of a milestone with golden
  images already stored: every existing painting replays identically, so no golden
  had to be regenerated and nobody had to decide by eye whether a mark had got
  better. Add capability beside the old path, never through it.
- **`sketch_lines()` is derived from the log, not stored.** Pencil records
  accumulate, erase records clip. Undo and replay are then right for free, because
  there is no second copy of the drawing to keep in step. REVIEW 20 was exactly the
  bug you get from the other design.
- **`compare()` separates *wrong* from *impossible*.** Cells whose reference is
  below the palette's floor are reported as `unreachable` rather than as work.
  `off` is unchanged, so nothing that used to be reported stopped being reported —
  the split is additional information, not a quieter threshold. A measuring stick
  that reports an unmeetable target costs strokes: two fresh sessions spent about
  twenty-five each finding that out for themselves, back when the floor was `0.235`.
  M6b took it to `0.13`, so the list is normally empty now — which is the right end
  state for a split like this. **Build the tool that tells the painter the truth,
  then go and fix the thing it was telling the truth about.**
- **Drawing does not count as a stroke.** `History.UNPAINTED_KINDS`. The brief's
  definition of done counts strokes, and a painter charged for the underdrawing is
  a painter who skips it.

## Gotchas for the next session

0. **The measurement can be right and the instrument still wrong.** Two M5 findings
   were tools that lied: `value_of` returned linear luminance while the greyscale
   view showed sRGB, and the first attempt at the halftone screen measured the height
   map's autocorrelation rather than the paint that landed. Before trusting a number,
   check it against the picture the painter actually sees.


1. **Look at `samples/brushes.png` after any engine change — and then paint
   something.** Every defect in the M1/M2 review was found by looking, and none by
   the test suite. But the sampler shows *isolated strokes at full load*: it was
   perfectly happy with a gate that silkscreened the canvas weave across every
   accumulated mass. Block-ins on top of block-ins are a different test. Keep a
   throwaway abstract script around for it.
2. **Assert on the canvas, not on the return value.** Both of the M4 engine findings
   were invisible from the API: a stroke reported 278 dabs and had changed nothing.
   Diff `canvas.rgb` either side of a stroke when you touch deposition.
3. **Anything linear in per-dab alpha cannot produce a persistent mixture.** If you
   find yourself tuning a wet-blending coefficient and seeing no effect, re-read
   REVIEW.md finding 7 before spending an hour on it.
4. **`np.savez_compressed` appends `.npz`** to a path without it. Save through an
   open file handle. There is a test guarding this.
5. **`import easel.brush as b` gets the function, not the module**, because
   `easel/__init__.py` rebinds the name. Use `from easel.brush import ...`, or
   `importlib.import_module("easel.brush")`.
6. **`sin(pi)` is slightly negative in float32**, and a negative base with a
   fractional exponent is NaN. This bit the `taper` pressure profile.
7. **Windows heredocs**: several multi-KB Python files could not be written through
   `bash` heredocs in this environment. Use the file-writing tool for anything large.
8. **Check what `import easel` actually resolves to** before trusting a measurement.
   A previous session left an editable install pointing at a copy of the repo under
   its own scratch directory, so everything imported that copy rather than
   `C:\git\EaselAPI\src`. `python -c "import easel; print(easel.__file__)"`, and
   `pip install -e .` from the repo root if it is wrong.
9. **The repo is LF** (`.gitattributes`: `* text=auto eol=lf`), even though a Windows
   checkout may hand you CRLF files. Write LF, or git will warn on every commit.
10. **A golden failing is an instruction to look, not to regenerate.** The test
    writes `tests/golden/<case>.actual.png` beside the stored `<case>.png` and says
    how far apart they are. Open both. `python scripts/make_golden.py <case>` only
    after deciding the new marks are better. A golden regenerated without looking
    records that a mark changed and asserts that nobody minded, which is worse than
    having no golden at all.
11. **Anything a mask is computed from has to be in its cache key.** REVIEW 19: the
    tip-mask cache was keyed on `ceil(radius)` while the mask used the exact radius,
    so the painting a script produced depended on what had run before it in the same
    process. If you add a parameter to `tip_mask`, add it to the key *and* quantise
    it before anything reads it.
12. **`np.cross` no longer does 2-D vectors** (numpy 2). `prepare.py`'s
    Douglas-Peucker writes the perpendicular distance out by hand.
13. **numpy rejects a float32 probability vector** that misses 1.0 by an ulp, which
    a quarter of a million squared distances comfortably does. `_kmeans` renormalises
    in float64.

14. **The tool shapes how a picture is built, not what gets picked — and the first
    version of this note got that wrong.** `REHEARSAL3.md` asserted, from two
    paintings and a reading of the guide, that a painter given it "will paint a
    horizontal landscape". Thirty-two fresh sessions later
    (`rehearsal3/unprompted/`): six of eight given the real guide named a street or
    an interior, and the claim is corrected in place. What did survive is smaller and
    more useful — no estuary appeared in any of the sixteen samples without the
    guide's landscape words, and a painter told what the engine is *bad* at justifies
    its choice by horizontal bands and rectangles six times in eight. Before
    concluding anything about what a painter chose, ask what it was offered — and
    then go and measure it, because a plausible story about a tool's influence is
    worth about as much as a plausible story about a bug.
15. **A worked example in the guide is an instruction, whatever the prose beside it
    says.** The `edge()` silhouette recipe laid a vertical column at every step and
    was followed exactly, three rehearsals running, producing exactly the combing the
    same guide warns about elsewhere. Read the code blocks as if they were the whole
    document, because to a fresh session they nearly are. The same applies to
    nouns: the back-to-front example was, word for word, the estuary REHEARSAL2
    painted, and a painter told "paint something of your own" after reading it has
    been handed a subject. The recipe now lives in `CALIBRATION.md` with abstract
    knots, and the guide carries no subjects at all.
    **This rule was broken again after REHEARSAL4, in the other direction, and it is
    worse that way.** The depth-order paragraph written to fix the human's note used
    the *copy reference* as its worked example — mug, tea, cup, rim — and the scale
    rule used a head and a cheek. An unprompted subject leaking out of the guide
    costs you the unprompted stage; **a copy reference leaking in costs you the copy
    score, and does it invisibly, because the number simply improves.** The human
    caught it by reading the diff. Both are the same failure of nerve: a rule is
    easier to write with a concrete example, and the nearest concrete example is
    always whatever you were just looking at. Write the rule with a list, or with a
    ratio, and **grep the guide for the current references before every run** —
    `mug`, `tea`, `cup`, `face`, `head`, and whatever the references hold next time.
16. **Never change the engine while a measurement is running.** The three sessions of
    the M6 pass painted against one engine and every fix landed after the last of
    them exported. Otherwise the run measures a moving target and none of the numbers
    can be compared with each other.
17. **Check the painters' numbers.** Every figure in `REHEARSAL3.md` was re-measured
    from the exported PNGs (`rehearsal3/verify_pass.py`). They were mostly right and
    not entirely — a painter reporting on its own painting is not a measurement.
18. **A canvas-mutating `Session` method must push an undo snapshot immediately
    before it touches the canvas, in the same method.** `undo()` pairs the top of
    the snapshot stack with the last log record on the assumption that the two
    always move together. REVIEW 23: `dry()` mutated the canvas and logged a
    record without snapshotting first, so `undo(1)` right after a `dry()` popped
    the *previous* action's snapshot while only dropping the `dry` record —
    correct-looking return value, canvas silently two steps back instead of one,
    and `replay()` from the still-intact log then disagreed with what was on
    screen. If you add a new kind of mark, grep for `push_snapshot` in
    `session.py` and add the call before you add the record, not after.
19. **A tuned constant often encodes a *ratio*, not an absolute — so it moves when
    the thing it is relative to moves.** The mixing exponent was set at `0.5` in
    REVIEW 6 to give white its real tinting strength, and the comment said so
    without saying strength *compared to what*. M6b darkened the palette, which
    widened its value range from `0.73` to `0.83`, and `0.5` silently went from
    carrying a 50/50 white mix `0.235` of the way up that range to `0.158` — the
    same number, quietly doing a different job, and finding 6 reopening with
    nothing about white touched. When you tune a constant, write down the invariant
    you tuned it to hold and not just the value you landed on: the next person to
    move the inputs then knows whether the constant has to follow.
20. **A workaround built around a defect has to be taken out when the defect is
    fixed, and its *documentation* is the part that gets left behind.** The
    `unreachable` split (REVIEW 21) was correct and stayed; the guide paragraph
    teaching painters to compress a reference's range onto the palette's, and
    `CALIBRATION.md`'s formula for doing it, were the workaround, and were still
    true-sounding after the reason for them had gone. Grep for the *number* — here
    `0.23` — not just the feature, when a limit moves.
21. **Normalised space is not isotropic, and `size` is measured against the long
    side.** A coordinate is a fraction of the *width* in x and of the *height* in y,
    so on a canvas that is not square a step of `0.07` down is a different number of
    pixels from `0.07` across — while a brush at `size=0.07` is `0.07` of the long
    side whichever way it travels. `block_in` has always mixed the two (`band` comes
    from `b.size` and is compared against `r.height`), and M6c's `sweep` follows it
    on purpose rather than introducing a second convention in one call: its passes
    step one part-brush *in normalised units*, so a sweep run down a 4:3 canvas
    overlaps more than the same sweep run across it. The numbers are in
    `CALIBRATION.md` under *`sweep`*. If this is ever made pixel-true, make both
    pixel-true in the same change, and expect every golden image to move.
22. **A record that carries a place has to carry the whole place.** `dry` and
    `erase` used to log `{"region": [x0, y0, x1, y1]}`, and a shape logged as its
    bounding box would replay as a rectangle — worse, a shape logged as *nothing*
    would replay as the whole canvas. They now log `shape` (the points) or
    `region` (the bounds), and `_place_from_params` in `session.py` is the one
    place that reads either back. `sketch_lines()` reads the same field, because
    what an eraser removed from the canvas has to be what it removed from the
    lines.
23. **A rehearsed mass *is* pixel-identical to the painted one, and the trick is a
    copy.** The trial needs its own generator so that trying something cannot change
    the painting that follows, and it needs the *same draws* the real call would make
    so that what is rehearsed is what lands. Those read as opposites and are not: the
    trial gets its own generator **object** holding a copy of the session's stream
    state (`_trial_session`). Strokes never needed it -- they are seeded per index --
    but `block_in` and `sweep` take their pass wander from the running stream, and
    before `engine_changes/` the trial had a *differently seeded* one, so a rehearsal
    showed the right masses in the right places with a different hand. There is a test
    for equality now, and one that the painting after two rehearsals is unchanged;
    both are needed, and passing one is not passing the other.
24. **A self-intersecting outline is accepted.** `Polygon` checks for three
    distinct points and a non-zero area, not for simplicity, and everything
    downstream is even-odd — so a bow-tie fills as two triangles rather than
    raising. `inset` is a mitre offset and can fold a spiky outline through
    itself, which is why it checks the result's area and centre and falls back to
    pulling the points toward the centre.
25. **When a document explains a limit, check which layer actually imposes it.**
    Twice now a guide passage has stated a *palette* choice as an *engine* fact and
    been believed: REVIEW 33 (the `0.23` value floor was the swatches, not the model)
    and REVIEW 35 ("nothing in this engine reflects less than `0.01`" was the box's
    range, not the engine's). Both read as physics and both were furniture. The tell
    is a sentence that tells the painter what is impossible; go and try it before
    believing it, because the fix for an engine limit and the fix for a palette
    choice are nothing alike.
26. **An identity in floating point is a claim to be measured, not assumed.** The
    first M8b fix restored a clipped colour by adding back `c - np.clip(c)`, which is
    exactly right on paper. The K/S round trip does not land on its own input, though,
    so the correction missed by a constant `1.7e-6` *in one direction* on every blend,
    and a near-black leaked 23 levels over 5000 dabs. A single application looked
    perfect. Iterate the operation a few thousand times and compare to the start --
    a drift that is invisible once is a defect once a painting has 30,000 dabs in it.

## What to do next, in order

**Start here. `REHEARSAL6.md` is the most recent measurement.** The brief's definition
of done has now been run end to end a second time, on both references, and **every
criterion in it is met** -- including the `preview`/`rehearse` clause REHEARSAL4 failed,
and the unprompted pair broke its own composition by the widest margin any run has
managed (`+8.12` dB to `-9.52`, with the edge split reversed rather than levelled).
Items **00a-00e** below come out of it and go before everything else. The 0a-0f block
under them is REHEARSAL5's and is kept because items 0b-0e are still the standing rules;
**0f is done.**

**00a. The signature exemption is a promise the engine does not keep, and it costs
paintings marks. Fix it in the engine.** `PAINTER.md:1265` says up to five marks noted
`signature` "do not come out of your stroke budget". `History.stroke_count`
(`src/easel/history.py:87`) counts every record whose kind is not `dry`/`look`/`pencil`/
`erase`, so it charges them. The exemption exists only in `rehearsal4/verify_done.py`,
which no painter sees. **Both REHEARSAL6 painters found this independently**, and the
sitter painter -- which was planning to 299 -- undid, dropped the mole on the sitter's
neck, and re-signed with one mark. `UNPAINTED_KINDS` is the wrong shape for this: the
exemption is per-*record*, capped at five, and everything past five charged, or the
cap is not a cap. Deleting the promise from the guide is the other honest option and
the worse one -- a painter that pays for its signature will not sign.

**00b. The depth-order paragraph has failed three runs. Rewrite it.** Containment
`17.5%`, `16.3%`, `13.2%` against REHEARSAL3's `0.1%`: the dark still leaves the cup.
Item 0c below left it untouched on the grounds that one session is not evidence it
fails. Three are. What is now certain is that stating the rule, giving it a runnable
three-mass example *and* putting it in the checklist is **not sufficient**, which is
the same lesson REHEARSAL.md -> REHEARSAL2.md taught about the guide generally.

**00c. Retire or re-scale the value criterion.** Worst cell on the last three mugs:
`0.0985`, `0.0961`, `0.0987`, against a `0.10` threshold. Three different painters have
cleared it by a thousandth. It is saturated, and on all three runs `probe_human_notes`'s
containment caught a defect it could not see. The second number is doing the work now.

**00d. Two costing rules mislead a painter about what a mass costs, and both go before
M9** because M9 exposes the API. **A curved `ribbon`**: `block_in` on one `0.029` wide
at brush `0.015` costs **19 passes**, where the same width straight costs **3**. The
guide says both "the passes are counted across the mass, not over its area" and "a
shaped mass costs what its box costs"; for a curved ribbon those disagree and the box
wins. It ate 7% of a painter's budget in one call. **`inset()` on a concave shape**:
`inset(0.052)` on a real 15-point coat outline keeps **62.7%** of the area, and the
block-in then covered 76.2% of the actual mass with a whole lobe at 15.5%. The guide
offers "`inset()` the shape by half the brush size" unqualified and CALIBRATION's
99%-coverage figure is measured on a convex blob. `ENGINE_CHANGES.md`'s note that the
2.7x erosion is "correct and documented" is about the maths; this is about the advice.

**00e. Four smaller guide defects, each of which cost a painter strokes.** Exercise 1's
`at_value()` only searches upward and silently returns the base when asked for anything
darker. `sweep(cross=0)` raises while omitting `cross` works. `undo(n)` counts log
entries, not paid marks. `look(region=)` pads the crop past the span asked for. And the
largest omission: **nothing in the guide says how to bury something** -- "when something
is wrong, paint over it" does not say with what, and a bristle leaves the old paint
showing between its streaks, a flat leaves a rectangle, a round tip leaves a capsule.
The answer a painter spent fifteen strokes arriving at: a long stroke, solid tip,
`load=1.0`, full opacity, run along the grain of what is there so its ends fall outside
the repair.

---

**REHEARSAL5's list, kept. `REHEARSAL5.md` changed the ordering when it was written.** The guide changes from REHEARSAL4 have now been tested: one worked, one did
nothing, one backfired, and the pass criterion turned out to be gameable and was gamed.
The list below is the order to work in; items 0a–0f are new and everything after them is
history kept for context.

**0a. ~~`ENGINE_CHANGES.md` — hand it to a fresh session.~~ Done — `engine_changes/`.**
All three landed, no golden moved, both samplers byte for byte unmoved. `blob(region,
radius)` takes option (a): one radius is a circle wherever the shape is put, which is
what `ellipse`'s own docstring had been promising while the region branch did something
else. `rehearse()` takes a `sweep` under `edge=`, and — the half that mattered — the
trial session now holds a *copy* of the real stream state, so a rehearsed mass is
pixel-identical to the painted one instead of merely being in the same place. `inset()`
splits in two: the 2.7× reproduces on a star and is correct erosion (documented, not
changed), and underneath it was a genuine defect on concave shapes that do not contain
their own centroid. **Three things for whoever holds the guide**, none of them mine to
edit: `PAINTER.md:543`'s `blob(cell("D5"), 0.22)` is *still* not "a mass filling a cell"
under either rule — `0.22` is a radius, so it is 3.9 cells across and always was, and
the fix cannot make it smaller; `PAINTER.md:1032` says `wobble=0.25` where the default
is `0.22`; and the note `ENGINE_CHANGES.md` expected in `CALIBRATION.md` about rehearsal
fidelity was never there, it was note 23 above. `engine_changes/README.md` has the rest.

**0b. The pass criterion is fixed in the brief and needs no more argument.** `compare()`
alone rewards damage — REHEARSAL5's painter laid a bar of dark it knew was bad to move
two cells inside `0.10` and said so in its first paragraph. The brief now adds
`probe_human_notes.py`'s containment as a second number and a procedural rule: **the
last ten strokes of a copy may not be value corrections.** Enforce both on the next run.

**0c. Guide changes are made; do not make more before the next run.** The seven nouns
are stripped (see 0d), the background rule has gained its missing half — *and the marks
inside it are not parallel lines* — and the signature is added. **The depth-order
paragraph is deliberately untouched** even though REHEARSAL5's containment number did
not move: one session is not evidence it fails, and rewriting it now is the changelog
habit this file forbids under *Key decisions*.

**0d. The leak rule is now three strikes and a procedure.** Mug, sitter, boat — the last
of which put six of six fresh sessions on the same rowing boat and contaminated two live
experiments (`rehearsal5/naming/THE_BOAT.md`). Any list is a ranked list and its first
item is the answer, so a guide example may not name a paintable object at all. Before
every run: grep for the references' nouns **and** read the guide's examples and name the
subject yourself.

**0e. Stop running naming probes.** Three attempts, and the dissociation is settled: 0 of
8 sessions *name* water, 4 of 4 *paint* it. Verbal probes measure what a session says
when interrupted. The finding they did produce is worth keeping and is better than a
tally — **the estuary is not a subject this model picks, it is a world it puts things
in**: given a boat it beaches it on a mudflat, and when told to break the structure it
painted a pond seen from above. Twelve sessions told to audit their own defaults named a
landscape as the first thing that arrived and walked away from it
(`rehearsal5/naming/A_reflective_samples.md`).

**0f. ~~Then one more `Level1.jpg` run, then M9.~~ Done -- `REHEARSAL6.md`, and it was
the whole definition of done rather than only the mug.** It was the first run measured
on two numbers rather than one and the first where a signed painting was expected, and
all three of the brief's additions did what they were added to do: containment caught a
defect the value criterion reported as clean, all four paintings were signed by painters
neither of whom was told to, and **the last-ten rule was tested rather than merely
passed** -- the sitter painter found a cell out of tolerance in its closing marks and
painted a face plane instead of the number, writing that chasing it "would have fixed E4
and ruined the jaw". That is REHEARSAL5's failure mode arriving and being declined by a
painter that did not know the rule existed for that reason. M6 is closed. What the run
found is items 00a-00e above.

---

1. ~~**Finish M6: one more run, one narrow question.**~~ **Run — `REHEARSAL4.md`,
   and M6 is still not finished.** The whole definition of done was run end to end:
   two fresh sessions, the mug and the sitter, plus the two unprompted paintings.
   **Read `REHEARSAL4.md` before anything below it in this list** — items 2 and 3 are
   answered there, and item 1's own narrow question is answered *yes*.
   - **The value error is gone.** 0 of 64 cells out on both copies, against
     REHEARSAL3's 8; the guide fixes made after REHEARSAL3 survive their first
     fresh-session test. But the margin is `0.0015` on the mug and `0.005` on the
     sitter, so treat the criterion as saturated rather than as comfortable.
   - **A different criterion failed instead**, and nobody was watching it: the pass
     session called `preview()` once and `rehearse()` never, so it cannot point to a
     mark it rejected *before painting it*. It spent 138 of 299 strokes repainting
     one table three times. The sitter session, which rehearsed constantly, called
     `rehearse` "the best thing in this toolkit".
   - **The human's note is the most valuable thing in the run** and no criterion in
     the brief could see it: the tea is painted before the rim, so it flows out of
     the cup (17.5% of its own area escaped, against REHEARSAL3's 0.1%), and the
     table was blocked in over the finished handle. `rehearsal4/HUMAN_NOTES.md`.
   - Fourteen guide changes come out of it, and **they are now made** — see
     *What was changed in `PAINTER.md`* in `REHEARSAL4.md` for the table. All 37
     guide code blocks still run, full suite still green. **Every one of them is a
     hypothesis until a fresh session paints against it**, so the next move is that
     run, not more editing.
   - **The human's read of the paintings is in `REHEARSAL4.md` and it changed two
     conclusions.** On the mug, R4 is the better copy and R3 the prettier one; the
     remaining tell is the table, *"the mass that needed no drawing is the one that
     shows the grid."* On the sitter, **R3 reads more as a person than R4** — R4 has
     the better face and lost the figure around it. That is a tension in the M6
     method itself: landmarks buy features and cost the mass. Both are now guide
     changes and both need the next run to test them.
   - **A leak was introduced and caught**: the first version of these edits taught
     depth order using the copy reference by name (mug, tea, cup) and scale using a
     head and a cheek. Neither appeared in the guide before. A copy reference inside
     the painter's manual feeds straight back into the copy score and would have been
     invisible in the numbers. Fixed, and the rule now stands: **grep the guide for
     the current references before every run** (gotcha 15).

   The original item, for context — the reasoning still holds:
   The protocol has been run —
   three fresh sessions, `REHEARSAL3.md`. Read that first; it says what passed and
   what did not. The copy stage failed only on value, and failed it in a single
   direction: every wrong cell on the mug was too *light*, straight down the
   shadow side. Everything that failure points at is now in `PAINTER.md` —
   `compare()` on the empty canvas, planning the three values as numbers, and
   painting back to front — **and a guide fix is a hypothesis until a fresh session
   paints against it.** That is the whole lesson of `REHEARSAL.md` → `REHEARSAL2.md`.
   The value-compression passage is gone: M6b removed the reason for it, and a run
   against the old palette would have measured a moving target (gotcha 16).
   - **Same reference, `Level1.jpg`, fresh session, `PAINTER.md` only, own pencil.**
     The question is narrow: does the value error go away? With the darks in place
     the criterion is **every** cell on the mug within `0.10`, not `fixable` — see
     the brief's *Reachable* paragraph.
   - Do not re-run the sitter or the assisted mode to decide this. The sitter
     answered its question — the tools do reach below a cell — and the assisted run
     answered its own: the machine sketch is a wash and slightly worse.
   - Write it up as `REHEARSAL4.md`, short. It only has one thing to report.
2. **The vocabulary is no longer all rectangles — now find out whether that was
   enough.** M8 is built (above): a mass can be a shape, `block_in` fills one, and
   the guide teaches it. What that has *not* shown is the thing the unprompted
   experiment actually asked, which was never about the engine's capability but
   about what a painter reasons its way to. Thirty-two fresh sessions
   (`rehearsal3/unprompted/`) justified band-shaped pictures six times in eight, in
   as many words: *"the rectangular regions are working for me instead of against
   me."* The reply to that is now in the box, so the open question is whether a fresh
   session reaches for it: does the copy stage use shaped masses, and do the two
   unprompted paintings stop being stacks of bands? `probe_axis_alignment.py` gives
   the number, though the pair in `m8/` shows how blunt it is at this scale (27.5%
   as boxes against 25.0% as shapes, for two pictures that look nothing alike).
   What separated them cleanly was the share of paint landing outside the intended
   masses, 17.8% against 10.7%; on a fresh session's painting the equivalent
   question is simply whether the log shows shapes at all. Fold this into REHEARSAL4
   rather than running it on its own — the same run answers it and the value
   question, and running two measurements against one painting is free.
3. **Decide what the unprompted stage is for** (`REHEARSAL3.md`, *Still open*).
   It is a question about the brief, so it is the human's to answer, and it is cheap
   either way. 63% of thirty-two fresh sessions named the same subject before reading
   anything, so the *choice* of subject carries almost no signal — the recommendation
   is to have the human name a subject with no reference image, which measures
   invention instead of the model's prior at the same cost. Until that is decided,
   do not read anything into what an unprompted painting is *of*.
4. **Two engine changes the guide critique asked for — now phases M6b and M6c in
   the brief, and they go before REHEARSAL4.** A review of `PAINTER.md` before
   REHEARSAL4 (`REVIEW.md`, *Guide critique*) found five things; three were guide
   edits and are made (no subjects, the calibration numbers split out into
   `CALIBRATION.md`, the measuring section cut back from an optimiser loop to two
   `compare()` calls, the drawing order reconciled in one sentence). The other two
   are engine work. The human has decided the first: **darken the masstones**,
   goldens included. The brief's build order has the specifics; the evidence is
   here:
   - **The `0.23` value floor is the pigments, not the mixing model.** Mixing here
     never takes a channel below the darker of its two ingredients, so nothing is
     darker than the darkest pigment, and `burnt_umber` (`#4A3728`) reads `0.23` on
     its own. The swatches are lighter than tube masstones. Two fixes: darken the
     masstones of the dark pigments (ultramarine, burnt umber, alizarin, viridian,
     burnt sienna) so ultramarine + umber reaches near-black the way real paint
     does -- the honest fix, and it moves every golden image and every rehearsal's
     colours; or add one genuinely dark pigment, which is additive and leaves the
     goldens alone but does not make the classic mixture work. **The first is
     taken (M6b), and is now done.** The box floors at `0.13`, three hundredths
     above the Kubelka-Munk reflectance floor (`0.01` linear, value `0.10`) that is
     the model's real bottom; the guide's floor paragraph, `CALIBRATION.md`'s
     compression formula and the brief's *Reachable* paragraph are rewritten, and
     `compare()`'s `~` split stays for the deepest few cells a photograph can hold.
     Two things M6b turned up that were not in the plan: equal white ratios cannot
     give an even value scale at *any* exponent, so exercise 1 had to mix to a value
     instead (it was asking "do these look evenly spaced?" of steps running `0.03`
     to `0.21` apart); and the exponent itself had to move, because it encodes
     white's tinting strength *relative to the palette's range* and the range
     changed underneath it.
   - **Sweeping a shaped mass should be an API call, not a recipe. Done (M6c).**
     `s.sweep(edge, ...)` steps passes inward from a hand-given boundary; the
     recipe is out of `CALIBRATION.md` and the numbers behind it are in its place.
     It is not the traced-copy question, because the boundary is the painter's own
     -- but the `sketch()` rule applies to it, and the guide says so: a run that
     hands `ref_outline(n)` straight to `sweep()` is an assisted mode. It did not
     make M8 unnecessary, and M8 has not made it redundant: sweeping helps the
     painter who already has a boundary in hand, and a shaped `block_in` helps the
     one who can name the silhouette but has not drawn it. They meet in the middle
     -- `sweep` takes a shape as its edge, and a traced one carries its own mark.
5. ~~**M7 — Marks at detail scale.**~~ **Done — `M7.md`.** What it leaves behind,
   for whoever runs the next fresh session: a lone `s.dab()` is now a light touch at
   about half the width asked for (`press=3` for the mark at full size), and
   `s.glaze()` thins at both ends unless it is given `pressure="even"`, because it
   defaults to a `round_soft` at a `taper`. Whether `glaze()`'s own default should
   change is an API question and was deliberately left alone.
6. Consider varying `block_in`'s pass *axis* automatically between passes. The
   travel direction alternates on its own (REVIEW finding 12), and since REVIEW 22
   the painter can *choose* the axis — but a mass still gets one axis per call unless
   the painter passes a sequence.
7. ~~**The wet-blend reflectance floor** (brief item 11).~~ **Done — M8b.** The one
   finding in the repo found by reading the code rather than by looking at a picture,
   and the last engine change before the server.
8. Then M9 — the MCP server: one tool per CLI verb, plus `look`, `preview` and
   `compare` returning their images inline. It exposes the API, so everything that
   changes it goes first, and that list is now empty. The server's tool
   surface has to carry shapes as arguments, which is the one new thing M8 adds to
   its design: a place is a name, a cell, a span, a rectangle **or a list of
   points**, and `sweep` takes the same.

## Verify the scaffold

```bash
pip install -e ".[dev]"
pytest -q                              # 232 tests, about 100s (the goldens repaint)
python -m ruff check src tests scripts examples   # ruff is not on PATH here either
python rehearsal/check_guide_blocks.py # every python block in PAINTER.md runs
python scripts/make_brush_sampler.py   # then look at samples/brushes.png
python scripts/make_shape_sampler.py   # then look at samples/shapes.png
python m8/paint_two_ways.py            # the shaped/boxed pair, and their numbers
python scripts/make_golden.py          # only after looking at what changed
python examples/exercises.py           # writes out/ex_*.png, including the M6 loop
python -m easel brushes                # the CLI, without needing it on PATH
```

And the M6 tools, end to end, against any photograph:

```bash
python -m easel new p.easel --size 900x675 --ground toned_grey --seed 7
python -m easel prepare p.easel ref.jpg --level coarse
python -m easel mark p.easel rim_l 0.335 0.315
python -m easel look p.easel --region D4 --fine --reference ref.jpg
python -m easel compare p.easel ref.jpg
```
