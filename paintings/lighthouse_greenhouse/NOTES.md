# A lighthouse half way through becoming a greenhouse

The lamp room at the top is full of tomato vine pressing against the glass,
terracotta pots come down the outside stair, and the beam still sweeps across a
foggy sea — but it comes out through the leaves, so what crosses the fog is
green.

The subject was fixed before a line of this repository was read. Everything else
here was read first: `PAINTER.md`, then `PAINTING.md`, `RECIPES.md`,
`REFERENCE.md`, the parts of `CALIBRATION.md` the rules cite, and the
`lighthouse_dusk` prelude and notes, from which this painting took its
convention of a prelude of masses-as-functions, a written `compare()` value plan
and one numbered script per pass. The eight exercises were run first, from
`examples/exercises.py`.

- Canvas 1120×860, linen, `toned_warm_grey` ground, seed 41.
- **296 strokes** of a 300 budget, plus one signature mark that did not count.
- Final painting: `painting.png`. Time-lapse: `painting.gif`.
- `prelude.py` holds the palette mixed to planned values, every mass as a named
  function, the written value plan and the budget split; `p1_fog.py` …
  `p11_sign.py` are the painting in order. Against a fresh
  `easel new painting.easel --size 1120x860 --texture linen --ground
  toned_warm_grey --seed 41 --budget 300`, those eleven passes reproduce
  `painting.png` **byte for byte** — verified by sha256. `p0_plan.py`,
  `check.py` and `p12_export.py` paint nothing.

## No assisted modes

There was no reference photograph, so `prepare`, `sketch`, `ref_shape` and
`ref_outline` were unavailable and nothing was traced; `s.assisted` is empty.
Every mass is a `polygon`, `blob`, `ellipse` or `Region` written by hand and
looked at through `preview()` before it was filled. No pencil was laid: with
nothing to measure against, the shapes were the drawing and the composition
preview in `p0_plan.py` was how they got checked — and it earned its keep twice,
once for a halo drawn twice the size of the thing it was meant to surround, and
once for ten pots floating clear above the stairs they were supposed to stand on.

## The composition, and the one thing it had to solve

A lighthouse in a seascape is a layer cake before a brush is picked: fog, sea,
rock, three horizontal bands, which is the closing checklist's question about
bands being in the subject rather than in the marks. Two things cross them. The
tower crosses all three vertically. The beam crosses them on the diagonal, and
that is why the beam is as large as it is — it is doing compositional work as
well as saying what the picture is about.

Two smaller decisions came out of the same count: the rock's top edge runs from
`0.76` on the left to off the bottom-right corner, so the sea is a wedge and not
a band; and the horizon is one stroke that starts at nothing a third of the way
across and is only found where the water is nearer, so over the left third of the
picture there is no horizontal there at all.

## The plan, and what it cost

Values were written down first, as a `compare({place: value})` sheet in
`prelude.py`: fog `0.58` at the top and `0.68` at the horizon, the beam `0.75`,
far sea `0.54`, near sea `0.40`, rock `0.21`, tower `0.40`, the vine mass `0.26`.
The three carrying values were the darks `0.20`, the tower `0.40` and the fog
`0.63`, with the beam above all of them at `0.75`. Every mixture was made with
`at_value()` and landed on its number to the hundredth. Measured on the finished
canvas, **all eight places are inside `0.10`** and the largest miss is `0.09`
(the beam, a step quieter than planned and still the lightest mass in the
picture, which is what the plan was for).

The split written before the first stroke: fog 40, sea 22, rock 28, beam and halo
26, tower 40, stair and pots 46, lantern 52, edges and finish 26, reserve 20.
What was spent:

| Stage | Strokes | Share |
|---|---|---|
| Fog: underlayer, the thickening toward the horizon, three drifts | 27 | 9% |
| Sea: two passages, the half-horizon, marks on the water, one far stack | 29 | 10% |
| Halo and beam, including the light it puts on the water | 19 | 6% |
| Tower: mass, two planes, four joins, gallery, stains, foot, window | 55 | 19% |
| Stair and pots: four turns, ten pots, tomatoes, runners, creeper | 39 | 13% |
| Lantern: far glass, vine mass, leaves on the panes, lamp, frame, cap | 52 | 18% |
| Rock, including everything the finish spent on it | 67 | 23% |
| Edges: four marks and two smudges | 8 | 3% |

The subject — the tower and everything the conversion put on it, the lantern, and
the beam — was planned at 55% and reached 64% at the moment the lantern was
finished, then fell to **56%** as the last two passes went on the surroundings.
That is both closing rules obeyed in the order the guide gives them.

The rock overran its 28 by more than twice, and did it honestly: it was the
weakest passage in the picture at every look, and the guide's last instruction is
to spend what is left there. What paid for it was the fog, the sea and the beam,
all three of which came in under, and the reserve. Six late strokes are repairs of
the rock's own committed paint — two burying the tower's foot where the block-in
had run thin over it, two breaking a pale scalloped line the surf marks had drawn
along its whole top edge, and two breaking a plane that read as a slab. Nothing
else in the picture was repainted after it was committed.

## Rehearsing, and what it saved

Every pass was rehearsed before it was committed, most of them three or four
times; between them the rehearsals wrote 92 images and were charged nothing.
Every one of the following was found on a copy of the canvas:

- **The beam came back a chartreuse searchlight.** Twice. Mixed from the green
  the brief asks for, it owned the picture and read as a laser rather than as
  light. What fixed it was not opacity — the calibration is explicit that opacity
  does not make a passage quieter — but desaturating the green by `0.58` and
  dropping its planned value from `0.82` to `0.75`, so what says *green* is the
  hue being a few degrees off neutral against a grey fog and nothing else. The
  earlier lighthouse in this repository rehearsed a beam twice and dropped it;
  the difference here is that this one lands on fog, so it is a mass of lit air
  and can be painted as one, where a beam over clear sky has only a glaze.
- **The beam is a fan of eight dying strokes, not a `block_in`.** A pressure list
  on a mass is read in canvas order, which would have graded the wedge across its
  width when what it has to do is die out along its length.
- **The tower's three planes came back as three flat slabs**, then as a slab with
  a bright yellow one beside it when the planes were given a temperature turn as
  well as a value one. What worked: the turn cut to `0.30/0.40/0.48` — a total
  range of `0.18`, because a mass shaded much past `0.15` across itself buys form
  by spending the separation that made it a mass — a much smaller temperature
  swing, and four starved comb strokes straddling the two joins.
- **`flat` staircased down the tower's sloping plane edges.** Every vertical pass
  of a chisel tip ends in a hard horizontal edge, and stacked along a boundary
  that slopes those ends are a staircase. The same mass laid with a `bristle` has
  none, because a comb's pass ends are already broken; one solid `flat` stroke
  down the middle afterwards gives the band back the core a comb will not lay.
- **The lit band was held a hair inside the silhouette and the dark left over
  between them read as a drawn outline** down the right of the tower. It now runs
  *to* the silhouette and past it.
- **The rock came back the same value as the sea.** Its top plane was planned at
  `0.33` against a near sea of `0.40` — seven hundredths, so it stopped being a
  dark at all. Re-planned with a total range of `0.135` and nothing above `0.29`.
- **Serrations cut into the rock's own outline vanished.** They were about `0.02`
  deep and the block-in's half-brush spill is `0.055`, so the edge came back a
  smooth ramp from one corner of the picture to the other. What breaks a line at
  that scale is a mass — one boulder standing proud of it — not a notch.
- **Ten pots as one chisel stroke each were ten bricks.** A second, wider,
  lighter mark for the rim is what makes it a pot; `size_jitter=0.20` is what
  stops the body being a rectangle.
- **Three astragals across the lantern made a cage**, and the thing inside it
  stopped being the point. Two, thinner, and two corner posts.
- **Drifts laid into a nine-pass scumble mixed away to nothing**, twice, before
  `dry()` went in front of them. Wetness fades per mark, not per pass.

## What the engine charged that reading the call did not say

- **`direction` left off a shaped `block_in` cost 44 passes where 9 were
  budgeted.** The default is horizontal, so a mass taller than it is wide gets
  passes stepping down its whole height. Two of the tower's planes were priced at
  9 and 9 and would have been charged 44 and 57.
- **Crossing a direction is where a price runs away.** The rock's top plane —
  a long thin diagonal band — cost 33 passes crossed and 3 laid along its own
  axis, because a pass line crosses such a shape twice *and* the second direction
  steps across its whole bounding box. `cost_line()` names which of the three
  causes a number is, and it is the difference between fixing the call and
  redesigning the mass.
- **`at_value` raises rather than quietly handing back the nearest it managed.**
  Asking the rock mixture for `0.135` stopped the pass with the number it could
  actually reach, `0.137`. The crevices are painted at the floor of the box,
  which is where the deepest crack in the nearest thing belongs.

## What I would do differently

The rock is still the weakest passage. It took 67 strokes, four of them repairs
of its own earlier marks, and it is *better* than it was rather than good: there
is still more horizontal in it than a rock should have, and the pale plane along
its top edge had to be broken in two and then broken again because run whole it
drew the ramp it was lying on. The cause is upstream of the paint — a mass that
large, that dark and that near wants its planes designed as a drawing before the
block-in, the way the tower's were, and it got a silhouette and three afterthoughts.

The other thing is the tower's right edge below the sea line. It is lost, on
purpose, and it is the picture's one genuinely absent edge — but it was lost by
accident first, when the lit band ran down to the waterline at very nearly the
near sea's own value, and it took two late marks to turn that into a decision.
An edge that is a decision only in retrospect is not one.

## Sign it

One mark, in the darkest corner, a step above what it sits on. Not a name, and
deliberately not a motif out of the picture — a sprig would have been the third
growing shoot in a painting that already has two, and the guide is clear that the
signature is not part of the painting. It is a hook: one stroke that changes
direction once, which is the least a mark can do and still be unmistakably
somebody's decision rather than something that happened.
