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
Unreachable cells print `~` instead of `*` and are counted separately. Note this
does *not* change what counts as out: `off` is unchanged, so nothing that was
reported stops being reported.

**Superseded in part by M6b.** The split was the right tool and the floor was the
wrong number: finding 33 says why, and the masstones are darker since. The box now
bottoms out at `0.13` rather than `0.235`, `Level3.jpg`'s eighteen unreachable
cells are the painter's own work again, and the guide no longer teaches compressing
a reference's range onto the palette's -- that paragraph was the workaround, and it
is gone. What survives here is the split itself, for the deepest few cells a
photograph can still hold below `0.13 - 0.10`; on an ordinary reference expect none.

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

- **Pressure changes opacity, not width.** ~~Open.~~ **Taken in M7 — see `M7.md`.**
  A stroke at `pressure=0.1` and one at `1.0` cover an identical bounding box - 58px
  tall in both - and differ only in how much paint lands (mean delta 0.013 against
  0.089). Because dabs overlap and accumulate, an opaque colour saturates and the six
  named profiles become visually indistinguishable: guide exercise 2 as written
  demonstrated nothing, and the three pressure columns of `samples/brushes.png` look
  alike for every brush. Making pressure modulate dab radius would fix that *and*
  attack "everything the same width", which is on the brief's clip-art list. It would
  also change every stroke in the engine, which is the thing finding 11 warns against
  doing by eye late in a milestone — so it waited for a milestone of its own, with the
  golden images in place as its gate.

  What M7 did: the **round** tips (`round_soft`, `round_hard`, and so `liner`) scale
  their dab radius with the pressure profile, with a floor of a third of the width
  and never below 0.75 px of radius; the oriented tips keep their chisel, because a
  `flat` brush's width is the mass it lays. Measured after
  (`m7/probe_pressure.py`): `round_hard` at `size=0.06` on a 600 px canvas runs
  14 px at pressure 0.1 against 36 px at 1.0, and a single stroke at
  `pressure=[1, 0]` runs 12 px to 6 px along its length — which is the tapering lid
  line `REHEARSAL2.md`'s eye test could not paint in one mark. The strength formula
  is unchanged, so the light end of a taper still accumulates to nearly full colour
  and reads as thin rather than as faint. Judged on the sampler and on a real
  painting (`m7/mug_compared.png`) before any golden was regenerated.

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

- **The Kubelka-Munk reflectance floor (finding 5's `0.01`) was a floor on the
  answer and not only on the arithmetic.** Carried here through M6b, M6c, M7 and M8
  on the grounds that fixing it would change the wet blend on every soft dab edge in
  the engine, and so wanted a session with the budget to render both versions of a
  real painting and judge. **Taken in M8b, and that premise turned out to be wrong**:
  the correction is *absent* rather than merely small for any colour inside the K/S
  band, so both samplers, both real paintings in `m7/repaint.py` and all seven golden
  images come back byte for byte identical. Finding 35 has the reproduction, the fix,
  the two things the fix itself cost, and what it buys.

---

## Not yet reviewed

The MCP server (M9 in the brief), which is now built (`M9.md`) and has not had an
adversarial code review of its own. What such a pass should aim at: `_place` and
`_plan` in `easel/mcp_server.py` -- the only code in the repo that turns untyped
JSON into engine objects -- and the echoed Python beside them, where two defects
were already found by driving the tools rather than by reading them (`M9.md` §5).
The engine itself is untouched by the milestone, so everything reviewed below still
stands.

---

# Guide critique — before REHEARSAL4

A reading of `PAINTER.md` as a whole, by a reviewer, after the M6 final pass and
before the next run. Not an engine review: the finding is that the guide had
become a lab notebook, and two of its passages were teaching the painter to work
around engine defects rather than reporting them here. What follows is what the
critique said, what changed in the guide, and the two items it leaves open.

## Fixed in the guide

- **It leaked subjects.** The brief says the guide must not contain example
  subjects, and it named sky, water, a post, a wall, a table, a mug, a spoon, hair,
  a coat, a face, an eye and the lip of a cup — and its back-to-front example was
  the estuary REHEARSAL2 painted. Every example is now an abstract mass, the
  landmark names are `top_l` / `top_r` / `base`, and the engine's own painter-facing
  strings (`easel brushes`, the `mark()` docstring and error, `prepare()`'s
  docstring) were neutralised the same way. NOTES gotcha 15 records why the nouns
  matter as much as the code blocks.
- **It had turned into a curve-fitting manual.** "Work down `fixable`, largest
  first, and stop when it is empty" is an optimiser loop, two paragraphs above the
  sentence saying that matching cell by cell is tracing. `compare()` is now asked
  for twice — once on the empty canvas to read the reference's range, once after
  the block-in to check the three masses — and *When to stop measuring* sits
  directly under it. Every calibration number (graphite survival by opacity,
  wetness decay per stroke, the load window, run-out per texture, `block_in`
  overhang, the 35%-versus-20% axis table) moved to `CALIBRATION.md`. The guide
  went from about 8,500 words to about 6,900, a fifth of which is the seven
  exercises.
- **The drawing order contradicted itself.** Section 2 said draw after the far
  masses; the reference section was headed *The drawing, before the masses*. One
  sentence now reconciles them in both places: landmarks before anything, pencil
  after the far masses, near masses on top.
- **The pressure section.** Cut to what pressure does today, with a note in
  `CALIBRATION.md` that M7 rewrites it rather than patching it.

## Fixed after the critique

### 33. The `0.23` value floor is the pigment swatches, not a painting lesson

**Found by**: the guide critique, which called the compression formula, the `~`
marker and two paragraphs on not fighting the floor "an engine defect dressed up as
a painting lesson".

**Evidence.** `Palette.value_of` per pigment, one flat pass on toned grey:
`burnt_umber` 0.23, `ultramarine` 0.26, `alizarin` 0.30, `burnt_sienna` 0.33,
`viridian` 0.39. `mix("ultramarine", "burnt_umber", 0.5)` reads `0.226`, a hair
under umber alone. The mixing model (a power mean of Kubelka-Munk K/S, per
channel) cannot take any channel below the darker ingredient's, so no mixture is
darker than the darkest pigment in the box — and the darkest pigment is a swatch
at `#4A3728`, far lighter than a tube masstone. Real ultramarine and burnt umber
mixed go close to black; that is the whole point of the mixture, and here it
cannot happen. Finding 21 reported the floor correctly and then built a tool
around it; this finding says the floor itself is the defect.

**Fixed in M6b** by darkening the masstones, which is what the human decided
rather than adding a black. The six darks are now written as tube masstones and
the box floors at `0.13`:

| Pigment | Was | Now | Value was | Value now |
|---|---|---|---|---|
| `burnt_umber` | `#4A3728` | `#2A1E1A` | 0.23 | 0.13 |
| `ultramarine` | `#2E3B8C` | `#1A2856` | 0.26 | 0.17 |
| `alizarin` | `#8E2438` | `#3E1A22` | 0.30 | 0.15 |
| `burnt_sienna` | `#8A3D24` | `#56291A` | 0.33 | 0.21 |
| `viridian` | `#20705B` | `#1A4638` | 0.39 | 0.24 |
| `cerulean` | `#2A6FA8` | `#215884` | 0.42 | 0.33 |

`mix("ultramarine", "burnt_umber", 0.5)` reads `0.137` against `0.226` before, and
the model's own limit — the `0.01` linear reflectance floor from finding 5 — is
`0.10`. The three hundredths between them are hue, and they are not recoverable:
a dark that is still blue cannot sit on the floor in all three channels, and
pigments with no hue left break the mixtures findings 5 and 6 protect. Cerulean
came down with the rest to keep the ladder between viridian and cadmium red from
opening into a gap.

**The mixing exponent moved too**, `0.5` to `0.35`, and that was not cosmetic.
Finding 6 chose `0.5` so that white would carry a 50/50 mixture about a quarter of
the way up the palette's value range — `0.235` of it, measured on the old swatches.
Darkening the darks widened the range from `0.73` to `0.83` and left `0.5` crossing
only `0.158` of it: finding 6's own complaint, returning with nothing about white
changed. `0.35` puts it back at `0.234`, and the mixes the finding was tuned
against land where they did (`cerulean + white` at `0.7`: `0.698` → `0.707`; the
ultramarine/burnt-sienna cool grey `0.567` → `0.555`). Lower again and yellow +
blue loses its green and goes brown, so `0.35` is where it stops. `blend_wet` uses
the same exponent, so the palette's number and the canvas's pixel stay the same
mixture; it costs about `1.2x` in the per-pixel wet blend.

**Every golden image moved, and was looked at first** — the three `marks_*` cases,
`drawing`, and the sampler, plus a real painting (`rehearsal/own*.py` re-rendered
under both palettes, which is a scratch comparison and not a change to the record).
The darks are deeper and still hold their colour; break-up, dry brush, the tooth
speckle, the knife edge and the graphite showing through a glaze are unchanged. On
that painting the value range went from `0.212`–`0.910` to `0.122`–`0.945`.

The guide's floor paragraph, the compression formula in `CALIBRATION.md`, and the
brief's *Reachable* paragraph are rewritten for the new range. `compare()` keeps
its `~` split for the deepest few cells a photograph can still hold — see
finding 21.

**Also fixed here: exercise 1 was a trap.** It asked "do the steps look evenly
spaced in greyscale?" of nine steps mixed at equal white ratios, which under this
model run `0.03` to `0.21` apart — the answer was plainly no and the exercise had
no way to say so. It now mixes to a *value*, bisecting for the ratio, and the nine
bands render `0.148` to `0.951` in steps of `0.100`. The ratios it prints (a third
of white for the first step, nine tenths for the eighth) are the lesson the old
version buried.

## Open, with evidence

## Fixed since the critique

### 34. Sweeping a shaped mass is a recipe the painter has to retype

**Found by**: the guide critique.

The guide argues, correctly, that a mass with a silhouette is laid as passes swept
along its edge and stepped inward, not as a box and not as columns. It then handed
the painter fifteen lines of code to do it. That is an API call — phase M6c in
the brief has the shape — and the recipe sits in `CALIBRATION.md` until it is one.

**Fix.** `s.sweep(edge, brush, color, into=, depth=, size=, passes=, cross=,
closed=, density=)` in `easel/session.py`. The first pass runs along the boundary
and each one after it is the same curve offset one part-brush further in — the same
spacing rule `block_in` uses — with successive passes alternating direction, and
`cross=` lays a second set leaning across the first. It emits ordinary strokes, so
the log, `undo` and `replay` needed no changes at all.

Two things the recipe left to the painter, and this had to decide:

- **Which side of the edge the mass is on.** An open boundary has two sides and
  guessing is the loudest possible failure — the whole shape lands inside out — so
  `into=` is required for one: a compass word or an angle steps every pass the same
  way, which is what the recipe did, and an `(x, y)` point inside the mass steps
  each point along the boundary's own normal instead, which is what a curved edge
  needs. A closed boundary has an inside, so `closed=True` needs neither.
- **What happens past the middle.** Offsetting a closed curve inward eventually
  folds it through itself, and every pass after that crosses itself. Points that
  travel backwards along the boundary relative to the last one kept are dropped, and
  a pass with nothing left is not laid: asking for more depth than the mass has
  costs strokes that never happen rather than a scribble in the middle of a good
  mass.

**Measured** (`scripts/probe_sweep.py`, one boundary, three ways, re-run under
M6b's darks): a `block_in` over the bounding box puts 19.4% of its paint outside
the shape and scores 35.9% on the axis-alignment metric; the sweep, for the same
five strokes, puts 6.5% outside and scores 20.9%. Crossing at 26° takes the value
spread inside the mass from `0.031` to `0.011` for twelve more strokes, without
moving the silhouette. The numbers and the sheet are in `CALIBRATION.md` under
*`sweep`*; the recipe is out of it, and the guide's *A region is a rectangle*
paragraph is one call.

**Additive, as the brief asked.** No golden image moved; one was added
(`tests/golden/sweep.png`, the geometry rather than the marks). Ten tests in
`tests/test_precision.py`.

---

# The wet-blend reflectance floor — M8b

Item 11 of the brief, and the last thing before the server. One finding, carried in
*Open, with evidence* since the M6 code review and fixed here. `m8b/README.md` is the
evidence; `m8b/compared.png` is the pair.

### 35. The reflectance floor was a floor on the picture, not just on the arithmetic

**Found by**: the adversarial code review during M6 — the only finding in this file
found by reading the code rather than by rendering something and looking at it, and the
only one whose reproduction a painter could not have run, because its two halves
concealed each other.

**Symptom, one.** A pixel with no paint landing on it changed colour. `Canvas.stamp`
blends a dab's whole *square* bounding box, and a round tip's corners have an alpha of
exactly zero, so a black pixel in one of those corners came away at sRGB 25 — from a
dab whose mask value at that pixel was `0.00000000`. One `round_soft` dab on a black
canvas moved 625 pixels off zero where the tip reaches 437.

**Symptom, two.** A colour below the floor could not be laid as written, at any
opacity. `cadmium_yellow` (`#FFC012`, blue linear `0.006`) painted opaque read blue 25
against its swatch's own 18; a literal `#000000` landed at grey 25; and
`mix("cadmium_yellow", x, 0.0)` — mixing with *nothing* — came back seven levels of
blue lighter than cadmium yellow.

**Cause.** `blend_wet()` and `mix_many()` convert every ingredient to K/S space, and
`_to_ks` clips its input to `[0.01, 1 - 1e-4]` first. The clip was never taken back
off, so it was not only a floor on the mixing arithmetic — where finding 5 needs it —
but a floor on the answer. At an `amount` of zero the blend returned the *clipped*
canvas rather than the canvas.

Why it stayed open so long: the two halves hid each other. The canvas could only hold a
sub-floor pixel if a sub-floor colour could be laid, and symptom two says it could not.
The M6b re-measurement therefore found `0.0000%` of pixels below the floor on a real
painting and concluded the first half was unreachable. That was true, and beside the
point — it was unreachable because the second half was blocking the door.

**Fix.** The clip stays on the arithmetic and comes back off the mixture, weighted by
how much of each ingredient is in it (`_solo`, `_unclip` in `easel/color.py`). `amount`
of 0 returns the canvas and 1 lays the colour, both exact to the eighth bit of the
export. Finding 5 is untouched — the K/S maths still runs on clipped values — and the
mixtures it and finding 6 were tuned against do not move: `cadmium_red + ultramarine`
is the same violet `(66, 49, 64)`, `cerulean + white` the same `(132, 189, 206)`, the
ultramarine/burnt-umber dark and the cool grey identical to the level. The only
mixtures that move are cadmium yellow's, in the blue channel it writes under the floor,
by at most 3 of 255.

Two things the fix itself cost, both found by measuring rather than by reasoning:

- **Measured against `np.clip` it leaks.** The K/S round trip lands a hair below its
  own input, so an offset taken against the clip rather than against what the round
  trip actually returns left a constant `1.7e-6` gap in one direction on *every* blend.
  Sub-floor pixels drifted downward with no convergence — a near-black went 23 levels
  adrift over 5000 dabs, which is this same finding again in slow motion. Measured
  against `_solo` the two cancel, and a pixel that settles a hair under the floor is
  pinned there on the next dab rather than creeping.
- **It has to be skipped where the clip does not bite.** Computing it unconditionally
  cost 20% of the time to paint a picture, and shifted in-band results by a few parts
  in a million for no reason anyone could see. Gated on `_outside_band`, in-band work
  is bit for bit what it was — which is why no golden moved — and the common path came
  out about 5% *faster* than before, because the incoming colour's K/S is now worked
  out on the `(3,)` colour rather than on a broadcast copy of the whole dab.

**Judged on the sampler and a real painting, as the brief asks.** Nothing in the
existing corpus moves: the seven goldens, `samples/brushes.png`, `samples/shapes.png`
and both real paintings in `m7/repaint.py` are byte for byte identical, and
`tests/test_floor.py::test_work_inside_the_band_is_bit_for_bit_what_it_was` holds that
against the pre-M8b formula written out in full. What the change *buys* is in the
controlled pair in `m8b/`, painted with a supplied near-black: the dark mass goes from
18 distinct levels to 32, and from 39.8% of its pixels pinned at the old floor's value
to 2.9%, with local contrast up from 4.55 to 6.06. Looked at, and the gain is not that
the dark is darker. Two fifths of that mass was a single value — which is what a hole
looks like — and the bristle comb's streaks and the linen tooth inside it were being
crushed flat against the floor. They survive now.

**What it changes outside the engine.** `PAINTER.md` and `CALIBRATION.md` both said
"nothing in this engine reflects less than `0.01` linear", which was two claims wearing
one coat: the *box* bottoms out around `0.13` because of the pigments in it, and the
*engine* will lay whatever colour it is handed. Only the first is a painting lesson,
and this is finding 33's distinction again. Both files now say so and neither changes
its advice: mix your darks, do not reach for a tube of black. `palette.py`'s rule that
a dark swatch must be written at or above the floor was a workaround for this defect
and is gone; `tests/test_floor.py` checks every pigment against what the canvas
actually receives instead, and `cadmium_yellow` — which broke that rule and always had
— passes.

---

# Adversarial code review — engine, CLI, security, CI and test coverage (post-M8b)

Two reviews, done together. The first continues the practice above: read the code
itself, not by rendering and looking, hunting for crashes, corruption and
silently-wrong results — this time over the areas that had not had a dedicated
code-level pass since the M6 code review (`regions.py`'s shape and sweep code from
M6c/M8, the painting-ops half of `session.py`, and the M7/M8b changes to
`brush.py`/`stroke.py`/`color.py`), plus a re-pass of everything reviewed before, on
the grounds that a lot of code has landed since. The second is broader than the
brief's own framing asks for: a general pass over security/trust boundaries,
`.github/workflows/ci.yml` and `pyproject.toml`, and whether the test suite actually
proves what it claims to — not just "does the output look painterly."

Method: fourteen independent reviewers, one per file or dimension, each handed the
full list of findings already fixed above so as not to re-report them. Every finding
below was then checked by two more reviewers working from the code alone — one
trying specifically to refute it, one judging whether the proposed fix was correct
and proportionate — and only survived here if both agreed it was real. Thirty-eight
candidates went in; thirty-seven survived that pass. (The other: a claim that
`Region` accepted non-finite bounds the way `Polygon` guards against — true, but the
reviewers judged the reproduction given didn't establish it caused the "permanent
undo/log corruption" claimed. Finding 47 below fixes the same gap anyway, found
independently and reproduced against `Canvas.region_px`.)

## Fixed

### 36. A malformed `rng_state`, `meta` blob or log entry in a session file failed silently or crashed raw

**Symptom.** `_decode_rng` wrapped the whole state-restore in `try: ... except
Exception: pass`, so a corrupted `rng_state` field was swallowed and `Session.load()`
quietly handed back a session seeded from OS entropy instead of the file's own seed —
two loads of the *same file* then painted differently from that point on, with no
error at all. Separately, `json.loads` on a corrupted-but-zip-valid `meta` blob or log
entry raised a bare `json.JSONDecodeError`, which `Session.load()`'s except clause
(`zipfile.BadZipFile, KeyError, TypeError, EOFError`) did not list, so it escaped as a
raw traceback instead of the same clear message every other corruption case gets.

**Fix.** `_decode_rng` no longer swallows its own exception — a bad state now
propagates. `ValueError` (which `JSONDecodeError` subclasses) was added to
`Session.load()`'s except tuple, so both failure modes turn into the same
`"... is not a valid Easel session file, or is corrupted"` message
(`easel/session.py`). `test_block_in_after_a_reload_draws_from_the_same_stream_as_never_saving`
covers the rng half; no test exercised the swallowed-corruption path directly since
by definition it never raised.

### 37. `Session.replay()` reset the look counter and dropped the prepared reference

**Symptom.** `replay()` returns a fresh session sharing the original's `out_dir`, but
its `_look_counter` restarted at 0 — the very next `look()` on the replayed session
silently overwrote `look_001.png`, a file the original session had already written.
`_preparation` was not carried across either, so `replayed.ref_shape(...)`,
`.sketch()` and `.look_areas()` all raised `"No prepared reference yet"` right after a
`prepare()` + `replay()`, even though `marks` and `assisted` — state of exactly the
same kind — were already preserved two lines above.

**Fix.** `replay()` now also copies `_look_counter`, `_last_look` and `_preparation`
onto the fresh session, the same treatment `marks` and `assisted` already got
(`easel/session.py`).

### 38. A failed `stroke()`/`pencil()` orphaned an undo snapshot, so the next `undo()` deleted an unrelated stroke

**Symptom.** `stroke()` and `pencil()` push an undo snapshot, *then* parse the points
and call `paint_stroke`/`draw_pencil`, whose own validation (bad shape, a NaN/Infinity
point) can still raise. A raised exception there left a snapshot on the stack with no
matching log record. `History.pop_snapshots()` assumes a strict 1:1 correspondence
between its snapshot stack and the log — so the next `undo(1)` popped that orphan
against the *previous, successful* record instead, silently deleting a stroke that had
nothing to do with the failure.

**Fix.** `History.discard_snapshot()` drops the most recently pushed snapshot without
touching the log; `stroke()` and `pencil()` call it in an `except` around the fallible
part of each, then re-raise (`easel/history.py`, `easel/session.py`). Found
independently by two reviewers, one reading `session.py`'s painting operations, one
reading `history.py`'s undo bookkeeping.

### 39. `undo()` never trimmed time-lapse frames for the strokes it undid

**Symptom.** Neither of `undo()`'s two paths (the fast snapshot restore, or a full
rebuild from the log) removed the corresponding frames from `History._frames`, so a
time-lapse GIF or contact sheet kept frames for strokes no longer on the canvas.

**Fix.** `History.drop_last_frames(n)` removes the most recent `n` frames;
`undo()`'s fast path calls it with the count of undone records that actually produced
a frame (every kind except `dry`, which only touches wetness and has nothing a plain
render would show change). The log-rebuild path needs no separate handling: it
replays only the kept records through the same stroke/pencil/dry/erase calls, which
now build exactly the right frame count on their own (`easel/history.py`,
`easel/session.py`).

### 40. `erase()` never recorded a time-lapse frame

**Symptom.** `erase()` visibly changes the rendered canvas — it clears the `sketch`
channel, which the thumbnail includes — the same way `stroke()` and `pencil()` do,
but unlike them it never called `add_frame()`, so a drawing rubbed out mid-painting
vanished from the time-lapse with no frame showing it happening.

**Fix.** `erase()` now records a frame when `timelapse` is on, matching `stroke()`
and `pencil()` (`easel/session.py`). This also closes finding 39's `frames_to_drop`
count for `erase` records.

### 41. `easel run` silently discarded painted strokes when a script called `sys.exit()`

**Symptom.** `sys.exit()`/`exit()`/`quit()` raise `SystemExit`, which is not an
`Exception` subclass, so `_cmd_run`'s `except Exception:` never caught it. Uncaught,
it propagated straight out of `main()`, skipping `session.save()` entirely — a
script that exited early (deliberately, or a stray `exit()` copied from an
interactive example) silently lost everything painted so far, and with exit code 0
the CLI looked like it had succeeded, with nothing saved and no message printed.

**Fix.** `_cmd_run` now catches `SystemExit` explicitly, saves the session, and
prints a clear message before returning the script's own exit code
(`easel/cli.py`).

### 42. `easel mark --forget` with no name silently listed marks instead of erroring

**Symptom.** `_cmd_mark` checked `args.name is None` before checking `args.forget`,
so `easel mark p.easel --forget` (no name given) fell into the "list every mark"
branch and silently ignored the flag — it neither erred nor forgot anything.

**Fix.** `_cmd_mark` now raises a clear `ValueError` when `--forget` is given without
a name (`easel/cli.py`).

### 43. `History.summary(last=0)` returned the whole log instead of nothing

**Symptom.** `self.records[-last:]` with `last=0` is `self.records[-0:]`, which
Python treats as `self.records[0:]` — the entire log, not the empty slice
"the last zero entries" implies.

**Fix.** `summary()` checks `last <= 0` explicitly and returns `""`
(`easel/history.py`).

### 44. `History.save_contact_sheet(columns=0)` crashed with a raw `ZeroDivisionError`

**Fix.** Raises a clear `ValueError` up front instead (`easel/history.py`).

### 45. NaN/Infinity `Canvas` dimensions or `texture_strength` bypassed validation and crashed raw, or silently NaN'd the whole canvas

**Symptom.** `if width < 8 or height < 8` lets NaN and Infinity straight through —
both compare `False` to `< 8` — so `int(width)` then failed with an unrelated raw
`ValueError`/`OverflowError` instead of the constructor's own clear message. A NaN
`texture_strength` was never checked at all and silently NaN'd the whole tooth field
and, through it, every pixel it gates — rendering as solid black with no error
anywhere near the cause.

**Fix.** `Canvas.__init__` now checks `math.isfinite` on both dimensions before the
size comparison, and validates `texture_strength` is finite before using it
(`easel/canvas.py`).

### 46. `stamp()` clamped thickness but not wetness, so a bad `wetness_gain` could pin a pixel's paint acceptance shut

**Symptom.** `thickness` is clamped to `[0, MAX_THICKNESS]` right after it is
updated; `wetness` was not. A brush override with an out-of-range (or NaN)
`wetness_gain` could push a pixel's wetness far past 1.0, or to NaN permanently.
`effective = alpha * (1.0 - 0.55 * wet)` then goes negative and clips to zero for
every dab that lands there — the pixel stops accepting paint until wetness decays
back down, which at the normal 6%-per-stroke rate can take hundreds of strokes for a
large overshoot, and never happens at all for NaN.

**Fix.** `wetness` is now clamped to `[0, 1]` in the same place thickness already
is (`easel/canvas.py`).

### 47. `Region` accepted NaN/Infinity bounds, crashing opaquely wherever they were later used

**Symptom.** `Region.__post_init__` only checked `x1 <= x0`/`y1 <= y0`, both of which
are `False` for NaN — unlike `Polygon`, which already guards its points with
`math.isfinite`. A `Region` built this way crashed with a raw, unrelated exception the
first time a consumer multiplied a bound by a canvas dimension and rounded it to a
pixel index (`Canvas.region_px`), far from anywhere that named the actual problem.

**Fix.** `Region.__post_init__` now checks `math.isfinite` on all four bounds first,
matching `Polygon` (`easel/regions.py`).

### 48. `thumbnail_srgb8()` could produce a zero-width or zero-height frame on an extreme aspect ratio

**Symptom.** The box-average downsample divides both axes by a `step` sized off the
*longer* one. A canvas far thinner than `step` on the other axis — an extreme aspect
ratio, still at or above the 8px minimum — floored that axis's block count to zero,
handing PIL a zero-width or zero-height frame: corrupting the time-lapse in memory and
crashing `save_gif()` on it.

**Fix.** Each axis's step is now capped at that axis's own size before dividing. For
the ordinary case (both axes at least `step`) this changes nothing — the cap does not
bite — so no golden image moved (`easel/canvas.py`).

### 49. `draw_pencil` mis-anchored its sub-pixel mask, jumping pencil lines a pixel at a time

**Symptom.** The tip mask's sub-pixel phase was computed against `math.floor(cx)`,
but the mask was then handed to `canvas.rub(cx, cy, ...)` with the *raw* `cx`
still attached — and `rub()` anchors a mask with `round(cx)`, not `floor(cx)`.
Whenever a dab's fractional position was `>= 0.5`, `round` and `floor` disagreed by
one whole pixel, so the mask (built for one anchor) landed at another, snapping the
line sideways. `paint_stroke`/`Canvas.stamp` already avoid this by computing the floor
first and passing that integer value on; `draw_pencil` did not.

**Fix.** `draw_pencil` now floors `cx`/`cy` first and passes that value to
`canvas.rub()`, matching the pattern `paint_stroke` already uses
(`easel/stroke.py`). **This changes pencil line rendering** — looked at on the
`drawing` golden case (before/after, both pencil lines and the two demonstration
dabs) before regenerating: the wavy lines and the circle outlines are visibly the
same drawing, with individual segments landing a pixel more precisely on their
intended path. `tests/golden/drawing.png` and its hash are regenerated; no other
golden case touches pencil and none of the other six moved.

### 50. `StrokeResult.bounds` used the canvas's long side for both axes, understating extent on a non-square canvas's short axis

**Symptom.** A dab's pixel radius was converted to normalised units by dividing by
`canvas.long_side` for *both* the x and y extents, while the dab's centre was
correctly normalised per-axis (`/width` and `/height` separately). On a canvas far
wider than tall, this understated the reported extent on the y axis by a factor of
`height / long_side`.

**Fix.** The radius is now normalised per axis, the same way the centre already is
(`easel/stroke.py`). `StrokeResult.bounds` is not currently read by anything in the
engine (not stored on `StrokeRecord`, not consumed by `session.py`), so this has no
rendering effect — it only corrects the metadata a direct `paint_stroke()` caller
would see.

### 51. `parse_color()` never validated finiteness, so a NaN colour component silently NaN'd the canvas

**Symptom.** Every path through `parse_color` — the already-linear fast path and the
tuple/list/array path — accepted a NaN or Infinite component. NaN sails through
`np.clip` unchanged (it is neither `< 0` nor `> 1`), so it reached `blend_wet`, which
NaN's every pixel it touches from then on — rendering as solid black with no error
anywhere near the actual cause. This is the same failure mode as finding 45's ground
colour, from the palette/mixing side rather than the canvas-construction side.

**Fix.** Both paths now raise a clear `ValueError` on a non-finite component
(`easel/color.py`).

### 52. `Polygon.inset()` skipped its own fold-detection when growing

**Symptom.** The mitre-offset self-intersection check (area not collapsed, centre
still inside) only ran when shrinking (`amount > 0`) — the boolean short-circuited it
away entirely when growing (`not smaller` was `True`). A spiky or very concave
outline grown outward can fold through itself at its own reflex vertices just as
easily as one shrunk inward can, so growing had no protection at all.

**Fix.** The same sanity check now runs both ways, mirrored for the grow direction:
the *original* centre must still land inside the grown shape, and the grown area must
not have shrunk. Either check failing falls back to the existing
`_toward_centre` scaling, exactly as the shrink path already did
(`easel/regions.py`).

### 53. `Preparation.split()` could hand back an area number k-means never assigned to any pixel

**Symptom.** k-means can converge with an empty cluster on duplicate-heavy colour
data — a large flat-coloured area is exactly that. `split()` unconditionally added a
fresh number to its returned list for every requested part, regardless of whether
`assign` actually contained that cluster's index. A number with no pixels behind it
crashed with `KeyError` on the caller's very next `prep[number]`,
`prep.region(number)`, or `prep.outline(number)`.

**Fix.** `split()` now skips a part whose cluster is empty and only returns numbers
that were actually assigned to at least one pixel (`easel/prepare.py`).

### 54. `compare()`'s per-cell means could divide into an empty slice and silently vanish as NaN

**Symptom.** Dividing a small region into ten row/column tenths could round a cell's
start index to or past the array's own width/height, slicing to an empty array and
`.mean()`-ing it to NaN. A NaN `delta` compares `False` against any threshold, so a
cell like that silently dropped out of `off`/`fixable`/`worst` instead of being
reported — a real difference in a legitimately-out region could go unmeasured simply
because the crop was too small to subdivide cleanly.

**Fix.** Each axis's start index is now clamped to a valid row/column first, and its
end index given at least one unit past that and clamped to the array — guaranteeing a
non-empty slice regardless of how small the source array is (`easel/measure.py`).

### 55. `look(values=True, diff=True)` tinted the whole canvas as changed even when nothing was painted

**Symptom.** `Session.look()` always stored `_last_look` as the plain colour render
(`canvas.to_srgb8(impasto=impasto)`), ignoring both `values` and `sketch`. The next
`diff=True` call then compared whatever *this* call actually rendered — greyscale,
when `values=True` — against that stored colour array. Grey and colour differ almost
everywhere by construction, so the diff overlay tinted nearly the entire canvas as
"changed" regardless of what had actually been painted since the previous look.

**Fix.** `_last_look` is now captured through a small helper that renders the same
way `render_look` itself does — greyscale when `values=True`, colour otherwise, both
respecting `sketch` — so a diff compares like with like. `look_image()` had the
identical bug and got the identical fix (`easel/session.py`).

### 56. `look(region=..., grid=True)` drew the full A-H/1-8 grid mislabelled onto the crop

**Symptom.** `_draw_grid` divided the panel's own pixel dimensions into eight equal
columns and rows regardless of whether the panel was a crop — correct only when
looking at the whole canvas. Against a `region=` crop it drew eight lines spanning
just the crop and labelled them A through H, which do not correspond to any real
cell boundary: exactly the "which cell is this" question the grid exists to answer,
answered wrong.

**Fix.** `_draw_grid` now positions every line and label through `frame.to_px`, which
already maps normalised canvas coordinates into the panel — the whole canvas when
uncropped (unchanged behaviour) or the crop's own sub-rectangle when cropped, only
labelling cells actually visible (`easel/look.py`).

### 57. `CellCompare.off` ignored the `Comparison`'s own configured threshold

**Symptom.** `compare(threshold=...)` lets a painter set what counts as out, and
`Comparison.off`/`.fixable`/`.table()` all honour it — but the per-cell
`CellCompare.off` property read the module-level `VALUE_THRESHOLD` constant instead,
regardless of what was actually asked for. A cell's own `.off` could disagree with
whether it appeared in the comparison's own `off` list.

**Fix.** `CellCompare` now carries the threshold it was built with, and `off` reads
that instead of the constant (`easel/measure.py`).

### 58. `Session.load()` never cross-checked `meta`'s width/height against the stored array shapes

**Symptom.** `canvas.width`/`canvas.height` came from `meta` alone and drove every
pixel-coordinate computation from that point on (`to_px`, `region_px`, `stamp`'s own
clipping) without ever being checked against the actual shape of the loaded `rgb`
array. A hand-edited or corrupted file with mismatched declared dimensions would
either paint at the wrong scale silently or crash deep inside a `stamp()` call, far
from anywhere that could say why.

**Fix.** `Session.load()` now raises a clear `ValueError` (caught and wrapped the
same way every other corruption is) when the stored array's shape disagrees with
`meta`'s declared width/height (`easel/session.py`).

### 59. A crafted or oversized reference image escaped the CLI's clean-error handling

**Symptom.** Pillow's `DecompressionBombError` — its guard against a crafted or
merely huge image decoding into an enormous array — subclasses plain `Exception`,
not `OSError`, so `main()`'s except tuple did not catch it: it escaped as a raw
traceback instead of the same `"easel: ..."` message every other bad-input case
gets. (`PIL.UnidentifiedImageError`, for an unreadable file, is already an `OSError`
subclass and was already covered.)

**Fix.** `main()`'s except tuple now names `PIL.Image.DecompressionBombError`
explicitly (`easel/cli.py`).

### 60. CI set no `permissions:`, leaving the default (broader) `GITHUB_TOKEN` scope in effect

**Fix.** Added a top-level `permissions: contents: read` — every job here only
checks out code and uploads a build artifact (`.github/workflows/ci.yml`).

### 61. CI's actions were pinned to mutable tags rather than commit SHAs

**Symptom.** `actions/checkout@v4`, `actions/setup-python@v5` and
`actions/upload-artifact@v4` are tags, not immutable references — whoever controls
that tag can repoint it to different code without this repository's review.

**Fix.** All three pinned to the commit SHA of their current latest release, with
the version kept alongside as a comment (`actions/checkout@11d5960a... # v4.4.0`,
and so on) — the standard form Dependabot's already-configured `github-actions`
ecosystem update recognises and keeps current. A Dependabot PR bumping the same
three actions to v7 (mutable tags) merged to `main` while this one was open;
resolved by taking v7 and re-pinning it to its own commit SHA
(`actions/checkout@3d3c42e5... # v7.0.1`, `actions/setup-python@5fda3b95... #
v7.0.0`, `actions/upload-artifact@043fb46d... # v7.0.1`) rather than reverting
either change (`.github/workflows/ci.yml`,
`.github/dependabot.yml`).

### 62. CI never installed the `mixbox` extra, so `color.mix_many`'s pymixbox path was never exercised by any job

**Symptom.** `pyproject.toml` declares `mixbox` as a distinct optional-dependency
group from `dev`; the `test` job installs only `.[dev]`, on every leg of its matrix.
`color.py`'s mixbox import is wrapped in a bare `try/except`, so `MIXBOX_AVAILABLE`
is always `False` in CI, and the runtime call site at `mix_many` (line ~289, marked
`# pragma: no cover`) has no guard of its own — a pymixbox API break there would
surface as an uncaught crash for the one audience that opts in, with zero warning
from CI.

**Fix.** A new `tests/test_mixbox.py`, skipped unless `MIXBOX_AVAILABLE`, checks the
integration seam itself (runs, returns a valid finite colour, is order-independent,
mixing a colour with itself is a no-op) without asserting exact values — the rest of
the suite hard-codes Kubelka-Munk-specific numbers that were never meant to be
mixbox-aware, so this file must not be allowed to flip `MIXBOX_AVAILABLE` on for
them. A new `mixbox` CI job installs `.[dev,mixbox]` on a single OS/Python leg and
runs *only* that file, leaving the main `test` job's install and every other test
untouched (`.github/workflows/ci.yml`). Verified locally: installing `pymixbox` and
running the *existing* suite unmodified breaks eight tests (`test_floor.py` and six
golden cases, all hard-coded to the Kubelka-Munk model) — confirming the new job has
to stay scoped to the one new file, not broadened to the whole suite.

### 63. `Session.rng`'s save/load round-trip had no test coverage at all

**Symptom.** `block_in()`/`sweep()` draw their pass-wobble from `self.rng`, which is
persisted through `_encode_rng`/`_decode_rng` on save/load. No test in the suite
calls `block_in`/`sweep` on a session obtained from `Session.load()` — the closest,
`test_undo_after_reload_uses_replay`, exercises `replay()`, which reseeds `self.rng`
from `self.seed` directly rather than testing whether the *persisted* stream survives
a round trip. A broken round trip (finding 36's swallowed-exception bug, among other
possible ones) would have passed the whole suite silently.

**Fix.** `test_block_in_after_a_reload_draws_from_the_same_stream_as_never_saving`
paints identically in two sessions, saving and reloading one partway through, and
asserts the canvases are pixel-identical (`tests/test_engine.py`).

### 64. `undo()`'s log-rebuild fallback never re-adopted the replayed session's `rng`

**Symptom.** `undo()` falls back to `self._adopt(self.replay(upto=keep))` when too
few snapshots are cached, or always for a freshly-loaded session. `replay()` builds a
fresh session whose `rng` is correctly reseeded and re-advanced for exactly the kept
records — but `_adopt()` only copied over `canvas` and `history`, leaving
`self.rng` wherever it happened to be before the undo. A `block_in()`/`sweep()`
painted after this fallback path drew its wobble from a stream a true replay up to
that point would never have produced.

**Fix.** `_adopt()` now also takes on `other.rng` (`easel/session.py`). See *Open,
with evidence* below for the related case this does not close.

### 65. The golden determinism test only spot-checked one of seven cases

**Symptom.** `test_golden_cases_are_deterministic` built `"marks_linen"` twice and
compared the hashes — a real property, but checked for exactly one of `gc.CASES`'s
seven. Determinism depends on how each case consumes randomness (a bristle's comb,
`block_in`'s wobble, dab jitter), which is exactly the kind of thing that differs
case to case and that a single spot-check would miss.

**Fix.** Parametrized over every case (`tests/test_golden.py`). All seven pass.

### 66. The shape sampler's "cross" column duplicated the axis pass for shapes whose own axis runs vertical

**Symptom.** `scripts/make_shape_sampler.py`'s "cross" column used
`direction=("axis", 90.0)` — but `90.0` is an *absolute* angle, not "90 degrees from
whatever this shape's axis is". For the sheet's mostly-horizontal shapes this
happened to look like a cross by coincidence; for `hull` and `ribbon`, whose own axis
already runs close to vertical, the second pass landed at nearly the same angle as
the first instead of crossing it.

**Fix.** The cross direction is now resolved per shape, as `(shape.axis, shape.axis +
90.0)` (`scripts/make_shape_sampler.py`). `samples/shapes.png` regenerated and
looked at: the `cross` column now visibly crosshatches every row, `hull` and
`ribbon` included, where it previously matched the `axis` column almost exactly for
those two.

## Open, with evidence

- **`blend_wet()` does not honour `MIXBOX_AVAILABLE`.** `mix_many()` routes through
  pymixbox's latent-space blending when the optional extra is installed;
  `blend_wet()` — the per-pixel function every actual dab on the canvas goes through
  — always uses the built-in Kubelka-Munk arithmetic regardless. `blend_wet`'s own
  docstring says plainly why this matters: *"the palette's number and the canvas's
  pixel are the same mixture or neither can be trusted."* When mixbox is installed,
  they silently stop being that. Not fixed here: pymixbox's Python API
  (`rgb_to_latent`/`latent_to_rgb`) takes one colour triple at a time, not an array,
  so making `blend_wet` route through it for real would mean either a per-pixel
  Python loop in the hottest path in the engine (a stamp can touch thousands of
  pixels; painting a whole passage stamps thousands of times) or a from-scratch
  vectorised reimplementation of mixbox's latent space — either is real engineering,
  neither is a small fix, and finding 62 establishes this path has *never* been
  exercised by CI, so there is nothing here yet to test a fix against. Wants a
  session with the budget to prototype and measure the performance cost, the way
  finding 11 got before it was fixed.

- **`Session.load()` restores `out_dir` from the session file with no validation.**
  `out_dir` round-trips through save/load because that is how `easel look p.easel`
  keeps writing to the same place across CLI invocations — a real, load-bearing use,
  not an oversight. But it means loading and then `look()`-ing a `.easel` file
  someone else handed you writes wherever *they* set `out_dir` to, silently,
  including an absolute path outside the working directory. Rejecting an absolute or
  `..`-escaping `out_dir` outright would also reject configurations a user
  legitimately sets themselves with `--out-dir` when *creating* a session — the CLI
  has no way to tell "the invoker chose this" from "the file says so" apart, because
  it is the same field either way. Wants a product decision (a new CLI flag to
  override the stored value? a warning when a loaded `out_dir` differs from the
  cwd?) rather than a rule a reviewer should pick unilaterally.

- **`undo()`'s fast snapshot path does not rewind `Session.rng`.** Finding 64 fixed
  the log-rebuild fallback; the common case — snapshots still cached, `undo()` just
  restores one — does not rewind `self.rng` at all, so `s.block_in(...); s.undo(1);
  s.block_in(...)` draws different wobble than a fresh session doing the same two
  calls would. A correct fix needs an `rng` snapshot at the same granularity as the
  canvas snapshot, but `block_in`/`sweep` draw their wobble from a lazily-evaluated
  generator (`_shape_paths`/`_block_paths`/`_sweep_wobble` are Python generators),
  interleaved *between* the per-path `stroke()` calls that push each canvas
  snapshot — so by the time a given `stroke()` call's snapshot is pushed, that
  path's own wobble has already been drawn from `self.rng`. Snapshotting `self.rng`'s
  state at that point and restoring it on undo would leave the stream advanced past
  the undone stroke's own draw rather than rewound to before it — subtly wrong in a
  way a quick fix here is more likely to get wrong than right. Affects only the
  specific sequence "paint with `block_in`/`sweep`, undo, paint with `block_in`/
  `sweep` again" — `stroke()`/`pencil()`/`dry()`/`erase()` alone never touch
  `self.rng` at all, and neither does the normal `stroke()`-count-many-undos-then-
  keep-painting pattern PAINTER.md actually teaches.

## Investigated and *not* a defect

- **`Region` accepting non-finite bounds**, reported independently by the security
  reviewer alongside finding 47 with a claim of "permanent undo/log corruption" from
  it. The adversarial-refutation pass couldn't reproduce corruption specifically
  (a `Region` built this way crashes on first real use — `Canvas.region_px`, per
  finding 47 — rather than silently corrupting anything), so it was not counted as
  confirmed on its own terms. Finding 47 closes the same underlying gap regardless.
