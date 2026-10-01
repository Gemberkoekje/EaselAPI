# Uktarl's Room: four vampires at cards under a carved sunrise

Painted with `easel-paint` **0.8.0** on the day it was released, by `claude-opus-5-5` at max
effort, in a session of the owner's own tabletop-campaign project on the owner's Windows
machine; it upgraded the installed 0.7.0 before it opened the guide. The owner asked it to *look
up what the rooms of Uktarl Krannoc look like* and paint *an appropriate painting*. So the
subject was set, and the room, the moment and the composition were the painter's: area 6c
of the first level of *Dungeon of the Mad Mage*, seen from its doorway, with the leader of
four costumed card-players standing inside a carved sunburst. The campaign's own files are
left out of this filing, as the pack's were for the Bell-Warden: the paths of the dossier
and map the room was read from, the catalogue entry the painter drafted, and the WebP copy.
**It is the first painting made against 0.8.0.** What it says about that release is read
in [`PLAN-0.9.0.md`](../../../PLAN-0.9.0.md).

**It is not a fresh painter.** It began with its own memory note from the project's earlier
paintings. Then it read `PAINTER.md` from the installed wheel and 0.8.0's changelog entry
from the repository's checkout on the same machine, then the notes of the Bell-Warden and
Wenna Brask with the second's prelude, then `RECIPES.md` and `REFERENCE.md` whole: 33,596
words of the documents before its first exercise (measured from its
session; see *What happened when it was filed*). It ran `easel demo mistakes` and all ten
exercises ([`exercises/exercises.py`](exercises/exercises.py)), and laid its mixtures side
by side before the first mass ([`swatches.py`](swatches.py)).

**To understand this, start by reading [`prelude.py`](prelude.py)**: the projection, every
shape drawn in pixels through `s.px`, the mixtures, the `s.plan(...)`, and the three heads
drawn in their own radii through `hp()`, `dp()` and `ah()`. Then read the passes
`p01_draw.py` to `p17_finish.py` in their numbering, which is also the order they rebuild
in. [`verdict.md`](verdict.md) is the painter's own review, written after the export.
[`reports.txt`](reports.txt) is every block `easel run` printed after a pass, as the session
file kept them: 46, rehearsals included. [`versions/`](versions/README.md) holds the three
rehearsed versions the verdict's pricing and seam claims rest on, recovered from the
session's transcript. [`evidence/`](evidence) holds five pictures. The account under *The
painter's notes* is the painter's; everything else here is the filer's.

## The plan, as declared

| declared | |
|---|---|
| why | *Four vampires at cards beneath a carved sunrise: its rays fan out from behind Uktarl's head like a saint's halo, and no real vampire would stand in it.* |
| values | Uktarl's face `0.68`; the lit gilding above his head `0.50`; the table top by the candle `0.46`; the corner `A1` `0.22`; the mountain's right flank `0.22`; the floor at the left `0.15`; the near bandit's back `0.14` |
| lightest | Uktarl's face |
| subject share | `0.30`, on the marks noted `"subject"`: Uktarl alone |
| ground | `"buried"` |
| key, bands | not declared |

1024×768, linen, ground `#54443a` (`0.28`), seed 31. **410 of a 450 budget**, the last 40
left on purpose. 26 rehearsals and 20 committed runs, every one saved with what its check
said; none of the rehearsals charged. At the end: the subject 114 of the 410 marks, `28%`
against the `30%` planned; *6 of 7 places inside 0.10*, the table top by the candle
`-0.18`; Uktarl's face the lightest place, `0.65` as a place and `0.69` at its brightest
twentieth; `8.49%` bare ground; `0 of 44` masses in a rectangle; `59%` of edges under
2.5 px.

## The passes

| File | What it is | Strokes |
|---|---|---|
| `prelude.py` | runs before every pass: a camera 1.62 m up at the doorway and the wall 7.4 m away; every shape, in pixels; the mixtures, each at the value it is planned at; the plan; the three heads in their own radii; and three regions of the relief that share Uktarl's outline, for the light behind him | |
| `p01_draw.py` | the drawing, as guides, and the candle and lantern as landmarks. Free; run three times | 0 |
| `t01_notan.py` | the arrangement flat at its planned values, `s.thumbnail()` at 384 px. Free; run once, before any paint | 0 |
| `p02_wall.py` | the wall in a bristle, then thirteen rays, each one flat stroke held to its own wedge | 25 |
| `p03_mountain.py` | the mountain dark against the gold: its mass, strata in a starved bristle, the ridges the lamp finds, seven cave mouths, four crevices | 38 |
| `p04_lamplight.py` | the lantern's pool on the relief in four soft strokes, the inner rays struck again in the gilding's lit colour, the corners glazed down | 18 |
| `p05_floor_tub.py` | the floor's two halves along their receding lines; the tub's far inner wall, the blanket in it, one catch-light on the near rim | 29 |
| `p06_uktarl_body.py` | the cape's lining, lit where the candle reaches, a join along its terminator, the folds; the body, the raised arm, the collar as two flaps with a black edge each, the cravat | 51 |
| `p07_uktarl_head.py` | the head lit from below: the shade mass, the brow's half-tone and the lit plane sharing the terminator at the brow line, a join, the far cheek; eyes, catch-lights, brows, nose, mouth, fangs; the wig | 51 |
| `p08_backlight.py` | the lantern's light on the relief round his silhouette: soft strokes held to the three regions that share his outline, and a glare where the rays meet | 7 |
| `p09_doppelganger.py` | the body; the head as Uktarl's was laid, lit from the other side; ears, eyes, nose, mouth, a tooth; the collar | 43 |
| `p10_table.py` | the top, its near edge, the candle's pool in three soft strokes, two cracks | 11 |
| `p11_left_bandit.py` | the dress, the wig, the neck and the face as the others were laid, the features, two strands of hair across the face, a hand | 36 |
| `p12_card_game.py` | the laps, the candle and its flame, a film of its light; fans of cards in three hands, cards on the table, coin stacks, loose coins, a ring | 41 |
| `p13_near_bandit.py` | the nearest figure: the cloak, the hood, the profile the candle finds, two rims | 22 |
| `p14_relief_details.py` | the carved dwarves in the cave mouths, the crags by Uktarl lit, two cracks across the rays | 13 |
| `p15_light_edges.py` | the glare above his head, the candle's warmth on him and the table, a rim on every figure facing the flame | 10 |
| `p16_hand_and_crags.py` | the fan in Uktarl's hand again, with pips and a thumb; the far crags' lit faces | 13 |
| `p17_finish.py` | two edges lost with a smudge each, and the signature, which the budget does not count | 2 |
| `look_*.py` | seven free looks, each run beside a pass for a crop or a clean view: `look_head.py`, `look_all.py`, `look_d.py`, `look_a.py`, `look_table.py`, `look_relief.py`, `look_hand.py` | 0 |
| `swatches.py` | the painting's mixtures side by side, on a session of their own | |

## The painter's notes

What follows is the painter's own `NOTES.md` as it stood when the painting was handed over,
on 2026-10-01: verbatim, except that its headings are set here as bold lines and the cuts
are marked.

> _To understand this, start by reading `prelude.py` (the projection, the drawing in pixels,
> the mixtures, the plan), then the passes in order, `p01_draw.py` to `p17_finish.py`; each
> pass's docstring says what it lays and, where a first version failed, why it was replaced.
> Painted 2026-10-01 with Easel 0.8.0 (`easel-paint`, upgraded from 0.7.0 for this picture),
> following its `PAINTER.md`. The six-mistakes demo and the ten exercises were done first
> (`exercises/`), and this painting's own mixtures were laid side by side before the first
> mass (`swatches.py`)._
>
> *[The painter's title and its picture are left out here; the picture is `painting.png`.]*
>
> **What it is.** Dungeon of the Mad Mage, level 1, area 6c, *Uktarl's Room*, the way the
> party sees it from the doorway in the south wall. The whole north wall is a stone relief:
> a rugged mountain hollowed into caverns of tiny carved dwarves, with carved rays of
> sunlight fanning out behind it to the edges of the wall. A stone tub, where Uktarl sleeps,
> is sunk into the floor under it. Four Undertakers in vampire costume play cards at a
> decrepit table near the door. Uktarl Krannoc has risen behind the table to greet the
> party, holding his cape out like a wing, a fan of the marked deck in his other hand. At the
> left end of the table sits a bandit in a long black wig. At the far right sits the
> doppelganger, bald and pointed-eared. Nearest us is a hooded bandit, looking round.
> *[A sentence on the copy made for the campaign's app is left out here.]*
> `uktarl-krannoc-timelapse.gif` is the log replayed, every second mark.
>
> **Where the room came from.** The campaign's dossier (*[its path, left out]*, areas
> 6 to 6e and 7 to 7b, and the `uktarl-krannoc` entity) for what is in the room. The
> level map (*[its file, left out]*) for its shape: about 20 ft across and
> 30 ft deep, entered from the south, with the tub against the north wall and the round
> table in the middle. Uktarl's other room, the vampire haven he retreats to (7a, the hall
> of bedrolls under frescoes of a giant bat terrorising villagers, and the crypt 7b with
> its coffin), is not in this picture.
>
> **Why this subject** (the `why=` in the plan): *four vampires at cards beneath a carved
> sunrise: its rays fan out from behind Uktarl's head like a saint's halo, and no real
> vampire would stand in it.* The relief's sun is behind the mountain, so its rays leave a
> point the viewer never sees. The drawing puts that point behind his head, and the lantern
> that lights the relief stands behind his chest. Looked at small (`look(scale=256)`), the
> first thing in the picture is a vampire inside a sunburst.
>
> | | |
> |---|---|
> | Canvas | 1024 × 768, linen, ground `#54443a` (0.28), seed 31 |
> | Budget | 410 of 450 strokes, the last 40 left unspent on purpose (below); the subject 114 of them (28%, against 30% planned) |
> | Lightest | Uktarl's face, as planned: 0.65 as a place, 0.69 at its brightest twentieth |
> | Masses laid as rectangles | 0 of 44 |
> | Ground | buried, as declared; 8.5% shows through the bristle of the wall, where it reads as the stone's warmth |
> | Reproducible | the log replays to the stroke. The pass scripts are the final versions; each was rehearsed, most several times, before it ran once |
>
> **Changes from the book**
>
> - **Uktarl stands.** The book sits all four at the table. He has risen to meet the party,
>   which is the moment a DM shows this picture. It also puts his head where the rays meet.
> - **The light is mine.** The book does not say how 6c is lit. A lantern on a crate by the
>   tub lights the relief from behind him, and a candle on the table lights the four of them.
> - **The tub is off to the right** under the relief rather than centred, so that some of it
>   shows past the doppelganger. The book only says it lies beneath the relief.
> - **Four different costumes.** The book says only "disguised as vampires". The costumes
>   differ so the four read as four people, not one printed four times: a high red-lined
>   collar, a long black wig, a bald head with pointed ears, and a hood.
>
> **Safe to show the players.** The disguises are painted as convincing, so the picture does
> not give away the DC 14 Insight check. The doppelganger looks like one more costumed
> bandit. No dwarf in the relief is marked out, so the stone key stays hidden. The joke is in
> the composition, and only for whoever thinks about it.
>
> **What went wrong, and what fixed it**
>
> - **The thumbnail caught two drawing faults before any paint** (`t01_notan.py`, free, new
>   in 0.8.0). Uktarl's face was planned at the same value as the glow behind it and
>   vanished into it. The doppelganger's ears were two matching peaks and read as cat ears.
>   The ears were made small and angled back, and the face was taken lighter than the glow.
> - **A sunburst is thirteen strokes.** Each ray is one wide flat stroke laid from the sun
>   outward and held to its own wedge with `clip=`. It costs one stroke per ray, and the
>   wedge, not the brush, makes the shape.
> - **Light multiplies; paint blends.** The lantern's pool, three soft strokes over the
>   relief, lightened rays and gaps alike and flattened them. Re-striking the inner part of
>   each ray in the gilding's lit colour, inside its own wedge, brought the pattern back
>   brighter near the lamp, which is what lamplight does.
> - **The mountain failed first as planes.** That first pass, with ten lit facets, cost 129
>   strokes (`clean-small` on every facet) and read as fence posts on a flat violet stage
>   flat. What replaced them was
>   the idea, not a brush: the sun rises behind a *dark* mountain, the picture everyone
>   already knows. So the mountain is quiet, and the lamp catches only the crags beside him.
>   It cost 38.
> - **The backlight first hugged his outline** like a digital outer glow. A third, wider and
>   fainter stroke on each side turned it into a pool. Then it showed a hard vertical seam
>   where its clip region ended. A clip region has to reach past the soft stroke's radius,
>   or the stroke's edge becomes the region's.
> - **The collar cost 43 strokes** as one wide shape laid with small brushes. A mass is
>   priced across its passes, and that collar was wide and thin. As two flaps, each laid
>   along its own length, with the black outside as two edge strokes, it cost about 10.
> - **The first face was a mask.** Lit from below, with the terminator under the eyes, the
>   sockets and the brows made one dark band across the face. With the terminator moved up
>   to the brow line, the eyes sit in lit skin and can be found as marks. A pointed chin, a
>   thin smirk and two fang tips made the rest.
> - **Two identical small upright marks in a dark hole read as eyes**, not as the carved
>   dwarves they were meant to be. Breaking up each pair (one sitting, one leaning, one
>   swinging a pick) and dimming them to carved stone made them figures again.
> - **A fan of cards was a napkin** when its chisel marks were short, wide and all the same
>   value. Card-shaped marks, every other one a step darker, a red or black pip near each
>   top, and a thumb across the base read as cards.
> - **Small mechanics.** A block-in clipped to half of its polygon, run along a diagonal,
>   lays half its passes outside the clip (`landed nothing`). Make two polygons instead. A
>   floor laid along receding lines without `edge="hard"` spills its chisel ends above the
>   floor line. A `union()` raises unless the parts overlap.
>
> **What it still is**
>
> - **The hooded bandit in front is the weakest passage.** Its hood reads as the back of a
>   bald head, and the profile at its edge is a pale strip. It does its job as the dark
>   thing that pushes the table back, but a better drawing would give the hood a peak and a
>   fold, and turn the head further.
> - **The mountain is still flatter than carved stone**, away from the crags by Uktarl. Most
>   of it is behind figures, which is why the strokes went elsewhere.
> - **The bandit's plum dress is one flat shape.**
> - **The faces are masks.** For four actors in stage make-up that is not wholly wrong.
> - **No clear light, by the check's own measure:** the 95th percentile is 0.52. The lights
>   are small: his face, the inner rays, the flame. On a projector a picture this dark loses
>   its middle values first, so if it looks muddy there, a brightened copy is the fix, not
>   more paint.
> - **Why 40 strokes are left:** the weak passages above would need redrawing, not more
>   marks, and the picture reads at every size it will be met at.
>
> **The signature**
>
> Four free marks in the floor's own dark at the bottom right, close in value to what they
> sit on: a small carved sunrise, an arc and three short rays, the room's own sign.
>
> *[A section giving the campaign catalogue's entry for the picture, and the open question
> about its `origin` field, is left out here.]*
>
> **Working notes**
>
> - `look_*.py` and `t01_notan.py` are free looks run beside a pass (`easel run x.easel
>   pass.py look_head.py --rehearse`), each writing one named PNG into `out/`. They paint
>   nothing.
> - The face, the doppelganger's and the bandit's heads are drawn in head radii through
>   `hp()`, `dp()` and `ah()`: a centre, two radii and a tilt. The lit planes take their
>   edges from the same outline, so they meet it exactly.
> - No pass's `easel log` showed *NO PAINT LANDED*. The faintest marks are the signature's
>   three rays, at 8 or 9 units of paint each: faint, as a signature should be. The one pass
>   the check names (`record 186`, outside its clip) is a single pass of the far-cheek shade.

## What happened when it was filed

Everything under this heading is the filer's, not the painter's.

- **What was filed, and what was not.** The scripts keep the painter's names and take the
  repository's line endings. The session file (`uktarl.easel`, 8.0 MB) is not committed,
  because `*.easel` never is; its 46 saved reports are written out as
  [`reports.txt`](reports.txt), which is `easel log uktarl.easel --reports -n 46`. The
  export and the time-lapse are `painting.png` and `painting.gif`. The WebP copy and the
  campaign's paths and catalogue entry are not filed. The look scripts, `t01_notan.py`
  and `swatches.py` are filed because the notes name them; none of them paints on the
  painting. Of the pictures in the painter's `out/`, four are under
  [`evidence/`](evidence), renamed: `thumbnail_first.png` (the first thumbnail, before any
  paint: the face the same value as the glow behind it, and the doppelganger's ears as a
  cat's), `mountain_facets.png` (the mountain's first pass, 129 strokes), `collar_v.png`
  (the body's first pass, with the V-shaped collar, 85) and `labels_on_the_face.png` (the
  head from the head pass's last rehearsal look, enlarged three times). The fifth,
  `backlight_seam.png`, was rehearsed again here from its recovered script, because the
  painter's own crop of it was overwritten by the next version.
- **Rebuilt here, pass by pass, through `easel run`**, on the checkout at `v0.8.0`'s code:
  the same 429 records, 410 spent, every record identical to the painter's file, and an
  export identical to the painter's PNG to the pixel, on the machine it was painted on. The
  passes rebuild **in their numbering**: the drawing ran three times and the thumbnail
  once, but neither lays a record, so neither moves a mark. To rebuild, in this directory:

  ```bash
  easel new uktarl.easel --size 1024x768 --texture linen --ground "#54443a" --seed 31 --budget 450
  easel run uktarl.easel p01_draw.py p02_wall.py p03_mountain.py p04_lamplight.py p05_floor_tub.py p06_uktarl_body.py p07_uktarl_head.py p08_backlight.py p09_doppelganger.py p10_table.py p11_left_bandit.py p12_card_game.py p13_near_bandit.py p14_relief_details.py p15_light_edges.py p16_hand_and_crags.py p17_finish.py
  easel export uktarl.easel rebuilt.png
  ```

  About 75 seconds. The look scripts write into `out/`, which is ignored.
- **One thing the rebuild does not have: a landmark.** The painter's file holds three
  landmarks, `candle`, `lantern` and `sun`, and the rebuild two. The first version of
  `p01_draw.py` marked the `sun` at the point the rays leave, which is behind Uktarl's
  head. The version that replaced it no longer marks it, and its `s.unguide()` clears the
  guides but not the landmarks. So every look after it drew `sun` and the guide's own note,
  `Uktarl`, across his forehead and eyes ([`labels_on_the_face.png`](evidence/labels_on_the_face.png)).
  That is half of the verdict's *a label sat right on the 48-px face*: the other half is
  the note.
- **What the tool said**, from the saved reports. At the call: `clean-small` on the
  mountain's first version, `glaze-far` on the lamplight pass, `chisel-pressure` on the
  far crags. After the pass: the stack-of-bars line on 3 of the 20 committed runs and 8
  of the 26 rehearsals; the one-disc line on 7 committed passes and 10 rehearsals; the
  graded-passage line and *took 6 earlier details out of sight* once each, on the near
  bandit's pass; and `landed nothing:` on two rehearsals and one committed pass, for passes
  of a mass outside its clip. The standing lines: `values:` said *no clear light* on all
  43 reports after the first mark; `edges:` read `70%` under 2.5 px after the wall and
  `59%` at the end; `subject:` read `48%` against the planned `30%` after Uktarl's head, a
  share of the marks laid so far, and fell to `28%` as the other figures went down.
- **How the painter read the check.** Its verdict says it stopped reading the habit
  warnings, and its commands show it. Up to the body's first rehearsal it printed the tail of
  every rehearsal. From the body's second rehearsal on, 29 of the 30 `easel run`s it typed
  filtered the output down to the lines it named: the total, `dearest:`, `landed`,
  `subject:`, and, on two passes, the disc line. The near bandit's
  commit printed its tail, and `easel check` printed the closing checklist in full.
- **The verdict's measured claims, re-measured**, in full in
  [`PLAN-0.9.0.md`](../../../PLAN-0.9.0.md), section 3. **Confirmed:** no exclusion and no
  rotation in the shape tools; 43 of the 44 masses held hard, `59%` of edges under 2.5 px,
  two lost; no `--region`, `--no-sketch`, `--no-marks` or `--scale` on `easel run`; the
  collar's 43 strokes against about 10; the 102 marks on Uktarl before the others were
  begun, and 22 on the last figure; the package's 90,369 words; the six coin and card
  marks the near bandit buried; the table top `0.18` under its plan. **Changed shape:**
  of the 28 marks the closing check called discs, 20 are the features of three faces and
  one is a ridge on the relief, 56 pixels from the left bandit's eye; the mountain's 129
  strokes were its ten facets laid across their length, 88 against 31 along it, and not
  the cost of a concave shape; and *no clear light* has the remedy the verdict asks for
  already, `plan(key="low")`, which on this picture would have said *Uktarl's face stands
  clear -- 0.69 at its brightest twentieth against 0.50 for everything else, 0.19 over*
  from the head's pass on. The painter had judged that its picture was not low-key. By the
  check's own test it is: its top twentieth, `0.52`, is under the box's middle, `0.54`.
  No document states that test.
