# Step 10 of `PLAN-0.9.0.md`: a shape cut at its notch, priced as its two parts (G2 (b))

**To understand this, start by reading the plan's section 6, *Asked back after step 7*,
and the painter's own words,
[`answers-step7.md`](paintings/Claude/uktarl_krannoc/answers-step7.md); then
`Polygon.split()` and `_notch_cut` in `src/easel/regions.py`, `_check_parts` in
`src/easel/session.py`, and `CALIBRATION.md`'s *A shape cut at its notch*.**

Branch: `step-10-parts-price`, stacked on `curator-questions-step2` (#114, the answers'
filing) at `5547d01`.

---

## What landed

| | |
|---|---|
| **`src/easel/regions.py`** | `Polygon.split()`: the shape cut in two at its deepest notch, two parts that tile it, named `"<name>, part 1"` and `"part 2"`; `ValueError` for a shape with no notch a tenth of its width deep, and for a `difference()`. `_notch_cut` (the cut, off the outline alone), `_narrowest` (a shape's least width and the direction along it), and their helpers |
| **`src/easel/session.py`** | `_check_parts`, `parts-cheaper`, at `block_in`'s call and in the price walk, so `cost()`, `rehearse()` and `paint()` say it too; `_cheapest_way`, a part at its axis or its narrowest, whichever is cheaper; `_PARTS_RATIO = 2.0`, `_PARTS_SAVED = 5`. `_pass_pieces`'s docstring no longer says the notice is with the painter |
| **`src/easel/notices.py`** | the code, a fact, under *A shape cut at its notch* |
| **`scripts/check_guide_blocks.py`** | a recommended block may name the notice it shows on a comment, `# says <code>`, and is held to exactly those codes; every other block stays notice-clean |
| **`PAINTING.md`** | the ribbon round a bend: its two blocks say `parts-cheaper`, and the paragraph says the third lever, *or cut it*, with the notice's numbers |
| **`REFERENCE.md`** | `a, b = shape.split()` among the shape methods; the notice's row |
| **`tests/test_parts.py`** | the cut on the collar, a long V, the bend; no cut on a convex, quadrilateral or roughened shape, or a difference; the collar's notice word for word; the parts laid at the angles quoted cost what it said; the bend through `cost()`; a clean edge's parts inset; the recipes' grip, shade and figure silent; a direction is not the cut; a sequence and a small mass silent; nothing drawn from the stream |
| **`scripts/probe_uktarl_session.py`** | `--parts-built`: the sheet's shapes through the built check, and the corpus replayed, counting the notice in committed passes |
| **`README.md`**, **`llms.txt`** | thirty-four notices |
| **`CALIBRATION.md`**, **`SUGGESTIONS.md`**, **`PLAN-0.9.0.md`** | the passage; the concave-shapes row built; the status line and step 10's row |

## Decisions and gotchas

- **Twice, not the painter's 2.5×.** The engine cuts the collar where the painter did,
  (0.500, 0.495) to (0.500, 0.518), but its halves keep the V's middle, which the
  painter's prelude flaps left out: 5 + 4 against the flaps' 3 + 4, so 22 against 9 is
  2.44×. At 2.5× the painter's own V would be silent. Its answer said *2× would serve as
  well; one number to remember serves better*. The guide's recipes are at 1.29× and under,
  the corpus at 1.67× and under, so twice separates them as 2.5× did on its numbers. **A
  reading for the painter to confirm**, since the number is its.
- **The cut is the narrowest parts, not the shortest line.** The first prototype cut along
  the shortest line from the notch, and on a V whose base lies far below the notch that
  runs across one arm (17 + 9 against 9 + 9). Choosing among cuts by their parts' price
  works too, but needs the brush, and then `split()` would need it to hand back the parts
  the notice priced. Narrowest parts needs only the outline, and on every shape benched it
  speaks where the price would.
- **Each part at its axis or its narrowest.** The principal axis, weighted by edge length,
  leans toward a flap's short ends; along its narrowest a convex part is as cheap as it
  gets. The notice quotes the angle it priced, so a painter laying each part at that angle
  pays what it said (a test holds the collar's halves to 5 and 4).
- **Against the cheaper of the direction laid and the axis.** The painter's words were *the
  mass's price*; measured against the direction laid, a convex facet laid the dear way
  would bring two notices for one fault. So it speaks for the cut, and the direction is
  `direction-given`'s and `direction-default`'s. When the direction laid is dearer than the
  axis, the notice says both.
- **Searched only where it can speak**: the shape cut by its own outline at the direction
  laid, and dear enough to save five strokes (7 or more), with one direction. That is 26
  of the corpus's 663 distinct masses, at 12 ms each.
- **`PAINTING.md`'s bend now trips a notice on purpose**, as its painter wanted (*the
  example would then show a notice it means to show*). The guide check's rule that a
  recommended block is notice-clean gained the one exception a block names itself.
- **The quoted angles run from -90 to 90**, as the engine's axes do: the painter's example
  said *58° and 116°*, the notice says *-57 and 59*.
- **A heredoc holding Python with quotes broke Bash again** (*unexpected EOF*): scratch
  scripts went through the file tool.

## Not done here

`cost_line()`'s reason for a concave mass still names its own lever, *lay the straight
stretches as strokes, or use a wider brush*, and not the cut; the two could say one thing.
The notice cuts once: a shape of four parts is split again by the painter, part by part,
and the notice speaks on a part only if that part is dear enough on its own. The parts as
shapes are handed back by `split()`, not by a call that takes the notice's own numbers.

## Next

Step 11 (K, N, M1: `s.plan(cut=)`, the alpha softened to 0.85 px, `export(size=)`, the
lines inside a cut) or step 12 (O3, `easel run` with a self-built session, `p.grey()`, the
deposit table), in either order; then the cut, step 13.
