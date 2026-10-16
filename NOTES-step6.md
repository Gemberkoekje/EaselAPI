# Step 6 of `PLAN-0.9.0.md`: a frame, a turn in pixels, and a share of the budget

**To understand this, start by reading the plan's sections 4E and 4F, and section 6's P4,
P5 and Q5, then the painter's own words,
[`answers.md`](paintings/Claude/uktarl_krannoc/answers.md) D and E, and The Curator's
[`answers.md`](paintings/Claude/the_curator/answers.md), question 5, then
`CALIBRATION.md`'s *A frame, a turn and a share of the budget, as built*, then
[`tests/test_frame.py`](tests/test_frame.py) and [`tests/test_shares.py`](tests/test_shares.py).**

Branch: `ccr-9c669476-nor0aj`, off `main` at `9b9e0ee` (#107, step 5, merged).

---

## What landed

| | |
|---|---|
| **`src/easel/regions.py`** | `.rotated(degrees, about=None, *, aspect)` on `Region` (which comes back a `Polygon`), `Polygon`, `Difference` (holes turned with it) and `Group` (every part about one point, points with them); `_turned`, the turn made with across measured in the height's units; `_aspect_needed`, the `TypeError` naming `aspect=s.aspect`. `Frame`: `at(u, v)`, `polygon(points)`, `arc(t0, t1, n)`; radii over `1` refused with the `*s.px(rx, ry)` form. `ellipse()`'s `rotate=` docstring says it turns in coordinates |
| **`src/easel/session.py`** | `s.frame(centre, rx, ry=None, tilt=0)`, the aspect from the canvas, `ry` left off round in pixels; `plan(shares=)`, refused on a painting with no budget; `_shares_line`, a standing line in `report()` and a line of `checklist()` |
| **`src/easel/plan.py`** | `Plan.shares`, `Plan.part_of(note)`, `declared_shares()`, `build(shares=)`; saved under the plan's `"shares"`, a malformed entry dropped on load; `shares of the budget: ...` in the plan as printed |
| **`src/easel/cli.py`**, **`src/easel/mcp_server.py`** | `easel plan --share PART SHARE`, the server's `plan(shares=)`; the prelude scaffold's commented `shares=` |
| **`src/easel/__init__.py`** | `Frame` exported, and so in an `easel run` script's scope |
| **`PAINTER.md`** | `shares=` in the plan's sentence and `s.plan(shares=)` where the split is named; `s.frame()` in one clause beside `s.px`; the share paragraph leads with the budget, `subject:` kept as the share of the marks so far. 6,700 words, one more than before, inside 6,700 |
| **`REFERENCE.md`** | the turn and the frame under *Shapes*, `r.rotated`, `g.rotated`; `shares=` in *What the plan changes*, a `shares:` row among the standing lines; `--habit` and `--share` on `easel plan`'s line; `s.frame` in the session's block. 12,111 words, 318 more: nothing cut |
| **`README.md`** | the shapes row carries `rotated()` and `s.frame()`, the plan's row `shares=` |
| **`scripts/probe_uktarl_session.py`** | `--frame-built`, the prelude's three heads through `s.frame()` and the square turned; `--shares-built`, the built line pass by pass against the bench's. The shares bench's `p16` and `p17` keys corrected |
| **`tests/test_frame.py`**, **`tests/test_shares.py`**, **`tests/test_mcp.py`** | the new behaviour; the server's `plan` declaring and clearing shares |
| **`CALIBRATION.md`**, **`SUGGESTIONS.md`**, **`PLAN-0.9.0.md`**, **`LESSONS.md`** | the round's *as built*; the rows for rotation, the budget and The Curator's pixels; the status line, step 6's row and Q5's; *a bench's table is an instrument too* |

## Decisions and gotchas

- **Three were the owner's, asked before building** (this session): a session in pixels
  throughout is **not built** (Q5; Wenna Brask agreed in 0.8.0's round it should not be,
  and no bench has measured it) and stays an open candidate in `SUGGESTIONS.md`;
  **`aspect=` is required** on `.rotated()`, left off it raises a `TypeError` naming
  `aspect=s.aspect`, since a shape does not know its canvas and a default would turn in
  fractions, the skew the painter measured; **a part is the name in the note**, in any
  case, the longer name winning where two do, so a block-in's own note counts.
- **The frame's units are an ellipse's**: `rx` a fraction of the width and `ry` of the
  height, so pixels are `*s.px(24, 34)`. The painter's sketch of the call,
  `s.frame(s.px(512, 344), 24, 34, tilt=-6)`, typed the radii in pixels; a radius over 1
  is refused with the `s.px` form rather than read as 24 canvases.
- **`arc(t0, t1, n)` is the painter's `head_arc()` without the warp**: `n` steps, `n + 1`
  points, degrees, `0` the right and `90` the bottom (clockwise, as `v` runs down), in the
  frame's own units. The painter asked to keep its warps its own; in local units each is
  a list comprehension, and the probe and the tests apply the prelude's three.
- **`ellipse(rotate=)` and `blob(rotate=)` still turn in coordinates**, and so does
  `s.circle(rotate=)` on a wobbled outline. Seven calls in three paintings' preludes use
  it, all on 1024×768; turning them in pixels would move every rebuild. The docstring and
  `REFERENCE.md` say so, and `.rotated(aspect=)` is the turn in pixels.
- **A shape turned off the canvas is clamped to it**, as `shifted()` clamps: points are
  held to `0..1` when a `Polygon` is made. A frame's `at()` is not clamped: a point past
  the picture's edge is still a point.
- **The shares line is of the budget, rounded to a stroke** with Python's `round`, which
  gives the painter's own table: 25% of 450 is 112, 11% is 50, 5% is 22. A signature is in
  no part and not counted; the marks in no part are, at the end, `; 12 in no part`, so a
  part at 0 is told apart from a pass whose notes never named it. Off the log, so a
  counted copy prints it too.
- **A standing line**, as step 5 built them: over a pass it prints when it changed from
  the painting as committed; the checklist and `--check` print it whatever.
- **`subject_share=` stays**, and the `subject:` line is still a share of the marks so far.
  The guide's plan sentence now names `shares=` in its place.
- **The file**: the plan's `"shares"` is a list of `[part, share]` pairs, read with
  `.get`; 0.8.0 opens the plan without it. A line, never a mark, so nothing to refuse.
- **The bench's table was keyed wrong for two scripts**: `p16`'s and `p17`'s calls by
  lines 39 and 71 past their own, so 15 strokes fell to the table. Corrected, the parts
  match the painter's own count but for the 7 strokes of the cards in Uktarl's hand,
  which it counted by pass with the relief. Nothing step 2 printed of the line moved.

## Next

Step 7 (G1, G2 (a), H1 and H2) and step 8 (I2 to I5: the recipe *A thing drawn in its own
frame* uses `s.frame()`) can go in either order. Step 9 counts the reading path, which
this step lengthened in `REFERENCE.md` by 318 words.
