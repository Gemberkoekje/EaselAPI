# Phase notes — scaffolding, M4, the M5 rehearsal twice, then M6's tools

**To understand this, start by reading `painting-api-brief.md` (the spec), then
`REHEARSAL.md` and `REHEARSAL2.md` (the two M5 rehearsals and their verdicts), then
`PAINTER.md` (what a fresh agent is given), then `src/easel/session.py` (the object
everything goes through), then `src/easel/stroke.py` and `src/easel/canvas.py`
(where the marks actually happen).**

Status: **M1–M5 done and measured. M6's tools are built; M6's rehearsal is not
run.** Everything the milestone asks the engine and the guide for exists, is
tested, and has been looked at. The one thing outstanding is the part that cannot
be done here: *"then run the M5 protocol again, fresh session, same reference"*.
The engine's author has now seen every one of these tools work, so a run by this
session would measure the author and not the guide — the human is running it as a
separate session, deliberately. **That run is the measurement, and until it happens
M6 is not done.** See *What to do next*.

M7 (marks at detail scale) is specified and not started; the golden images it needs
as its gate now exist. M8 (MCP) is untouched and correctly last.

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
| M6 Precision | **Tools done, rehearsal outstanding.** Golden images first (and they found REVIEW 19 on their first run). Then: the `sketch` graphite channel with `pencil`/`erase`/`sketch_lines`, landmarks, matching crops with `grid="fine"`, `preview()`, `rehearse()`, `compare()`, `prepare()`, the `liner` preset, six CLI verbs, and the guide's drawing step. The fresh-session run of the M5 protocol is the measurement and has not happened. |
| M7 Marks at detail scale | Specified; not started. Its gate — the golden images — now exists. |
| M8 MCP server | Not started, and correctly last. |

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

tests/test_engine.py      94 tests: bounds, determinism, undo, replay, colour,
                          paint behaviour, composition, persistence, error messages.
tests/test_precision.py   42 tests for M6: the graphite channel and what buries it,
                          landmarks, matching crops, and mostly what the planning
                          tools must *not* do -- preview paints nothing, rehearse
                          commits nothing, neither disturbs the painting after it.
tests/test_golden.py      visual regression. `tests/golden_cases.py` holds the fixed
                          scripts; `tests/golden/*.png` are the stored renders, and
                          they are there to be *looked at* when a case fails.
scripts/make_golden.py    regenerates them. Only after looking.
scripts/make_brush_sampler.py   regenerates samples/brushes.png — the primary
                          test artefact. Look at it after every engine change.
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
PAINTER.md                the guide a fresh agent is given. The deliverable.
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

## What to do next, in order

1. **Finish M6: run the protocol.** Everything else in the milestone is built. What
   remains is the measurement, and it has to be a **fresh session** — new context,
   `PAINTER.md` only, no source, no access to this write-up. The brief says two
   references and they answer different questions:
   - **An ordinary object (a mug on a table will do). This one is the pass.** The
     human recognises the object; `s.compare(ref)` reports no cell *on the object*
     more than `0.10` out; and the painter can point at strokes it rejected in
     `preview()` or `rehearse()` before painting them. Under 300 strokes — drawing
     and rehearsals do not count against that.
   - **Then the sitter. That one is the measure of reach**, not a pass/fail:
     recognisable as the person or not, and the write-up says *which features got
     there*. This is the question the second rehearsal could not answer.
   - **The headline run gets no `s.sketch(reference)`.** The pencil must be the
     painter's own: sketch, look, adjust, paint. A run started from the machine-laid
     outlines is an assisted mode — worth running as a second data point, reported
     separately, and never the number that says M6 is done, or the criterion is
     measuring the segmenter. The unprompted stage never receives a sketch it did
     not draw itself.
   - Write it up as `REHEARSAL3.md`, in the shape of `REHEARSAL2.md`: what it got,
     what it cost, and a measurement behind every guide fix. Every time the fresh
     session reaches for the source to get unstuck, that is a guide gap — fix the
     guide.
   - Then fix what it finds, and only then call M6 done.
2. **M7 — Marks at detail scale.** Vary the bristle comb per stroke and scale its
   streaks with the
   brush, decide the pressure question (`REVIEW.md`, *Open, with evidence*; the
   eye test in `REHEARSAL2.md` says width, for tapering marks), and give `dab()` a
   `press` count so a catchlight can land at full strength.
   Both change every stroke, so both want the sampler *and* a real painting as
   the evidence, and a milestone of their own.
3. Consider varying `block_in`'s pass *axis* automatically between passes. The
   travel direction alternates on its own (REVIEW finding 12); the axis still does
   not.
4. Only then, M8 — the MCP server: one tool per CLI verb, plus `look`, `preview`
   and `compare` returning their images inline.

## Verify the scaffold

```bash
pip install -e ".[dev]"
pytest -q                              # 143 tests, about 35s (the goldens repaint)
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
