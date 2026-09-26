# Answers to the questions after filing

*From the painter, 2026-09-26. Each **M** was measured today on Easel 0.7.0 from
`bell.easel`. The probes replay the log to just before the thing measured, then lay it
again from its own log record on two throwaway copies (`s.scratch()`) with the same seeds,
so the one difference between the copies is the one thing changed. Each **O** is what my
session shows I saw at the time, with the transcript's timestamp (UTC, 2026-09-25). Each
**R** is reasoning.*

## The two findings

Both are right, and there is a third of the same kind.

- **The 0.52.** At 14:49:13 my session guessed wet paint (*highlights are blending into
  still-wet shade beneath them*) and added the two `dry()`s. At 14:49:50, after the third
  rehearsal, it put the reading down to *the dark eye socket skewing the measurement*. Eight
  minutes later my verdict said *they landed at 0.52 instead of 0.64 until I added dry()*
  anyway, and my notes said *highlights landed dull because they mixed into the wet shade
  under them*, which is the sentence the filed `NOTES.md` quotes at line 105. Both were wrong
  when I wrote them, and I already had the reason. **O**
- **The spark.** Confirmed: it moved one pixel by more than `0.02` in value and laid `0.2`
  units of paint, the same wet or dried. **M**
- **The ember did not land either.** Record 253, the `round_hard` dab at `0.0068` with
  `press=2` under the spark, laid `1.6` units of paint. It moved 5 pixels, by at most 22
  levels of 255, to a dull brown (`[45, 45, 52]` to `[65, 55, 44]`). The glint in the picture
  is the glaze laid over it, record 254 (`round_soft`, `0.022`): 342 pixels, up to 41 levels,
  133 units. So a round dab stops landing somewhere above `0.0068`, not only at `0.0028`.
  That is for step 2's measurement. **M**

## Question A: a light landing dull in wet paint, anywhere else

**Seen: only in exercise 4, which exists to show it. Measured today: once in the painting,
the two lights on the claws. Wet paint cost them `0.05`, and their size cost them about five
times that.**

- **Exercise 4.** Yellow laid over ultramarine from the stroke before lands at a median of
  `0.51`. Over the dried stripe it lands at `0.76`, and the yellow's own value is `0.79`. I saw
  it on the exercise sheet (**O**) and re-ran it today for the numbers (**M**).
- **In the painting and its rehearsals I never saw one.** My session mentions a light landing
  dull once, and that is the guess above. (**O**)
- **Every light laid onto fresh paint, measured** (**M**). Each is laid twice from its own
  record: once as painted, and once on a canvas dried first (or, where the painting had
  dried, without that `dry()`). It is read over the pixels the mark moved by more than
  `0.02`:

| Records | Mark | Its own value | Wetness under it | As painted | Dried first | Wet paint cost |
|---|---|---|---|---|---|---|
| 259, 260 | the claw lights, `round_hard` `0.0035` and `0.0032`, one to three strokes after the claws | 0.60 | 0.48 | 0.29, 0.27 | 0.34, 0.32 | **0.05**; 0.06–0.07 at the 90th percentile |
| 253 | the ember dab, `0.0068`, on the socket laid the stroke before | 0.62 | 0.54 | 1.6 units, 5 px | 2.2 units, 5 px | none that matters: it lands nothing either way |
| 250, 251 | the teeth, `0.0035` and `0.003`, on the maw's dark | 0.72, 0.60 | 0.00, 0.16 | 0.44, 0.375 | 0.44, 0.388 | 0.013 at most |
| 87–89 | the plinth's top plane, `flat` `0.02`, on the plinth's mass and side | 0.54 | 0.05–0.43 | 0.480–0.519 | 0.488–0.523 | 0.012 at most |
| 241–246 | the head's plane and the two marks before it, without the `dry()` at 240 | 0.64 (plane) | 0.001 under the plane's first stroke | 0.603–0.611 (plane) | identical to three decimals | none |
| 247–248, 262–265 | the horns' and the ridges' lights; the last four without the `dry()` at 261 | 0.60–0.72 | 0.000 | 0.48–0.62 | identical | none |

  The `dry()`s had nothing to dry. Wetness falls ×0.94 a stroke (`canvas.py`,
  `_WET_DECAY_PER_STROKE`), so forty strokes take it under a tenth. Wet paint only reaches a
  light laid within a few strokes of what is under it, and in this painting that means the
  claws. (**M**)

- **The claw lights are a case, and a warning against the warning.** Even dried, they land
  `0.26` to `0.28` short of their own value, because a `0.0032` to `0.0035` round lays 10 to
  16 units of paint over about 26 pixels. Wet paint accounts for about a sixth of what they
  lost, and their size for the rest (**M**). An `into-wet` notice gated on a light landing
  short on wet paint would fire on these two and send me to `dry()`, which recovers `0.05` of
  `0.31`. That is the engine making my own misattribution for me. **I suggested the warning,
  and I withdraw it as written.** If it is ever built, it has to measure the mark laid wet
  against the same mark laid dry, not against its own value. (**R**)
- **What would have helped instead** is a fact at the call for any mark that lands far short
  of its own value, whatever the cause. In this painting it would have named the spark, the
  ember and the claw lights (**M**). Those are the eye and the claws, the two give-aways my
  why-sentence names, and the reason my verdict found them too small to read. (**R**)

## Question B: what a planned place reads

**(1): its median, as one number for both `plan:` and `lightest:`. And yes, a split place
should say so, on a line that already names it, measured from its own median.**

- **At the finish** (**M**):

| Place | Planned | Mean | Median | 75th | 90th |
|---|---|---|---|---|---|
| head top | 0.66 | 0.524, a miss at −0.14 | 0.606 | 0.622 | 0.626 |
| plinth top | 0.54 | 0.458 | 0.503 | 0.520 | 0.527 |
| floor | 0.17 | 0.197 | 0.169 | 0.210 | 0.287, a miss at +0.12 |

  The other four places are inside their plan under all four readings. By the median and by
  the 75th percentile, all seven are inside. By the mean, the head's top misses. **By the
  90th, the floor misses from the plinth's pass on**, because the lamp's pool lies inside it.
  At every pass end all four readings name the same lightest place. So the 90th cannot read
  `plan:`. And (2) would keep the mean's *head top -0.14* on `plan:` beside a `lightest:` line
  reading `0.63`: two lines disagreeing about one place by a tenth.
- **That is the reading that sent me wrong.** What I compared at 14:49 was the number
  against the value I had mixed, *0.52 instead of the mixed 0.64* (**O**). Under (2), `plan:`
  would still have printed the 0.52's miss, and I would have gone looking for a cause again
  (**R**).
- **The split, measured at every pass end** (**M**). A tenth or more of a place's pixels
  more than `0.15` from its own median marks exactly two places, both for a real reason:
  - the plinth's top from the subject's pass on (15%, then 18%), because the creature's feet
    stand in it;
  - the head's top from the details pass on (24%), because of the eye and its socket.

  No other place reaches 7% at any pass end. The nearest is the floor, over the lamp's pool.
  Printed only where a line already names the place, it would have appeared on the
  `lightest:` line alone: for the plinth's top while that line named it the lightest place,
  and for the head's top after.
- **Measure it against the median, not a fixed `0.35`.** Say *head top reads 0.61; 24% of it
  darker by more than 0.15*. The `0.35` was chosen knowing the eye was there, and the next
  place's detail will sit somewhere else (**R**). The same clause also shows a median's own
  failure: a detail that covers more than half its place (**R**).

## Question C: declaring a key

**(1): the top twentieth under the box's middle. With a caution about the cluster question
that comes with every option: on my picture it would have been the next *no clear light*.**

- **The ceiling would never have spoken on my picture, which is what I want from it** (**M**).
  The top twentieth, the `values:` line's upper end, ran from `0.28` to `0.38` over all 25
  values lines of my reports. It never came within `0.16` of `0.54`. Both (1) and (2) at
  `0.40` would have stayed silent throughout. That is the right shape for a declaration: silent
  while I keep it, speaking when I leave it.
- **(2) asks for a number I did not have** (**R**, from **M**). My plan named values for seven
  places and none for a key. Asked for one, I would have written `0.40` and been told nothing.
  Or I would have written `0.35`, and four reports that reached `0.38` (lines 82, 118, 135 and
  144 of `reports.txt`) would have told me I had left a key I had only guessed at.
- **(3), with no ceiling, turns the key into a switch** that only silences *no clear light*.
  Your plan's own rule 4 rules that out. (**R**)
- **The cluster judgement, as the line makes it today, would have fired on every report**
  (**M**). My bottom two clusters were `0.03` to `0.09` apart on all 25 values lines. That is
  under `VALUE_THRESHOLD`'s `0.10` every time, the same count as *no clear light*.
- **The 0.07 gap is not where my picture's fault is** (**O**). I posterised the finished
  picture at the midpoints between its three clusters. The `0.18` band is the room. The
  `0.25` band holds **both the creature's shaded side and the lamp's glow behind its head**.
  The room and that band read as two masses. What reads as one is inside the `0.25` band: the
  creature's chest against the glow, held apart only by the rim of light. No gap between
  clusters can see that. A planned pair could have, had I planned the body as a place (**R**).
- **So under a key, print the clusters, and wait before judging them.** A fixed `0.10` is a
  yardstick for a picture that uses the whole box, and a low key compresses it: my finished
  picture's line spans `0.16` to `0.35`. Measure the gap on the corpus's dark pictures before
  the line judges one. (**R**)

## Question D: the documentation

**Which persuaded me.** My session quotes rules and never quotes a story. So where I acted on
a rule, I say which story sits beside it and whether I can tell that it did any work.

- **Keep, beside the upstream rule: eighty strokes on four treatments.**
  - What I did (**O**): after the cat's rehearsal I scrapped the pass and redrew (14:41, *I'm
    scrapping this and redrawing with a clearer profile pose*). After the piebald and the arch
    I changed the zones' geometry, not the brush. My verdict said the rule *saved the
    painting*.
  - Why keep the story (**R**): the bold sentence did the work, a number and a destination.
    The story is what makes *twice* a stopping rule rather than a preference.
  - Keep it once. It is one painting told in five places with three morals: lines 97–99, 119,
    200–201, 205–208 and 443–448 (**O**). Its moral is strongest beside this rule (**R**).
- **Keep: the picture finished without opening the other four.**
  - What I did (**O**): before my first mass I read the recipes' headings and twelve of the
    recipes, *before tackling unfamiliar passages like turning forms and lost edges* (14:26).
    The room's beam of lit air is laid from *A volume of lit air*, as its comment says.
  - Why keep it (**R**): I cannot separate the bold instruction from the story beside it, but
    the story is what makes it an instruction rather than a pointer.
- **Keep: the pier.**
  - What I did (**O**): I wrote the why-sentence before the first mark. At the end, my verdict
    answered the checklist's question on it: *the reason the picture exists is in it, but only
    on close inspection*.
  - Why keep it (**R**): it is the only story about a failure that no line catches. The pier
    passed every line of the checklist, so no measurement can stand in for it.
- **Drop: the four near-parallel fingers, and the arrangement redrawn three times.**
  - Nothing in my session shows either at work (**O**). My wing has four fingers, fanned, and
    I never counted them. My second redraw did change the view, which is the three-times
    story's point, but the session gives the ears as the reason, not foreshortening.
  - Both rules carry their own instrument (**R**): the band count, and the question *what is
    this thing's foreshortening?*
- **Drop the framing *every painter so far*.**
  - I find it three times in `PAINTER.md`, at lines 109, 373 and 407 (**O**).
  - It persuaded me once, on boxes: my verdict said *I painted no boxes (0 of 17), because it
    warned me* (**O**).
  - What did it was the second half, *and the checklist counts them*: a promise that it would
    be measured (**R**). The first half is no longer true: 0 of 17 (**M**).

**Did the card alone carry what I needed to start? For the method, yes. For the vocabulary,
no. And I never put it to the test.**

- What I read (**O**): my session read the README's first 400 lines, then `PAINTER.md` to line
  700. Then it read `REFERENCE.md` to line 520, in two reads five seconds apart, before the
  exercises and not when a situation called for it. So I cannot say what the card alone would
  have done.
- What I can count (**M**): of the calls my scripts lean on, the card (lines 1–143) names
  none:
  - `at_value`, 29 uses;
  - `edge=`, 14;
  - `s.dry`, 10;
  - `clip=`, 8;
  - `.shifted`, 4;
  - `.inset`, 3.

  The exercises carry `at_value` (exercise 1) and `edge="hard"` (exercise 5). **`clip=`
  appears nowhere in `PAINTER.md`**, and it is half of what made my lighting.
- The method I used as written (**O**): the order, rehearsal, the six mistakes and the
  upstream rule.
- What the card lacks (**R**): a first page someone could start painting from needs one more
  line, saying that a mass can be held to a shape with `clip=` and `edge="hard"`, and putting
  `at_value` beside `mix`.

## Question E: what a pass cost, call by call

**After every pass: rehearsed, counted and committed. Name both the function and the line.
List up to four calls, stopping once three quarters of the pass is named.**

- **After every pass** (**O**, **R**).
  - I rehearsed every pass before running it once. On my session, then, the committed line
    would have repeated the last rehearsal's, at the price of one line.
  - The committed report is the one that is kept. None of my 27 had a per-call line, so the
    23, 22, 20 and 14 had to be rebuilt from the log.
  - A painter who does not rehearse sees the line only on the commit, and needs it most.
- **Both the function and the line** (**M**).
  - On the subject's pass, the three dearest calls are all in `lay_body`, at lines 36, 38 and
    40. Every one of their records is noted `subject`, so neither the function nor the note
    can tell them apart.
  - On the details pass, the two dearest are both in `lay_core_shadow`, at lines 12 and 14.
  - The function is the name I think in, because I named my functions after masses. The line
    is the call I change (**R**). Name the function once per run of calls from it, as in your
    example.
- **Four, as a ceiling** (**M**). The log grouped your way: a mass call is its records
  sharing `via` and stream state, and a hand mark is one call. The costly calls, and how much
  of each pass three and four of them name:

| Pass | Strokes | Costly calls, dearest first | Three name | Four name |
|---|---|---|---|---|
| room | 41 | 16 and 7 `scumble`, 6 and 5 `block_in` | 71% | 83% |
| plinth | 49 | 19, 13, 9 and 3 `block_in` | 84% | 90% |
| subject | 102 | 23, 22, 20, 14, 12 and 5 `block_in` | 64% | 77% |
| details | 68 | 24, 17 and 4 `block_in`, then 23 marks by hand | 66% | (only three) |
| finish, glow | 16, 4 | none | | |

  A fixed three stops the room and the subject's pass short. Four is enough on every pass of
  mine, and three is enough when three already name three quarters.
- **One more figure per call: strokes that landed nothing** (**M**).
  - 13 of my 280 strokes show as *NO PAINT LANDED* in `easel log`.
  - Twelve are passes of three clipped `block_in`s that fell outside their clip, paid for and
    laying nothing: 2 of the 23 at `p04_gargoyle.py:40`, 6 of the 24 at `p05_details.py:12`,
    and 4 of the 17 at `p05_details.py:14`. The last two are a quarter of the core shadow's
    strokes.
  - On the dearest line, *24 block_in at p05_details.py:12 (lay_core_shadow), 6 landing
    nothing* would have told me to fit that shape before paying for it.
  - The thirteenth is the spark. It is a hand mark, which the dearest line never lists, so it
    needs its fact at the call. (**R**)

---

*Corrected on my side today: the painting's notes in the pack's folder, and my own memory of
the painting. Both carried the wet-paint lesson. The filed `NOTES.md` quotes that sentence at
line 105; I have not touched the repository.*
