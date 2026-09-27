# Step 3 of `PLAN-0.8.0.md`: guides on any ground, a shape handed to the drawing, and pixels

**To understand this, start by reading the plan's A1, A2 and A5 with their *Step 2* and
*Step 3* notes, then `_draw_guides` in `src/easel/look.py`, `Session.guide`,
`Session.pencil`, `Session.px` and `_outline_of` in `src/easel/session.py`, and `Group` in
`src/easel/regions.py` -- and read `NOTES-step2.md` first if you have not, because this step
builds what that one decided.**

Branch: `claude/v0-8-0-plan-yqm1vt`, off `main` at `41eb63b` (step 2, #90).

---

## What this step was for

The rows the plan calls *small and certain*, built as step 2's bench and the second
painter's answers decided them: the drawing a painter judges its arrangement on, readable
over the paint it is judged against; a shape drawn as the shape; and the pixel helper and
the group the second painter wrote for itself. None of it waits on the first painter's
answers to the step-2 package except A1's casing, which is one constant. Nothing here
changes what a mark lays: no golden moved, and no painting rebuilds differently.

## What landed

| | |
|---|---|
| **A1: a guide that reads on any ground** | `look._draw_guides`: every guide's casing, `(236, 236, 232)` three pixels wide at `_GUIDE_CASING_ALPHA`, 150 -- then every guide's graphite core, one pixel, opaque -- then every note in a box of the panel labels' colours. `_guide_layer` draws one tone of all the guides at once. `_GUIDE_ALPHA` is gone |
| **A2: a shape to `guide()` and `pencil()`** | `session._outline_of`: a `Polygon`, a `Region`, a name, a cell, a span or four numbers becomes its closed outline, through `polygon()`. `pencil(smooth=None)` |
| **A5: pixels, and a group** | `Session.px`, `Session.px_size`, `Session.circle(px=)`; `regions.Group`, `group()` and `_point_of`; `about=` on `Polygon.scaled` and `Region.scaled`; `as_region` refuses a group by name. `Group` and `group` are exported, so every script run by `easel run` has them in scope |
| **The bench** | `probe_bell_session.py` keeps 0.7.0's guide as `draw_07`, for its `today` candidate and row 1's claim, and checks the engine's line against the `casing 150` candidate |
| **Documents** | `REFERENCE.md`: the units paragraph, `pencil`'s row, the shapes, places and session blocks, and a paragraph on `group()`. `RECIPES.md`'s straight-edge recipe. The docstrings of all of the above, and `ellipse`'s, `blob`'s, `polygon`'s and `Polygon.closed`'s. The README's feature table |
| **Tests** | `test_requests.py` *0.8.0 A1* (1), *0.8.0 A2* (5) and *0.8.0 A5* (6); `test_reference.py` holds `group` to the page |
| **Record** | `CALIBRATION.md` (*A guide that reads on any ground* and *Drawing units* say what was built), `CHANGELOG.md`, `SUGGESTIONS.md` (three rows, the round's count), `PLAN-0.8.0.md` |

## Decisions and gotchas

**1. The casing is at 150 of 255 until question 4b comes back.** Both casings met the
plan's target on every one of the bench's 35 grounds; the bench's eye, and mine on its
sheets, found the translucent one reads everywhere and gives way to the paint most, and the
opaque one the loudest -- a white line with a dark core on a dark canvas, a double line on
grey. The pick is the painter's, so it is one constant, `look._GUIDE_CASING_ALPHA`, and
`test_a_guide_reads_over_dark_paint_mid_grey_and_a_light_ground` passes at 150 and at 255.
If 4b comes back opaque: the constant, the CHANGELOG line, the `SUGGESTIONS.md` row and the
plan's A1 note.

**2. The engine's line is the bench's candidate, to the pixel, and the bench keeps 0.7.0's.**
`_draw_guides` makes the same PIL calls in the same order as the probe's `draw_candidate(
"casing 150")`: a layer of every casing, then a layer of every core, then a layer of notes,
each composited over the last. Re-run, `--guides` prints every number it printed before the
build and one line more: *the engine's line since step 3 is the 'casing 150' candidate, notes
and all, to the pixel over 35 of 35*. That needed the probe's `today` to stop calling the
engine: it drew `today` with `_draw_guides`, so after the build it would have measured the
new line under the old name -- and `make_package.py` lays those sheets out as the blind
package's F. The probe now carries 0.7.0's function as `draw_07`, verbatim but for its
constants, for `today` and for row 1's claim.

**3. Measured, not reasoned: the worst grey.** I first wrote that the casing at 150 is
weakest near `0.49`, *about 0.255*, from arithmetic on the two tones. Swept over flat greys
`0.02` to `0.98` a hundredth apart, it is `0.49` and `0.261`, and no grey puts a pixel of the
line under `0.25` (`CALIBRATION.md`). The test's mid-grey band, `0.50`, reads `0.273`.

**4. There is no server tool for `guide` or `pencil`.** The plan said the server's `guide`
and `pencil` tools should take a place. The server's `guide` hands over the documentation,
and nothing on it draws: a drawing goes through `run`, which takes a script, and a script
takes a shape as the Python does. Nothing else to change; struck where it stood in the plan.

**5. `smooth=None`.** `pencil`'s `smooth` defaulted to `True`, and left so, a shape handed
over would either be splined into the pot or have an explicit `smooth=True` silently
ignored. Left out, it is now *splined for a list of points, not for a shape*; passed, it is
kept either way. No list of points draws differently, which is the plan's *not proposed:
moving smooth's default*. Replay passes the record's own `smooth`, so nothing old moves.

**6. `ellipse(..., px=True)` cannot be built as written.** `ellipse()` is a module function
and has no canvas to count pixels on; only the session knows its size. What makes a pixel
radius work is that two radii are measured along the two axes as a point is -- `rx` a
fraction of the width, `ry` of the height -- so `ellipse(p, *s.px(rx, ry))` is exactly `rx`
pixels across and `ry` down, on any canvas (60 by 44 for `30, 22`, measured). That is in
`s.px`'s docstring, `ellipse`'s and `REFERENCE.md`. A round shape takes `px=` on
`s.circle`, which knows the canvas. The alternatives were a session `s.ellipse` shadowing
the module's, with a different default for one radius, or a `px=` on `ellipse` taking the
canvas's size; both are more to know than a helper already there. **This is the call most
worth the owner's look**: the plan wrote `ellipse(..., px=True)`, and the painter asked
only for `s.circle(p, px=25)`.

**7. The group holds points.** The plan says *holding shapes*; the painter's `T()` also
moved the eyes' centres with the head (`far_eye = P(*T(388, 280))` in its prelude), so a
group of shapes alone could not have replaced it. A point in a group comes back a point,
a group in a group comes back a group, and a group unpacks:
`head, eye = group(head, eye).scaled(1.3, about=s.px(300, 266))`. `about=` is a point, a
place or a group, whose middle it takes; left out, the middle of the box round every part.
The test checks the painter's own `T()` point for point, on a polygon, a region and a point.

**8. A group is not a place, and says so.** `block_in`, `look(region=)`, `dry(region=)` and
the rest take a place through `as_region`, which would have failed on `float(Polygon)`; it
now raises *a group is several places, not one*, naming `for part in g` and `g.bounds`.
`guide()` and `pencil()` say *draw each*, since a pencil line is one record.

**9. What `px_size` was tested against.** A stroke at `pressure="even"` and
`size=s.px_size(40)` is 40 px thick on 1024x768 and on 768x1024. A dab at its default press
is about half its size -- 20 px for `s.px_size(40)` -- and my first test, written against a
dab and expecting 30 to 46, was wrong about the dab, not the unit.

**10. Stale docstrings, fixed on the way.** `polygon()`'s example called `s.polygon(...)` and
`blob()`'s said `s.blob(...)` passes the aspect; neither method exists. `Polygon.closed` said
it is what to hand the pencil to draw the silhouette; it now says to hand over the shape.

**11. `PAINTER.md` was not touched.** Its worked example near the end -- three landmarks
drawn with `s.pencil([a, b, c, a])` -- is a triangle through the default spline, so it draws
the rounded triangle this step is about. The plan leaves a list of points splined on
purpose, and the card is 45 words from its budget; **for step 9 (F)**, which moves text out
of the card anyway: `s.pencil(polygon([a, b, c]))` there, or say what it draws.

**12. On this machine.** `pyproject.toml` sets `addopts = "-q"`, so `pytest -q` is `-qq` and
prints no summary line: run plain `pytest` and read the last line, or the exit code. A Bash
`cd` moves the session's working directory (`NOTES-step2.md`'s gotcha 11, again).

## What step 3 did *not* touch

What any mark lays. No golden, sampler or rebuild moves: a guide is the view's, the two
drawing calls raised on a shape before so no saved log holds one, and every other change is
a helper that returns numbers. The MCP server and the CLI are unchanged.

## File map

| File | What changed |
|---|---|
| `src/easel/look.py` | `_draw_guides`, `_guide_layer`; `_GUIDE_CASING`, `_GUIDE_CASING_WIDTH`, `_GUIDE_CASING_ALPHA` in place of `_GUIDE_ALPHA` |
| `src/easel/session.py` | `pencil` and `guide` take a shape (`_outline_of`); `px`, `px_size`; `circle(px=)` |
| `src/easel/regions.py` | `Group`, `group`, `_point_of`; `scaled(about=)` on `Region` and `Polygon`; `as_region` names a group; four docstrings |
| `src/easel/__init__.py` | `Group`, `group` |
| `scripts/probe_bell_session.py` | `draw_07`; `today` and row 1 drawn with it; the built line checked against its candidate |
| `REFERENCE.md`, `RECIPES.md`, `README.md` | as above |
| `tests/test_requests.py`, `tests/test_reference.py` | the tests above |
| `CALIBRATION.md`, `CHANGELOG.md`, `SUGGESTIONS.md`, `PLAN-0.8.0.md` | the record |
| `NOTES-step3.md` | this file |

## Next

- **The first painter's answers** to 4, 9, 10, D and 5f, filed as
  `paintings/Claude/bell_warden/answers-step2.md` and re-measured. 4b settles the casing
  (decision 1); 4a, 4c and 4d the thumbnail.
- **Step 4**: C, the dearest calls, with H1, H2 and H3 -- none of which waits on the answers.
