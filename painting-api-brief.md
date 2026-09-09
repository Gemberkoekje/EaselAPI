# Build brief: headless painting API ("Easel")

You are building a tool that lets an AI agent paint — not draw, not rasterize, but paint: brushes, paint load, wet and dry, canvas texture, mistakes that stay. The tool is headless (no GUI, no Krita), produces PNGs, and is meant to be driven from a Claude Code session by an agent that can look at its own work between strokes.

Two things are being built:

1. **The engine + API** — a library and thin CLI.
2. **The painter's guide** — a document that teaches a *fresh* agent, with no knowledge of the engine internals, how to paint with it well.

The second is not an afterthought. The engine will be judged by what a fresh session paints with only the guide in hand.

## The experiment this serves

After the build, a **separate, fresh Claude Code session** receives only: the installed library, the painter's guide, a canvas size, and a reference photo of an ordinary object. It is asked to paint a faithful copy. When done, it is told: "Now paint something of your own. No subject, no theme, no prompt." Nothing else. The human watches the output and does not intervene.

Design every decision toward that: the painter is a language model that reasons well, sees images well, and is bad at absolute pixel coordinates.

## Decisions already made (override only with a stated reason)

- **Language:** Python 3.12+, numpy for all pixel work. No native dependencies that are painful on Windows (no GObject/libmypaint bindings). Pillow only for PNG I/O and text overlays.
- **Interface, in order of priority:** (1) Python library, (2) thin CLI wrapping it, (3) MCP server — optional, last, only if 1 and 2 are solid.
- **Canvas model:** single canvas, no layers. Real painting has no layers; the painter learns to work in passes instead. Undo exists (snapshots), but is documented as "scraping the canvas," not a free action.
- **Coordinates:** normalized 0.0–1.0 on both axes, origin top-left. Never expose raw pixels to the painter. Add named-region helpers on top (see Composition).
- **Determinism:** every session takes a seed; the same script with the same seed produces the same PNG.
- **Feedback loop:** `look()` is the most important function in the API. Treat it that way.

## Architecture

### Canvas
- Float32 RGB in linear light, converted to sRGB only at export.
- Additional per-pixel channels: `wetness` (0–1), `thickness` (paint height, for impasto and dry-brush behaviour).
- Procedural canvas/paper texture: a height map that modulates paint deposition. Selectable at creation: smooth panel, linen, rough paper. Ground colour selectable (white, toned grey, burnt-sienna wash).

### Brush engine
Dab-stamping along a path (this is how MyPaint and Krita work; do not attempt fluid simulation).
- A **stroke** = a path (list of normalized points, smoothed with Catmull-Rom or similar) + a brush + a pressure profile.
- A **brush** = a tip mask + dynamics. Tip masks are procedural: round soft, round hard, flat (rectangular, rotates to follow stroke direction), bristle (flat with random striations and gaps — this one matters most for looking painterly), palette knife (hard-edged, drags rather than deposits).
- **Dynamics:** size, opacity, hardness, spacing (as fraction of size), jitter, paint load (how much paint the brush carries — it runs out along a stroke), pressure curve (default: taper in and out), speed-to-size mapping.
- **Pressure profile:** the painter gives either a scalar, a list, or a named profile (`taper`, `press_in`, `lift_off`, `even`).
- Deposition is modulated by canvas texture: low paint load on rough texture = dry brush effect for free.

### Paint behaviour
- **Wet blending:** when a stroke lands on wet pixels, it mixes with what's there proportionally to wetness rather than covering it. `dry()` reduces wetness across the canvas (all or a region). Wet also decays slowly per stroke count so the painter doesn't have to manage it constantly.
- **Colour mixing:** naive RGB averaging turns everything grey-brown. Use a pigment-style model. Prefer the `pymixbox` package (Mixbox; verify licence suits this project) — if unsuitable, implement a simple subtractive approximation and document its limits. Mixing applies both on the canvas (wet blending) and on the palette (see below).
- **Smudge / blend tool:** picks up colour from the canvas and drags it. Distinct from painting.
- **Glaze:** a thin transparent layer over dry paint — implemented as low-opacity deposition that does not raise `thickness`.
- **Impasto is optional.** Track `thickness` and offer a subtle relief shading in export if it's cheap; do not let it eat the schedule.

### Palette
A palette object the painter mixes on, like a real one: a small set of starting pigments (a warm and cool of each primary, plus white, a dark — no black by default), `mix(a, b, ratio)`, `tint`, `shade`, `desaturate`, and named slots so the painter can say `palette["sky"]` later. Mixing on the palette uses the same pigment model as the canvas.

### Composition helpers (this is where the model's weakness lives)
- Named regions: `region("top-left")`, thirds grid, golden-section lines, `horizon(0.4)`.
- Relative placement: `below(region, amount)`, `between(a, b)`.
- Shape primitives that emit *strokes*, not fills: `fill_region_with_strokes(region, brush, colour, direction, density)` — block-in as a painter does it, with visible brushwork.
- Value tools: `values_only()` view in `look()` (greyscale), so the painter can check its value structure the way a painter squints.

### look()
Returns a PNG path (and, in the MCP variant, the image itself). Options:
- `scale`: default downsampled to ≤1024px on the long side.
- `grid`: overlay a labelled grid (A–H × 1–8) so the painter can say "the dark shape near D6" and later target `cell("D6")`.
- `region`: crop to a named region at full resolution.
- `values`: greyscale.
- `side_by_side(reference)`: for the copy stage.
- `diff`: highlight what changed since the last `look()`.

### History
Every stroke is logged as data. The whole painting is replayable from the log + seed. `undo(n)` restores a snapshot. Export a time-lapse (contact sheet or GIF) from the log — cheap and very useful for the human watching.

## CLI
`easel new`, `easel run script.py`, `easel look [--grid] [--values] [--region R]`, `easel undo N`, `easel export out.png`, `easel timelapse out.gif`. Session state lives in a single `.easel` file (npz). The CLI exists so a painter can work in small increments from a shell without holding a Python process open.

## The painter's guide (deliverable, `PAINTER.md`)
Written for an agent that has never seen the source. Contents:
- The API, briefly, with 5–6 complete tiny examples.
- **A painting workflow**, not a tool reference: tone the ground → establish the big value shapes with a large brush → check values with `look(values=True)` → refine mid-tones → edges (lost and found) → highlights last, smallest brush, least strokes. Say explicitly: look every 5–15 strokes; a stroke you didn't look at was a guess.
- What the model is bad at and what to do about it: don't reason in pixels, use regions and the grid; don't draw outlines and fill them, paint masses; when something is wrong, paint over it rather than undo.
- What each brush is for, in one line each.
- Nothing about what to paint. The guide must not contain example subjects that would bias the unprompted stage. Use abstract exercises (value scales, edge studies) for its examples.

## Build order

1. **M1 — Foundation.** Canvas, round brush, straight and curved strokes, `look()`, PNG export, seed. Deliver a brush sampler sheet (`samples/brushes.png`): every brush at three sizes, three pressure profiles, on each canvas texture. This sheet is your primary test artefact; regenerate it after every engine change and actually look at it.
2. **M2 — Painterly.** Flat and bristle tips with direction following, paint load and run-out, canvas texture modulation, wet blending, `dry()`, pigment mixing, palette.
3. **M3 — Composition and looking.** Regions, grid, relative placement, stroke-based block-in, values view, side-by-side, diff, history and time-lapse.
4. **M4 — CLI and guide.** CLI, `PAINTER.md`, install instructions (`pip install -e .`).
5. **M5 — Rehearsal.** Run the experiment protocol yourself on a reference image, as if you were the fresh session, using only `PAINTER.md`. Every time you reach for source code or internal knowledge to get unstuck, that is a gap in the guide — fix the guide, not your painting.
6. **M6 — MCP server**, only if everything above is solid. One tool per CLI verb, plus `look` returning the image inline.

## Review loops (do these, don't skip them)

After M2 and again after M4, run an **adversarial review** in a separate reasoning pass: read the code and the guide as a hostile painter looking for reasons the output will look like clip-art. Typical findings to hunt for: strokes with identical edges everywhere, no variation in paint load, colours converging to mud, straight lines that are too straight, everything at the same opacity, a guide that describes functions but not painting. Write findings to `REVIEW.md`, fix them, note what changed.

Visual regression: golden-image tests for a fixed set of strokes. Property tests: strokes never write outside the canvas, undo restores exact state, replay from log reproduces the export byte-for-byte.

## Non-goals
- No GUI, no Krita/GIMP integration, no tablet input.
- No fluid simulation, no physically based watercolour.
- No image-to-image, no style transfer, no diffusion models anywhere in the pipeline. The point is that the strokes are chosen.
- Not pixel art. Not vector.

## Definition of done
A fresh session, given `PAINTER.md` and a reference photo, produces a recognizable copy in under 300 strokes without touching source code, then produces a second painting with no prompt. Both exports plus their time-lapses exist. The engine's author has not seen the second painting before the human has.
