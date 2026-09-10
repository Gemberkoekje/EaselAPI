# Level3 — copy. Log.

## The answer to the question, first

**Is it recognisable as this person? No. It is recognisable as *the photograph*.**

Put the two side by side and you get the same scene: same crowded dim room, same warm
tungsten key, same big black coat filling the lower right, same shaggy head in profile
with the mouth open mid-sentence, same raised gloved hands on the left, same orange
carton in the near corner. Cover the reference and you get "a long-haired bearded man
in profile, talking, in a dark bar". You do not get *him*.

**What got there:**

- **The head's silhouette.** The hair mass — the crown, the fall down the back, the
  outline against the lit wall — is the best thing in the picture and it is what makes
  the painting read at all. A viewer identifies him as a shaggy-haired man from across
  a room, and that survived.
- **The profile.** Brow, nose, lip and chin read as a profile line. It is soft, but it
  is a profile and it faces the right way.
- **The beard as a mass**, and the lit jaw plane sitting above it. The face has a jaw.
- **The open mouth**, as a dark with a light above it. Not a mouth you could describe,
  but the *gesture* of speaking is there.
- **The eye's position**, and a dark iris in it.
- **The lit cheek plane** — the one part of the face with any modelling.
- **The whole value map.** 62 of 64 cells within 0.10.

**What defeated me:**

- **The eye itself.** This photograph is a picture of a man's *stare* — the eye is wide,
  the sclera shows above and below the iris, and that is the entire expression. I got a
  dark dot and a pale smudge. No lids, no gaze. This is the biggest single failure and
  it is the difference between "a man" and "this man".
- **The moustache and the nostril.** A soft dark band and a dark almond. The shape of a
  man's moustache is half of what you recognise him by and mine has no shape.
- **The proportion of the face.** My `nose` landmark was placed on the bridge, not the
  tip — about 0.02 of the canvas too high — so the painted nose sits high and the face
  is fractionally short between nose and mouth. I found this out at 6× magnification
  with 30 strokes left, far too late to redraw.
- **Hair as texture.** It is a mass with four strokes of light on it. In the photograph
  it is hundreds of separate lit strands and that is a lot of what makes him look like
  himself.
- **The four other people.** Blocked shapes at roughly the right value. The man in the
  flat cap and the woman in the beret are smears. Nobody would identify any of them.
- **The hands.** Two slabs with lines scratched in for fingers. In the photograph they
  are the second most expressive thing in the frame.

---

## What I did

Canvas 1200×800 (the reference is 3:2), `linen`, ground `umber_wash`, seed 11.

I chose `umber_wash` after measuring all seven grounds by exporting a swatch of each
and reading its luminance: 0.425, the darkest on offer, and warm. The photograph's
median cell is around 0.20, so even the darkest ground is too light — but a warm mid
ground meant every gap that shows reads as room light, and it saved me the whole
upper-left corner (A1, B1, A3, A4 are 0.43–0.44 in the reference and the bare ground
is 0.43; I painted marks into them for surface, not for value).

The order was: `compare()` on the empty canvas → seven landmarks → far background →
right-hand background figures → left-hand figures and foreground → pencil the head →
neck → coat → hair → face → beard → features → value corrections → the last ten.

`compare()` on the empty canvas was the single most useful thing I did in the whole
run. It hands you the photograph's entire value map as numbers before you have spent
anything. My eye had this picture at least two stops too light, exactly as the guide
warns. Without that table I would have painted a dim bar as a beige room.

### Stroke counts

| stage | this pass | running |
|---|---|---|
| far background (walls, ceiling, dark shelving, cool patch) | 45 | 45 |
| right side: wall correction, seated man, red shirt, table, bag | 52 | 97 |
| left side: figures, beret, red hair, hands, gloves, carton, glass | 79 | 176 |
| pencil underdrawing (6 lines) | 0 | 176 |
| neck, coat core, coat edge sweep, fleece | 37 | 213 |
| coat's near arm, whole head laid as hair | 20 | 233 |
| face mass, beard mass | 19 | 252 |
| face features, hair repair, two smudges | 19 | 271 |
| value corrections (coat bottom, tablet, wall, hands, carton, jaw) | 13 | 284 |
| more corrections; then `undo(1)` to free a stroke | +6 −1 | 289 |
| **the last ten** | 10 | **299** |

**Final: `s.stroke_count == 299`.** Free and uncounted: 6 pencil lines, 7 marks,
~25 looks, 2 previews, 5 rehearsals, 8 compares, 3 erases.

**`compare()` at the end: 2 of 64 cells out of tolerance, worst 0.11.** Both are H3 and
H4 — the lit wall in the top-right corner, background, not on the man. Every cell that
touches the subject is inside 0.10. E4 (his jaw) was the last one on the object to come
in, and it came in as a consequence of fixing a drawing error, not a value.

I supplied exactly one colour of my own: `coat = "#100d0b"`, value 0.053. The
reference's coat cells measure 0.04–0.07, and the box's darkest mixture is 0.137, which
would have put F5 at exactly +0.10 — on the threshold with no room for a single lighter
mark anywhere in the cell. I checked the arithmetic before deciding, as the guide asks.
Everything else in the painting is mixed from the twelve pigments.

---

## The marks I rejected

All of these are on disk. Nothing here touched the canvas.

**`out/rehearse_027.png` — the cheek as three `round_hard` strokes at `pressure="even"`.**
Three fat pink sausages lying on the face. A round tip at even pressure lays a solid
lozenge with no tooth and no direction, so three of them read as three *objects* stuck to
the head rather than as one plane turning. Rejected outright. `out/rehearse_026.png` is
the same passage as bristle passes running down the form — worse than I wanted but
clearly better than B, so that is the shape the repair eventually took.

**`out/rehearse_028.png` — the entire feature set at the size I first wrote it.** This
is the most useful thing I rehearsed and every mark in it is wrong the same way: too
big. The eyebrow (`liner`, size 0.009) came out a black caterpillar. The iris (0.013)
a black blob half the width of the face. The nostril dab (0.014) a brown egg sitting on
the cheek, and in the wrong place. The nose-tip highlight a white bead poking off the
profile. The tooth (0.009) a white bar. The lip (0.011) a red sausage. I re-cut every
one of them to roughly half, and moved the nostril and the eyebrow after reading their
true positions off the reference panel of that same rehearsal. Had I painted that plan
I would have spent eleven strokes making the face worse and had nothing left to fix it.

**`out/rehearse_034.png` — `hair_lt` (value 0.47) at size 0.050 dragged across the jaw**
to lift cell E4. It came out as a pale stripe cutting straight through the beard, which
is what a mark chosen to move a number looks like. Rejected. Running `compare(region=
cell("E4"))` instead showed the reference is 0.49–0.53 at x 0.50–0.56, y 0.40–0.46 —
that is *lit skin*, and my beard polygon had simply been drawn too tall and swallowed
it. So the real fix was a drawing fix, and the pale stripe was a symptom.

**`out/rehearse_035.png` — the profile edge as a `flat` at size 0.024, `pressure="even"`.**
A hard bar with square ends laid along the nose. `flat` holds its chisel square to its
travel, so a short one terminates on a flat vertical, which is exactly the "drawn line
around a painted shape" the guide warns about. Rejected for `bristle`, whose broken
comb keeps the edge from reading as a line.

**`out/rehearse_037.png` — the forehead wisp as `bristle` at size 0.008.** Invisible. A
bristle at that size is four streaks with gaps and nothing between them. Swapped for
`liner` at 0.005, which holds its load and actually draws a hair. (CALIBRATION says
this outright. I read it and then wrote 0.008 anyway.)

**`sweep(left_edge, ..., cross=0)` for the coat's near edge** — rejected by the engine,
which refuses `cross=0`. On reflection I did not replace it: the coat's left edge meets
the black glove, both near 0.06, and a lost edge there is the right decision and the
one lost edge the checklist asks for. The best mark I never made.

---

## What the last ten strokes were for

In order, strokes 290–299:

1. **The lit plane of the cheek and jaw** (`bristle`, skin at 0.50). Putting back the
   plane my beard shape had swallowed. This is the mark that gave the face a jaw.
2. **The stubbled underside of the jaw** (`bristle`, 0.41) — the transition from that
   plane down into the beard.
3. **The profile edge**: the dark background carried *up to* where the face stops, brush
   centre outside the head. Not an outline — the guide's method, and the only way I had
   left to make brow, nose and lip read as a silhouette.
4. **A loose strand of hair falling across the forehead** (`liner`, 0.005). He has three
   or four of them in the photograph and they sit right over the brow.
5. **The hair in front of the ear** — the sideburn, which is where the hair mass and the
   face actually meet.
6. **The ear.** One dab. It had not existed until then.
7. **The dark of the open mouth.**
8. **The tooth catching the light**, `press=3`.
9. **The eye** — the iris, `press=3`, because at `press=2` it had not landed.
10. **The signature** (see below).

Nine of those ten are marks about the picture; none of them was chosen off the
`compare()` table. Strokes 1 and 2 *did* bring cell E4 inside tolerance, and I want to be
straight about that: I found the problem through `compare(region=cell("E4"))`, but what
I painted was a plane of a face that had been drawn wrong, not a number. If I had been
chasing the number I would have painted the pale stripe in rehearsal 034, which would
have fixed E4 and ruined the jaw.

The tenth mark was originally **the mole on his neck** — a real, specific feature of this
particular face, at (0.588, 0.434). I lost it to the signature accounting below. At 7 px
on a 1200 px canvas it did not read anyway; I checked the export before deciding.

---

## The signature

One `liner` mark in the bottom-left corner: a short vertical dropping about 0.036 and
turning right about 0.029 — a bracket, or the back corner of a stretcher bar. Value 0.30
against a ground of about 0.40, so it is a shade darker than what it sits on and does
not announce itself. It is in the emptiest, darkest part of the canvas, on top of
nothing I painted.

Why that: I do not have a name, so a name would be a lie. What I do have is the object —
this thing is a rectangle of canvas with something stretched behind it, and the mark is
the corner of the stretcher seen from the back. It is a mark about the made-ness of the
thing rather than about me.

It cost me a stroke I had not budgeted, which is the next section.

---

## What the guide got right

- **"Look every 5 to 15 strokes."** The two passes where I wrote fifty strokes without
  looking (the right-hand figures, the left-hand figures) are the two worst passages in
  the painting. That is not a coincidence and I knew better at the time.
- **Running `compare()` on the empty canvas.** Described as one of two moments to
  measure; it is worth more than that. It is the only reliable way I have of knowing how
  dark a dim photograph actually is, and it costs nothing.
- **Back to front.** Laying the dark shelving mass across C2–D3 *before* the head meant
  the profile had something to stop against, and it is the reason the silhouette works
  at all. I never had to cut a background in around a face.
- **`preview` and `rehearse` over `undo`.** Every expensive mark I rehearsed came out
  better. The one big set I did *not* rehearse — the three cheek highlights — was the
  worst thing in the painting and cost two of my final ten to bury.
- **`sweep` along a boundary.** The coat's back is the best passage in the picture: nine
  strokes, the passes follow the curve of his shoulder, and the silhouette is a real
  edge. This did exactly what the guide and CALIBRATION said it would.
- **"Scale a mark off the thing it describes, not off the canvas."** I ignored it and it
  cost me eleven rejected marks and a repaint. It is the most expensive sentence in the
  guide to skip.
- **The floor arithmetic.** "Anything the reference puts at 0.03 or above is reachable"
  is true and I nearly did not believe it. Half the coat's cells came in at +0.03.
- **"White is a weaker lightener than you expect."** Yes. Every pale mixture needed a
  white ratio above 0.6.

## What the guide got wrong, or left out

1. **Signature marks are not free.** The guide: *"Up to five marks, and they do not come
   out of your stroke budget, so long as each one carries `note="signature"`."* They do.
   Two liner strokes with `note="signature"` took `s.stroke_count` from 299 to **301**,
   and the brief I was working to says `stroke_count` is the number that counts. I had to
   undo, drop a real mark, and re-sign with one stroke instead of two. If there is a
   separate exempt counter somewhere, the guide does not name it, and `stroke_count` —
   the only number it tells you to watch — includes them.

2. **`sweep(cross=0)` raises.** The guide presents `cross=` as advice ("Take it") and
   CALIBRATION tabulates an uncrossed sweep as a real option. Passing `cross=0` is a
   `ValueError`. Omitting the argument works. Nothing says so, and I lost the rest of a
   script to finding out.

3. **`undo(n)` counts log entries, not strokes.** `undo(3)` after two signature strokes
   and one `erase` removed the two strokes and the erase — two strokes, not three. If
   you are ever undoing to claw back budget, that matters, and the guide calls undo
   "scraping the canvas" without saying what a unit is.

4. **A shaped `block_in` can leave part of a concave shape bare, and inset makes it
   worse.** `block_in(coat.inset(0.052), size=0.105)` on a fifteen-point concave polygon
   left his entire near arm — a lobe roughly 0.18 wide and 0.45 tall — completely
   unpainted. CALIBRATION says "coverage at density=1.0 is 99% of the shape", measured
   on a blob. A blob is convex. I did not find the hole until `compare()` showed it,
   twenty strokes later, and it cost six to fill. The guide should say: preview the
   inset shape, not just the shape.

5. **There is no budget arithmetic for a *picture*, only for a *mass*.** `extent/step`
   is right and useless when the question is "how do I spend 300 strokes across five
   people at four depths". I planned 45 strokes for the left-hand figures and spent 79;
   I planned 35 for the right and spent 52. By the time I touched the subject I had 124
   strokes left out of 300 — and the subject is the entire point of the exercise. The
   guide says "you will use too many strokes on detail and too few on structure"; my
   failure was the opposite and more banal, and nothing in the guide warned me about it.
   **Rule I would add: decide what fraction of the budget the subject gets, before the
   first stroke, and spend the background out of what remains.** For this picture it
   should have been 180 on the head and 120 on everything else. It was 124 and 176.

6. **`look(region=...)` pads the crop to the panel's aspect ratio.** Ask for `C2:F6` and
   you are shown more than C2:F6. The guide says a small region is "enlarged so that a
   single cell fills the panel" but never says the *extent* changes. I did pixel
   arithmetic off two such crops to locate features and got both wrong; the fix is to
   calibrate off the drawn `mark()` crosses, which are on both panels and whose canvas
   coordinates you know. That trick is worth a sentence in the guide.

7. **Exercise 1's `at_value()` silently fails downward.** It searches the white ratio,
   so if you ask for a value *darker* than the base it returns ratio 0 and hands you the
   base. I copied it, asked for 0.30 from a base at 0.41, and painted a field at 0.41
   without noticing. The guide hands you that function; it should say it only goes up.

8. **`dab(press=2)` is far weaker than the table suggests.** CALIBRATION's numbers are
   for white on three grounds. A near-black iris at `press=2` on a lit cheek barely
   registered and I spent one of my last ten redoing it at `press=3`. The working rule is
   simpler than the table: **`press=3` for anything you want to actually land; `press=1`
   or `2` is a whisper.**

9. **`preview(points)` draws the brush at some default width** and never says which. The
   silhouette previews came back as a wide band over the outline, which is fine for
   checking placement against the reference and no use for checking an edge.

10. **`compare(region=cell(...))`'s detail lines are `col,row`** — the transpose of how
    the table above them is printed. I worked it out by cross-referencing a value, which
    took a minute and a half I did not need to spend.

11. **Nothing about a scene with more than one subject.** Every piece of advice in the
    guide assumes one object against a ground. This photograph has five people at four
    depths, a table, and a foreground still life. The depth ordering rule scales fine;
    the *attention* rule does not, and the checklist question "is the thing you measured
    most carefully still attached to the picture?" has a harder version I hit here: is
    the thing you measured most carefully still the thing the picture is *about*?

---

## Honest opinion of the painting

It is a competent block-in and an unfinished picture, and the two are not the same thing.

The value structure is genuinely good — look at `out/look_041.png`, the greyscale pair.
The dark coat, the mid room, the lit wall on the right, the light hands and carton all
sit where they sit in the photograph. If value is what carries a copy, this one carries.
The composition is right, the key is right, the warm dim-tungsten colour is right, and
there is a real edge along the coat's back that I like.

Everything above that level is unresolved.

The face has one plane, one dot for an eye, and a smudge for a mouth. It reads as a face
because it is head-shaped and has a beard-coloured region in the right place, not because
anything in it is drawn. The hands are two pink slabs with three scratches each. The
carton is a stack of orange bars. The four background figures are colour patches — the man
on the right has a face made of one dab of `skin_far` and it shows.

Specific flaws I would fix first, in order:

- **The eye.** Two more strokes — an upper lid and the sclera below the iris — would
  probably move this from "a man" to "this man" more than anything else on the list.
- **The pale rectangles on the cheek.** I buried them, but you can still see two hard
  horizontal edges across the temple where the `flat` strokes ended. They are the
  loudest wrong thing in the head.
- **The bristle sprinkle in the hair at the back.** Two strokes at size 0.013–0.016
  laid a field of dots that looks like dust, and my repair only half covered it.
- **Everything on the left half.** The hands, the beret, the red hair and the carton are
  all bars and slabs. The checklist asks "is any mass a rectangle that should have been
  a shape?" — the carton, honestly, yes, and so is the tablet at the bottom, and so are
  most of the marks on the hands.
- **The tablet in the foreground** is a grey box. It is the last thing I painted before
  the corrections and it looks it.

The thing I got most right was the decision to lay the whole head as hair first and cut
the face into it, so the hairline is a real edge I never drew. The thing I got most
wrong was arithmetic: 176 strokes gone before the subject existed.

---

## Every moment I wanted to open the source

Kept as I went. None of these were opened.

1. **`at_value()` returning the base unchanged** when I asked for a value below it. I
   wanted `mix`'s signature to see whether it would take a black or an umber as the
   second ingredient so I could search downward too. Worked it out by printing.
2. **`sweep(cross=0)` raising.** I wanted the signature of `sweep` — specifically whether
   `cross` had a default and what it was. Guessed that omitting it worked. It did.
3. **Costing a `block_in` before calling it.** CALIBRATION gives `extent/step` but not
   how `extent` is computed for a *shape* with a given `direction=` in degrees. I wanted
   the pass-counting code. Instead I over-ran my budget twice and adjusted.
4. **`preview`'s default brush size.** The silhouette previews came back as a band and I
   wanted to know how wide, to judge whether an edge would land. Ignored it and used
   `rehearse` for anything that mattered.
5. **`dab(press=n)`'s curve for dark colours.** The iris at `press=2` did nothing
   visible and CALIBRATION only tabulates white. I wanted the pressure profile across
   the stamps. Used `press=3` and moved on.
6. **`desaturate`.** When `desaturate(V(warm,0.30), 0.35)` printed 0.41 I suspected
   `desaturate` of moving the value, contradicting the guide. I wanted the function. It
   turned out to be my own `at_value` bug (item 1), which I only established by printing
   the un-desaturated mixture — a source read would have taken ten seconds.
7. **`note="signature"` and the budget.** This is the one I most wanted. Two signature
   strokes moved `stroke_count` and I wanted to see how the note is checked, or whether
   there is a second counter that excludes them. Resolved by undoing and re-signing with
   one mark, which cost me a real stroke.
8. **`undo(n)`'s unit.** `undo(3)` removed two strokes. I wanted to know whether it
   pops log entries or marks. Established empirically by printing `stroke_count` either
   side, which is the right way, but I wanted the definition.
9. **`Shape.inset()` on a concave polygon.** When the coat's near arm came out bare I
   wanted to know whether `inset` collapses thin lobes or whether the block-in simply
   found no room for a pass. Never established. I filled it with a separate polygon.
10. **`erase(region=)`.** I wanted to know whether it removes only graphite or also
    paint before I ran it across a finished coat. Ran it on a region I could afford to
    lose first — which is the painterly answer, and slower.
11. **How `look(region=)` decides its crop.** Twice my pixel-to-canvas arithmetic was
    off because the panel showed more than the span I asked for. I wanted the cropping
    code. Instead I recalibrated off the `mark()` crosses, which is more reliable anyway.
12. **`bristle`'s minimum useful size.** When two strokes at 0.013–0.016 came out as
    dotted lines I wanted `BRISTLE_PITCH` and the count rule. It is in CALIBRATION and I
    had read it; I wanted the source because I did not believe the picture.
13. **`compare(region=)`'s detail-line axis order.** Wanted the print statement. Worked
    it out by matching a value against the table.
14. **What `s.log()` returns.** It prints as a string and I wanted to know whether the
    stroke records were addressable, so I could count my own last ten programmatically
    rather than by reading the tail. Printed `type()` and read the tail.

The pattern: nine of the fourteen are questions about a *contract* — what a parameter
means, what a unit is, what a default is — not about behaviour. Behaviour I could always
get from the picture, and the picture was usually a better teacher. Contracts I could
not get from the picture at all, and every one of them cost me either strokes or a
script. The two that actually cost me marks in the finished painting (the signature
budget, and `undo`'s unit) are both contract questions, and both are things one sentence
in the guide would have settled.

---

## Files

- `copy.easel` — the session, 299 strokes
- `copy_final.png` — 1200×800
- `copy_timelapse.gif` — 107 frames
- `out/` — every look, preview, rehearsal and compare heat map, numbered in order
- `pass1.py` … `pass14_fix.py`, `probe_*.py` — the scripts, in the order they ran
