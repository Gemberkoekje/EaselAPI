# Phase notes — scaffolding

**To understand this, start by reading `painting-api-brief.md` (the spec), then
`PAINTER.md` (what a fresh agent is given), then `src/easel/session.py` (the object
everything goes through), then `src/easel/stroke.py` and `src/easel/canvas.py`
(where the marks actually happen).**

Status: the scaffold is complete and working end to end. Against the brief's build
order that is **M1 and M2 done, M3 done, M4 mostly done**; M5 (rehearsal) and M6
(MCP) are untouched.

---

## What exists

| Milestone | State |
|---|---|
| M1 Foundation | Done. Canvas, round brushes, curved strokes, `look()`, PNG export, seed, sampler sheet. |
| M2 Painterly | Done. Flat/bristle/knife with direction following, paint load and run-out, texture modulation, wet blending, `dry()`, pigment mixing, palette. |
| M3 Composition | Done. Regions, grid, relative placement, stroke-based block-in, values view, side-by-side, diff, history, time-lapse. |
| M4 CLI and guide | CLI done, `PAINTER.md` written, `pip install -e .` works. Not yet exercised by a fresh session. |
| M5 Rehearsal | **Not started.** This is the next thing to do. |
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

tests/test_engine.py      66 tests: bounds, determinism, undo, replay, colour,
                          paint behaviour, composition, persistence, error messages.
scripts/make_brush_sampler.py   regenerates samples/brushes.png — the primary
                          test artefact. Look at it after every engine change.
examples/exercises.py     the abstract warm-ups from PAINTER.md, runnable.
PAINTER.md                the guide a fresh agent is given. The deliverable.
REVIEW.md                 adversarial review: ten defects found and fixed, four
                          things investigated and found *not* to be defects.
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
- **Region names are deliberately neutral** (`upper-band`, not `sky-band`). The
  experiment's second stage is meant to be unprompted.

## Gotchas for the next session

1. **Look at `samples/brushes.png` after any engine change.** Every defect in
   REVIEW.md was found by looking, and none of them by the test suite. Numbers will
   not tell you a stroke has gone mechanical.
2. **Anything linear in per-dab alpha cannot produce a persistent mixture.** If you
   find yourself tuning a wet-blending coefficient and seeing no effect, re-read
   REVIEW.md finding 7 before spending an hour on it.
3. **`np.savez_compressed` appends `.npz`** to a path without it. Save through an
   open file handle. There is a test guarding this.
4. **`import easel.brush as b` gets the function, not the module**, because
   `easel/__init__.py` rebinds the name. Use `from easel.brush import ...`, or
   `importlib.import_module("easel.brush")`.
5. **`sin(pi)` is slightly negative in float32**, and a negative base with a
   fractional exponent is NaN. This bit the `taper` pressure profile.
6. **Windows heredocs**: several multi-KB Python files could not be written through
   `bash` heredocs in this environment. Use the file-writing tool for anything large.

## What to do next, in order

1. **M5 rehearsal.** Paint a reference photo using only `PAINTER.md`, as if a fresh
   session. Every time you reach for the source or for internal knowledge, that is a
   gap in the guide — fix the guide, not the painting. This is the highest-value
   remaining work by a distance, because it is what the whole thing is judged on.
2. **Golden-image tests.** A fixed set of strokes, hashed, so brush-engine
   regressions fail loudly. The property tests catch behaviour, not appearance.
3. **The M4 adversarial review** of the CLI and the guide (REVIEW.md covers M2 only).
4. Consider varying `block_in` direction automatically between passes.
5. Only then, M6 MCP server — one tool per CLI verb, plus `look` returning the image
   inline.

## Verify the scaffold

```bash
pip install -e ".[dev]"
pytest -q                              # 66 tests
ruff check src tests scripts examples
python scripts/make_brush_sampler.py   # then look at samples/brushes.png
python examples/exercises.py           # writes out/ex_*.png
```
