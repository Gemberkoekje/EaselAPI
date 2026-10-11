# Answers from the painter of The Curator's interim art

*To Questions 1 to 8 (`PLAN-0.9.0.md`'s Q1 to Q8). Written 2026-10-11, in the session that painted the nine pieces.*

**Labels.** **M** I measured it. **O** I observed it, in a file, a log, the documents or an image. **R** I reasoned it. Where a question asks how the tool should behave, my choice comes first, in bold.

**Sources.** The scripts as committed in `the-curator/tools/easel/` (commits `e48ea6f5`, `9ef7e93d`, `76122c4e`); their run logs and stage images in the session's scratch folder; and the evidence manifest on the `easel-evidence` branch (`d7826408`), whose `L` numbers are lines of the session transcript. The measurements made for these answers used easel-paint 0.8.0 on the machine that painted the pieces. Their scripts are in `measurements/` beside this file; the paths in them are this session's.

**What I didn't use.** I didn't re-read the transcript for these answers. An earlier attempt to read it, for the evidence bundle, was stopped by the session's permission system, and I haven't tried again. Where only the transcript could settle a point, such as why I did something or the order of attempts within one piece, I say so. A few points rest on my own notes from earlier in the session; they're marked *(notes)*.

---

## Question 1: transparency

**Both, from one declaration. `s.plan(cut=place)` names the cut once, the checklist reads inside it, and `s.export(path)` writes the alpha from it unless `alpha=` says otherwise. By default the edge falls as a held edge's does. Softening is an option, given as the edge's width in pixels.**

- **R** I'd have used `s.export(path, alpha=place)`. It replaces both of my cut scripts and the bookkeeping between them.
- **O** That bookkeeping is where two declarations drift. The patron and candle scripts write their outlines to `outline.json` for the cut script to read back (`patron_default.py:46`, `candle.py:24`), and `cut_arch.py` types the arch's numbers a second time (960, 400, 260, as in `doorway_wall.py:6`).
- **O** The place I cut along is not the place I laid the paint in. I ran the masses past the outline on purpose, 8 px and 4 px on the patron (`patron_default.py:58–60`) and 3 px on the candle (`candle.py:39–41`), and cut along the outline itself, so the edge never showed bare ground or a brush's end. So `alpha=` has to take a place of its own, as "the places you name" allows. Alpha taken from the masses as laid would keep the spill.
- **M** Edge widths, 10–90% of full alpha or of the value step, measured across the edge:
  - a held edge (`flat`, `edge="hard"`): 0.87 px at the patron's size, 0.81 px at the candle's;
  - my arch cut (drawn at 4×, reduced, no blur): 0.9 px at one jamb, 1.5 px at the other;
  - my softened cuts (the same, then a 0.8 px blur): 2.5 px across the candle's upright side, 3.0 px along a row crossing the patron's sloping side.

  (`held.py`, `edges.py`)
- **O** *(notes)* I blurred to keep the figures from looking cut out of paper. I never compared a blurred cut with an unblurred one in the game, so I have no evidence the blur was better.
- **O** One number points the other way. The checklists put the median painted edge in these pieces at 2.6–3.3 px (the `edges:` line in every log). A held cut is among the hardest edges in its picture, and my softened one sits near the median.
- **R** Still, the held edge should be the default. It is what the tool does at every held edge inside the picture, and it guesses nothing about the scene the sprite will stand in. Softening is that guess, so the painter should make it, in pixels (`soften=2.5`). A blur radius was the wrong unit: I had to measure today to learn that my 0.8 meant 2.5 px.

## Question 2: a warm grey

**`p.grey(value, warmth=…)`, with the fact at `mix()` as the backstop. The recipe alone wouldn't have done it. The stage image showed me the purple; no number did.**

- **M** On my machine the turn is where filing found it. I brought burnt umber with ultramarine to value 0.44. The HSV hue is 17° at 10% ultramarine, 11° at 18%, 0° at 25%, 338° at 30% and 300° at 35%, and chroma falls from 0.025 to 0.011. White mixed in before `at_value` changes nothing: umber with 18% ultramarine comes back `#716361` at value 0.40, with 20% white or without it. The arch stones' 22% white changes nothing either: the same three hexes come back without it. (`hues.py`)
- **O** I thought the white mattered. The arch stones mix in 22% before `at_value` (`doorway_wall.py:61, 69`), and so does the wall's unused `stone` slot, at 20% (`:19`).
- **M** Shipped mixtures still in the turned band, most of them darks:
  - beyond_doorway's `stone`: 25% ultramarine, hue 0°;
  - its `stone_shade`: 30%, 334°;
  - the wall's `plaster_dark`: 25%, 340°;
  - the wall's `joint`: 35%, 276°;
  - the counter's `seam` and the shelves' `shadow`: 30% at value 0.14, 300°, chroma 0.008.
- **O** The only colour numbers I printed were value and chroma (`swatch.py`, `p0.py`), never hue, so no number could have shown me the turn. The swatch didn't show it either; it is where I chose the 25% mix. Its candidate `umber+ultra(0.25)` is the same mixture as beyond_doorway's shipped `stone`, and today it measures as a neutral (chroma 0.013, hue 0°).
- **O** *(notes)* The lavender showed in the stage images (`look()`) of the shelves and the wall. I fixed both by eye, warming the mixes with yellow ochre or burnt sienna; the shipped warm mixes are at `doorway_wall.py:16, 61, 69` and `shelves.py:10`. Later runs overwrote those images, and the scripts were edited in place, so no file shows the purple versions.
- **O** A printed line is not a reliable stop for me. Notices are still standing in the shipped scripts' logs: three in beyond_doorway's, three in the patron's, and one each in the counter's and the desk's (`repro/`, `repaint/`). The cabinet's checklist said its planned light missed by 0.49 (`plan: … D4:E5 -0.49`), and I shipped it.
- **R** A named grey changes what I type, not what I'm told. I mixed by naming pigments and shares and then fixing the value (94 `p.mix` and 62 `p.at_value` calls). `p.grey(0.44, warmth=0.3)` fits that habit and cannot come back violet. The fact at `mix()` costs nothing and catches whoever mixes by hand. A recipe has to be found first: I opened five of RECIPES.md's sections, and none of them was about colour.

## Question 3: how paint lands

**Painting at two to four times the size and exporting at size would have served the small pieces, as long as the export keeps the canvas weave at the exported scale. The table belongs in pixels. And the call that lays a mark under its cliff should say so, because nothing did.**

- **O** The order of the pieces, by the last-modified times of their files:
  - beyond_doorway, 01:52–01:59;
  - desk, 02:05–02:10;
  - counter, 02:11–02:15;
  - shelves, to 02:46;
  - the wall and its arch cut, 02:51–02:54;
  - cabinet, 02:56–02:57;
  - patron and its cut, 02:59–03:00;
  - candle, 04:10–04:12.

  The order of attempts within a piece is in no file, because the scripts were edited in place.
- **O** The calls I fought, and what the shipped scripts settled on:
  - **`block_in` leaving gaps.** The desk and counter got a solid flat base under the planks, so a gap shows a dark seam rather than ground (`desk.py:24`, `counter.py:22`). The patron's bristle masses got `solid=True` and then a flat pass (`patron_default.py:58–60`); its bristle passes still print the solid-comb notice.
  - **`at_value`'s reach.** I used hex near-blacks, "darker than the mixes reach" (`locked_shelf.py:21–22`, `patron_default.py:47–50`, `candle.py:32`).
  - **Thin flat marks.** I changed them to `round_hard` after a notice that a flat that narrow lands nothing *(notes)*.
  - **`press=`.** I tried it to make a stroke land harder. It takes one point only, and no script keeps it *(notes; no `press=` in any script)*.
  - **The candle's shading.** It ended at opacity 0.9, laid twice 1.5 px apart (`candle.py:44–46`), plus a darker edge stroke (`candle.py:47`). **M** *(notes)* On the one row I measured then, the edge pixel went from 214 to 192 and the next from 205 to 198, and the rest of the row moved by one level at most. The earlier version no longer exists.
  - **The budget.** I went over it at least once and raised it *(notes)*. The shipped budgets run from 110 to 460 strokes.
- **O** The shipped scripts show no wider brush for any faint mark, and the files don't say whether I tried one. I enlarged the candle only to look at it: `cand/stage4_big.png` and `cand/rgb_big.png` are exact 2× nearest-neighbour copies. I drew both cut masks at 4×.
- **M** The candle wasn't the only light lost to brush width.
  - The patron's plan says "with the light behind just catching hood and shoulders". I laid that as three `round_hard` rim strokes, 2.5–3.7 px wide, at opacity 0.4–0.7, in a mix at value 0.70. In the shipped figure only 10 pixels pass value 0.40, and its 99.9th percentile is 0.20 (`patron_light.py`). Enlarged, the rim is a few broken flecks on the hood's crown and nothing on the shoulders (`patron_rim.png`).
  - The cabinet's lock is its "one bright note". Its bright edge is a 1.8 px liner at value 0.72, and nothing in the lock's cell passes 0.46 (`cabinet_lock.py`).
- **M** `size` is a fraction of the long side, so the larger numbers made the narrower marks. The candle's thin marks were size 0.004–0.013, which is 1.2–3.9 px. The patron's were 2.5–3.7 px and the shelves' 3.6 px. The desk's and the wall's were size 0.002–0.004, which is 3.8–7.7 px (`widths.py`). On the candle, nothing said a word about a faint mark: not its own run, not `s.report()`, not `easel run --rehearse` (Question 7).
- **M** Painting larger serves. I painted the candle at 4× (480×1200, with only the `Session` line changed) and reduced it to 120×300.
  - The wax top's mean value goes from 0.78 to 0.81, and its 95th percentile from 0.87 to 0.92.
  - The checklist's planned light reads 0.92 at its brightest twentieth, against 0.86, and "2 of 2 places inside 0.10", against "1 of 2".
  - It spends the same 47 strokes, in 12.6 s against 2.1 s.

  (`compare4x.py`, `commands.sh`)
- **O** In the image, the drips at the top read clearly at 4× and only faintly at 1×. The catch: reduced from 4×, the linen weave all but disappears, and the brass base loses the grid it shows at 1× (`candle_1x_vs_4x.png`). A piece painted large would read smoother than its neighbours in the same scene. So `size=` should keep the weave at the exported scale, or at least say what it did to it.
- **R** I'd paint the small pieces larger (the candle, the cabinet, the patron), but not the 1920-wide ones. Their thin marks were already 3.8–7.7 px and mostly meant to be faint (signatures, grain), and painting them larger costs several times the run time.
- **R** The table should be one table, per brush and in pixels, of how many levels one touch moves. It should cover the opacities people use, laid once and twice, solid or not, with the cliff drawn across it: 6.5 px for a round tip, 4 px for an oriented one. Beside it, one line each:
  - `density` is spacing, so it changes nothing on a single stroke;
  - `solid` is load: it keeps a pass from running dry and doesn't make one touch land harder;
  - `press` restamps a one-point mark and does nothing else;
  - under the cliff, change size first, with a wider tip or a larger canvas, before opacity or repeats.

  The pieces exist, but apart: REFERENCE.md's arguments table (lines 126–141), the oriented tip's 4 px (REFERENCE.md line 127; CALIBRATION.md line 496), and the round tip's 6.5 px, which is only in a CALIBRATION.md table (line 3591). None of them is in my canvas's pixels or at the call. What would have made me reach for the right one first is the call itself: "size=0.009 is 2.7 px on this canvas; a round tip lands in one touch from 6.5 px."

## Question 4: a piece that is one layer

**`key="low"`, said plainly where the plan is introduced, and the cut declared in the plan. Not the scene. On a cut-out, keep every line, measured inside the cut, and add one line for the cut's own edge.**

- **O** Six checklists say *no clear light*: the cabinet, the counter, the patron, both shelves and the wall (`repro/`). Three of their plans put the lightest place at 0.40–0.44, under the box's middle (`shelves.py:27`, `counter.py:18`, `doorway_wall.py:24`), and the patron's plan puts it at 0.10. The cabinet's plan puts its lock at 0.6, which didn't land (Question 3), and its `plan:` line says so whatever the key.
- **M** The patron's line is reading the ground that the cut throws away. Inside the cut, its planned light D1:E3 reads 0.16 at its brightest twentieth. My measure of the whole cell gives 0.54 (the checklist says 0.53), and the cut-away's median value is 0.53. So "values: 0.09–0.54 … nothing above 0.54" is reading the bare ground. (`patron_light.py`, `cutaway.py`)
- **M** On the candle, 63.0% of the canvas is cut away, and its checklist, re-run, says 67.14% bare ground. Its values' middle cluster, 0.54, is the cut-away's median value, 0.54. 27% of its planned light D1:E2 is cut away. On the wall, the arch's opening is 19.6% of the canvas and 8% of its planned light. **R** That 27% accounts for most of the candle line's "32% of it darker by more than 0.15".
- **O** *(notes)* I filtered the candle's checklist output and never registered the 67%.
- **R** `key="low"` is one word, and it describes each of these pieces honestly on its own: their light is in another canvas, the doorway beyond or the flame the game draws in code. The cut is what makes the checklist read what ships. Not the scene, though. The game composes the scene with parallax, a light mask and a flame drawn in code (`game/art/layout.json`, and the README's "the candle's flame (still drawn in code)"). A scene declared in Easel would check a picture that never appears on screen.
- **R** On a cut-out, keep every line, measured inside the cut:
  - `ground` above all. Bare ground inside the silhouette is the only bare ground that shows, and measuring it would have checked the margin I painted past the outline instead of leaving it a guess;
  - `values` and `lightest`, which on the patron were reading the ground;
  - `plan`, with its places clipped to the cut;
  - `edges`, plus one more line for the cut's own edge, its width against the picture's median, since the silhouette is the edge every player sees;
  - `boxes`, without "check the background hardest", because a cut-out has none;
  - `bands`, `unspent` and the three questions, with "looked at small" meaning the size the game shows it.

## Question 5: pixels

**A canvas made with pixel coordinates throughout, sizes included. `s.frame` would not have retired `n(x, y)`. `s.px` already exists, and it didn't either.**

- **O** `n(x, y) = (x / W, y / H)` places every point in four scripts (`doorway_wall.py`, `locked_shelf.py`, `patron_default.py`, `candle.py`): boxes, bars, the patron's splines and the candle's body. I computed the rounds among them, the arch, the dish and the face, with cos and sin in pixels inside it (`doorway_wall.py:45–48, 76, 81`, `candle.py:16`, `patron_default.py:63`). `s.frame` would tidy those few lines.
- **O** `s.px(x, y)` is in 0.8.0 and is exactly my `n()`: see REFERENCE.md lines 39–42 and 670, and PAINTER.md line 159, "Where a drawing wants pixels, `s.px(x, y)` is a pixel's place." Line 159 was inside guide lines I printed twice (L1327, L3878), and one of my greps had `s.px` among its patterns (L3890). I defined `n()` four times anyway. The files don't say why; the transcript might.
- **R** Every coordinate in those four scripts came from the game, in pixels: the arch from `layout.json` (`doorway_wall.py:6`), the candle from the placeholder's geometry and the flame point (`candle.py:12–13`), and the patron from its slot. With `s.px` I'd still wrap every point; on a pixel canvas I wouldn't.
- **R** Sizes matter more than points. Sizes in pixels would have shown the candle's problem as I typed it: `size=2.7`, not `0.009`, next to the desk's `size=5.8`. As fractions, both looked thin (Question 3).
- **R** `polygon()` can't take pixels on its own: a polygon doesn't know its canvas, so it would need the session anyway. The canvas is the place to say it once.

## Question 6: geometric subjects

**I didn't open *The one ruled line*. I read *A scene with straight edges*, which gives the right advice, and I didn't carry that advice to my flat-on subjects.**

- **O** My RECIPES.md reads were lines 35–92, 271–301, 572–620, 735–787 and 852–895 (L2848, L2881); the ruled line is at lines 1051–1086. The manifest says I listed the headings (L2844), but whether that list reached line 1051 isn't in my files.
- **O** *A scene with straight edges* (lines 35–92) says what a recipe needs. Thin members are "thickest near the viewer, thinnest far off, and thinned to nothing where they cross the brightest light", and the recipe goes wrong as "a diagram — every line ruled to the same weight". But it is framed for a scene seen at an angle. My slots are flat-on, and I laid the cabinet's grille as two-point strokes of one weight, opacity 0.95, `pressure="even"` (`locked_shelf.py:51, 53`). That is the diagram it warns of.
- **O** No script sets `jitter`. I made the irregularity myself, in pixels:
  - `box()` corners ±1.5 px (`locked_shelf.py:13–16`);
  - bar ends ±1 px and bar spacing ±2 px (`locked_shelf.py:49–53`);
  - the voussoirs' outer radius −4 to +6 px, and the jamb stones ±3 px (`doorway_wall.py:59, 70`);
  - the arch joints as the gaps left between stones (`doorway_wall.py:52`).
- **R** *The one ruled line* answers the opposite question, how to make a line straight, so it wouldn't have helped. A recipe for these subjects needs to say:
  - **A shelf** is three values, not a line. The lit top edge is thin, found near the light and lost away from it, and broken where a book stands forward. Below it come the front face and the shadow under it, which is darker, wider and softer. The shelf's ends sink into the uprights' shadow.
  - **A bar** is a dark with one lit side toward the light, lit along part of its length only. Spacing and angle are off by a pixel or two, and a knot of the darker value sits where bars cross. Its ends are lost into the frame's shadow rather than stopped on a line.
  - **A joint** is the gap where two stones don't meet: the darker value left between masses, not a line drawn over them. It is uneven in width, darkest where the stones turn into shade, and nearly gone where the light is strongest. Each stone is a step off its neighbours.
  - **The amounts in pixels**, at the size the thing is seen (mine were ±1–3 px), and a checklist line naming long edges laid with under half a pixel of wander.

## Question 7: rehearsal

**I had read that they exist, and I didn't use them. Make the tool work my way: print the after-pass check where a self-built script already stops, at `s.look()`.**

- **O** `easel --help` lists `run` and `check` (`venv.log`; printed at L1089). The guide's first page, which is what `easel guide` prints and which I printed in full twice, says "**Rehearse every pass before you pay for it.** … `easel run pass.py --rehearse` does it for a whole script" (its lines 23–25), and it names `report()` (line 97). PAINTER.md's lines 671 (`easel check`) and 747–761 ("The habit here is: rehearse every pass with `--rehearse`") were inside lines I printed (L2831). I called none of them.
- **O** Here is how I worked instead. Every script builds its own seeded `Session`, takes a stage number and gates each pass with `if STAGE >= n:`. Every run ends with `s.look()` (12 calls across the scripts), and at stage 99 with `s.checklist()` and `s.export()`. The README promises that a run at stage 99 writes the shipped PNG again.
- **R** *(reconstructed; my reasons at the time would be in the transcript, if anywhere)*
  - Each run rebuilt the picture from a blank canvas, so nothing a run did survived it, and I never met the cost a rehearsal saves. Every run was already a rehearsal, at 2 s for the candle (measured today).
  - The script was the deliverable, rerunnable to the pixel, so a session file built up by commits would have been a second source of truth.
  - `easel run` takes a session file with `s` already defined (PAINTER.md:747), and my scripts made their own.
- **M** What I missed, tried today on the candle. `easel run candle.easel pass.py --rehearse` takes my script with two lines changed (the `Session` line removed, the stage fixed). Beyond the checklist, it adds one line: "dearest: 19 block_in at pass.py:40, 7 at :38, 5 at :39 -- 31 of the 47". `s.report()` at the end of the candle and the patron repeats the checklist's lines. None of the three mentions the candle's faint drips or the patron's missing rim. (`commands.sh`)
- **R** The documents said it three times and I didn't change course, so a fourth time won't do it. Make the tool meet the script:
  - `s.look()` prints the check on the marks since the last look, including the dearest and wasted calls by line;
  - `easel run` accepts a script that builds its own `Session`;
  - that check includes a notice for faint marks, since no path has one now.

## Question 8: the reference

**No to both. What would have sent me there first is the five-file table, placed at the top of what `easel guide` prints by default.**

- **O** `--reference` is named in `easel guide --help` ("REFERENCE.md instead: units, defaults, every argument") and in REFERENCE.md's own list of commands. `easel --help` says only "guide  print the painting guide that ships with the engine" (`venv.log`). The manifest records no run of `easel guide --help`.
- **O** The one line saying REFERENCE.md holds "every fact on one page: units, defaults, what each argument does" is PAINTER.md line 15, in the five-file table. `easel guide` with no flags prints lines 28–146, byte for byte (`commands.sh`), so the table isn't in it. Its last paragraph mentions "the other four files" without naming them. Lines 1–27 are the only lines of the guide I never printed: of my recorded greps over its opening, only line 1 matches.
- **O** I knew the file existed. It was in my listing of `easel/docs` (L1323, L2838), and I grepped it once, for "direction" (L2885). The links to it that I read point at sections (the plan, the report table, the shell), not at units and defaults. Its first section, *Units, which is where the surprises are*, holds the two facts behind Questions 3 and 5: `size` as a fraction of the long side, and `s.px`.
- **O** When I needed an argument, I went to the code: `inspect.signature` on `ribbon`, `polygon`, `Session.block_in` and `Session.stroke` (L3890), and `catmull_rom`'s docstring (L4003).
- **R** In order:
  1. the table at the top of the default `easel guide`, the page I read first and in full;
  2. a line in the docstrings of `Session`, `block_in` and `stroke`, "units and defaults: `easel guide --reference`", because that is where I actually looked;
  3. the flags, on `easel --help`'s line for `guide`.

  A notice that a mark is under its cliff could end with the same pointer.
