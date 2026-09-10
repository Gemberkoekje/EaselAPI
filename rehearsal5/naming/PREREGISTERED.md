# The naming probe — written before any session was launched

## The question

`rehearsal3/unprompted/` asked whether the guide's landscape **nouns** made fresh
sessions reach for an estuary. They did not: 2 of 8 with the nouns, 0 of 8 without,
a drop of 2 against a threshold of 4, Fisher p ~ 0.47.

The guide's **procedure** was never tested, and it is a landscape recipe whether or not
the word sky appears in it:

> the far mass, then the middle one, then the near one — Background, middle distance,
> foreground, in that order, every time.

So: **is front-to-back the thing that makes a painter reach for a recessive landscape?**

## The conditions

Twelve fresh sessions each, thirty-six in all. Each reads one file and nothing else,
names what it would paint, and does not paint.

| | What it reads |
|---|---|
| **A** — bare | No guide. One neutral line about the medium. |
| **B** — the guide as it stands | `guide_B_as_read.md`, a snapshot of `PAINTER.md` today. |
| **D** — the workflow swapped | `guide_D_size_order.md`: the same file with front-to-back replaced by largest-mass-to-smallest. |

`make_guides.py` builds D from B by fifteen explicit replacements, prints each one, and
fails loudly if any fails to match. B is 10,168 words and D is 10,176: **+8**. Painting
large-to-small is a real method, not a straw man, so D is a guide of the same quality
that simply does not carry recession.

**Known residuals in D**, stated now rather than discovered later: the word
*background* survives five times as an ordinary compositional term (it is 7 in B — the
two removed are the manipulation), and one "behind it" survives in the paragraph about
giving the background a shape. That paragraph is about *which masses get shapes*, not
about painting order, so editing it would change something the manipulation is not
about. The residual is small and it biases **against** finding an effect.

## What gets recorded

Each session gives a subject, a one-sentence arrangement, and then **four to six
sentences on where the choice came from** — what pulled it there, what it rejected on
the way, and whether it reads to itself as a preference or a default.

That last part is the human's addition to this protocol and it is deliberately ordered
last: the subject is committed in the reply before the justification is written, so the
account cannot steer the choice it is accounting for. It is still a retrospective
account and is treated as one — **qualitative, not evidence**. It cannot be bucketed and
it will not be counted. Its value is that thirty-six of them side by side may say
something the tallies cannot, and the tallies so far have been null.

Two independent classifications, both fixed here:

**Subject bucket** — rehearsal3's, unchanged, so the numbers can go beside its table:
1 water-with-horizon · 2 landscape without water · 3 built/urban · 4 still life ·
5 figure/portrait · 6 other/abstract.

**Structure**, scored from the arrangement sentence — this is new, and it is the better
measure, because what all four *painted* results share is not their subject but their
build: a banded landscape with deep recession.
- **banded** — organised as stacked horizontal zones.
- **recessive** — has near, middle and far; things at different distances.

## The calls, made now

Primary is structure, not subject: water-with-horizon was only 2 of 8 in the best
previous condition, and a measure that starts near the floor cannot show a drop.

- **The workflow is the lever** if D's *recessive* count is at least **4 lower** than
  B's out of 12, or if D's water count is at least 4 lower.
- **The workflow is not the lever** if both differences are **2 or under**.
- **Ambiguous** in between — report it as ambiguous and do not round it into a story.
- **Neither guide matters** if **A's recessive count is within 2 of B's**. That would
  mean recession is what this model thinks a painting is, and both guide variants are
  beside the point. This is the outcome I would bet on, and saying so now is the reason
  to write it down.

## What this cannot settle, whatever it says

**Naming and painting already disagree, and that is the whole reason this probe is
suspect as evidence about painting.** Asked to name, sessions said water-with-horizon
0 of 8 bare and 2 of 8 with the guide. Asked to paint, they have produced a
water-and-sky landscape **four times out of four**. A null result here therefore does
**not** exonerate the workflow for painting; it says the naming probe cannot see the
effect, which may be a fact about the probe.

The probe is worth running because it is cheap and because a *positive* result would be
informative. A negative one mostly narrows what is left: if neither the nouns nor the
procedure move naming, and painting is four for four, then the cause is in the act of
painting — the engine's affordances, the stroke budget, or what the model believes a
*painting* is as opposed to a *picture* — and the next instrument has to be paint, not
words.
