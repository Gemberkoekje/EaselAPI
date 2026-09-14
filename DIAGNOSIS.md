# Diagnosis: you have looked, it is wrong, and you do not know which file says why

**This file is not for reading.** It adds nothing: every row points at text that already
exists somewhere else, and the pointer is the whole entry. Read it front to back and you
have read a list of ways to fail, which is the one thing `LESSONS.md` measured as not
working — and a list of failures read before you make any of them may teach you to see
failures you were not going to make.

**Use it the other way round.** You have rehearsed a pass and looked at it. Something in
the image is wrong and you can describe it. Find the description, follow the pointer,
make the mark. `grep -i rings DIAGNOSIS.md` is the intended interface.

**Follow the pointer; do not work from the row** — one session recognised five on
sight, followed none, and repaired a staircase the expensive way while the row's own
target held the cheap one. **A row naming a file you were not given is not for you.**

It indexes [`PAINTER.md`](PAINTER.md), [`PAINTING.md`](PAINTING.md),
[`RECIPES.md`](RECIPES.md), [`REFERENCE.md`](REFERENCE.md) and
[`CALIBRATION.md`](CALIBRATION.md). Every pointer is checked against those files by
`tests/test_diagnosis.py`, because an index that has drifted is worse than none.

---

## A mass, a plane, a silhouette

| What you are looking at | Where |
|---|---|
| A mass that came out a rectangle when you built it as a shape | `PAINTER.md` → *What you are bad at*; `PAINTING.md` → *Masses that are not rectangles* |
| A mottled field with the ground showing through in flecks, at `density=1.0` | `RECIPES.md` → *A plane that is a plane* |
| Faint striping across a large flat plane, and `opacity` will not remove it | `PAINTER.md` → *2. Tone the ground*; `CALIBRATION.md` → *`block_in`* |
| A mass that has eaten a sawtooth out of the one beside it | `CALIBRATION.md` → *`block_in`* |
| A staircase along a boundary that is not parallel to the passes | `CALIBRATION.md` → *The chisel staircase*; `PAINTING.md` → *The shape each tool leaves behind* |
| A clean edge that came back stringy, or that ate the corners | `CALIBRATION.md` → *The contour of a clean edge*; `CALIBRATION.md` → *A clean edge on a narrow mass* |
| Slabs stuck on a smooth shape, or a woven surface where planes should be | `RECIPES.md` → *A mass built of planes* |
| Two flat stripes where a round form should have turned | `RECIPES.md` → *A form that turns* |
| A bare strip of ground along the canvas frame | `CALIBRATION.md` → *`block_in`* |
| A small mass that came back the colour of whatever it was laid over, or a solid mass that will not reach the value you mixed | `CALIBRATION.md` → *What a solid mass actually lands at* |
| A mass that shows its passes because you laid it with a round tip | `CALIBRATION.md` → *`block_in`* |

## A soft passage, a glow, a gradient

| What you are looking at | Where |
|---|---|
| A wide soft passage that came out as three or four hard bars, or a venetian blind with gaps between the passes | `RECIPES.md` → *A quiet gradient*; `CALIBRATION.md` → *The band, and the brush that closes its joins* |
| A band you laid by hand, stroke by stroke, that ribbed where a `scumble` of the same shape did not | `RECIPES.md` → *A passage brightening toward one side* |
| A sky, a far field or a sheet of water — a third of the canvas, graded — that reads as a stack of bands, or shows horizontal strata with flecks of bare ground in them | `RECIPES.md` → *A graded field that is most of the picture* |
| A glow with visible concentric rings, like a contour map | `CALIBRATION.md` → *`scumble`* |
| A glow that came back a solid disc with a thin ramp round it, a daisy of petals radiating from a shared centre, or a rim with nothing in the middle | `RECIPES.md` → *A passage light in the middle* |
| A passage that will not go quiet however low you set `opacity` | `CALIBRATION.md` → *Opacity does not make a passage quieter* |
| A passage that bloomed past the outline at one end and is barely there at the other | `CALIBRATION.md` → *The band across a wedge* |
| Light that is **in** a medium rather than on a surface: a beam, a shaft, a halo, a lamp under water | `RECIPES.md` → *A volume of lit air* |
| A ribbed slab, a fan of ribbons, or a searchlight that owns the picture | `RECIPES.md` → *A volume of lit air* |
| A beam brightest at the wrong end | `RECIPES.md` → *A volume of lit air* |
| A passage lit on the side you did not mean | `REFERENCE.md` → *Where a stack of passes starts* |
| A join you have smudged twice and it is still there | `RECIPES.md` → *A quiet gradient*; `CALIBRATION.md` → *`smudge`* |
| A field gradated top to bottom that reads as a stack of bands | `PAINTER.md` → *5. Refine the mid-tones* |

## An edge

| What you are looking at | Where |
|---|---|
| A finger-shaped lobe dragged out of one mass into another | `RECIPES.md` → *A mark that crosses a boundary* |
| A thumbprint at the end of a smudge | `CALIBRATION.md` → *`smudge`* |
| Every edge equally sharp; the picture reads as clip-art | `PAINTER.md` → *6. Edges: lost and found* |
| Two edges *nearly* lost, reading as neither | `RECIPES.md` → *An edge that is actually lost* |
| A drawn line running round a painted shape | `PAINTER.md` → *What you are bad at* |
| A mechanical straight line in a picture that has none | `RECIPES.md` → *The one ruled line* |
| A long edge that came out scalloped | `RECIPES.md` → *The one ruled line*; `CALIBRATION.md` → *`scumble`* |
| A thin member beaded into a chain of separate blocks | `RECIPES.md` → *The one ruled line* |
| A silhouette you cannot sharpen without drawing along it | `PAINTER.md` → *What you are bad at* |

## A small mark

| What you are looking at | Where |
|---|---|
| A row of floating discs: one silhouette, printed over and over | `RECIPES.md` → *A small irregular bright mark*; `CALIBRATION.md` → *At the scale of a feature* |
| A capsule with rounded ends, or a rectangle with chisel ends | `PAINTING.md` → *The shape each tool leaves behind* |
| A small mark that did not register at all | `RECIPES.md` → *A small round thing*; `CALIBRATION.md` → *At the scale of a feature* |
| A cast shadow reading as a hole punched through the surface | `PAINTER.md` → *4. Check your values* |
| A cast shadow as a filled slab with two hard ends | `PAINTER.md` → *4. Check your values* |
| A tapered arc that left a seam, or came back a ghost | `RECIPES.md` → *A tapered arc* |
| A small object reading as a bulb, a brick, or a bite | `RECIPES.md` → *A small container with something spilling from it* |
| A chisel mark given a pressure list that did not taper | `REFERENCE.md` → *Pressure*; `CALIBRATION.md` → *Pressure* |
| A starved brush that laid almost nothing | `CALIBRATION.md` → *Load and run-out* |
| A bristle under `size=0.025` reading as four streaks with gaps — when you wanted a plane, not a broken mark | `CALIBRATION.md` → *The bristle comb* |
| A hole in a mass laid as a dot in its interior | `PAINTER.md` → *What you are bad at* |

## Colour, value, paint

| What you are looking at | Where |
|---|---|
| A glaze that is a stripe at one opacity and invisible at the next | `CALIBRATION.md` → *`glaze`*; `PAINTING.md` → *Wet paint* |
| A colour sampled off the canvas that came back near black | `PAINTING.md` → *Colour*; `REFERENCE.md` → *Colour* |
| A mixture that should have been a grey and came out green | `PAINTING.md` → *Colour* |
| A mixture that should be halfway and came out too dark | `CALIBRATION.md` → *The value scale* |
| A value the palette refused as out of reach | `CALIBRATION.md` → *What the box reaches* |
| A mass that will not go darker however many passes you lay | `CALIBRATION.md` → *What the box reaches* |
| A light laid over a dark that went olive, or a dark that sank | `PAINTING.md` → *Wet paint*; `CALIBRATION.md` → *Wetness* |
| A mass that looks lighter than the number you mixed it at | `CALIBRATION.md` → *The paint and the view of it* |
| A mixture that reads more vivid than `value_of` suggested | `PAINTING.md` → *Colour*; `CALIBRATION.md` → *Chroma* |
| A form shaded until it stopped separating from its background | `PAINTER.md` → *4. Check your values* |
| Pencil still showing where you did not mean it to | `CALIBRATION.md` → *Graphite under paint* |

## The picture

| What you are looking at | Where |
|---|---|
| Two masses you planned as different that read as one | `PAINTER.md` → *4. Check your values* |
| The lightest thing in the picture is not the thing it is about | `RECIPES.md` → *A subject that is one thing against a ground*; `PAINTER.md` → *A checklist before you call it finished* |
| A stack of horizontal bands with a subject standing in one of them | `RECIPES.md` → *A subject that is one thing against a ground* |
| One half of the picture empty, and every fix puts a second subject in it | `RECIPES.md` → *A picture with an empty half* |
| A correction that buried the fine marks standing on a mass | `RECIPES.md` → *A repair under things that are standing on it* |
| Something that has escaped the thing containing it | `RECIPES.md` → *A hollow thing*; `PAINTER.md` → *3. Paint from back to front* |
| Three of a thing reading as three copies of one thing | `PAINTER.md` → *What you are bad at* |
| A background of square patches, every edge parallel to the canvas | `PAINTING.md` → *The angle of the mark* |
| A scene of straight edges that reads as a diagram, every line the same weight and nothing lost | `RECIPES.md` → *A scene with straight edges* |
| A surface's grain laid as thirty strokes all running one way | `PAINTING.md` → *The angle of the mark* |
| A well-built feature in a picture that has not come up with it | `PAINTING.md` → *When to stop measuring* |
| A third of the budget in hand and nothing you can name to spend it on | `PAINTER.md` → *A checklist before you call it finished* |

## What it cost

| What you are looking at | Where |
|---|---|
| A pass that charged several times what you budgeted for it | `PAINTING.md` → *Try the mark before you spend it* |
| A shaped mass that cost far more than its axis price | `CALIBRATION.md` → *A shaped mass with `direction` left off* |
| A curved `ribbon` that cost ten times its own width | `CALIBRATION.md` → *Shaped masses* |
| A rehearsed pass reporting a budget that is not the painting's | `REFERENCE.md` → *What counts against the budget* |
| An `undo` that gave back fewer marks than you asked for | `PAINTER.md` → *What you are bad at*; `CALIBRATION.md` → *The log, undo, and the stream* |
