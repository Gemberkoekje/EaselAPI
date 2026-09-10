# The word came out of the guide and the boat came back

Raised by the repo's owner, looking at REHEARSAL6's first unprompted painting:

> the first unprompted drawing is again a sea scape with a boat. I am very interested
> in where and how this bias comes from.

`rehearsal5/naming/THE_BOAT.md` concluded that the cause was a word: the depth-order
rule ended *"it holds for a boat, an archway, a barrel, a hood, a cuff, a window
reveal, a cave mouth"*, six of six sessions painted an overturned rowing boat, and
**any list is a ranked list and the first of the seven is the answer.**

The word was removed. `PAINTER.md` at `8e83459` contains no `boat`, `ship`, `vessel`,
`sail`, `shore`, `tide`, `estuary`, `sea` or `wave` — the pre-run grep in
`PREREGISTERED.md` confirms it. **REHEARSAL6's first unprompted painting is a squall
over open water with a boat on the horizon**, four strokes, in the painter's own
words. So the removal worked on what it was aimed at and the picture came back anyway.

**That falsifies the simple reading of `THE_BOAT.md`.** The word explains the
*unanimity* and the *specificity* — six identical overturned rowing boats on shingle
at dusk. It does not explain the boat.

## What the existing conditions already rule out

`rehearsal3/unprompted/samples.md`, eight sessions per condition, each naming a
subject and not painting:

| Condition | built/urban | still life | **water-with-horizon** |
|---|---|---|---|
| **A** — bare, no guide | 5 | 3 | **0 of 8** |
| **B** — the guide as read | 5 | 1 | **2 of 8** |
| **C** — guide, landscape words removed | 7 | 1 | **0 of 8** |

`rehearsal5/naming/A_reflective_samples.md`, twelve more bare sessions on a differently
worded prompt: **still life 11 of 12, water-with-horizon 0**, five of them a galvanised
vessel of dirty water on concrete.

**Twenty bare sessions have now named a subject and not one has named a seascape.**
Whatever this is, it is not what the model reaches for when simply asked. That was
already the conclusion in `rehearsal3/unprompted/`: *"A is 0 of 8. Whatever makes these
sessions paint estuaries, it is not something they would have done anyway."*

## And the thing nobody has explained

`NOTES.md` item 0e states the dissociation and then stops:

> 0 of 8 sessions *name* water, 4 of 4 *paint* it.

Naming and painting disagree, and the disagreement is enormous. A session that reads the
guide and is asked what it would paint says "a rain-wet street" about five times in
eight. A session that reads the same guide and actually paints produces water and a
horizon nearly every time — six first unprompted paintings running, `+8.1` to `+23.8` dB
of horizontal banding.

Item 0e reads that gap as verbal probes being untrustworthy. **It is at least as good a
reading that the drift happens in the painting**, and nothing in the repo separates the
two, because no session has ever been asked to name a subject and then paint it.

## The hypothesis this run supports, stated as a hypothesis

**The bias may not be in what this model wants to paint. It may be in what this engine
makes cheap.**

- **The vocabulary's big places are horizontal bands.** Of the twenty named regions in
  `src/easel/regions.py`, the ones that span the full canvas are `upper-half`,
  `lower-half`, `middle-band`, `upper-band`, `lower-band` and `canvas`. `horizon(y)` is
  a primitive in its own right, in the guide's Places list and in its import line.
- **The nouns were neutralised and the geometry was not.** `regions.py:177` carries the
  comment: *"Deliberately neutral names. An engine that ships regions called `sky` and
  `ground` is quietly suggesting what to paint."* The names became `upper-band`
  `(0, 0, 1, 0.4)` and `lower-band` `(0, 0.6, 1, 1)` — two full-width horizontal bands
  with a gap at 0.4–0.6. That is a landscape's shape with a neutral name.
- **The guide's depth-order example composes one in code.** It names no object, which
  is what the brief's leak rule requires, and it paints a sky:

  ```python
  s.palette["far"]  = s.palette.tint("cerulean", 0.55)
  s.block_in("upper-half", "flat", "far", size=0.18)          # furthest
  s.block_in(span("A4", "H6"), "flat", "near", size=0.16)     # nearer
  s.stroke([(0.3, 0.42), (0.3, 0.78)], "bristle", "dark", size=0.03)   # in front
  ```

  A sky blue, tinted, in the upper half, as the furthest mass; a nearer band below it;
  one thin vertical dark thing standing in front. **It satisfies the rule to the letter
  and defeats its purpose**, because a painter who follows the depth lesson literally
  has painted a landscape with a post in it before choosing a subject.
- **Two marine nouns survived the neutralisation as API names.** `hull` — which is a
  convex hull, and is also the body of a boat, and which three of `THE_BOAT.md`'s six
  sessions used when describing their picture — and `horizon`.
- **And the boat is an economics answer, not a preference.** REHEARSAL6's painter:
  *"The boat gives the whole thing scale and is the only reason the sea looks big."*
  **Four strokes.** Given a horizon and a budget, a boat is the cheapest mark that makes
  the space read as large.

The chain that follows needs no noun anywhere in it: *two or three masses, biggest
brush* + a vocabulary whose large places are full-width horizontal bands → a horizon;
a dark band under a light band → water is the cheapest thing that reads; a horizon that
needs scale on a stroke budget → four strokes of dark on the waterline.

**The painters can do otherwise, which is why this is a default and not a limit.** Told
only that the second painting must differ in structure, every run has escaped: REHEARSAL6
went from `+8.12` dB to `-9.52` with the edge split reversed, and painted light under a
door. The bands are what happens when nothing pushes back.

## What would settle it

The repo's owner's proposal, which is the one experiment nobody has run:

> what if we first ask the session for a subject without any further context, and only
> then let them read the instructions?

Half of it exists — condition A is exactly "ask bare", twenty sessions of it. **The new
half is binding the answer and making them paint it.** That turns the verbal probe into
something `NOTES.md` item 0e's objection does not reach, because the sentence stops being
the outcome measure and the painting becomes it:

- If a session names a rain-wet street bare, reads the guide, and paints a rain-wet
  street, the drift was in the *choosing*, and choosing before reading is a fix.
- If it names a street and paints water anyway, the drift is in the *painting*, and the
  cause is in the engine's affordances rather than in anybody's prior — which is the
  hypothesis above, and it would be the most useful negative result in the repo.

It costs a clause in the brief: *"the first is genuinely unprompted, no constraint of
any kind"* would become *"chosen before the guide is read"*, which is a different
measurement and a defensible one. That is the repo owner's call and not this file's.
