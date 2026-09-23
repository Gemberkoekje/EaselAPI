# The key -- open after Part 1

## 10. The edge candidates

| letter | candidate |
|---|---|
| A | A2 0.003 |
| B | A2 0.002 |
| C | A1 0.002 |
| D | today |

- **today** is `Polygon.coverage` at two samples a pixel: one fractional pixel a side at
  most, then a step.
- **A1** is the coverage ramped inward over the feather: nothing at the drawn line, full
  paint at the feather's depth. A smoothstep of the distance inside the outline, clamped
  under today's coverage, so it can never reach further out than today does.
- **A2** is the same ramp read against the canvas tooth, the way `Canvas.stamp` reads a
  starving brush: near the line only the peaks of the weave take paint, and deeper in the
  valleys do too. The boundary breaks at the weave's scale and each pixel stays crisp.
  Also clamped under today's coverage.
- The feather is a fraction of the long side, like `size`: `0.002` is 2 px at 1024 and
  2.9 px at 1440.
- On the three tower sheets every clip and hard edge in `p04_tower.py` is feathered. On
  the headland, ground and burial sheets only a mass's own outline under `edge="hard"`
  is, which is the default as decided.

**The bench's reading**, which is one eye's: A1 at `0.002` is hard to tell from today at
the painting's size, and past the value that moves the `edges:` line it is blur; A2 at
`0.002` reads as a crisp, painted edge on the tower, the headland, the bare-ground mass
and the burial; at `0.003` it starts to look ragged. **Its recommendation: A2 at
`0.002`.**

## 12. The dry-brush candidates

| letter | candidate |
|---|---|
| P | today |
| Q | B1 |
| R | B3 |
| S | B2 |
| T | B1+B2 |

- **today**: the tooth gate per pixel. A pixel takes paint where the tooth clears
  `(1 - load) x texture_sensitivity`, over a smoothstep band of `0.18`.
- **B1**: the tooth the gate reads is smoothed along the dab's direction of travel, over
  nine pixels, then rescaled to the tooth's own mean and spread.
- **B2**: each bristle of the comb carries its own load, the stroke's raised to a power
  drawn per bristle between a third and three. So a full brush is full in every bristle
  and an empty one in none, and in between some bristles keep their paint. A bristle
  under `0.10` lays nothing, whatever the tooth.
- **B1+B2**: both.
- **B3**: starved paint lands thinner, its alpha scaled by the load.

**The bench's reading**: today is a halftone of dots at the broken-mark loads. B1 makes
dashes that run with the brush. B2 makes a comb's streaks with body between them. B1+B2
is the most like a dry brush dragged. B3 is today's dots, fainter. At `load=0.45` on your
crosser, today lays 571 pieces with a median of 4 px, as long across the travel as along
it; B1 lays 218 pieces of 9, two and a half times as long as they are wide. **Its
recommendation: B1+B2, tuned so a load lays about today's paint.**

## 13. The ten crops

The gates, in order: the rule as it stands / the median brush / a 30% overlap break /
both (the plan's) / the narrowest brush at least half the median / that with a 10% break.
The last column is the bench's own reading, **a reading and not a measurement**: T a
graded passage coming back as bars, F separate things, ? can't tell.

| crop | pass | the run | the gates | the bench read it as |
|---|---|---|---|---|
| crop_01.png | `hands_beans/pass08_pickmass.py` | 9 marks, 0.015-0.05, step 0.017 | fires / fires / - / - / fires / - | T: a finger's form hatched in stripes |
| crop_02.png | `car_wash/p13_form.py` | 9 marks, sizes 0.024-0.046, step 0.038 | fires / fires / fires / fires / fires / fires | T: a graded curtain in visible bars |
| crop_03.png | `pier_underside/pass2_masses.py` | 10 marks, 0.1-0.18, step 0.077 | fires / - / fires / - / fires / fires | F: the pier's big fields stacked |
| crop_04.png | `pier_underside/pass4_water.py` | the overlap break's own run | - / - / fires / - / - / - | ?: faint bands in the water |
| crop_05.png | `lighthouse_greenhouse/opus/p3_beam.py` | 6 marks, 0.01-0.048, step 0.007 | fires / - / fires / - / - / - | T: a beam laid as rays |
| crop_06.png | `lighthouse_greenhouse/fable/p8_base.py` | 6 marks, 0.005-0.014, step 0.012 | fires / fires / - / - / fires / - | F: two pot rims, an arch's band, a base line |
| crop_07.png | `heron_lot/2/pass11_last.py` | 7 marks, 0.0045-0.036, step 0.007 | fires / fires / fires / fires / fires / fires | ?: lines across one plank |
| crop_08.png | `GPT/seaside-village` stage 25, the near boat's hull | 7 marks, 0.009-0.027, step 0.005 | fires / - / - / - / - / - | F: a hull's form, which reads smooth |
| crop_09.png | `lighthouse_greenhouse/sonnet/p3_beam.py` | 11 marks, 0.0405-0.0874, step 0.027 | fires / - / fires / - / fires / fires | T: a beam banded across its width |
| crop_10.png | `hands_beans/pass22_bowl3.py` | 5 marks, 0.038-0.05, step 0.038 | fires / fires / fires / fires / fires / fires | T: a bowl's inside in bands |

Over the 337 passes of the corpus that laid paint, the six gates fire on 9, 5, 7, 3, 7
and 5. On the bench's reading, the plan's gate silences three stacks read as true -- two
beams and a hatched finger -- as well as the three false ones, and the other variant
silences two of each. **Its recommendation: leave the rule as it stands**, unless your
T/F reads the crops differently, since the plan's own condition is a gate that keeps
every true positive.

## 11 and 14

**11.** The bench recommends option (b), `clip=` feathered too, inward. The reason your
decision kept clips hard was an outward feather breaking containment, which an inward
one cannot do, and without it the default misses the very strokes your verdict named.
The horizon would then take `feather=0`, which you said you wanted available. It is
your decision being revisited, so it is yours to overrule.

**14.** The bench recommends declining D1: the target was missed, and D0 is built
regardless.
