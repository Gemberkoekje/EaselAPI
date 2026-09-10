# Phase notes — scaffolding, M4, the M5 rehearsal twice, M6's tools, and M6's final pass

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
as its gate now exist. **M8 is new** — non-rectangular masses, added to the brief
after this pass, and it takes the slot before the server for the same reason M6 did:
it changes the API. M9 (MCP) is untouched and correctly last.

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
| M6c Sweep | **Done.** `s.sweep(edge, ...)`: passes swept along a hand-given boundary and stepped inward, `cross=` for the second set, `closed=True` for a boundary that comes back on itself (`REVIEW.md` 34). Ordinary strokes, so undo and replay came free. Additive: no golden moved, one added — and regenerated once when M6b's darks landed under it, geometry identical. The recipe is out of `CALIBRATION.md` and the guide's *A region is a rectangle* paragraph is one call. |
| M7 Marks at detail scale | Specified; not started. Its gate — the golden images — now exists. |
| M8 Non-rectangular masses | **New**, added to the brief after the M6 pass. Every named place is an axis-aligned rectangle, so a band is the only mass `block_in` fills honestly — and six fresh sessions in eight, given only the engine's mechanical limits, chose band-shaped pictures and said so. `ref_outline(n)` already returns a polygon. Before the server, because it changes the API. |
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
  regions.py   named regions, A–H/1–8 grid cells, relative placement.
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
tests/test_precision.py   60 tests for M6: the graphite channel and what buries it,
                          landmarks, matching crops, and mostly what the planning
                          tools must *not* do -- preview paints nothing, rehearse
                          commits nothing, neither disturbs the painting after it.
                          The last ten are M6c's: a swept mass keeps its silhouette,
                          the crossing closes it up, and a sweep deeper than its own
                          mass stops rather than scribbling.
tests/test_golden.py      visual regression. `tests/golden_cases.py` holds the fixed
                          scripts; `tests/golden/*.png` are the stored renders, and
                          they are there to be *looked at* when a case fails.
scripts/make_golden.py    regenerates them. Only after looking.
scripts/make_brush_sampler.py   regenerates samples/brushes.png — the primary
                          test artefact. Look at it after every engine change.
scripts/probe_sweep.py    what `sweep()` costs and what it buys, on one boundary
                          three ways. Writes out/sweep_sheet.png; the numbers behind
                          CALIBRATION's *`sweep`* section.
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

19. **Normalised space is not isotropic, and `size` is measured against the long
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

## What to do next, in order

1. **Finish M6: one more run, one narrow question.** The protocol has been run —
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
2. **The vocabulary is all rectangles** (`REHEARSAL3.md`, *How unprompted is
   unprompted?*). Twenty-two named regions, every one axis-aligned, and one helper
   named after a thing in the world: `horizon()`. **This is the one thing the
   unprompted experiment says to fix.** Thirty-two fresh sessions
   (`rehearsal3/unprompted/`) showed the guide's *words* barely steer the subject —
   but a painter told only what the engine is mechanically bad at justifies its
   choice by horizontal bands and rectangles six times in eight, in as many words:
   *"the rectangular regions are working for me instead of against me."* Painters are
   not accidentally laying bands, they are reasoning their way to band-shaped
   pictures because a band is the only mass this tool fills honestly. No amount of
   guide prose fixes that; the fix is to make a non-rectangular mass as cheap as a
   rectangular one. A polygon region — `ref_outline(n)` already returns one — is the
   largest open item in the repo, and it is partly the traced-copy question the brief
   reserves for the human. It changes what gets painted, so it wants a milestone and
   a real painting as evidence, not a rehearsal.
   - **The guide side is done.** The angle, back-to-front and `edge()` edits, and
     then the critique pass (below) that took every subject noun out of the guide --
     not on the strength of the p ≈ 0.10 pooling, which an earlier version of this
     note rightly refused to act on, but because the brief says in as many words
     that the guide must not contain example subjects, and it did. The engine side
     is item 4.
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
     hands `ref_outline(n)` straight to `sweep()` is an assisted mode. It does not
     make M8 unnecessary: `block_in` still fills a rectangle and every *named* place
     is still one, so a painter who has not read this far still reaches for a box.
     Sweeping only helps the painter who already has a boundary in hand.
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
7. Then M8 — non-rectangular masses (item 2 above is the argument for it), and only
   then M9 — the MCP server: one tool per CLI verb, plus `look`, `preview`
   and `compare` returning their images inline.

## Verify the scaffold

```bash
pip install -e ".[dev]"
pytest -q                              # 149 tests, about 35s (the goldens repaint)
python -m ruff check src tests scripts examples   # ruff is not on PATH here either
python rehearsal/check_guide_blocks.py # every python block in PAINTER.md runs
python scripts/make_brush_sampler.py   # then look at samples/brushes.png
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
