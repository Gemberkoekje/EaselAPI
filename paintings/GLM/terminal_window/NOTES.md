# A terminal window glowing green in a dark room — painting notes

**To understand this, start by reading files `prelude.py`, then `pass1a.py`, then `pass2.py`.**
The prelude holds the value plan and the named masses; the passes hold the method.

Exported: `painting.png` · time-lapse `painting.gif` · build-up grid `sheet.png`.
Session `painting.easel`, 1024x768, linen on a custom dark ground `#2e332c`, seed 7.
**126 of 300 strokes spent.** Rebuilt by running the pass scripts in order against the session file.

## Why this subject

The only light in the picture is inside it — a screen in a dark room — so every form is
lit by the subject itself, and the painting is about the *fall* of that light (screen →
glow → pool → darkness), not about a monitor. That reason is still in the picture: the
light's reach (halo, pool, lit keyboard rim, mug rim) is what the eye travels.

## The plan, written before the first stroke

Values as numbers: room 0.15–0.19 · desk 0.21 · glass 0.28 (lit centre 0.33) · pool
0.24–0.37 · phosphor text 0.56–0.72 · cursor 0.85 · bezel 0.14 (darkest, so it separates
against the lit wall) · keyboard 0.17 · floor 0.14. Three horizontal bands (wall, desk,
foreground), crossed by the monitor and the pool's diagonals. `compare()` after the
block-in: **0 of 6 places more than 0.10 out**; the one touching pair within 0.10 (dim
desk / keyboard ends) is an intended lost edge.

## Decisions and gotchas

- **Glazes crossing wet under a block-in print concentric rings.** The first halo was six
  crossing glazes; the bezel then landed in the not-yet-dry film and the wall right of the
  monitor came out ringed. Cost one `undo` back to the bare masses (the scraper, used
  properly). Replacement: ONE tight, low-contrast inward scumble (`halo_a 0.20 → halo_b
  0.235`, n=10) — smooth, and its own boundary disappears at 0.01 contrast.
- **`edge="hard"` scallops.** A masked block-in leaves the brush's own pass-ends at the
  outline: chisel bites with a `flat`, dab-end bites with a `round_hard`. The glass went to
  `edge="clean"` with the solid round tip — the contour sweep covers the edge strip; its
  slightly rounded corners happen to suit a monitor.
- **`region("bottom")` is the bottom THIRD, not the foreground band** — first version of
  pass 5 laid a dark film over the pool and printed a straight bar across it. Rehearsal
  caught it before committing; the foreground band shape `fore` (y 0.865+) was the intended
  target, and the pool's brightness survived.
- **Pressure lists on a `flat` change paint, not width** — used deliberately on the pool
  strokes (faded ends by paint, not by taper); the engine warns each time; accepted.
- Landmarks (`s.mark`) carried every feature; the mug is anchored entirely to `mug_c`
  arithmetic after its rim light and body drifted apart once.

## The closing checklist, honestly answered

- Clear light / mid / dark in greyscale: **yes** — text+cursor / glass+pool / room+floor.
- Edges varied: **yes** — hard at the screen corners and keyboard rim, soft in the halo,
  lost where desk meets wall and where the keyboard's ends dissolve.
- Ground showing through: **yes** — 12.78% bare ground reads as texture in the darks.
- Highlights few and deliberate: **yes** — cursor (0.85), prompt core, pool hotspot, mug rim.
- Mechanically repeated / tool-shaped marks: the checker counts three borderline round-tip
  marks (prompt core, mug far rim, contact shadow — all `liner`-scale feature lines);
  cropped in, they read as the thing's edges, not discs. The parallel-marks warning is
  standing: the scene's own planes are horizontal; the bands are crossed by the monitor and
  the pool, and the halo/pool passages break direction. Accepted as the scene's truth.
- Back to front: bezel under glass, mug's far rim under its contents under its near rim. **Yes.**
- Subject's share: 12/127 marks are noted `subject` (9%); counting the subject's own light
  (halo, pool, glass, bezel, glow glazes) the cluster is ≈58 marks ≈ **46%, against a
  ~45% plan**. The noted-only number under-reports; both are recorded here.
- Weakest passage: the wall's texture above the halo is thin paint over bare ground — the
  next strokes would go there if there were a next pass.
- Why this subject: the fall of light from a single source in the dark. **Still in it.**

## File map

- `painting.easel` — session state (log, canvas)
- `prelude.py` — mixtures (all via `at_value`), landmarks, named masses
- `draw.py` — graphite underdrawing (free)
- `pass1a.py` — three big masses · `pass1b.py` — halo scumble + pool strokes
- `pass2.py` — stand, bezel (clean), glass (clean/round), glow glazes, keyboard
- `pass3.py` — phosphor text, cursor · `pass4.py` — keyboard rim, mug, desk-edge spill
- `pass5.py` — corner darks, floor, one broken edge · `pass6.py` — highlights, signature
- `out/` — every look, rehearsal and compare along the way
- Calibration exercises live in `../scratch/` (value scale, wet/dry, box-vs-shape, swatch strip)
