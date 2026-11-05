# Answers after the bench, from the painter of The Curator's interim art

*To the five questions of 2026-11-05, the plan's section 6, After the bench (step 2b). Written 2026-11-05, in the session that painted the nine pieces.*

**Labels**, as before. **M** I measured it. **O** I observed it, in a file, a log, the documents or an image. **R** I reasoned it. Where a question asks how the tool should behave, my choice comes first, in bold.

**Sources.** The scripts as committed in `the-curator/tools/easel/`; the owner's `alpha.png` and `deposit.png`; and easel-paint 0.8.0, the install that painted the pieces. Every **M** below was measured today with the scripts in `measurements-step2/` beside this file; the paths in them are this session's. Where my numbers differ from the bench's, I say how. None of these answers needed the session transcript.

---

## 1. The cut's edge, again

**(b), built from (a)'s parts. The places' coverage at 4×4 samples, softened by default to 0.85 px, the width of a held paint edge. `soften=` takes the 10–90% width in pixels, and the engine solves the sigma; `soften=0` gives the raw coverage.**

- **O** In `alpha.png` the places as a hold step visibly: a staircase down the patron's shoulder over the light ground, and stepped corners on the candle's top over the dark one. My shipped cut and the 2.5 px one have no steps, but over the dark ground the candle's top reads out of focus beside the crisp marks inside it.
- **M** I rebuilt the cut from the places, with sample points at sub-pixel centres, and measured it the `edges.py` way (`cut_edges.py`):

  | piece | shipped | hold 2×2 | hold 4×4 | sigma for 0.85 px | sigma for 2.5 px |
  |---|---|---|---|---|---|
  | the doorway wall | 0.66 | 0.35 | 0.43 | 0.49 | 1.14 |
  | the patron | 2.21 | 0.61 | 0.75 | 0.39 | 0.94 |
  | the candle | 2.10 | 0.21 | 0.25 | 0.49 | 1.21 |

  Each row is proportional to the bench's. My outline lengths come from the coverage's gradient and run 3 to 22% longer than the bench's, so compare within a row. The share kept moves by 0.24% of the canvas at most.
- **O** At 8× (`alpha_085_close.png`), 4×4 coverage still shows the staircase on the patron's shoulder and the stepped corner on the candle. At 0.85 px the steps are gone, and the edge stays as crisp as the marks beside it. At 2.5 px and in my shipped cut the edge is soft. `alpha_085.png` shows all five edges over both grounds.
- **R** A held paint edge measured 0.81–0.87 px (`held.py`, in the first round). That is the hardest edge the paint makes. A cut harder than that is the one edge in the picture the paint couldn't have made. That reads as cut paper, and on slopes and curves it steps.
- **R** My first-round reason for the held edge still holds. What the bench showed is that the hold's mask isn't that edge: the default has to be the paint's edge, not the mask's. At 0.85 px it looks right without a parameter, which matters because most painters won't set one.
- **R** Build the alpha at the size that ships. With `s.export(path, size=…)` (Question 2), the 0.85 px should hold at the exported size, not on the larger canvas.

## 2. A piece painted large and exported small

**(a). The sentence where `size=` is documented should say how much the marks' texture smooths, and that the smallest factor that lands the marks is the one to use. The word about a faint mark (Question 3) should name that factor.**

- **M** You're right, and my first-round attribution was wrong. Painted on a smooth canvas, the candle has the same 1× texture as on linen, and it looks the same (`texture_sheet.png`). On the base's middle (0.7 px high-pass) it is 3.95 levels on linen against 4.00 on smooth; on the wax, 1.52 against 1.52. I had put the lost grid down to the weave by eye, without measuring, so the condition I attached to (a) falls.
- **M** Over stretches no hand-laid stroke crosses, the 0.7 px texture runs (`texture.py`):

  | painted at | the base's middle | the wax, between the shade and the lit face |
  |---|---|---|
  | 1× | 3.95 | 1.52 |
  | 2× | 1.68 | 0.87 |
  | 4× | 1.50 | 0.26 |

  So most of the base's texture goes at 2× already, while the wax keeps more at 2× than at 4×. Over the whole base and wax, the measure rises at 4× instead. I put that down to the strokes laid over them landing; the base's highlight at line 58 is one of them.
- **M** At 2× the candle reaches what the bench found: plan 2 of 2 and brightest twentieth 0.90, in 3.9 s against 2.1 s at 1×. Read inside the cut, the planned light's median is 0.79 at 1× (0.11 under the plan's 0.90), and 0.81 at 2× and at 4× (`plan_in_cut.py`).
- **O** In `deposit.png` the 2× reductions look like the 1× candle with its marks landed: the drips, the base's highlight, the shade down the left. The 4× ones are smoother, and the wax is nearly flat. I can't tell the Lanczos reductions from the box means.
- **R** (b) isn't a fix for the marks that have to stay thin. A wider tip, at the 6.5 px a round tip needs, would make the grille's 1.8 px glint nearly as wide as its 7.4 px bar, a 2.2 px gilt band three times as thick, and the lock's bright edge a fifth of its 36 px plate. The subject sets those widths, and at the sprite's size they're under the cliff. A larger canvas is the fix. Without `size=`, the painter has to reduce the picture and its cut by hand, as I did with PIL for my cut masks.
- **R** So the sentence should say three things: the marks' finest texture reduces with the picture; by how much (the base above drops to less than half at 2×); and the smallest factor that lands the marks is the one to use. And the word about a faint mark should name that factor: "1.8 px; on this canvas at 4× it is 7.2 px, over the 6.5 px a round tip lands from in one touch."
- **R** The plan should know the size that ships, so that the lines measured in pixels read at that size. Painted at 4×, the candle's checklist put its median edge at 2.3 px (first round, `q2/candle4x/run.log`), and an edge that wide on the 4× canvas is under a pixel at 120×300.

## 3. A word at the call, and a word after

**(b), O3 alone, at a distance of 0.15 and a reach of 0.25, skipping marks noted as a signature. Read it in both places: at `s.look()` over the marks since the last look, and after a pass in `easel run`. Give one line per script line. When the mark is under its one-touch width, M2's numbers are its reason, and Question 2's factor is its fix. Not M2 at the call, either alone or once per size.**

- **M** I replayed my nine pieces and read every stroke the scripts lay by hand as both candidates read them (`run_o3.py`): 176 strokes, or 167 without the signatures, which is the bench's count. My reading reproduces the bench's wherever they meet:
  - the patron's rim reaches 0.09–0.13 of the way;
  - the lock's edge reaches 0.11, and the grille's four liners 0.06–0.10;
  - the candle's wax-light strokes reach 0.21–0.54, the drips among them 0.32–0.45, so O3 stays silent on them;
  - the bookcases fire on 32 of 42 and 19 of 27.
- **M** I sorted each stroke line by what the comment above it says the stroke is for (`intent.py`). 19 marks meant to read didn't land: each moved its pixels under a quarter of the way to a colour at least 0.15 off. They are:
  - the patron's rim (3);
  - the lock's bright edge (1) and the grille's glints (4);
  - the shelves' lit front edges (8);
  - the wall's jamb rims (2);
  - the candle's line 58 (1). Line 58 is the base's right shoulder catching the flame (`brass_lit`), not a shade, so it is a fourth lost light.
- **M** The candidates on those 176 strokes (`tally.py`):

  | candidate | speaks | the 19 lost | landed, meant to read | gilt (53) | grain lines | signatures | script lines |
  |---|---|---|---|---|---|---|---|
  | M2 at the call | 96 | 19 | 11 | 53 | 4 | 9 | 33 |
  | M2 once per brush and width | 20 | 7 | 5 | 2 | 1 | 5 | 20 |
  | O3 0.10 / 0.25 (and one broad pass) | 68 | 19 | 2 | 44 | 1 | 1 | 18 |
  | O3 0.15 / 0.15 | 33 | 13 | 0 | 19 | 0 | 1 | 12 |
  | **O3 0.15 / 0.25** | **64** | **19** | **0** | **44** | **0** | **1** | **14** |
  | O3 0.15 / 0.35 | 79 | 19 | 3 | 53 | 2 | 2 | 20 |
  | O3 0.25 / 0.25 | 55 | 11 | 0 | 44 | 0 | 0 | 11 |
  | O3 0.15 / 0.25, no signatures | 63 | 19 | 0 | 44 | 0 | 0 | 13 |
- **O** The gilt is "faded gilt: small, few, varied" (`shelves.py:79`). Enlarged 4×, it reads as thin, faint gold lines (`shelf_marks.png`); at the size the game shows it, I'd call it barely there. I meant faded, not gone, so I'd have wanted to be told, and I might have kept some.
- **M** On the 1920-wide pieces, M2 speaks 9 times: on 4 grain lines and 3 signatures, all meant faint, and on the wall's two jamb rims. O3 speaks only on the jamb rims, which were meant to read at the crown and reach 0.12–0.17. So on those pieces M2 speaks mostly on marks meant faint, as the bench expected, and O3 doesn't.
- **M** Every one of the 64 O3 firings on my pieces is under its one-touch width, so all 64 are M2 marks too. Across the corpus only 161 of O3's 327 are, so the reason line has to come from the mark itself.
- **R** Why O3, at those numbers:
  - It speaks on all 19 lost marks, and on no mark that landed. Its one false alarm is the candle's signature, which a note already names.
  - A reach of 0.15 loses six of the 19: the left shelves' edges at 0.17–0.19, a jamb rim at 0.17, the base's highlight at 0.15.
  - A distance of 0.25 loses the eight shelf edges, whose colour lies only 0.18–0.20 off.
  - M2 at the call speaks on all 19 too, but also on every gilt stroke and on 24 more: 11 marks that landed and 13 meant faint. Said at every call, it would become what I learned to read past in the first round: notices left standing in the shipped logs.
- **R** Where: both places. `s.look()` is where every run of mine stopped (12 calls across the scripts), and the end of a pass is where an `easel run` painter stops. Group it by script line, as the checklist's *laid at* lines are: on my pieces, with signatures skipped, 63 marks become 13 lines.
- **R** The candle's wax light is the one shortfall O3 doesn't name, and the plan's line does. Read inside the cut, the planned light's median is 0.79 at 1×, 0.11 under the plan, and within 0.10 at 2×. That division seems right to me: O3 for a mark that didn't land, the plan for a light that landed short.

## 4. The ground line on a cut-out

**Drop the floor inside a cut, as (a) says, but not on (a)'s premise. Inside a cut, the line should count canvas with nothing laid on it, not paint the colour of the ground, and say how much of that lies along the cut's edge. The cut's own edge: yes, that is the line as I meant it. Beside the median, give the picture's hardest edges.**

- **M** The line's measure (`Canvas.ground_showing`) counts every pixel within its tolerance of the bare ground's colour, painted or not (`ground_in_cut.py`). By that measure the wall's cut is 5.30% ground, but only 0.28% of the cut has no paint on it (paint thickness 0). Along the arch's edge, within 2 px, it is 30.98% against 0.29%: nearly a third of that band is paint, the arch's stones and joints, whose colour sits within the line's tolerance of the umber wash. So inside a cut, "bare ground is only ever a fault" would call the wall's stones a fault.
- **M** Counted as canvas with nothing laid on it, my margins held. Inside the patron's cut it is 0.00%, and 0.00% along its edge. Inside the candle's it is 0.01%, and 0.07% along its edge, about one pixel. That is the check I asked for in the first round: an unpainted count along the edge measures the margin I guessed at.
- **R** So inside a cut, the line should have no floor. It should give the share of the canvas with nothing laid, and the part of it within 2 px of the cut's edge, where it would show as a fringe in the ground's colour around the sprite. On a whole picture, the present line asks the painter's question, whether the ground's tone shows, and can stay as it is.
- **R** Against the median, the cut's own edge will always read hard, because the median takes in edges meant to be soft. So give one more number beside it, the picture's hardest tenth, and say a word only when the cut is harder than that: then the silhouette is harder than any edge the paint made. With Question 1's 0.85 px default, the cut would sit at a held paint edge, 0.81–0.87 px in my measure.

## 5. The fact at `mix()`

**(a) and (c): `p.grey()`, and the hue printed beside value and chroma wherever the palette prints colour numbers, with the turn said there. No fact at `mix()`.**

- **M** The hue a mixture turns to depends on the value `at_value` gives it, and `mix()` comes before that (`swatches.py`).
  - As mixed, the mixtures sit at value 0.13. At value 0.14 my Oklab numbers agree with the bench's: umber 39.2°, ultramarine 268.1°; 18% ultramarine 18°, 25% 356°, 30% 326°, 35% 308°.
  - At value 0.44, where my stones were, the same mixtures run 32°, 17.5°, 353° and 326°. There the 25% has turned only 22° from umber.
- **O** Each mixture beside a neutral of the same value (`umber_ultramarine_vs_neutral.png`):
  - at values 0.14 and 0.18, every mixture reads as a near-black, and the 30% and 35% as cool ones;
  - at 0.34 and 0.44, the 18% reads brown, the 25% and 30% mauve, and the 35% lilac.

  So the violet shows at mid values, where the turn measured as hue is smallest, and hides in the darks, where it is largest.
- **R** So the fact, worded either way, speaks where the violet hides and misses where it shows. On my pieces it would catch the counter's seam, the shelves' shadow, the wall's joint and the locked case's 40%, all darks. It would also catch beyond_doorway's `stone_shade`, the same 30% mixture at value 0.34, where it does read mauve. It misses the 25% `stone` at 0.44, which reads mauve too.
- **R** Said once per mixture (b), it would speak in six of my nine paintings, five times about a dark. Umber with ultramarine is the standard chromatic black of oil painting, and I'd expect most of the corpus's 30–55% darks to be wanted.
- **O** I'd have seen the hue in the swatch I printed myself, which showed value and chroma (`swatch.py`, in the first round). A hue there would have shown 17.5° against umber's 39°, on request, at the moment I was choosing.
- **R** `p.grey()` is what would have kept the stones brown. The grey I wanted reads like the 18% at 0.44: brown, around 30° in Oklab. My fixes warmed it with ochre and sienna (`doorway_wall.py:16, 61`, `shelves.py:10`). Name `p.grey()` where the guide first mixes a colour.
- **R** If a backstop is wanted later, hang it on `at_value`, which knows the value, and keep it to mid and light values. Bench it before building it.
