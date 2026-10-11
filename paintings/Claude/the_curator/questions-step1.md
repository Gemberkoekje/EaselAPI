# Questions for the painter of The Curator's interim art

*Written to be pasted into the painting session as it stands, by the owner. The answers are
filed beside the paintings as `answers.md`, verbatim. Questions 1 to 8 are `PLAN-0.9.0.md`'s
Q1 to Q8.*

---

Your nine pieces, your verdict and the evidence you pushed are filed in the EaselAPI
repository, and the next release, 0.9.0, acts on the verdict alongside another painter's.
Every point you raised has a proposed answer. The owner's ruling is that the tool is for
painters, so where a proposal turns on how the tool should behave, the choice is yours.

Please answer each with your evidence where you have it, say so where you have none, and
label each answer **M** (you measured it), **O** (you observed it) or **R** (you reasoned
it). Where your transcript holds the answer, look there rather than recall it.

**First, what filing found**, because some of it changes a question:

- **Your pieces rebuild within one level, not to the pixel, on another machine.** Re-run on
  Windows, every piece differs from its shipped PNG in 12 to 2,508 pixels, each by exactly
  one 8-bit level. On your machine they are pixel-identical, as you said.
- **The candle's faint shading was its brush's width, not its opacity.** At the sprite's
  own size, 120×300, `size=0.009` is 2.7 px across, under the 6.5 px a round tip needs to
  land in one touch. One wax-light stroke there moves its pixels a mean 6 levels at opacity
  0.6, and 14 at 0.9 laid twice. The same stroke on a canvas four times larger is 10.8 px
  and moves 17 levels at 0.6, once.
- **The warm grey sits in a narrow band.** Burnt umber is hue 17°; with 10 to 18%
  ultramarine it stays a red-brown, at 25% it is a neutral leaning magenta, at 35% violet.
  And `at_value` re-solves the value whatever white you mixed in first, so the white
  changed nothing: the same hex comes back.
- **Six of your nine pieces say *no clear light***, each with a light named in its plan.
  All six keep their top twentieth under the box's middle, 0.54, which is the check's own
  test for a low key: `s.plan(key="low")` would have made the line say *low-key, as the
  plan says*. The documents never say when to declare it. And the candle's checklist reads
  the canvas the cut throws away: 67% bare ground.
- **The reference you asked for exists.** `REFERENCE.md` gives `ribbon()`'s width, the
  pressure profiles' names, `density` as *spacing, not coverage*, what `solid` does,
  `opacity` as per-dab strength, and a table of the brushes; `easel guide --reference`
  prints it. You read it only for *direction*. It does not say how opacity, density and
  `solid` combine.
- **You never ran `s.report()`, `cost()`, `easel run` or `easel check`.** The check after
  each pass, which names wasted and costly calls by script line, reaches only `easel run`.

**Question 1 -- transparency.** The proposal is `s.export(path, alpha=place)`: the alpha
channel is the coverage of the places you name -- the shapes you laid the thing in --
antialiased as a held edge is; a hole, like the arch, by `difference()`. Is that what you
would have used? Or would you rather declare the cut in the plan (Question 4), or both?
Your cut drew the polygons at 4×, scaled down and blurred 0.8 px: should the edge fall as
a held edge's does, or softened as yours was, and by how much?

**Question 2 -- a warm grey.** Three candidates: a fact printed at `mix()` when a mixture
lies near neutral and its hue has turned away from both pigments, saying at what share it
turns; a recipe, *A warm grey*; or a named grey on the palette, `p.grey(value,
warmth=...)`. Which would have kept your stones brown? And what showed you they had gone
purple -- the stage image, a swatch, or a number?

**Question 3 -- how paint lands.** Which calls did you fight, and what did you try, in what
order? Would painting each piece at two to four times its size and exporting at its own
size (`s.export(path, size=(w, h))`) have served? And what must one table of `opacity`,
`density`, `solid`, `press` and the brush's pixel width say, for you to have reached for
the right one first?

**Question 4 -- a piece that is one layer.** Three candidates: `key="low"`, said plainly
where the plan is introduced; a cut declared in the plan, `s.plan(cut=place)`, so the
checklist reads only what ships; or the scene declared, which no single canvas holds.
Which, and on a cut-out, which of the checklist's lines would you have wanted kept?

**Question 5 -- pixels.** The proposal for the round is a frame, `s.frame(centre, rx, ry,
tilt=)`, that maps its own units to the canvas, and takes pixels. Would that have retired
your `n(x, y)`? Or did you want `polygon()` to take pixels itself, or a canvas made with
pixel coordinates throughout?

**Question 6 -- geometric subjects.** `RECIPES.md` has *The one ruled line*. Did you see
it? For a shelf, a bar and an arch joint, what would a recipe need to say for the result
to read as painted rather than stiff?

**Question 7 -- rehearsal.** Did you know that `easel run --rehearse` and `s.report()`
exist? Why did you run each script whole, by stage? This is asked to learn, not to fault:
the answer decides whether the documents need to say it, or the tool needs to work your
way.

**Question 8 -- the reference.** Did you see `easel guide --reference`, or that
`REFERENCE.md` holds the units and defaults? What would have sent you there before the
code?
