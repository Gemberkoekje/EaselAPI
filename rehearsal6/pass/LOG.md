# Log

Three paintings, one guide, no source.

| | session | strokes | canvas | ground |
|---|---|---|---|---|
| copy | `copy.easel` | **292** | 1024×768 linen | `umber_wash` |
| own 1 | `own1.easel` | **204** | 1000×640 rough | `cool_grey` |
| own 2 | `own2.easel` | **157** | 640×900 smooth | `umber_wash` |

Final `compare()` on the copy: **0 of 64 cells more than 0.10 out; largest 0.10.**

Records kept: `out_copy/`, `out_own1/`, `out_own2/` (looks, previews, rehearsals,
heat maps). `probe/` holds a throwaway session I used to read the reference on a
flat canvas.

---

## Stage 1 — the copy

### What I did

**Read the photograph before touching the canvas.** I ran `compare()` on an empty
canvas first, as the guide says, and it changed the whole plan. The picture is a
white mug on a light wood table — my eye said *light subject, mid ground*. The
numbers said the reference's cell means run 0.06 to 0.58, that the D column from
rows 2 to 6 is nearly black, and that **no cell in the picture is dominated by the
mug's white**, because the white is always cut by the tea, the printed figure or
the shadow. That is not what the photograph looks like. It is what it measures.

**Chose the ground from the numbers.** I made seven throwaway sessions, one per
ground, and read each one's value off `compare`'s canvas column: white 0.96,
warm_white 0.93, toned_grey 0.53, toned_warm_grey 0.54, cool_grey 0.54,
burnt_sienna 0.46, **umber_wash 0.42** (`#7A6A57`). The table's mean is about 0.42
and it is warm. On the bare `umber_wash` ground, 45 of the 64 cells were already
within 0.10 of the reference. That one decision did more for the score than any
fifty strokes I laid afterwards.

**Order:** dark beyond the table's far edge → table masses → cast shadow →
landmarks and pencil → mug body → back rim → tea → near lip → shade band → handle
→ printed figure → spoon → tag, string, accents.

Eight landmarks, each read off a `grid="fine"` crop of a single cell and checked on
both panels: `rim_l` (0.288, 0.250), `rim_t` (0.485, 0.111), `rim_r` (0.632, 0.215),
`lip_f` (0.469, 0.333), `base_l` (0.366, 0.662), `base_f` (0.450, 0.676),
`base_r` (0.550, 0.650), `hand_o` (0.731, 0.262). The pencil went down after the
table and the shadow and under everything else, and it is buried nearly everywhere
it should be.

I did **not** call `sketch()`, `ref_shape()`, `ref_outline()` or `prepare()`. Every
outline in the painting is a polygon I typed from numbers I read off the fine grid.

**The measurement that saved the copy.** `compare(region=cell("D3"))` said the mug's
front wall immediately under the lip reads **0.22–0.34** — nearly as dark as the
shadow. I did not believe it; the crop looked like pale porcelain to me. I checked
the tenth-grid indexing against two cells whose contents I already knew (the spoon
in E1, the diagonal table edge in H1), confirmed the table is `(column, row)`, then
looked at `cell("D3")` blown up on its own. The numbers were right: the rim
overhangs and throws a hard band of shade across the whole front of the mug. It is
the strongest value event on the object and I would have painted straight past it.

### The last ten strokes

They were, in order (log entries #296–#305, before the signature at #306):

1. **visor** — the pale lens on the printed figure, `round_hard` 0.022, swell.
2. **visor light** — the lighter core inside it, `round_hard` 0.011.
3. **rim light** — the thin bright run along the top-left rim, `liner` 0.008 with a
   hand-written pressure list so it lands light, presses, and lifts.
4. **lip accent** — the one bright touch where the light catches the near lip.
5. **tag** — the tea bag's label lying on the table, `flat` with the blade pinned
   at 62° so it reads as a card and not as a smear.
6. **tag label** — a three-stamp `dab` for the white printed corner.
7. **string** — rim to tag, `liner` 0.005.
8. **hair** — the stray thread lying across the table, `liner` 0.004, pressure
   `[0.2, 1.0, 0.3]` so it appears and disappears.
9. **smudge, lose shadow edge** — the shadow's lower-left boundary given away.
10. **smudge, lose mug edge** — the mug's left silhouette lost into the table at one
    point, so not every edge in the picture is found.

None of them is a value correction. I finished all of those at #294 and checked
`compare()` came back clean before starting. Two are the mark that makes the motif
readable, two are edges deliberately thrown away, four are the small incidents in
the photograph I actually like (the tag, its label, its string, the stray hair), and
two are the highlights.

**The signature counts against `stroke_count`.** The guide says up to five
signature marks "do not come out of your stroke budget, so long as each one carries
`note='signature'`". Mine carried the note and `stroke_count` still went 291 → 292.
So the exemption is bookkeeping for a human reader, not for the counter. It did not
cost me anything here, but somebody planning to 299 will lose.

### The signature

A tick: down-right, then a longer stroke up-right, one `liner` mark, in a colour
within 0.03 of whatever it sits on. Bottom-left corner on the copy, bottom-left on
own1, low right on own2. I chose it because it is the smallest mark that is
obviously *deliberate* — two strokes' worth of intention in one stroke — and
because it is what a hand does when it wants to say "done" and nothing else. It is
not initials, because I do not have any, and a monogram I had invented for the
occasion would have been a costume. Close in value so it sits in the paint rather
than on it.

---

## Marks I tried and rejected

Every one of these is a real file in `out_copy/` or `out_own1/`.

**`out_copy/rehearse_004.png` — dry-brush cross to break the table's ribbing.**
`bristle`, size 0.10, `load=0.5`, `wood_hi`, three long diagonals at ~34°.
*Rejected:* it laid a speckled film that reads as noise, not as wood. Exactly the
failure CALIBRATION describes — "a pass laid at 0.5 because it sounded painterly
leaves a speckled film that everything after it sits on".

**`out_copy/rehearse_006.png` — the same paths with `round_hard` 0.11, `load=0.7`.**
*Rejected:* three fat soft-ended bars that obliterated the whole right field. A
round tip at that size is a capsule, not a scumble.

**`out_copy/rehearse_007.png` — `flat` 0.14 at `opacity=0.16` in `wood_lit`.**
*Rejected:* almost no change at all, and what change there was went the wrong way —
it lightened cells that already needed darkening.

**`out_copy/rehearse_008.png` — `flat` 0.15 at `opacity=0.20` in `wood_mid`.**
*Kept.* It knocked the light swathe back, crossed the ribbing, and darkened the
right-hand cells I needed down. This is pass 2.

**`out_copy/preview_029.png` — two candidate paths for the near lip, `lipA` and
`lipB`.** Previewed over the reference. *`lipB` rejected:* it rides above the rim
band on the left third — it would have put the mug's brightest passage on the tea.
`lipA` is what I painted.

**`out_copy/rehearse_041.png` — visor as `round_hard` at size 0.030.**
*Rejected:* too fat. It swallows the head and the lens stops being a lens.

**`out_copy/rehearse_042.png` — visor as `flat` at 0.022.** *Rejected without
argument:* a short flat stroke is a rectangle. A visor is not a rectangle.

**`out_copy/rehearse_043.png` — `round_hard` 0.022 plus a `mug_hi` core at 0.011.**
*Kept.* This is the pair of marks that makes the whole figure legible. Before it,
the figure was a brown lozenge.

**`out_own1/rehearse_009.png` — rain as four glazes at `opacity` 0.08–0.13.**
*Rejected:* invisible. Glaze is genuinely thin, which is what it is for, and
therefore useless for a veil you want to see.

**`out_own1/rehearse_010.png` — the same paths as `bristle`, `load=1.0`,
`opacity≈0.22`, `lift_off`.** *Kept.* The bristle comb *is* rain: parallel streaks
fading downward. The right tool was the one whose defect matched the subject.

**One scrape.** In own1 I laid five "veils" as `round_hard` at `pressure="even"` and
got five hard-ended cylinders standing in the sky like columns, plus two yellow
sticks and three pale ribbons on the water. Thirteen strokes. I used `undo(13)` —
the only undo in the session — and then rehearsed properly, which is what I should
have done first. The guide is right that undo is scraping; it is also right that
this is what scraping is for.

Previews that cost nothing and changed what I painted: `out_copy/preview_026.png`
(the mug silhouette before blocking it in), `out_copy/preview_032.png` (the figure's
silhouette), `out_own1/preview_005.png` (the cloud base before sweeping it).

---

## What the guide got right

- **"Look every 5 to 15 strokes."** Every disaster in this session happened inside a
  pass I wrote whole and didn't look at until the end.
- **Toned ground.** See above. It was the single highest-leverage instruction in the
  document.
- **`compare()` once on the empty canvas.** The reference column is the photograph's
  value map in numbers and it contradicted my eye twice, both times decisively.
- **Back to front.** The mug's left silhouette is a real edge because the table went
  down first and I laid table colour *back up to* where the mug stops. Every edge I
  tried to make by drawing a line along it failed and had to be buried — see below.
- **"A bristle stroke is never solid."** This one sentence explains three separate
  failures I had to diagnose the slow way: the printed figure reading +0.16 too
  light at `density=1.0`, orange specks that four bristle passes at `opacity=0.9`
  would not cover, and a sea that stayed streaky however many passes I put on it.
- **"`opacity` does not thin a long stroke."** I read it, believed it, and then in
  own2 laid a 900-pixel stroke of `spill` at `opacity=0.16` as "halation" and turned
  the entire white light column orange. The warning is correct and I earned it.
- **"You cannot reason in pixels."** Every time I located something by eye off a
  look PNG I was out by 0.1–0.2 of the canvas. I "repaired" three virga bars in
  own1 at y 0.25 when they were at y 0.45, and made a fresh mess in clean sky.
  `look(grid=True)` fixed it in one call. I should have reached for it every time
  and instead reached for it after the third failure.
- **`rehearse()` before an expensive mark.** The visor. Two free rehearsals decided
  whether the copy's subject was recognisable.
- **Values carry a copy.** `copy_final.png` is crude — blocky, stepped, patchy — and
  it still reads as the photograph with the photograph covered up, because the value
  map is right.

## What it got wrong, or left out

- **The signature exemption is not real** at the level of `stroke_count`. Stated
  above.
- **`block_in` on a `ribbon` is not costed by its width.** I budgeted 4 passes for
  the near-lip band (a ribbon 0.029 wide, `size=0.015`, `density=0.95`) and paid
  **21**. The guide's rule — "the passes are counted across the mass, not over its
  area", "a shaped mass costs what its box costs" — is true of a blob and badly
  wrong for a long curved ribbon, whose box is enormous compared to its width. That
  single call ate 7% of my budget and I nearly ran out of strokes for the handle.
  CALIBRATION should carry a ribbon in its table.
- **There is no advice on how to bury something**, and it is the thing I needed
  most. "When something is wrong, paint over it" — with what? A `bristle` at
  `opacity=0.9` does not bury (the comb leaves the old paint showing between
  streaks). A `flat` buries and leaves a rectangle with chisel ends. A `round_hard`
  buries and leaves a capsule with rounded ends. The answer I arrived at, after
  about fifteen wasted strokes across three paintings, is: **a long stroke, solid
  tip, `load=1.0`, full opacity, run along the grain of what is already there so
  its own ends fall outside the area you are fixing.** That belongs in the guide.
- **The brush table needs the converse warnings.** It says "small accents want
  `round_hard`" and "`flat` and `knife` want a length". It does not say that a short
  or medium `round_hard` stroke is a *capsule* — a lozenge with two rounded ends —
  which is exactly as much of a tell as a flat's rectangle. I made a dozen capsules
  before I stopped.
- **`smudge` did not behave.** CALIBRATION says 0.035–0.045 is the safe window. I
  used 0.032–0.042 six times on light/dark boundaries and got a visible pale
  thumbprint every time — it pulls the light mass into the dark one exactly as
  documented, but the *shape* of what it pulls is a finger-lobe, not a softened
  edge. Where it worked was running *along* a boundary, not across it. The guide
  demonstrates it across (`s.smudge([(0.3,0.4),(0.45,0.44)])` to soften an edge) and
  that is the usage that failed.
- **A cool mass on a warm ground reads two steps lighter than it measures.** I
  concluded three times that the mug was far too light, and `compare()` said it was
  within 0.05 each time. "Compare values, not colours" covers this in principle;
  the specific trap deserves a sentence, because the error is large and consistent
  and it makes you want to darken something that is already right.
- **Units on a non-square canvas.** `size` is a fraction of the long side while
  y-coordinates are normalised over the short side, so `block_in`'s overhang spills
  a *different number* vertically than horizontally. CALIBRATION spells this out for
  `sweep`'s `depth` and not for `block_in`'s overhang, and I lost a horizon to it in
  own1 — a water mass I placed at y 0.735 came up to y 0.66.
- **The two closing rules pull against each other on a scored copy.** "Spend the
  last third of your strokes on what is around the thing you measured" and "your
  last ten may not be value corrections" are both good; but every near mass I laid
  on top knocked a cell back out of tolerance, so my last third really was mostly
  corrections and I had to finish the correcting early and deliberately to protect
  the last ten. The guide does not say which rule wins, and it should.
- Small things I could not resolve from the guide: what compass words `sweep`'s
  `into=` accepts (I guessed `"up"`); whether `blob` takes two radii positionally
  (the guide shows it both ways and I guessed `rx, ry`); whether `overhang=0` does
  anything on a shape, which already defaults to 0.

---

## The paintings, honestly

### `copy_final.png` — 292 strokes

**Works:** the value map. Zero cells out, the greyscale comparison holds up, and
covered up the reference it still reads as a mug of black tea with a spoon in it on
a sunlit table with a heavy shadow. The ground standing in for the table is the best
decision I made. The cast shadow has weight and a soft outer edge. The handle reads,
including its hole, and the tag and string are the two marks that make it *that*
photograph rather than a mug.

**Doesn't work:** the mug is a patchwork of blue-grey rectangles with stepped edges.
I laid it `flat` at 87° and never resolved the passes into a surface; you can count
them. The foot is a light *bar*, not the rim of a base — I broke its two square ends
and it is still a bar. The tea's silhouette is lumpy where I finished it with a
round tip. The printed figure is a warm brown lozenge that only becomes a crewmate
because of two strokes at the very end. The table's right half still shows the
bristle ribbing from pass 1 under everything, and there are two pale lumps near the
handle's shadow that I painted over twice and never killed. There is essentially no
deliberate lost edge except the one I spent stroke #305 on. Pencil is visible around
the handle's hole where I did not intend it.

If I painted it again I would lay the mug with a round tip and half the number of
value zones, and spend the twenty strokes I wasted on the table's surface on the
mug's form instead.

### `own1_final.png` — 204 strokes. A squall over open water.

**Structure:** horizontal bands — cloud, a gap of light on the horizon, sea — cut by
one dominant diagonal falling from the upper left, with the focal point (a boat,
four strokes) small and off to the right third. Deep space, atmospheric, landscape
format.

**Works:** the value structure, the warm gap against the cold sea, and the rain,
which reads because I finally used the tool whose defect matched the subject. The
boat gives the whole thing scale and is the only reason the sea looks big.

**Doesn't work:** it is a marine cliché and I knew that when I chose it. The sea is
muddy and horizontally ribbed. The light band still has a slab-like top edge that I
attacked three times and never really lost. There is a pale lump at about
(0.57, 0.55) from a stroke I mis-placed and half-removed. The one surviving virga
bar reads as a smear rather than as falling rain. And I spent thirteen strokes on
cylinders that had to be scraped. Competent and forgettable.

### `own2_final.png` — 157 strokes. Light under a door ajar, at night.

**Structure, and this is deliberate:** everything own1 is not. Portrait instead of
landscape. Axial and near-symmetric instead of diagonal. Radiating from one point on
the centre line — the foot of the door — instead of receding into depth. Shallow
space with no horizon at all. The subject is cropped by the top and the bottom
edges. And there is no small focal object: the light *is* the subject, and the
composition is one vertical against one horizontal fan.

**Works:** it is the one I would keep. The pool spreading across the floor is the
best passage I painted in the whole session — it radiates, it is warm against a cold
wall, and its outer boundary dies away instead of stopping. The value range is the
widest of the three (0.15 wall against 0.93 light) and the picture is about that
gap. The complementary warm/cool does the work the guide promises it will.

**Doesn't work:** there is a mottled scar across the top third of the light column
where I ran a "repair" straight through it and then half-removed it — I can see the
bar, and a viewer will read it as damage. The wall is under-worked: a flat blue-grey
with four marks on it, and it does not read as plaster or as anything. The column's
dithered edge is an accident of laying a light colour over a dark one on a smooth
ground; I decided to like it, which is not the same as choosing it. The symmetry is
close to dead — I broke it in the last pass and only just. And I signed it twice,
because the first signature landed on the lit pool where the guide explicitly says
not to put it; the second is on the wall at the right, close in value.

---

## Every moment I wanted the source, and what I wanted to know

1. **`block_in` on a curved `ribbon` cost 21 passes where I had budgeted 4.** I
   wanted the actual pass-counting rule for a shape whose bounding box is far larger
   than the mass's own width.
2. **Is the sub-cell `compare()` table indexed `(column, row)` or `(row, column)`?**
   I spent four calls cross-checking against two cells whose contents I already knew
   in order to be sure. One docstring line.
3. **What does `sweep`'s `into=` accept?** I guessed `"up"` because the guide's
   example uses `"down"`. It worked. I still do not know the vocabulary.
4. **Does `blob(place, rx, ry, ...)` take two radii positionally?** The guide shows
   `blob(place, radius, wobble=, seed=)` in the shapes list and
   `blob(point, 0.16, 0.30, wobble=, seed=)` in exercise 8. I guessed `rx, ry`.
5. **Why does a mark with `note="signature"` still increment `stroke_count`?**
6. **What is `block_in`'s overhang in *y* on a non-square canvas?** `size` is against
   the long side and y is normalised against the short one; I wanted the conversion
   rather than discovering it by losing a horizon.
7. **Does `overhang=0` do anything to a shape**, whose default the guide says is
   already 0?
8. **Do `dab()` and `smudge()` accept `note=`?** I passed it, nothing complained,
   and the log shows notes on the smudges — but I only learned that afterwards.
9. **What value is each ground?** I built seven sessions and measured them with
   `compare()` because the guide names the grounds and neither file gives their
   values. That is a seven-row table that would have saved me ten minutes and is
   exactly the kind of thing CALIBRATION already does for pigments.
10. **What produces the dithered speckle** when a light colour goes over a dark one
    at full load on `smooth` — tooth, wetness, or dab quantisation? It defines the
    look of own2's light column and I could not tell whether I was choosing it.
11. **What is `smudge`'s kernel and how does it pick its direction?** Mine left
    finger-lobes on every boundary and I wanted to know whether that is the tool or
    my usage. (I now think it is my usage — across, not along — but I found that out
    by ruining six edges.)
12. **Is `angle=` on a pinned blade measured clockwise from horizontal**, like
    `block_in`'s `direction=`? I used `angle=62` on the tea tag and it looked right,
    which is not the same as knowing.
13. **Does `preview()` accept a bare shape as well as a stroke list, with a
    `reference=`?** The guide shows `s.preview(shape)` alone and
    `s.preview(plan, reference=...)` and I wanted to combine them. It worked.

I did not open any of it. Everything above was settled by writing code, running it,
and looking at the picture — which, when it worked, worked much better than reading
would have. The two things I learned that no documentation would have taught me are
that a bristle brush cannot bury anything, and that my eye is reliably wrong about
where a mark is on a canvas and reliably wrong about how light a cool colour is. The
grid and `compare()` fix both, and the whole discipline of this engine is just
remembering to use them before the mark instead of after it.
