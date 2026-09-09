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
- **`rough` texture passing more paint than `smooth` at low load.** Right about the
  ordering, wrong to stop there — see finding 11 in the M4 pass below. A wider spread
  of peaks does mean more peaks clear the threshold, and the dry-brush property is
  brokenness rather than coverage. But asking only which of two numbers was larger
  meant never asking what happened at the far end of the range, where the threshold
  left the narrow-toothed surfaces entirely and a starved stroke deposited nothing at
  all. The rewritten test asserted the wrong property and has been rewritten again.

---

## Known, still open

- **Residual dab-frequency ripple** on `flat` and `knife` at large sizes. Much
  reduced, and at this level it reads as ridging from a loaded brush rather than as
  machine stripes. Worth another pass if it ever reads as mechanical in a real
  painting.
- **`block_in` passes can read as parallel hatching.** Mitigated by per-pass wander,
  by alternating the travel direction of successive passes (M4 finding 12), and by
  `direction="cross"`; `PAINTER.md` tells the painter to vary direction between
  passes. Varying the *pass axis* automatically is still worth trying.
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

# Adversarial review — M4, the CLI and the guide

Same stance as above: a hostile painter, looking for the reasons a fresh session
will produce something that looks like clip-art or, worse, will quietly produce
nothing at all. This pass drove every CLI verb from a clean directory, ran every
runnable code block in `PAINTER.md` verbatim, and measured what the engine actually
deposited rather than what it reported.

## Fixed

### 11. A starved brush stopped dead instead of breaking up
**Symptom.** `s.stroke(..., load=0.2)` with the default `bristle` brush on the
default `linen` canvas changed **zero pixels**, and returned a record reporting 278
dabs. On `smooth` the same stroke died at `load=0.35`. On `rough` it kept marking
down to `0.1`. Nothing distinguished this from a stroke that worked.

This is the move `PAINTER.md` recommends — "low load plus rough canvas gives you dry
brush … one of the best tools you have" — so a fresh session following the guide, on
the surface the guide itself opens with, would have got nothing and no way to find
out why.

**Cause.** The tooth gate compares surface height against a threshold that rises as
the brush empties: `need = (1 - load) * texture_sensitivity`. Nothing bounded it.
Every texture is centred near 0.5 but they occupy very different spans — the gating
field's 2nd-to-98th percentile range is 0.27 on `smooth`, 0.39 on `linen` and 0.50 on
`rough` — so as the threshold rose it climbed clean past the highest peak of a
narrow-toothed surface. No peak left above the threshold means no paint anywhere.
The M2 review saw the *ordering* this produced (rough passing more paint than smooth
at low load), accepted it as physics, and never asked what happened at the far end of
the range.

**Fix.** One line: the threshold is capped at the surface's own tooth ceiling, its
95th percentile, measured once per canvas (`tooth_ceiling` in `easel/canvas.py`).
A brush therefore always has some peaks left to catch on, whatever it is painting on.
The cap engages *only* where the old code was producing nothing — at every other
load `need` is below it and the arithmetic is unchanged — so `samples/brushes.png`
regenerates byte-for-byte identical.

**Rejected, and why it is worth knowing.** The first fix was more ambitious: express
the threshold as a position *inside* each surface's own tooth range, so all three
textures starve at the same rate and differ only in the character of the breakup. It
worked, and it made the dry-brush window far wider on every surface. It also made the
gate bite into the tooth at every load, and painting a test abstract with it showed
why that is fatal: linen's weave is near-periodic, so a gate that reaches into it
prints the weave across every mass as a regular halftone screen — the exact failure
`build_surface` already warns about in its docstring. Rebalancing the aperiodic grain
against the height map cleared the lattice, but by then a one-line bug fix had turned
into a re-tuning of every stroke in the engine, by eye, immediately before the M5
rehearsal that is supposed to judge it. The narrow fix ships; the range-relative gate
is a reasonable thing to try again *after* M5, with the sampler and a real painting
as the evidence.

**Left as tuning, not a defect.** With the cap in place a `bristle` dry-brush pass on
linen is usable from about `load=0.5` down to `0.4`, faint by `0.35` and barely there
by `0.3`. `PAINTER.md` now gives that window and those numbers rather than the `0.15`
it used to suggest. Whether the window should be wider is a question for a rehearsal
with a real painting, not for a reviewer with a synthetic band.

**Guarded by** `test_a_starved_stroke_still_marks_every_surface`,
`test_canvas_tooth_gates_deposition`, `test_surfaces_break_up_at_their_own_scale`.

### 12. Every block-in pass ran the same way, so every mass faded
**Symptom.** `block_in("all", direction="horizontal")` left the right third of the
canvas **0.21 lighter in linear luminance** than the left third — close to a full
value step, on every mass the painter blocks in, always in the same direction.
`direction="cross"` halved it and left +0.08 on both axes.

**Cause.** Paint runs out along a stroke, and every pass started at the same edge, so
a dozen passes stacked their run-out on top of each other. Nothing in the painting
caused that gradient; the loop did.

**Fix.** Successive passes now alternate direction (`_block_paths` in
`easel/session.py`), the way a hand comes back across the canvas. The gradient falls
to +0.04, the same order as the incidental variation on the other axis.

**Guarded by** `test_block_in_passes_alternate_direction`,
`test_block_in_does_not_leave_a_run_out_gradient`.

### 13. `easel` is often not on `PATH`, and `python -m easel` did not work
**Symptom.** Installs where the scripts directory is not on `PATH` are the norm on
Windows — pip says so itself while installing: *"The script easel.exe is installed
in … which is not on PATH."* The whole shell section of `PAINTER.md` then fails at
its first line, and the obvious fallback answered *"'easel' is a package and cannot
be directly executed"*.

**Cause.** No `__main__.py`.

**Fix.** `src/easel/__main__.py`, four lines. `PAINTER.md` and `README.md` now give
`python -m easel` as the same command by another name, and tell the painter not to
spend any time fixing their `PATH`.

**Guarded by** `test_the_cli_runs_as_a_module`.

### 14. Dabs were reported; paint was not
**Symptom.** A mark's log line read `#015 stroke bristle #3a4a6b 212 dabs` whether it
covered half the canvas or did nothing at all. Dabs are *attempts*. This is what made
finding 11 invisible, and it would hide any future version of it.

**Fix.** `Canvas.stamp` returns the alpha it actually deposited, `paint_stroke` totals
it into `StrokeResult.paint`, and every record carries it. `s.log()` prints it as
`8.4k paint`, or `NO PAINT LANDED` for a mark that changed nothing. A painter reads
the log precisely when the canvas does not look the way they expected — which is
exactly when this is the number they need.

**Guarded by** `test_a_stroke_reports_how_much_paint_landed`,
`test_the_log_says_when_a_mark_laid_no_paint`, `test_paint_survives_a_save_and_reload`.

## Investigated and *not* a defect

- **`easel look --diff` across separate shell invocations.** Suspected dead: the
  previous look is a numpy array on the session, and each CLI command loads, acts and
  exits. It is in fact persisted in the `.easel` file as `last_look` and restored on
  load, so the diff spans invocations correctly. An empty diff between two looks with
  no painting in between is the right answer, not a broken feature.
- **Every code block in `PAINTER.md`.** Twenty-one of the twenty-three execute
  verbatim against a fresh session, reference images and all. The two that do not are
  the API-signature listings, which are deliberately elided pseudo-code and read as
  such.
- **CLI error paths.** A missing session, an unknown region, a missing script, a
  malformed `--size`, an `undo` larger than the history: each exits non-zero with a
  message that names the problem and, where there is one, the fix. None of them threw
  a traceback at the painter.
- **`easel run` on a script that raises.** Saves the session before reporting the
  error, so a half-finished pass survives. Verified deliberately.

## Method, for the next reviewer

Two of these four came from measuring what the canvas *did*, rather than from reading
the code or trusting a return value. The stroke reported 278 dabs and the canvas had
not changed. If you take one habit from this pass, take that one: after any change to
deposition, diff the canvas array either side of a stroke and assert on the pixels,
not on what the function said it did.

The second habit is the one this repo already prescribes, and it caught the first
attempt at finding 11: **paint something and look at it**, not just the sampler
sheet. The sampler shows isolated strokes at full load and it was perfectly happy
with a gate that silkscreened the canvas weave across every accumulated mass. One
throwaway abstract — block-ins, a dry-brush pass, a couple of accents — showed it
immediately. Keep one such script around and run it after any change to deposition.

---

# M5 rehearsal review

Painting a reference photograph from `PAINTER.md` alone. Findings 15-18 are engine
defects the rehearsal surfaced; the guide gaps it surfaced are in `REHEARSAL.md`
and were fixed in `PAINTER.md`. Three of the four below turned up in the first
forty minutes of painting, which is the case for the rehearsal in one line.

### 15. `block_in(direction="diagonal")` painted outside its region
**Symptom.** A block-in aimed at the middle of the canvas smeared across all of it.
Measured: a region spanning x 0.40-0.70 received paint from x 0.20 to x 0.89, and
the overspill was *identical* at brush size 0.20 and 0.08 - so it was not the brush
being wide, it was the geometry being wrong.

**Cause.** The `horizontal` and `vertical` branches of `_block_paths` clamp each
pass to the region's edges. The `diagonal` branch built the whole 45-degree line
through the region and never clipped it, so every pass ran out sideways by the
region's own height at each end.

**Fix.** Clip each diagonal pass to the region, along the line, then extend by the
overhang like the other directions (`session.py`). Diagonal was also the only
direction with no wander, though `_block_paths` documents wander for all of them;
it now gets the same wobble as the others.

**Guarded by** `test_block_in_stays_inside_its_region`, parametrised over all four
directions and two brush sizes. It fails on the old code at x 0.20 against a bound
of 0.30.

### 16. `value_of()` disagreed with `look(values=True)`
**Symptom.** Planning a first pass by the numbers produced a canvas with no value
structure at all. `value_of` called a colour that reads as a light mid-tone `0.26`,
and reported *every* mixed dark as `0.04` - ultramarine, burnt umber, either of
them shaded or desaturated, all identical. There was no way to tell a coat-black
from a burnt sienna with it, though the greyscale view shows them a clear step
apart.

**Cause.** `Palette.value_of` returned linear luminance. `Canvas.values`, which is
what `look(values=True)` renders, returns `linear_to_srgb(luminance(...))`. The two
value instruments the guide offers disagreed by the whole transfer curve, and the
docstring - "how light the colour reads" - described the one it was not returning.
Measured against flat swatches: ochre 0.30 vs 0.58, umber 0.04 vs 0.23, cadmium
yellow 0.59 vs 0.79.

**Fix.** `value_of` encodes to sRGB, so the number and the picture agree exactly
(`palette.py`). `test_white_actually_lightens` asserted `tinted > base * 2.0`, a
ratio that only meant "substantially" in linear units; it now asserts a difference
of 0.15, which is more than one step of a nine-step value scale.

**Guarded by** `test_value_of_agrees_with_the_values_view`,
`test_value_of_separates_the_darks`.

### 17. The tooth gate printed the linen weave as a halftone screen
**Symptom.** A broad scumble at `load=0.55` - inside the window `PAINTER.md` calls
usable, on the default surface - laid an even lattice of dots across the whole
canvas. It reads as silkscreen, and every stroke afterwards sits on top of it.

**Cause.** This is finding 11's rejected fix arriving on its own. The gating field
is `height * 0.72 + grain * 0.28`; the weave is coherent and periodic and the grain
is not, and at that weighting the weave won. Finding 11 predicted exactly this and
deferred it to M5 "with the sampler and a real painting as the evidence". The
rehearsal produced both.

**Fix.** Two changes, in `canvas.py`. The gate weighting goes to 0.52/0.48. On its
own that homogenised the surfaces - the grain was one fixed ~3px cell for every
texture, so with more weight all three broke up at the *grain's* scale instead of
their own, and `test_surfaces_break_up_at_their_own_scale` caught it (rough/linen
fell from 3.23 to 1.40). So the grain's scale now follows the surface: rough coarse,
linen fine, smooth between. Rough/linen is 3.32 after, slightly better than before,
and the three surfaces read as themselves on the regenerated sampler.

**Rejected first, and why it is worth knowing.** The initial attempt added
thread-to-thread variation to the linen weave itself in `texture.py`. It measurably
reduced the weave's local periodicity - row autocorrelation at the thread lag fell
from 0.63 to 0.45 - and did *not* remove the visible screen, because the screen
comes from the gate thresholding the weave, not from the weave's own amplitude. It
was reverted. The lesson: the autocorrelation of the height map is the wrong
instrument here. Look at deposited paint.

**Guarded by** `test_surfaces_break_up_at_their_own_scale`, unchanged - and it is
what caught the bad first weighting.

### 18. The reference panel got neither the grid nor the greyscale
**Symptom.** `look(reference=..., grid=True)` labelled the painting with A-H/1-8 and
left the reference bare. `look(reference=..., values=True)` - a call `PAINTER.md`
prints, commented "compare value structure, not colour" - put a greyscale painting
beside a full-colour photograph.

**Why it matters more than it looks.** The grid is the guide's entire answer to "you
cannot reason in pixels", and copying a reference is the one task where you need to
name a place on *something else* and hit it on your own canvas. Without it there is
no shared vocabulary with the thing being copied, and every coordinate comes out of
the painter's head - precisely the faculty the brief says is unreliable. Half the
rehearsal painting was made before this was fixed and half after; the difference was
not subtle.

**Fix.** `render_look` passes `grid` through to `_side_by_side`, which draws it on
the reference *after* the resize so the cells divide both frames identically; and
`values=True` converts the reference through the same luminance-then-sRGB path the
canvas uses, rather than PIL's `grayscale`, which weights the encoded channels and
would put the two panels on different scales (`look.py`).

**Guarded by** `test_the_reference_gets_the_same_grid_and_the_same_greyscale`.

## Open, with evidence

- **Pressure changes opacity, not width.** A stroke at `pressure=0.1` and one at
  `1.0` cover an identical bounding box - 58px tall in both - and differ only in how
  much paint lands (mean delta 0.013 against 0.089). Because dabs overlap and
  accumulate, an opaque colour saturates and the six named profiles become visually
  indistinguishable: guide exercise 2 as written demonstrated nothing, and the three
  pressure columns of `samples/brushes.png` look alike for every brush. Making
  pressure modulate dab radius would fix that *and* attack "everything the same
  width", which is on the brief's clip-art list. It would also change every stroke
  in the engine, which is the thing finding 11 warns against doing by eye late in a
  milestone. Not taken. `PAINTER.md` now states what pressure does and does not do,
  fixes the exercise so it demonstrates its lesson, and tells the painter that
  varying width is their own job.

---

## Not yet reviewed

M6, the MCP server, which does not exist yet.
