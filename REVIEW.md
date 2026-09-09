# Adversarial review — M1/M2 scaffold

Read as a hostile painter looking for reasons the output will look like clip-art,
rather than as an author checking their own work. Every finding below was found by
rendering something and looking at it, not by reading code.

Regenerate `samples/brushes.png` and look at it after any engine change. It is the
artefact that catches these; the test suite is not.

---

## Fixed

### 1. Thin tips laid down a picket fence
**Symptom.** `flat` and `knife` strokes were crossed by regular vertical bars.

**Cause.** Dab spacing was measured against the tip *diameter*. A flat or knife tip
is thin in the direction it travels (`aspect × diameter`), so spacing it like a
round tip left visible gaps between consecutive stamps.

**Fix.** Spacing is now measured against the tip extent along travel
(`easel/stroke.py`), and preset values were rescaled to match.

### 2. Overlapping stamps rippled at the dab frequency
**Symptom.** Even after (1), a soft regular banding remained along flat and knife
strokes.

**Cause.** The along-travel profile had a flat top. Overlapping plateau profiles do
not sum to constant coverage — they ripple at the stamp period.

**Fix.** The `u` profile is now a full-width ramp with no plateau
(`easel/brush.py`), and spacing is kept well under the ramp width. Measured ripple
on a straight flat stroke fell from ~7.8% to under 1%.

**Method worth reusing.** The ablation that found this: paint one straight stroke,
subtract a moving average, take the FFT of the residual, and read off the dominant
period. Ripple at exactly the dab spacing points at the stamp profile; ripple at
another period points somewhere else.

### 3. Running out of paint produced a halftone screen
**Symptom.** As load ran out, strokes broke up into a regular dot grid — print, not
dry brush.

**Cause.** Gating a near-periodic woven height field with a smooth threshold is a
halftone screen. That is precisely how halftones are made.

**Fix.** An aperiodic `grain` field is mixed into the tooth before gating
(`easel/canvas.py`), and the linen weave was coarsened and given much more thread
wobble (`easel/texture.py`).

### 4. Per-dab jitter made banding worse, not better
**Symptom.** Turning up `jitter` to break up regularity increased measured ripple
from 1.5% to 5.8%.

**Cause.** Independent per-dab noise makes neighbouring dabs clump and gap. The
clumps are themselves a periodic-looking artefact.

**Fix.** Jitter and size variation are now a *smoothed wander* along the stroke
(`_wander` in `easel/stroke.py`) — the uneven edge of a real brush, without the
ripple.

### 5. Red + blue came out green
**Symptom.** Kubelka-Munk mixing sent red + blue to dark olive instead of violet.

**Cause.** The reflectance floor was `1e-4`. A colour with a near-zero channel gets
an enormous K/S in that channel, which then swamps every mixture.

**Fix.** The floor is `0.01` — real pigments never absorb a channel completely — and
the shipped pigment hexes have no zero channels (`easel/color.py`).

### 6. White barely lightened anything
**Symptom.** `mix("cerulean", "titanium_white", 0.55)` returned a saturated blue,
not a pale sky blue. Every tint a painter asked for came out too dark.

**Cause.** Single-constant Kubelka-Munk treats white as just another reflectance,
but real titanium white is a strong scatterer that dominates a mixture well beyond
its volume share.

**Fix.** Mixtures combine as a *power mean* of K/S with exponent `0.5` rather than an
arithmetic mean. Checked against a table of known paint mixes: white now tints
properly while yellow + blue stays olive and red + blue stays violet.

**Rejected first.** Restoring luminance by multiplying the mixed colour. It
*increases* saturation, so white + red clipped to a neon orange instead of going to
pink. Mixing with white must desaturate; a multiply cannot do that.

### 7. Wet-into-wet did nothing
**Symptom.** The wet/dry exercise showed two near-identical yellow bands. Laying
yellow over wet blue gave the same result as over dry blue.

**Cause.** Two compounding problems.

First, attenuating a dab's alpha over wet paint is *algebraically identical* to using
a smaller alpha — it is linear in the same space. A stroke lays ~100 overlapping
dabs, so the pixel still converges on the pure incoming colour. Any purely
per-dab-alpha scheme has this property; no amount of tuning fixes it.

Second, once the brush was made to pick up wet paint, it sampled *under its own
centre* — where consecutive dabs overlap by ~95%. It only ever tasted the paint it
had just laid down.

**Fix.** The brush now picks up wet paint at its **leading edge** and carries the
contamination forward, with replenishment from its own reservoir so the carried
colour settles at a stable mixture instead of drifting. Measured: green/red ratio of
yellow over wet blue moved from 0.556 (dry) to 0.710 (wet).

**Rejected first.** Contamination without replenishment. It accumulates without
bound, so a stroke smears whatever it first touched across the entire canvas — the
block-in washed from blue to white left to right.

### 8. `easel new` wrote a file the other commands could not find
**Symptom.** Every CLI command after `new` reported "No session at p.easel".

**Cause.** `np.savez_compressed` silently appends `.npz` to a path that lacks it, so
`easel new p.easel` wrote `p.easel.npz`.

**Fix.** Saving goes through an open file handle (`easel/session.py`). There is a
regression test asserting the exact filename is honoured.

### 9. `easel undo` silently did nothing
**Symptom.** `easel undo p.easel 2` reported "Undid 0 strokes".

**Cause.** Undo used in-memory snapshots, and each CLI command loads a fresh session
from disk. Snapshots are far too large to persist.

**Fix.** Undo falls back to rebuilding from the stroke log, which is exact. This also
delivers the replay requirement: strokes are seeded per-index rather than from one
running stream, so `replay()` reproduces the export byte for byte.

### 10. The engine suggested what to paint
**Symptom.** Regions were named `sky-band` and `ground-band`.

**Cause.** Author convenience.

**Fix.** Renamed to `upper-band` and `lower-band`. The unprompted painting stage is
supposed to be unprompted, and a region called "sky" is a prompt.

---

## Investigated and *not* a defect

- **Dark specks inside light strokes on linen and rough.** These are the toned ground
  showing through paint that the canvas tooth held off. Verified no pixel is darkened
  by painting: the impasto relief only moves sRGB by ±17. This is dry brush working.
- **Yellow dabbed onto a wet blue passage turning green.** Correct pigment physics.
  It is documented prominently in `PAINTER.md` as the surprise it will be.
- **Angle quantisation (10°) faceting curved flat strokes.** Suspected, then tested
  by rendering curved strokes at 10°, 5° and 2°. The results are indistinguishable,
  so the coarse step stays and the mask cache stays small.
- **`rough` texture passing more paint than `smooth` at low load.** Expected: a wider
  spread of peaks means more peaks clear the threshold. The dry-brush property is
  *brokenness*, not total coverage, and rough measures ~1.75× smooth on band
  variance. The test that asserted coverage was wrong and was rewritten.

---

## Known, still open

- **Residual dab-frequency ripple** on `flat` and `knife` at large sizes. Much
  reduced, and at this level it reads as ridging from a loaded brush rather than as
  machine stripes. Worth another pass if it ever reads as mechanical in a real
  painting.
- **`block_in` passes can read as parallel hatching.** Mitigated by per-pass wander
  and by `direction="cross"`, and `PAINTER.md` tells the painter to vary direction
  between passes. A future version should probably vary it automatically.
- **~200 ms per stroke** on a 1024×768 canvas — about a minute for a 300-stroke
  painting. Acceptable, not fast. The hot path is the per-dab window blend.
- **`.easel` files are large** (megabytes) because the full float32 canvas is stored.
  Since replay is exact, a future format could store only the log and rebuild on
  load, trading file size for load time.
- **`easel.brush` is both a module and a function.** `from easel.brush import Brush`
  works; `import easel.brush as b` gets the function, because `__init__` rebinds the
  name. A known Python papercut, called out here so the next person does not lose
  ten minutes to it.

---

## Not yet reviewed

The M4 review (after the CLI and guide are exercised in anger) has not been done.
The rehearsal in M5 — painting from `PAINTER.md` alone and treating every reach for
the source as a guide bug — has not been done either. Both are still open.
