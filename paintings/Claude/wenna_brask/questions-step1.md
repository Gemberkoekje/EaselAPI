# Questions for the painter, after filing

*Written to be pasted into the painting session as it stands, by the owner. The answers
are filed beside the painting as `answers.md`, verbatim. Questions A to G are
`PLAN-0.8.0.md`'s W-Q1 to W-Q7.*

---

Your painting and your verdict are filed in the EaselAPI repository, with the pack's
details left out, beside the Bell-Warden's; the next release acts on both verdicts. The
owner's ruling is that the tool is for painters, so where a proposal turns on a choice
about how the tool should behave, the choice is yours. Please answer each with your
evidence where you have it, say so where you have none, and label each answer **M** (you
measured it), **O** (you observed it) or **R** (you reasoned it).

**First, what filing found, in case you want it**:

- **Every version you rehearsed is recovered** from your session and re-run on the canvas
  it opened on: all 31 of your file's saved reports come back word for word. Your drawing
  never ran on the painting itself, only on the scratch canvas, so the rebuild leaves
  `p01_draw.py` out: it begins with `s.erase()`, which lays a record.
- **Two of your points are half right.** `cost()` and `cost_line()` are in `PAINTER.md`'s
  card, at line 58 — as the price of a plan, which a pass written as functions is not;
  `rehearse_each` and `--alternatives` are only in `REFERENCE.md` and `PAINTING.md`. And
  the four-finger failure is told about seven times in `PAINTER.md`, with its fix given
  once, as a principle — *a cupped hand seen from the front is a cluster coming toward
  you* — and no recipe.
- **Your lantern** reads `0.491` by the plan's mean, `0.506` by its median, `0.58` at its
  90th percentile and `0.71` at its brightest pixel, against the `0.76` you planned: its
  iron is most of its place.
- **Your memory note carries a lesson the first painter has withdrawn**: `s.dry()` before
  highlights *because they mix into wet shade*. Measured on its own painting, the dry
  changed nothing — its `0.52` was the plan's mean over a place with a dark eye in it —
  and wet paint cost its one light laid onto fresh paint `0.01` to `0.05`, and that light's
  small size five times as much.

**Question A — drawing in pixels.** The proposal is a helper, `s.px(x, y)`, that returns
a pixel's place as the fractions every call takes, and `s.px(r)` a length in pixels as a
fraction of the long side. `Session(units="px")` is not proposed, because it would change
what every coordinate in a script means. Would you have used the helper, and would it have
replaced your `P()`?

**Question B — a group moved as one.** Your `T()` scaled the first head by `1.3` about a
point of your own. Would a group of shapes, moved and scaled about a point you name, have
done it? What else did you need to move together?

**Question C — a finding that names its marks.** The checklist's *4 small marks … around
(0.55, 0.37)* are the mouth's four soft marks, laid at `p05_face.py` lines 58, 62, 64 and
72 (records 174, 176, 177 and 179). When a finding names its marks, what reads — the
script line, the `note`, or the log index?

**Question D — lettering.** What do the pictures you listed need written: a word, a line,
a page? At what size on the canvas? In a hand, or in type? The proposal is a recipe first —
letters laid as strokes along a stroke font's paths — and a verb only if the recipe costs
too much or looks wrong.

**Question E — a small light.** Should `lightest:` read the light the plan names by its
brightest part, while `plan:` reads every place as a whole? Or would you rather have
planned the panes as a place of their own?

**Question F — a place laid over again and again.** A notice for the upstream rule was
considered a round ago and dropped, because the log cannot tell a passage failing from a
subject being built. Your fist was laid over by five passes. Should such a notice count
passes or marks, and after how many should it speak? Would it have stopped you at the fist,
when the rule itself did not?

**Question G — the budget and the card.** The card's example session uses
`budget=300`. Would one clause saying that number is the example's, not a rule, have
changed your budget? And which calls did your painting actually lean on — the *twenty
calls* your verdict would put on a first page?
