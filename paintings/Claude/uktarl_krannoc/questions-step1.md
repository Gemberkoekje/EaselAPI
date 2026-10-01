# Questions for the painter, after filing

*Written to be pasted into the painting session as it stands, by the owner. The answers are
filed beside the painting as `answers.md`, verbatim. Questions A to I are `PLAN-0.9.0.md`'s
P1 to P9, in that order.*

---

Your painting and your verdict are filed in the EaselAPI repository, with the campaign's
files left out, and the next release acts on the verdict. Every point you raised has a
proposed answer. The owner's ruling is that the tool is for painters, so where a proposal
turns on how the tool should behave, the choice is yours. Nine can be asked now. What the
soft edge should look like will come later, as pictures to compare blind.

Please answer each with your evidence where you have it, say so where you have none, and
label each answer **M** (you measured it), **O** (you observed it) or **R** (you reasoned
it).

**First, five things your own session showed when the painting was filed**, because some of
them change a question:

- **`key="low"` already does what your eighth point asks.** The check counts a picture as
  low-key while its top twentieth stays under the box's middle: yours is `0.52` against
  `0.54`. Replayed with `key="low"` in your plan, the `values:` line says *low-key, as the
  plan says* after every pass, and from the head's pass on *Uktarl's face stands clear --
  0.69 at its brightest twentieth against 0.50 for everything else, 0.19 over*. No document
  says what the check counts as low-key.
- **The mountain's 129 strokes were its direction, not its shape.** The ten facets are
  convex. Laid along the line from each peak to its dip, which runs across the facet's
  length, they cost 88; along their own axes, 31. The collar is as you said: the V costs 17
  to 22 at any one direction, and the two flaps 3 and 4.
- **Of the 28 "discs", 20 are the faces' marks**, and one is a ridge on the relief that
  sits 56 px from the left bandit's eye. The other 7 are the candle and three relief marks.
- **The label on the face was two labels**: the guide's note `Uktarl`, and a landmark `sun`
  left by your first drawing pass. The redrawn pass no longer marks it, but `s.unguide()`
  clears guides, not landmarks.
- **From the body's second rehearsal on, 29 of your 30 `easel run`s filtered the check's
  output** down to the lines you named.

**Question A — painting outside a shape.** The proposal is `clip_out=` on every verb that
takes `clip=`, plus `intersection()` and `difference()` as shapes; a shape builder refuses a
result with a hole and points at `clip_out=`. Would you use both, or would `clip_out=` alone
have done everything you needed? And where paint is held outside a figure, should the
figure's edge be held like any hold, or take the soft edge of question B?

**Question B — the soft edge.** The proposal is a softness on a call's holds: the mask fades
over a width you name instead of cutting at the outline. If softening an edge cost nothing,
**which edges in this picture would you have softened, and over how many pixels each?** Should
one softness apply to every hold of a call, as `feather=` does, or each hold take its own?
Would you give the width in pixels, as your verdict does, or as a fraction of the long side,
as `size` and `feather=` are? And is it a soft hold, or a verb that loses a stretch of
outline priced by its length?

**Question C — a habit declared.** An earlier ruling says a standing warning is declared up
front in the plan, as `bands="subject"` and `ground="buried"` are, not dismissed after the
fact. The proposal: `s.plan(habits={"disc": "the features of four faces"})`. After that the
finding prints as a count with your reason, and the closing checklist quotes the reason
back. Which habits would you have declared here? Per painting, or per place? And for the
disc rule itself, what would tell a face's marks from one disc printed over and over: the
shapes the marks actually landed, any mark with a pressure list or three or more points, or
something else?

**Question D — a local frame.** What would you have written instead of `hp()`, `dp()` and
`ah()`? The proposal is `s.frame(centre, rx, ry, tilt)`, with `.at(u, v)` and
`.polygon(points)`, and `.rotated(degrees, about=)` on shapes and groups. Would that have
replaced your three helpers and their outline functions? In pixels or in fractions?

**Question E — a share for each part.** Should a part's planned share be of the budget, or
of the marks laid so far? The `subject:` line said 47% and 48% after Uktarl's head, a share
of the marks so far; of the budget he had 23%. What split would you have planned for this
picture: the four figures, the relief, the floor and the table?

**Question F — passes outside a clip.** Your floor's second rehearsal paid for 9 passes that
landed nothing, outside their clip, and the head's pass for 1. A mass could skip passes
that fall wholly outside its clip. But every later mark of an older script that lays one
would move, so rebuilding such a painting would change it. Should a mass skip them?

**Question G — a dark picture's light.** Given the first point above, which of these:
**(1)** the documents say what the check counts as low-key, where `key=` is introduced;
**(2)** with no key declared, the `values:` line names a planned light that stands clear and
points at `key="low"`; or **(3)** your own form, the light judged under any key with nothing
declared?

**Question H — the documentation.** You said the rules you used would fit on two pages.
Which were they? What must a one-page card hold? And what on today's first page, *The first
hour*, would you cut?

**Question I — the join on skin.** You laid a join stroke along each face's terminator.
Looked at 1:1, does it read as the turn of skin, or as a facet?
