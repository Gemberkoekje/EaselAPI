# Step 5 of `PLAN-0.7.0.md`: an edge that is not a step, and an outline nobody ruled

**To understand this, start by reading the plan's workstream A, then `Session._clip_cover`
and `_held_feather` (with `_EDGE_FEATHER` above it) in `src/easel/session.py`,
`Polygon._edge_depth` and `roughen()` in `src/easel/regions.py`, and
`Canvas.broken_edge` in `src/easel/canvas.py` -- and read `NOTES-step4.md` first if you
have not, and `NOTES-step2.md`, whose bench this step builds.**

Branch: `feather-and-roughen`, off `main` at `c0fceae` (step 4, #78).

---

## What this step was for

The painter's finding 1: *hard edges are all-or-nothing* -- `0.30` in one pixel at the
tower, because a clip was cut as one pixel of four values and then a step -- *the least
paint-like thing in the engine, and I relied on it*. Decided after step 2 (questions 10
and 11): **A2 at `0.002`, on every hard edge and every clip, inward**, which the painter
chose blind, first of four; and for rock, **`roughen()`** with the default edge on top.
One bench was left for the build: whether the feather is a share of the long side or a
count of pixels.

## What landed

| | |
|---|---|
| **`feather=`** | on `stroke`, `block_in`, `sweep`, `scumble` and `cover`, and through `**kw` on `dab`, `glaze` and `smudge`: how far inside a held outline the edge breaks, a fraction of the long side like `size` |
| **The default** | `0.002` wherever a call holds its paint -- `clip=`, `edge="hard"`, `cover()` -- and nothing where it does not (`_EDGE_FEATHER`, `_held_feather`) |
| **The edge** | `Polygon._edge_depth` measures each pixel's distance to the outline itself; `Canvas.broken_edge` reads the canvas's own tooth against a need falling with depth, the stamp's own gate and band (`_GATE_BAND`, hoisted from `stamp`, the same `0.18`) |
| **Nothing past the line** | a pixel whose centre is on or past the drawn line takes nothing, even on a peak |
| **The frame is not an edge** | a side lying on the canvas frame never breaks |
| **A thin shape keeps its body** | on a shape narrower than four feathers the edge breaks over a quarter of its width |
| **The log** | `params["feather"]` beside `clip`, only where the edge was broken; a record without it replays cut on the line, so every clip saved before 0.7.0 replays as it was laid |
| **The memo** | the feather is in `_clip_cover`'s key |
| **The guards** | a feather on a call that holds nothing is refused, except `0`; past `0.05` it is named as a probable pixel count |
| **`roughen()`** | in `regions.py`, exported, on the MCP server as a place builder (`{"roughen": ..., "calm": ...}`), and in `REFERENCE.md`'s Shapes block |
| **The notices** | `spill` (both), `round-fringe` and `clean-small`'s burial branch name the broken edge where they name `edge="hard"` |
| **The golden** | a new case, `edges`: a mass held to its own outline at the default, a clipped mark, a roughened outline laid hard, a burial, a band cut on the line beside one broken, and a mass run off the frame |
| **The probe** | `probe_handover_session.py`: A2 is the engine's own now; `rebuild(cut=)`; `--edges` gains the unit, the seam and the painting as this engine lays it; `--corpus-edges` is new |
| **Tests** | `test_requests.py` *0.7.0 A* (18); the MCP place and plan cases (4); `test_reference.py` holds `roughen` to the page |

## Decisions and gotchas

**1. The unit is a share of the long side -- and the first reading of the bench was
wrong.** The bench step 2 left: at 1440x960 the painter found A2 at `0.002` -- 2.9 px
there -- *a little chewed*, and could not tell whether a pixel count would read better.
The tooth the edge breaks against is a weave that scales with the canvas (a thread is
1/130 of the long side) and a grain that does not (about 3 px at any size). Measured with
the painter's own instrument on the rock's steep side (`ground_edge_numbers`). It was
first run on the step-2 copy of A2 and read as *the share holds 1024's edge in the look
and a pixel count holds it nowhere*; on the edge as built the numbers are not those, and
that sentence had gone into the default's comment, `REFERENCE.md` and this file before
the probe corrected it -- measure the thing that was built, not its bench. **Built, the share bites at the export's own pixels exactly as
1024's does** -- `0.94` against `0.94`, wandering `0.44` against `0.40` -- which is where
the painter made its reservation (1:1), and **two pixels are no closer** (`1.06`, `0.38`);
in a look at the default size both are crisper than 1024's (`0.67` and `0.75`, wander
`0.32` and `0.27`, against `0.94` and `0.40`). By eye the two at 1440 are nearly the
same edge. So the unit is `size`'s, and the reservation was the bench's copy: it let the
weave's highest peaks through on the line itself, and its edge at 1440 measured `1.32`
and `0.49`. The bite is one worst row and noisy; the wander is the number to trust.

**2. Two differences from the bench copy, both on purpose.** The step-2 probe's A2 let
the highest peaks through on the drawn line itself and broke a side lying on the canvas
frame. Built, nothing lands on or past the line, and a side on the frame is not an edge:
a shape clamps a side drawn past the frame onto it, and broken there the frame would get
a strip of ground down it -- the reason `inset()` keeps the frame. Neither shows on the
sheets the painter read.

**3. A thin shape keeps its body -- found while building.** Inward, the edge reaches full
paint at the feather's depth, and a strip narrower than two feathers has no inside that
deep: ramped over the whole feather, it is broken from both sides into its middle. A
clip two pixels wide kept 37% of its paint at the default on a 1024 canvas, three 60%,
four 70%. So the depth at which the edge reaches full paint is the feather or a quarter
of the shape's width there (half the deepest inside pixel within twice the feather),
whichever is less: two pixels keep 100%, four 99%, six 91%, and a shape wider than four
feathers is exactly what it was -- the tower's sides reach full paint at the feather's
own depth everywhere. The tip of a sharp corner keeps its point the same way. (A strip
three pixels wide on this canvas reads 68%: its top line runs through a row of pixel
centres, and that row, on the line, takes nothing -- a third of the strip.)

**4. The brush carries a broken rim's colour in.** Deeper than the feather the mass is
not identical to the cut one: up to 6 levels of 255 move, a brush width in, because the
brush picks wet paint up off the canvas under each dab (`WET_PICKUP` in `stroke.py`) and
a rim with ground in it is different paint to pick up. Physical, and small against the
hundred-odd levels inside the feather; the tests bound it rather than demand equality.

**5. A feather needs an edge to break.** Given to a call that holds nothing -- a ragged
or clean mass with no `clip=`, a mark with none -- it would change nothing and say
nothing, so it is refused (`_held_feather`); `0` asks for what such a call does anyway
and is taken, so a helper that passes it on every mark is not refused on the marks it
does not clip. Past `0.05` it is almost certainly a pixel count typed into a fraction,
and the refusal says so. `cover()` asks before its dry is laid, because the dry is a
record too.

**6. A saved mark replays at the feather it was laid with, so no `REBUILDS` row.** The
feather rides beside the clip in the record, and only where the edge was broken; a
record without it replays cut on the line, which is every clip saved before 0.7.0. So
the default moved for new marks and never reaches a saved log -- a 0.6.0 file rebuilds
under this engine exactly as under its own, and `older-engine` has nothing to say about
this step. A 0.6.0 build opening a 0.7.0 file ignores the key (it reads the brush fields
it knows) and rebuilds the edge cut: an older engine rebuilding a newer file is not
something the stamp promises.

**7. What does move is a script re-run.** Every committed script that holds an edge and
leaves `feather=` off lays the broken edge now: the lighthouse handover's 33 calls
(`prelude.py`, `p02`-`p05`, `p07`-`p09`, `p11`), the hands' `pass06_cupplanes.py`, the
pier's `pass2_masses.py`, GPT's `paint.py` (thirteen clips, and every mass through a helper that lays it hard), Grok's
`prelude.py` and `pass4_boats.py`, Kimi's `pass3_fields.py` and `pass4_lighthouse.py`,
DeepSeek's `pass4_boat.py`, GLM's `pass2.py` and BigPickle's `sunset_paint.py`. Each
painting's *Reproducible* row in `PAINTINGS.md` is already a claim about the engine it
was painted under, and says so; the page's rule is that a rebuild lays with the engine
installed. No committed pass calls `cover()`. The guide's own blocks hold their edges
too -- `PAINTER.md`'s exercise 5 and most of `RECIPES.md`'s passages -- and a whole-canvas
region laid hard, which is most of them, has every side on the frame and does not move.

**8. Two masses held to one line leave the ground between them -- found while building,
and not a check.** A mass laid over paint breaks over that paint, which is the feather's
point; two laid up to one line on bare ground, each held to it, both break back from it,
and the ground shows along the seam as a broken line: 14.6% of the 8 px band on it, on a
warm ground and a grey one alike, against 0.0% cut and 0.0% with the first mass laid past
the line. That is an outline, and it is the guide's own rule -- *paint masses, never up
to a line* -- made visible where a cut edge used to hide it. **Measured before deciding**,
with the rule for reading it set down first: a check only if real paintings do it. Over
the ten corpus paintings whose scripts hold an edge, rebuilt cut and broken, no
`ground:` rises and the longest run of ground the feather uncovers is 12 px -- specks
where a hard rim met bare ground, none of it a line. So it is a number in
`CALIBRATION.md` and a clause in the notes and the changelog. The one place it happened
was a `RECIPES.md` passage -- two masses meeting at `x=0.22`, each `edge="hard"` -- which
now lays its first mass past the line; its demo still fails exactly the way it says.

**9. `roughen()`, from the painter's fifteen lines.** Three changes to its walk, each
because the helper is general where the painter's was for one headland. `amp` is the
walk's own spread in the long side's unit -- the painter's scaled a walk whose spread was
1.44, and measured in the canvas's height. A closed outline is walked twice round and the
second lap kept, so it ends where it starts and has no seam. And nothing on the frame
moves, nor either end of an open run, the wander dying away over three steps toward each:
an outline that ran off the canvas would otherwise pull back from the frame, and a
stretch would no longer meet the rest. `calm=` takes a place, a point or a list of them --
still on it, full again five `amp` away -- or the painter's own form, a function of the
point, which it wrote as `calm(x)` and is `calm(x, y)` here. Over the MCP server it is a
place object, with `calm` as places too, and its echo writes `roughen(polygon([...]))`,
because a run of points is an outline on the wire and an open run in Python.

**10. The probe's "today" patches too.** `feather()` in `probe_handover_session.py` let
"today" through untouched, and since this step the engine's own default breaks every
hold: a bench of *today* would have measured the new default under the old name. Every
candidate patches `_clip_cover` now, "today" to a cut edge, and `rebuild(cut=True)` is
the painting the painter had, which every claim and bench starts from.

## The numbers

On this machine, the painter's own measure and the probe's:

| | |
|---|---|
| **The unit at 1440** | the share bites `0.94` px at the export's own pixels against 1024's `0.94`, wandering `0.44` against `0.40`; two pixels `1.06` and `0.38`; in a look both crisper (`0.67` and `0.75` against `0.94`) |
| **A thin strip** | 2 px: 37% of it painted ramped over the whole feather, 100% built; 4 px: 70% and 99%; 6 px: 79% and 91% |
| **The seam** | 14.6% of the band on it bare; 0.0% cut; 0.0% with the first mass past the line |
| **The painting's own scripts** | `edges:` moves two points at most on any pass and ends at `54%` either way; the tower's step `0.288` against `0.290`; `ground:` `0.00%` both |
| **What it costs** | nothing a painting can measure: the thirteen scripts rebuild in 41.7 and 41.9 s broken against 42.2 and 41.2 s cut, each in a fresh process on a quiet machine. A held outline's mask is built once and remembered for a mass's passes, as it was |
| **The corpus** | 0.00% to 1.92% of each canvas moves, GPT's the most -- and at its edges: all but 19 of its 19,748 pixels more than eight levels apart lie within 3 px of a hold's outline; the longest run of ground uncovered anywhere 12 px |
| **Inside a mass** | past the feather's depth up to 6 levels of 255 move, a brush width in, from the brush picking a broken rim's paint up |

## What step 5 did *not* touch

What a saved mark lays: every record carries the feather it was laid with, and none from
before this step carries one. The existing goldens -- none of them holds an edge. The
sampler and the shape sampler, which hold none either. The `edges:` and `ground:` lines,
which the broken edge is invisible to on purpose.

## File map

| File | What changed |
|---|---|
| `src/easel/session.py` | `feather=` on `stroke`, `block_in`, `sweep`, `cover`, `scumble` and into `_clean_contour` and `_scumble_inward`; `_EDGE_FEATHER`, `_FEATHER_MAX`, `_held_feather`; `_clip_cover` breaks the edge and keys on the feather; the record and the replay carry it; the preview's filter; four notices; docstrings |
| `src/easel/regions.py` | `Polygon._edge_depth` (the distance to the outline, the frame left out, the width round each pixel); `roughen()`, `_calm_of`, `_grow_max` |
| `src/easel/canvas.py` | `Canvas.broken_edge`; `_GATE_BAND`, the stamp's band as a constant |
| `src/easel/__init__.py` | `roughen` exported |
| `src/easel/mcp_server.py` | `roughen` as a place builder, `_calm`, `_py_calm`; the plan help names the feather |
| `scripts/probe_handover_session.py` | A2 the engine's own; `feather()` patches "today"; `rebuild(cut=)`; the unit, seam and built benches; `--corpus-edges` |
| `tests/test_requests.py` | *0.7.0 A* (18 tests); the B8 bite tests held at `feather=0` |
| `tests/test_mcp.py`, `test_reference.py`, `golden_cases.py`, `golden/` | the `roughen` place and plan cases; `roughen` held to the page; the `edges` golden case, its image and hash |
| `REFERENCE.md` | the units row, the hold paragraph, the `feather` argument, `roughen` in Shapes |
| `PAINTING.md` | one sentence under *Masses that are not rectangles* |
| `RECIPES.md` | the passage where two masses met on one line lays the first past it |
| `CALIBRATION.md` | *A held edge, broken (0.7.0: the default moved)*; the bites and the burial say what the feather does to their numbers; the round's *Built, in step 5*; the index row |
| `README.md` | `roughen()` in the Shapes row |
| `CHANGELOG.md` | `[Unreleased]`: this step's section |
| `SUGGESTIONS.md` | finding 1 filled in; the counts |
| `PLAN-0.7.0.md` | status; 4A marked built, with what the build changed |
| `NOTES-step5.md` | this file |

## Next

Step 6, workstream B: the dry-brush gate, B1+B2 tuned to lay today's paint at each load.
It is a fix that changes what a rebuild lays, so it adds its row to `notices.REBUILDS`
with a counting `moves` predicate and writes **One fix changes what a rebuild lays** in
`[Unreleased]`, or `test_notices.py` fails (`NOTES-step4.md`, 6). Read the plan's 4B and
`NOTES-step2.md`'s gotchas 1, 9 and 10 first -- the probe's `_gated_stamp` was copied at
`v0.6.0`, and `Canvas.stamp` has changed since only by naming its band `_GATE_BAND`.
