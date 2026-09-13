# A lighthouse half-way to becoming a greenhouse

A painting made from `PAINTER.md`, with no reference photograph. The subject was given
before anything in the repository was read: a lighthouse mid-conversion into a
greenhouse. The lamp room at the top is full of tomato vines pressing against the
glass; terracotta pots spiral down the outside stair; and the beam still sweeps across
a foggy sea, tinted green now because it comes through the leaves.

- Canvas 1024×768, linen, `toned_warm_grey` ground, seed 47.
- **284 strokes** of a 300 budget, plus one signature mark that did not count.
- Final painting: `painting.png`. Time-lapse: `painting.gif`.
- `prelude.py` holds the palette mixed to planned values, every mass as a shape or a
  function, the helix of the stair, the pot recipe, the written value plan and the
  budget split. `p1_fog.py` … `p13_sign.py` are the painting in order; `p9b` runs after
  `p9`. Against a fresh `easel new painting.easel --size 1024x768 --texture linen
  --ground toned_warm_grey --seed 47 --budget 300` those fourteen passes reproduce
  `painting.png` **byte for byte** — verified by sha256, twice, from two fresh sessions.
  `p0_plan.py` and `p14_export.py` paint nothing and are not part of that sequence.

## No assisted modes

There was no reference, so `prepare`, `sketch`, `ref_shape` and `ref_outline` were not
used and nothing was traced; no pencil was laid either. Every mass is a `polygon`,
`blob`, `Region` or `s.circle()` written by hand and looked at with `preview()` before
it was filled. The stair is a helix computed in `prelude.py` from the tower's taper —
the one place a formula was used for a drawing, because a spiral seen from the side is
a shape no hand of mine would have guessed right: vertical where it meets the
silhouette, flattest across the middle.

## The ground

`toned_warm_grey` reads `0.54`, a step below the fog and a step above the sea, and it
is warm under a picture whose big masses are cool grey and grey-blue. It flecks
through the bristle passes at the top of the fog and through the gaps in the sea's
swell, which is most of what keeps those two quiet passages from going flat.

## The plan, and what it cost

Values were written down first, as a `compare({place: value})` sheet in `prelude.py`:
fog `0.62`–`0.64`, the beam `0.76` far off and `0.79` at the lamp, far sea `0.60`, near
sea `0.40`, rock `0.18`, the tower's lit face `0.52` and its shadow side `0.34`. The
three carrying values were rock `0.17`, sea and tower `0.34`–`0.56`, fog and beam
`0.66`–`0.80`, with the light between the leaves in the lamp room the lightest thing at
`0.90`. Every mixture was made with `at_value()` and landed on its number. Measured on
the finished canvas all nine places are inside `0.10`; the largest miss is the beam at
the lamp, `-0.09`, which is still the lightest big mass in the picture and sits under
the lamp room where the light between the leaves takes over.

The split written before the first stroke: fog 30, beam 20, sea 25, rocks 20, tower and
gallery 25, lamp room 40, stair and pots 40, vines and base 15, edges and finish 35,
reserve 50. What was spent:

| Stage | Strokes | Share |
|---|---|---|
| Fog: underlayer and two passages | 31 | 11% |
| Beam: three glazes, and two more for the counter-beam | 5 | 2% |
| Sea: the lost horizon, two passages, the beam on the water, five swells | 26 | 9% |
| Rock: mass, three planes, crevices, dry brush, the spur lost; then a second pass | 50 | 18% |
| Tower: halo, mass, lit face, terminator, gallery | 18 | 6% |
| Lamp room: green mass, light between leaves, leaves, stems, tomatoes, mullions, rail, dome | 51 | 18% |
| Stair and pots: three turns, eleven pots; then the handrail and balusters | 60 | 21% |
| Base and vines: boulders, door, pots by it, the vine that got out | 31 | 11% |
| Finishing: fog drift, weathering, foam, fog on the water, the lamp once more | 12 | 4% |

The subject — the lamp room, the beam, the stair with its pots, the vines — got **42%**
of the marks against a planned 38%, measured with `note="subject"` as the marks were
made. The lamp room began at stroke 116, 41% of the budget. The beam cost a sixth of
what was planned for it, because what finally worked was three glazes; the rock cost
two and a half times its share, because it was the passage named weakest at the end
and given a second pass. The reserve was 16 at the finish.

## Rehearsing, and what it saved

Twenty rehearsal runs, none charged, plus two cost checks and one sheet of colour
swatches on a scratch session. Everything here was found on a copy and thrown away
before it cost a stroke:

- **The first fog was green.** A grey-green mixture looked like fog on the swatch and
  read as a green sky on the canvas, and if the fog is green the beam's green has
  nothing to be green against. The fog became a neutral warm grey, cooler at the top,
  and the beam got its colour back.
- **The beam was built five times.** A bristle block-in of the wedge, its comb meant to
  read as rays, came back as a ribbed slab. Five flat strokes fanning from the lamp
  came back as a fan of hard ribbons. What reads as light in fog is the soft round
  tip's airbrush, which the guide says never to use for a mass and which is exactly
  right for a thing that is not a mass: three glazes along the beam's axis. The first
  of those was lime and brightest at its far end, because a round tip's width and its
  paint both follow pressure; mixed close to the fog and tapered toward the far end, the
  cone is narrow and bright where it leaves the glass and gone by the left edge.
- **The first sea was teal, with a scalloped horizon and swells that floated like
  logs.** Greyed by a third, with the far sea mixed only a step below the fog's horizon
  value and the swells thinned to a step below the water they lie in, it sat back into
  the fog.
- **The rock was built twice.** A thin top plane laid in eight passes came back as
  terraces, a warm face at `0.27` sat on the mass like a slab, and two crevices read as
  drawn lines. Bolder facets on the outline, broader planes with a wider brush, the
  warm face a step above the mass rather than three, and one crevice.
- **The tower's clean contour rose off its top as an arch.** `edge="clean"` splines its
  contour through the outline's points, and a four-cornered polygon gives it nothing
  to hold the top edge straight. The rock, with thirteen corners, had been fine. The
  tower's sides are subdivided into six points each now; the lit face's outer edge was
  also pulled half a brush inside the silhouette, because its overhang had been
  drawing the tower's left edge in steps.
- **The dome's horizontal passes serrated its curve**; a clean contour with a smaller
  brush fixed it.
- **The stair read as a dark hose wound round the tower.** Small lit tread marks along
  its top edge, rehearsed as the cheap answer, vanished at picture scale. A handrail
  above each turn with three balusters at uneven spacing, set between the pots, is what
  says it is a stair: twelve strokes.
- **Two darker rays in the beam near the lamp** — the shadows of leaves in the light —
  and a pale streak across the far sea's rows were rehearsed with the finishing pass
  and dropped: both read as marks drawn on the picture. The counter-beam, rehearsed on
  its own so it could be dropped, stayed: two faint glazes off to the right are what say
  the light is turning and not fixed, and they fill the one empty corner of the fog.

## The one scrape of the canvas

The last painting pass laid two soft strokes of fog on the far water, and both ran
straight across the tower and the stair's third turn, which are nearer than the fog.
The rehearsal had shown it and I had read the washed-out band as fog drifting past.
Nothing stood on those strokes yet, so the pass was undone — `easel undo painting.easel
3`, the three marks it had laid — and laid again with the strokes stopping short of the
tower. Painting over it would have meant re-laying the stair, its rail and two pots,
with sixteen strokes in hand.

Two things about that worth recording. `s.log()` on a rehearsal copy reports nothing
painted, so the count had to be read from the real session with `Session.load()`. And
`undo` does not put the session back exactly: the export of the working session
differed from a fresh run of the same scripts in `1.06%` of its pixels, `0.05%` of
them by more than `8` of `255`, all in the tower column and the rock where the re-laid
marks landed. Two fresh runs agree byte for byte, so the engine is deterministic and
the drift is the undo's. The scripts are the source, so `painting.png` and
`painting.gif` are the fresh rebuild's, not the working session's.

## What went right

- Back to front throughout: fog, beam, sea, rock, halo, tower, lamp room, stair, pots,
  boulders. Every edge on the tower is where its paint stops and the fog still shows;
  the tower stands in the rock because the boulders went on after it; the lamp room is
  three depths — the halo behind it, the vines and the light inside it, the mullions,
  the rail and the dome in front.
- The value structure held from the first pass to the last: light fog and beam, mid
  sea and tower, dark rock and iron, and the light between the leaves the lightest
  mark. The greyscale look reads without the colour, and the beam reads as light rather
  than as a painted wedge because it has no edge anywhere.
- The edges vary: the horizon and the rock's spur are lost into the fog, the beam and
  the halo are soft, the tower's silhouette and the lantern are hard.
- The pots are eleven of a kind and not eleven copies: no two the same size, three
  kinds of thing growing in them and two empty, one tipped over on its side, the ones
  on the shadow side a step darker. The stair's far side peeks out beyond both
  silhouettes, which is the whole reason it reads as going round.
- The escaped vine trailing down the lit face from the gallery, the tendril over the
  rail, the pots waiting by the door and the green damp stain running from under the
  gallery are what say *conversion* rather than *greenhouse*: the work is not finished
  and somebody is doing it.

## What still bothers me

- The tower's lit face still shows the vertical passes it was laid in, under the
  weathering streaks. It reads as a weathered tower, but as one striped by a machine.
- The far sea is rows of scallops, the flat's wander on six passes. The fog lying on
  the water softens them and they read as swell in fog; they are still rows.
- The stair band is a flat stroke and the treads are a line along its top. With the
  rail it reads as a stair; without the rail it did not, and the rail is doing the work
  the band should have done.
- The rock is the quietest passage and the darkest, and it is still more a shape than a
  thing. The second pass gave it a surface; it did not give it weight.
- Sixteen strokes unspent, on purpose. The marks I can name would be corrections to
  passages that already read, and the guide's rule that the last marks are about the
  picture and not about the score weighed more.

## The signature

One mark, in the quiet near water at the bottom left, a step lighter than the sea it
lies on: a curl on the round tip that thins to nothing at both ends. It is a tendril,
because the shape this session kept coming back to is the helix — the stair, the vine
that got out over the rail, the stems climbing the glass — and a curl is the smallest
piece of one. It is not a name and it repairs nothing; it lies in the water like
something reflected.
