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

---

# M6 review: found by the golden images, on their first run

The brief has asked for golden-image tests since M2 and they never existed. They
were built first in M6, before anything else in the milestone, and they failed on
the first full run of the suite — not because M6 had broken anything, but because
they were the first thing to compare two renders that had been produced in
different orders.

### 19. The same script painted different pixels depending on what ran before it
**Symptom.** `pytest tests/test_golden.py` passed on its own and failed as part of
the suite: 20% of pixels differed, max channel delta 49. Running the same golden
case twice in one process gave identical output; running it after a few unrelated
`tip_mask` calls did not.

**Cause.** The tip-mask cache was keyed on `ceil(radius)` while the mask was
*computed* from the exact radius. So a brush asking for r=5.9 got whatever mask
r=5.1 had built earlier in the process, and which one that was depended on the
order of everything that had run before it (`brush.py`).

**Why it matters.** This is the determinism promise, which the brief states in its
"decisions already made" and which everything downstream leans on: `replay()`,
CLI `undo` (which rebuilds from the log rather than from snapshots), and the
reproducibility of any painting a session hands back. Every CLI command is a fresh
process with its own cache history, so a painting built up over ten `easel run`
calls could not be reproduced by replaying its own log — and nothing in the API or
the test suite could have shown that. Size jitter means a real painting requests
hundreds of distinct radii per stroke, so this was firing constantly, not in a
corner case.

**Fix.** Quantise the radius to quarter-pixel steps *before* anything is computed
from it, and key the cache on the quantised value, so a mask is a pure function of
its cache key. A quarter pixel is finer than the existing sub-pixel phase step, so
nothing visible is given up. Every mask shifts by up to a quarter pixel: the
goldens moved on stroke edges only (max channel delta 59, mean 0.58, nothing
structural), which was looked at side by side before regenerating.

**Guarded by** `test_a_tip_mask_is_a_pure_function_of_its_arguments` and
`test_the_same_script_paints_the_same_pixels_in_a_dirtied_process`, plus every
golden case.

**What this says about the review loop.** Three adversarial reading passes over
this code did not find it, and no amount of looking at `samples/brushes.png` would
have: the sheet is regenerated in one process and looks correct every time. It took
two renders of the same script made under different conditions. That is the class
of defect visual regression exists for, and it was sitting in the engine for five
milestones because the tests the brief asked for had been deferred five times.

## Round five: the M6 final pass (`REHEARSAL3.md`)

Three fresh sessions painting from `PAINTER.md` alone, plus two notes from the
human. One engine defect, and two engine gaps that were tools telling the painter
something untrue.

### 20. `erase()` cleared the graphite and left the line in `sketch_lines()`

**Found by**: the assisted fresh session, with a reproducer, now
`rehearsal3/assisted/t2_erase_sketchlines.py`.

`erase(region)` rubbed the drawing off the canvas correctly. `sketch_lines()`,
though, was a filter over the log -- every record of kind `pencil`, whole -- so it
handed back lines that were no longer drawn, including ones wholly inside the
erased region. The guide documents `sketch_lines()` as the way to re-lay a drawing a
block-in has buried, so the two calls compose into a trap: rub out the line you
decided was wrong, recover the drawing, and the wrong line is back, silently.

Nothing on the canvas was wrong, which is why no test caught it. The canvas and the
API simply disagreed about what had been drawn.

**Fixed** by deriving `sketch_lines()` from the log in order rather than filtering
it: pencil records accumulate, erase records clip. A line that only crosses the
erased region comes back as the pieces outside it, cut at the boundary
(Liang-Barsky, written out in `_segment_inside`). Because it is derived and not
stored, it is automatically right through undo and replay -- there is a test for
both. `tests/test_precision.py::test_erase_takes_the_line_out_of_sketch_lines_too`
and `::test_erase_cuts_a_line_that_only_crosses_the_region`.

### 21. `compare()` asked for values the palette cannot reach

**Found by**: two fresh sessions independently, each mid-painting, each reporting
about twenty-five strokes spent on it.

There is no black pigment, by the brief's rule, so the palette floors at `0.235`:
`burnt_umber`, unmoved by eight dried passes (`0.231`), unmoved by four rounds of
glazing (`0.234`), `0.228` with all five darks mixed. A lamp-lit photograph does not
floor anywhere near there -- `Level3.jpg` has eighteen of its sixty-four cells below
what any stroke can reach. `compare()` reported those cells as out, marked `*`,
indistinguishable from a cell that was out because the painting was wrong.

`PAINTER.md` did state the range. It did not matter: a painter trusts the tool in
front of it over a paragraph four sections back, which is the same lesson as gotcha
0 in `NOTES.md` from the other direction. A measuring stick that reports an
unmeetable target is worse than one that reports nothing, because the painter spends
strokes on it.

**Fixed** with `Palette.darkest_value` and `Comparison.unreachable` / `.fixable`.
Unreachable cells print `~` instead of `*` and are counted separately, and the guide
now says what to do instead -- compress the reference's range onto the palette's
rather than matching it. Note this does *not* change what counts as out: `off` is
unchanged, so nothing that was reported stops being reported.

### 22. Nothing could sweep a mass along its own axis

**Found by**: the human, looking at the paintings.

`block_in(direction=)` took four names -- horizontal, vertical, a 45-degree
diagonal, and cross. Every named region is an axis-aligned rectangle. An oriented
tip is held square to its travel. So every mass in every painting this engine has
produced was laid along the canvas's axes, and measured that way: every copy came
out squarer than the photograph it was copied from, and both unprompted paintings
came out squarer than anything else in the repo (`rehearsal3/probe_axis_alignment.py`).

Not strictly a defect -- nothing lied. It is a capability that was never there, and
one that was there and undocumented: `angle_follow=False, angle=45` has turned any
oriented tip since M2, and `PAINTER.md` never mentioned it.

**Fixed** by accepting a number of degrees, or a sequence of them, in
`direction=`. Additive: the four named branches are byte-for-byte what they were,
with a test asserting `"cross"` still means a horizontal pass then a vertical one,
and every golden image regenerated identical. The guide gained *The angle of the
mark*, and its own silhouette recipe -- which laid a vertical column at every step,
and scored worst of four in the probe -- was rewritten to run passes along the form.

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

---

# Adversarial code review — CLI, session and engine robustness

Every prior round above was found by rendering something and looking at it. This
one was different on purpose: three fresh sessions read the code itself (no
painting), one over `cli.py`/`session.py`/`history.py`, one over the numeric core
(`canvas.py`, `brush.py`, `stroke.py`, `color.py`, `texture.py`), one over
`measure.py`/`prepare.py`/`look.py`/`palette.py`/`regions.py` -- hunting for
crashes, corruption and silently-wrong results a "does the painting look right"
pass would not surface. Every finding below was reproduced against the actual
code, not inferred from reading it. None of it moved a golden image.

## Fixed

### 23. `dry()` did not snapshot before mutating the canvas, desyncing undo from the log

**Symptom.** `s.stroke(...); s.dry(); s.undo(1)` restored the canvas to the state
*before the stroke*, not before the dry -- while only removing the `dry` record
from the log. The log still claimed the stroke happened; `s.replay()` then
disagreed with what was on screen.

**Cause.** Every other canvas-mutating call (`stroke`, `pencil`, `erase`) pushes an
undo snapshot immediately before it changes the canvas, so one snapshot always
corresponds to the record it undoes. `dry()` called `self.canvas.dry(...)` and
logged a record without ever pushing a snapshot, so the snapshot on top of the
stack after a `dry()` belongs to whatever came *before* it.

**Fix.** `dry()` snapshots first, like the others (`easel/session.py`). Also fixed
in passing: it logged its record's `index` as `len(self.history.records)` instead
of `self._index_base + len(...)`, the only one of the four record-adding methods
that skipped `_index_base` -- harmless everywhere except inside a `rehearse()`
trial, where the number shown in the log would have been wrong.
`test_undo_after_dry_lands_on_the_state_before_dry_not_before_the_stroke`.

### 24. `undo(n)` past `MAX_SNAPSHOTS` silently undid fewer strokes than asked

**Symptom.** A script that made more than 24 strokes (the snapshot cap) in one
process and then called `s.undo(30)` got only 24 strokes undone, no error -- while
the identical log, saved and reloaded, correctly undoes all 30 through log replay.
Same session, different answer, depending only on how many snapshots this process
happened to have cached.

**Cause.** `undo()` took the fast snapshot path whenever *any* snapshots existed,
even fewer than requested, and returned however many that path actually managed
rather than falling through to the always-correct log-replay path for the
shortfall.

**Fix.** The snapshot path is only taken when it can satisfy the whole request;
otherwise `undo()` rebuilds from the log, exactly as it already did for a
freshly-loaded session (`easel/session.py`).
`test_undo_beyond_cached_snapshots_matches_a_fresh_reload`.

### 25. `easel new` silently overwrote an existing session

**Symptom.** Re-running `easel new p.easel ...` on a painting already in progress
replaced it with a blank canvas, no confirmation, no error.

**Fix.** `easel new` now refuses to touch an existing file unless `--force` is
given (`easel/cli.py`). `test_new_refuses_to_clobber_an_existing_session_without_force`.

### 26. `Session.save()` was not atomic

**Symptom.** `save()` opened the destination `.easel` file directly and streamed
the new archive into it. The file is the painting's only copy; a crash, a full
disk, or a killed process partway through left it truncated with no way back.

**Fix.** Saves now write to a temp file beside the destination and `os.replace()`
it into place -- atomic on both POSIX and Windows for a same-filesystem
destination, which the temp file always is (`easel/session.py`).
`test_save_replaces_the_file_atomically_and_leaves_no_temp_behind`.

### 27. A corrupted or incompatible session file crashed with a raw traceback

**Symptom.** Three separate ways to get a `Traceback (most recent call last)`
instead of the `easel: ...` message every other bad-input case gets: a truncated
`.easel` file (`zipfile.BadZipFile`) -- the exact failure mode finding 26's
non-atomic save made a real risk, not a contrived one; a log entry with a field
this build's `StrokeRecord` does not know about (`TypeError`); an output path
that collides with an existing non-directory file (`FileExistsError`).

**Fix.** `Session.load()` wraps the structural part of reading a session
(`zipfile.BadZipFile`, `KeyError`, `TypeError`, `EOFError`) and re-raises as the
same `ValueError` every other unreadable-session case already produces, without
swallowing the deliberate format-mismatch `ValueError` it already raised. The
CLI's top-level handler now also catches `OSError` (covers `FileExistsError` and
friends) alongside the exceptions it already caught (`easel/session.py`,
`easel/cli.py`). `test_a_corrupted_session_file_raises_a_clear_error`,
`test_a_corrupted_session_file_fails_the_cli_cleanly`.

### 28. `easel run`'s `SyntaxError` in the painter's own script escaped as a raw traceback

**Symptom.** A script with an ordinary Python 2-ism or typo failed at `compile()`,
outside the `try` that gives a runtime error in the same script the friendly
"script raised, session saved with N strokes" treatment -- bare traceback instead.

**Fix.** `compile()` gets its own `try`, reporting the syntax error clearly and
distinctly from a runtime failure (nothing ran, so there is nothing to save)
(`easel/cli.py`). `test_run_reports_a_syntax_error_without_touching_the_session`.

### 29. `cell("A12")` silently resolved to cell A1 instead of raising

**Symptom.** `cell("A12")`, `cell("D67")` and `cell("B23")` all returned a valid
cell -- the *wrong* one -- instead of raising. `cell("H88")` correctly raised, by
luck.

**Cause.** The validation and the lookup both wrote `text[1:] not in GRID_ROWS` /
`GRID_ROWS.index(text[1:])`, and Python's `in` on a string is substring
membership: `"12" in "12345678"` is `True` (a match at index 0), so a two-digit
row typo passed validation and `.index("12")` returned 0.

**Fix.** Require `len(text) == 2` and check `text[1]` (a single character) against
`GRID_ROWS`, not `text[1:]` (`easel/regions.py`). This also feeds `as_region()`
and `span()`, both of which fall back to `cell()`.
`test_two_digit_row_typo_is_rejected_not_silently_truncated`.

### 30. A region touching the canvas's or a reference image's far edge could crop to zero pixels

**Symptom.** `Canvas.region_px()` clamped its two endpoints to the same `[0,
width]` range independently, so a region rounding to exactly `width` on its low
edge produced `x0 == width`, and the "at least one pixel" guard then returned
`x1 = width + 1` -- one column past the array. `Session.compare()`'s own,
separate cropping of the *reference* image had the same class of bug with no
guard at all: two independently-clamped endpoints do not by themselves guarantee
`x1 > x0`. A crop landing exactly on that gave a zero-width PIL crop, which does
not raise -- it silently fed an empty array into `compare()`'s per-cell means,
which came back as NaN, which then broke `Comparison`'s own bookkeeping (a NaN
cell is neither "off" nor "not off" under `abs(delta) > threshold`, so it printed
as out-of-range in the table while being excluded from the counts the same table's
caption claims to summarize).

**Fix.** Both places now clamp the *start* of the crop first, to leave room for at
least one pixel before computing the end -- `x0` to `[0, width-1]`, then `x1` to
`[x0+1, width]` -- instead of clamping both ends to the same range and only
patching up the width afterwards (`easel/canvas.py`, `easel/session.py`).

### 31. NaN/Infinity coordinates crashed opaquely, or were silently persisted

**Symptom.** A NaN or Infinity point in a stroke or a pencil line reached
`np.arange` inside path resampling and failed there with a cryptic numpy message
naming no bad input (`ValueError: arange: cannot compute length`, or a
maximum-size error for Infinity) -- plausible for an agent whose own upstream
coordinate math momentarily divides by zero. Separately, `mark()` used
`np.clip(x, 0, 1)` to bound a landmark, and `np.clip` does not sanitise NaN, so a
non-finite mark was accepted silently and written into the session's own JSON
metadata as a bare `NaN`/`Infinity` token -- round-trips through this codebase's
own `json.loads`, but is not standard JSON.

**Fix.** `paint_stroke()` and `draw_pencil()` reject non-finite points with a
clear message before resampling; `mark()` rejects a non-finite position
(`easel/stroke.py`, `easel/session.py`).
`test_nan_or_inf_point_is_rejected_not_a_cryptic_numpy_crash`,
`test_marking_a_non_finite_point_explains_itself`. Also fixed:
`pressure_curve([], n)` (an empty pressure list) reached `np.interp` with empty
arrays instead of raising; `test_empty_pressure_list_explains_itself`.

### 32. `merge()`/`split()` could trace the wrong connected component's outline

**Symptom.** `_trace_outline`'s own docstring claims "only the outer boundary of
the largest run", but it started tracing from the mask's topmost-then-leftmost
pixel regardless of which run that belonged to. Invisible for an area fresh out of
`prepare_reference()` (always one connected run), but `merge()`'s own docstring
example is joining hair split by an ear -- two pieces that do not touch -- and the
outline of the merged area silently covered only whichever piece happened to
contain that one pixel, sometimes the *smaller* one. `split()`'s k-means
partition has the same exposure: two separated patches of similar tint can land
in one part with no regard for contiguity. `Session.sketch()` draws pencil
straight from these outlines, so assisted mode could silently omit whole pieces of
a merged mass from the underdrawing.

**Fix.** `_trace_outline` now finds every 8-connected run in the mask and traces
only the largest, matching what it already claimed to do
(`easel/prepare.py::_largest_component`).
`test_outline_traces_the_largest_run_when_merge_joins_two_that_do_not_touch`.

## Open, with evidence

- **The Kubelka-Munk reflectance floor (finding 5's `0.01`) also perturbs pixels
  that are not being mixed with anything.** `blend_wet()` converts *both* colours
  to K/S space before weighting them by `amount`, and `_to_ks` clips its input to
  `[0.01, 1-1e-4]` first -- so a pixel darker than that floor gets rounded up to it
  by the K/S round-trip even at a tiny `amount`, not just `amount == 1`. Reachable
  through ordinary painting, not a contrived input: `Canvas.stamp()` calls
  `blend_wet` across a dab's whole square bounding box, and any pixel inside that
  square but outside the tip's actual footprint has a small but non-zero `amount`
  from the mask's soft edge. Measured: a pure-black pixel one mask-corner away
  from an unrelated `round_soft` stamp lightened from linear `0.0` to `0.016`ish
  (sRGB `(0,0,0)` to roughly `(26,26,26)`). The same floor also caps how dark any
  *pigment* can ever read: `cadmium_yellow`'s blue channel (`#FFC012`, linear
  `~0.006`) can never paint truer than sRGB blue `25`, off by 7 from the swatch's
  own `18`, at any opacity, because every application re-floors it.

  Not taken, on purpose: the floor is load-bearing for finding 5 (without it, a
  near-zero channel's K/S blows up and swamps a real mixture -- "red + blue comes
  out green"), so shrinking it risks reopening that finding, and the fix that
  *doesn't* risk it -- keeping the floor's effect proportional to `amount` instead
  of applying it to `dst` outright -- changes the wet-blend formula for every soft
  dab edge in the engine, which is most of what this engine paints. That is
  exactly the kind of change finding 11 warns against making by eye late in a
  milestone, and every golden image would need regenerating and *looking at*, not
  just re-hashing, to know whether it actually looks better. Left for a session
  with the budget to render both versions of a real painting side by side and
  judge.

---

## Not yet reviewed

The MCP server (now M8 in the brief), which does not exist yet.
