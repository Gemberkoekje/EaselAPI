# Phase notes — scaffolding, M4, the M5 rehearsal twice, M6's tools, M6's final pass, and M8's shaped masses

**To understand this, start by reading `painting-api-brief.md` (the spec), then
`REHEARSAL3.md` (the M6 final pass — the most recent measurement, and it says what
is still wrong), then `REHEARSAL.md` and `REHEARSAL2.md` (the two M5 rehearsals),
then `PAINTER.md` (what a fresh agent is given) and `CALIBRATION.md` (the measured
numbers the guide no longer carries), then `src/easel/session.py` (the object
everything goes through), then `src/easel/stroke.py` and `src/easel/canvas.py`
(where the marks actually happen).**

Status: **M1–M5 done. M6's tools are built and its protocol has now been run —
three fresh sessions, `REHEARSAL3.md`. M6 is not done: the copy passes on
recognition, stroke budget and rejected marks, and fails the `0.10` number.** Five
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

M7 (marks at detail scale) is specified and not started; the golden images it needs
as its gate now exist. **M8 is done** — a place can now be a shape, and `block_in`
fills one, which is the largest open item the unprompted stage pointed at; see
*M8 — shaped masses* below. M6b (darks) and M6c (sweep) are still open and still
belong before REHEARSAL4. M9 (MCP) is untouched and correctly last.

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
| M6b Darks | **New**, decided by the human after the guide critique. The `0.23` value floor is the pigment swatches, not the mixing model (`REVIEW.md` 33); darken the masstones so ultramarine + umber reaches the model's own floor. Moves every golden, and that is accepted. Before REHEARSAL4. |
| M6c Sweep | **New.** `s.sweep(edge, ...)`: passes swept along a hand-given boundary and stepped inward, replacing the fifteen-line recipe in `CALIBRATION.md` (`REVIEW.md` 34). Additive; one golden added. Before REHEARSAL4. |
| M7 Marks at detail scale | Specified; not started. Its gate — the golden images — now exists. |
| M8 Non-rectangular masses | **Done.** `Polygon` is a place beside `Region`, built with `polygon`, `ellipse`, `blob`, `hull` or `ribbon`; `block_in` cuts every pass against the outline, so a shaped mass keeps its silhouette and a concave one keeps its bite. `direction="axis"` sweeps along the mass's own long axis. `dry`, `erase`, `look`, `compare`, `preview` and `rehearse` all take a shape. Additive: no golden moved, one was added. Evidence in `samples/shapes.png` and `m8/`. |
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
tests/test_precision.py   50 tests for M6: the graphite channel and what buries it,
                          landmarks, matching crops, and mostly what the planning
                          tools must *not* do -- preview paints nothing, rehearse
                          commits nothing, neither disturbs the painting after it.
tests/test_shapes.py      36 tests for M8: the shape itself, the five builders, and
                          what a shaped block-in must do -- stop at the silhouette,
                          come back in pieces across a concave mass, and log
                          ordinary strokes so undo and replay are right for free.
tests/test_golden.py      visual regression. `tests/golden_cases.py` holds the fixed
                          scripts; `tests/golden/*.png` are the stored renders, and
                          they are there to be *looked at* when a case fails.
scripts/make_golden.py    regenerates them. Only after looking.
scripts/make_brush_sampler.py   regenerates samples/brushes.png — the primary
                          test artefact. Look at it after every engine change.
scripts/make_shape_sampler.py   regenerates samples/shapes.png — every shape
                          builder against every sweep direction, with the box each
                          mass would have been in the last column.
m8/paint_two_ways.py      M8's other half of the evidence: one composition painted
                          as boxes and as shapes, same seed, same colours, and the
                          axis-alignment number for both.
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
                          the axis-alignment table, the shaped-mass sweep recipe).
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
rectangles; as shapes it is a picture. 53 passes against 46, and the axis-aligned
edge share (`rehearsal3/probe_axis_alignment.py`) went 31.4% → 25.2%. The number
moves less than the pictures do, because much of what that probe counts is the
bristle comb's own streaks along each pass — which is M7's business, not this one's.

**What it does not fix.** The painter still has to *decide* to use a shape. The
vocabulary is no longer all rectangles, but the guide is now the thing under test
again: whether a fresh session reaches for `blob` and `hull` instead of `span`, and
whether the unprompted paintings stop being bands, is a question for a run, not for
this note.

## Key decisions, and why

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
- **`compare()` separates *wrong* from *impossible*.** The palette has no black and
  floors at `0.235`; photographs do not. Cells whose reference is below the floor
  are reported as `unreachable` rather than as work. `off` is unchanged, so nothing
  that used to be reported stopped being reported — the split is additional
  information, not a quieter threshold. A measuring stick that reports an unmeetable
  target costs strokes: two fresh sessions spent about twenty-five each finding this
  out for themselves.
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
19. **A record that carries a place has to carry the whole place.** `dry` and
    `erase` used to log `{"region": [x0, y0, x1, y1]}`, and a shape logged as its
    bounding box would replay as a rectangle — worse, a shape logged as *nothing*
    would replay as the whole canvas. They now log `shape` (the points) or
    `region` (the bounds), and `_place_from_params` in `session.py` is the one
    place that reads either back. `sketch_lines()` reads the same field, because
    what an eraser removed from the canvas has to be what it removed from the
    lines.
20. **A rehearsed mass is not pixel-identical to the painted one.** A rehearsal
    gets its own generator on purpose (so trying something cannot change the
    painting that follows), strokes are seeded per index and so come out the same,
    but a `block_in`'s pass wander is drawn from the session's stream and does not.
    Same masses in the same places, different wobble. Do not write a test that
    asserts equality there; assert the overlap.
21. **A self-intersecting outline is accepted.** `Polygon` checks for three
    distinct points and a non-zero area, not for simplicity, and everything
    downstream is even-odd — so a bow-tie fills as two triangles rather than
    raising. `inset` is a mitre offset and can fold a spiky outline through
    itself, which is why it checks the result's area and centre and falls back to
    pulling the points toward the centre.

## What to do next, in order

1. **Finish M6: one more run, one narrow question.** The protocol has been run —
   three fresh sessions, `REHEARSAL3.md`. Read that first; it says what passed and
   what did not. The copy stage failed only on value, and failed it in a single
   direction: every wrong cell on the mug was too *light*, straight down the
   shadow side. Everything that failure points at is now in `PAINTER.md` — value
   compression, `compare()` on the empty canvas, `fixable` versus the cells no paint
   can reach, and painting back to front — **and a guide fix is a hypothesis until a
   fresh session paints against it.** That is the whole lesson of
   `REHEARSAL.md` → `REHEARSAL2.md`.
   - **Same reference, `Level1.jpg`, fresh session, `PAINTER.md` only, own pencil.**
     The question is narrow: does the value error go away? If no cell on the mug is
     more than `0.10` out except the two that cannot be painted, M6 is done.
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
   the number; the pair in `m8/` gives it a scale (31.4% as boxes, 25.2% as shapes,
   same composition). Fold this into REHEARSAL4 rather than running it on its own —
   the same run answers it and the value question, and running two measurements
   against one painting is free.
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
     taken (M6b).** Either way the
     Kubelka-Munk reflectance floor (`0.01` linear, value about `0.10`) is the new
     bottom, and the *Reachable* paragraph in the brief, `compare()`'s `~` split and
     step 3 of the guide all get shorter or go. Until it is decided the guide says,
     in one paragraph, that the floor is an engine limit and not a lesson.
   - **Sweeping a shaped mass should be an API call, not a recipe.** The guide
     argues for laying a silhouetted mass as passes swept along its edge, and the
     painter is then expected to retype fifteen lines to do it. `CALIBRATION.md`
     holds the recipe for now. The call is M8's polygon `block_in`, or a smaller
     `sweep(edge_points, ...)` that steps a stroke inward from a hand-given
     boundary; the second is not the traced-copy question, because the boundary is
     the painter's own, and could land before M8 proper. **That is M6c.**
5. **M7 — Marks at detail scale.** Vary the bristle comb per stroke and scale its
   streaks with the
   brush, decide the pressure question (`REVIEW.md`, *Open, with evidence*; the
   eye test in `REHEARSAL2.md` says width, for tapering marks), and give `dab()` a
   `press` count so a catchlight can land at full strength.
   Both change every stroke, so both want the sampler *and* a real painting as
   the evidence, and a milestone of their own.
6. Consider varying `block_in`'s pass *axis* automatically between passes. The
   travel direction alternates on its own (REVIEW finding 12), and since REVIEW 22
   the painter can *choose* the axis — but a mass still gets one axis per call unless
   the painter passes a sequence.
7. Then M9 — the MCP server: one tool per CLI verb, plus `look`, `preview` and
   `compare` returning their images inline. It exposes the API, so everything that
   changes the API goes first: M6b, M6c, M7 and the wet-blend floor (brief item 11)
   are what is left of that list now M8 has landed. The server's tool surface has to
   carry shapes as arguments, which is the one new thing M8 adds to its design: a
   place is a name, a cell, a span, a rectangle **or a list of points**.

## Verify the scaffold

```bash
pip install -e ".[dev]"
pytest -q                              # 200 tests, about 60s (the goldens repaint)
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
