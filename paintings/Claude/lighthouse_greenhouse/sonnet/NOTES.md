# A lighthouse mid-conversion into a greenhouse

A painting made from `PAINTER.md` and its referenced files alone, with no reference
photograph — the subject was given whole: a lighthouse mid-conversion into a
greenhouse, the lamp room at the top filled with tomato vines pressing against the
glass, terracotta pots spiralling down the exterior stairs, and the beam still
sweeping across a foggy sea, tinted green through the leaves.

- Canvas 1024×768, linen, `cool_grey` ground, seed 74, budget 340.
- **274 strokes** of 340, plus one signature mark that did not count.
- Final painting: `painting.png`. Time-lapse: `painting.gif`.
- `prelude.py` holds the palette mixed to planned values, every mass as a named
  shape function, the written value plan, and the budget split; `p1_fog.py` …
  `p8_sign.py` are the painting in order, `p9_export.py` writes the outputs. `p0_plan.py`
  and `check.py` paint nothing and are not part of that sequence. Against a fresh
  `easel new painting.easel --size 1024x768 --texture linen --ground cool_grey --seed 74
  --budget 340`, those nine passes reproduce `painting.png` and `painting.gif` **byte
  for byte** — verified by sha256.

## No assisted modes, and no pencil

There was no reference, so `prepare`, `sketch`, `ref_shape` and `ref_outline` were
never in play. There was also no `pencil()` underdrawing: every mass here is a
`polygon`, `blob`, or hand-placed point, and the composition was checked with
`s.preview()` and `s.cost()` against the grid instead of graphite — cheaper to
iterate on, since a rejected polygon is a one-line edit and a rejected pencil line
is an `erase()`. `p0_plan.py` is that check: every mass previewed and costed
against `look(grid=True)` before anything was painted.

## The ground

`cool_grey` reads close to the picture's own middle value, which is exactly what a
foggy day wants: a mid-tone with almost no chroma of its own, so nothing has to be
painted just to establish "this is overcast."

## The plan, and what it cost

Values written down first, as a `compare({place: value})` sheet in `prelude.py`:
upper fog `0.57`, the diffused glow low in the fog `0.66`, near sea `0.47`, rock
`0.20`, tower shadow `0.45`, tower lit `0.72`. Three carrying values: rock `0.19`,
fog `0.57`, glow `0.67`. Checked against the finished canvas, three of six planned
cells came back more than `0.10` out — and all three are the plan's fault, not the
picture's: two value-plan rectangles were written before the rock's final silhouette
and the tower's lit face were fixed in place, and ended up straddling rock-and-fog or
fog-and-tower-lit half and half, which `compare()` duly reported as a large, confident
miss. The picture itself reads the three values cleanly in `look(values=True)`;
the lesson (`PAINTING.md`, *Painting without a reference*) is to re-read a plan
cell's outline whenever the mass under it moves, not just trust the number.

The split written before the first stroke: fog and sea 45, rock 30, beam 20, tower
45, stairs and pots 55, lamp room and vines 60, edges and finish 35, reserve 50 (340
total). What was spent:

| Stage | Strokes | Share |
|---|---|---|
| Fog: underlayer, two long passages meeting at the glow, five quiet ripples | 48 | 18% |
| Rock: mass, three planes, three crevices, two dry-brush touches | 60 | 22% |
| Beam: five straight trapezoid segments, two edge-smudges | 30 | 11% |
| Tower: mass, lit face, terminator, weathering, two boulders | 46 | 17% |
| Stairs and pots: five flights, four landings, nine pots at three marks each | 44 | 16% |
| Lamp room: halo, gallery, glass-as-vines, roof, mullions, escaping and climbing tendrils | 38 | 14% |
| Finish: lost edge, rock texture, foreground mist, three highlights | 8 | 3% |

The subject — stairs, pots, tower and lamp room together — is 128 of 274 strokes
(47%); the beam, which the brief names as part of the same conversion, brings it to
158 (58%). 66 of 340 stayed unspent; see *What still bothers me*.

Rock overran its plan (60 against 30) because the "mass built of planes" recipe —
base, three tiling planes, crevices, dry brush — is not a cheap recipe, and a small
supporting mass still needs all of it once its colours are wrong the first two times
(below). The beam overran too (30 against 20), entirely on the fourth attempt at its
technique. Stairs and the lamp room both came in under plan, because a switchback
staircase turned out to be strokes, not masses — see next.

## Rehearsing, and what it saved

Twenty-five separate rehearsal runs, none charged; four of them were dropped
entirely and never painted. Everything below was found on a copy of the canvas:

- **The switchback stair, drawn as one bent `ribbon` through six landing points,
  costed at 141 strokes — 41% of the whole budget** — before a single stroke was
  laid. `PAINTING.md`'s own warning is exact: a bend prices on the *box* it sweeps,
  cut into pieces by the outline, not on the ribbon's own width. Cut into five
  straight flights, each a `stroke()` rather than a mass (`PAINTING.md`, "a mass
  much longer than it is wide is a stroke"), the same staircase cost five.
- **`block_in(tower(), ..., edge="clean")` on the tower's narrow taper drew a tall
  pointed arch above the flat top that was never in the polygon.** The tower's top
  is a fifth the width of its base; whatever `edge="clean"`'s contour sweep does at
  a hairpin turn that sharp, on this build it overshot upward by several percent of
  the tower's own height. Dropping `edge="clean"` for the default ragged edge (and a
  bigger brush, for fewer visible passes) removed it outright. Not tried again on
  the lantern or roof, which are similarly narrow.
- **The beam took four rehearsed attempts.** `scumble(beam_shape, ..., direction=
  "vertical")`, left to size itself (`3 × extent / n`), sized off the wedge's wide
  end and bloomed out the narrow source instead of tapering it. Thirteen vertical
  cross-section strokes on `round_soft` fixed the taper but came back a chain of
  separate soft blobs — round_soft airbrushes above `size≈0.05` and the gaps between
  centres were real. One long `round_soft` stroke down the centreline, pressure
  tapering its width from thin to the far end's full span, came back a sun: the wide
  end's paint is spread over so much more area than the narrow end's that it read as
  nearly gone, and almost everything visible sat close to the source. What worked:
  the wedge cut into five straight trapezoids, each `block_in` at its *own*
  brush size fitted to its local width, ragged edges left to overlap into their
  neighbours, then one smudge along each of the wedge's two long edges to lose the
  staircase the five flat segments drew.
- **A saturated mixture reads far more vivid in a large flat plane than its own
  `value_of()` suggests, against neighbours this desaturated.** `rock_warm` and the
  beam's own colour were each mixed once, checked only by their target value, and
  painted at that value straight into a picture that is otherwise almost entirely
  cool and grey — and both came back closer to traffic-cone orange and highlighter
  yellow than to rock or lamplight. Printing `hex()` beside the value (`PAINTING.md`
  says to, for exactly this reason) and desaturating hard — `0.5–0.65`, not the
  `0.15–0.35` that was tried first — is what actually fixed it; a colour that looks
  restrained in a two-inch swatch test is not the colour it will read as once it
  covers a tenth of the canvas next to nothing else warm.
- **A short `flat` stroke is a rectangle, and a pot painted with one is a barrel.**
  The first pots used `flat` with a `pressure` list meant to taper wide-to-narrow —
  but pressure only changes paint on an oriented tip, never width (`PAINTING.md`,
  *Pressure*), so every pot came back a chisel-ended box. `round_hard`, where
  pressure genuinely narrows the mark, gave the taper on the first retry.
- **`bristle` below about `size 0.02` is a gapped comb, not a line.** The pots'
  trailing plants and the tendrils climbing the tower were first laid in `bristle`
  at the vine's own thin scale and were nearly invisible — the comb's gaps at that
  diameter are most of the mark. `round_hard`, which holds a continuous line at any
  size, replaced it everywhere on the picture thinner than a stair-rail.
- **Two rehearsals were dropped outright.** A dark arc at each pot's rim, meant to
  separate "terracotta pot" from "round fruit," was tried twice — a straight
  diagonal slash and then a shallow curve — and both read as a bite or a frown
  rather than a rim. Neither was painted; the pots stayed as they were rather than
  spending strokes on a fix that made the crop look worse, not better.

## What went right

- Back to front throughout: fog, rock, beam, tower, stairs and pots, lamp room and
  its tendrils. The beam is behind the tower for exactly the reason the reference
  painting's halo is behind its tower — light in the air belongs to the air — and
  every edge where the tower or a boulder meets what is behind it is a real edge,
  never a line cut carefully around something already there.
- The fog and the sea share one field with no horizon at all — two long scumbles
  meeting at the same colour where they overlap, rather than a ruled line anywhere.
  That is the picture's one deliberately, fully lost edge, and it is also simply
  what fog is.
- The vine motif ties two ends of the picture together: the same tendril shape
  spills past the lantern's frame at the top and climbs the tower from the stairs
  below, so the pots and the lamp room read as one conversion in progress rather
  than two unrelated details.
- Values hold in greyscale — rock dark, fog and tower-shadow mid, the tower's lit
  face and the beam the two lightest things in the picture, both where the plan put
  them.

## What still bothers me

- The pots, cropped into, read closer to small fruit than to terracotta with a
  trailing plant — round, with no rim. Both attempts at a fix are in the rehearsal
  log above and neither survived contact with a second look.
- The beam's lower edge, after one smudge per long boundary, still shows a little
  of the five straight segments it was built from if you look for it, though it
  reads as a soft wedge at picture scale.
- 66 of 340 strokes unspent, on purpose: every correction left to name by the end
  was a fix to a passage that already reads, in a picture that is not short of
  incident anywhere. If that judgement is wrong, the pots are where the strokes
  should go.

## The signature

One mark, lower right, in the mist over the water: a small curl that thins to
nothing at both ends, given the faintest breath of the same green the beam picked
up from the leaves. It is the shape this session kept returning to for anything
growing — the tendrils, the trailing plant on every pot — so it is what stands in
for a name here too. It is not a title and it repairs nothing.
