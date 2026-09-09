# Phase notes — scaffolding, M4, then the M5 rehearsal, twice

**To understand this, start by reading `painting-api-brief.md` (the spec), then
`REHEARSAL.md` and `REHEARSAL2.md` (the two M5 rehearsals and their verdicts), then
`PAINTER.md` (what a fresh agent is given), then `src/easel/session.py` (the object
everything goes through), then `src/easel/stroke.py` and `src/easel/canvas.py`
(where the marks actually happen).**

Status: **M1–M5 done, and M5 measured.** M6 (MCP) is untouched and correctly last.

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
| M6 MCP server | Not started, and correctly last. |

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
               `paint_stroke()` is the hot loop.
  palette.py   pigments (no black), mixing, named slots.
  regions.py   named regions, A–H/1–8 grid cells, relative placement.
  look.py      the look() renderer: grid, values, crop, side-by-side, diff.
  history.py   stroke log, undo snapshots, GIF and contact-sheet time-lapse.
  session.py   the one object a painter holds. Also save/load and replay.
  cli.py       easel new / run / look / undo / export / timelapse / log / brushes.
  __main__.py  so `python -m easel ...` works when `easel` is not on PATH, which
               on Windows is most of the time.

tests/test_engine.py      92 tests: bounds, determinism, undo, replay, colour,
                          paint behaviour, composition, persistence, error messages.
scripts/make_brush_sampler.py   regenerates samples/brushes.png — the primary
                          test artefact. Look at it after every engine change.
examples/exercises.py     the abstract warm-ups from PAINTER.md, runnable. Kept in
                          step with the printed ones -- two were rewritten in M5.
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
REVIEW.md                 three adversarial reviews. M1/M2: ten defects fixed. M4:
                          four more (findings 11–14), plus four things investigated
                          and found *not* to be defects. Read the M4 "Method" note
                          before reviewing anything else here.
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

## What to do next, in order

1. **Vary the bristle comb per stroke.** Every wide bristle mark prints the same set
   of streaks, so any large mass laid with it goes to corduroy — the second
   rehearsal's copy shows it in the background and the hair, and the guide now
   steers painters to `flat` for quiet masses as a workaround. Spacing, phase and a
   few missing bristles varied per stroke would fix the cause. It changes every
   stroke: do it at the start of a milestone, with the sampler *and* a real
   painting as the evidence, per the M2 and M5 precedents.
2. **Golden-image tests.** A fixed set of strokes, hashed, so brush-engine
   regressions fail loudly. The property tests catch behaviour, not appearance, and
   this milestone changed deposition — `samples/brushes.png` has been regenerated and
   is no longer byte-comparable with anything before it.
3. **Decide the pressure question.** Pressure scales opacity and not width; the
   measurements and the argument either way are in `REVIEW.md` under *Open, with
   evidence*. If it is taken, take it early in a milestone and re-look at the sampler
   and a real painting, not at the sampler alone.
4. Consider varying `block_in`'s pass *axis* automatically between passes. The travel
   direction alternates on its own (REVIEW finding 12); the axis still does not.
5. Only then, M6 MCP server — one tool per CLI verb, plus `look` returning the image
   inline.

## Verify the scaffold

```bash
pip install -e ".[dev]"
pytest -q                              # 92 tests
python -m ruff check src tests scripts examples   # ruff is not on PATH here either
python rehearsal/check_guide_blocks.py # every python block in PAINTER.md runs
python scripts/make_brush_sampler.py   # then look at samples/brushes.png
python examples/exercises.py           # writes out/ex_*.png
python -m easel brushes                # the CLI, without needing it on PATH
```
