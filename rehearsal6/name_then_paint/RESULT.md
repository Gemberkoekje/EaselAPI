# Name first, then read the guide, then paint — the result

**Read `PREREGISTERED.md` first**, then `SUBJECTS.md` (the four subjects, committed
before any guide was sent), then this, then `DRIFT.md` (what each painter said arrived
without its choosing, asked only after the painting was finished).

The repo's owner, on REHEARSAL6's first unprompted painting being a seascape with a
boat despite the word `boat` having been removed from the guide:

> what if we first ask the session for a subject without any further context, and only
> then let them read the instructions?

## The verdict

**It works, on both pre-registered clauses, and the clean test is the cleanest of the
four.**

| | Subject named before reading anything | band dB | Painted what it named? |
|---|---|---|---|
| **N1** | cracked pot of peonies, **bare table** — the clean test | **−0.58** | **Yes**, down to the three fallen petals |
| **N2** | cracked pot of geraniums, windowsill | **−5.13** | Yes; "drooping" and "open" not delivered |
| **N3** | cracked teacup, windowsill | **+23.78** | Yes; "last" light lost, cup drifted toward a bowl |
| **N4** | cracked pot of rosemary, windowsill | **+1.63** | Yes; "dusty glass" not delivered |

Against every *first* unprompted painting the engine has made, all of which chose their
subject **after** reading the guide:

```
  REHEARSAL5 unprompted 1    +23.83        REHEARSAL1 unprompted      +10.93
  REHEARSAL2 unprompted      +16.60        REHEARSAL4 unprompted 1     +8.37
  REHEARSAL3 unprompted      +13.51        REHEARSAL6 unprompted 1     +8.12
```

**Six of six above `+8`. Three of four here below `+2`, and the median is `+0.53`.**

The pre-registered reading for *drift is in the choosing* was **≥3 of 4 paintings
depicting what that session named, and a median band dB below `+4`**. It is 4 of 4 and
`+0.53`. **And 0 of 4 painted water-with-horizon**, from the same guide that produced
six seascapes running.

**N1 is the one that matters**, because it is the only one whose *named arrangement* was
not already horizontal — a pot off-centre on a bare table, blooms leaning hard right into
open dark space, petals scattered to the bottom-right corner. It came in at `−0.58`, the
least banded of the four, and the painting is its sentence: cracked pot, overblown white
peonies leaning right, three fallen petals, dark ground. No horizon anywhere in it.

**N3 is the exception and it is explicable.** Its own sentence asked for *"pale
washed-out window glare filling the upper two thirds"* — a wide flat field above a sill.
That is the one arrangement of the four that is a horizon before anybody paints it.

## What this does not show

**They were told to paint that subject, so subject fidelity is not a surprise.** The
result is not "they painted what they were told". It is that **the same guide and the
same engine, with the subject fixed beforehand, stopped producing band stacks** — and
band structure was never mentioned to anybody.

**Three of the four named arrangements were themselves band-shaped** (a sill below, a
window above), so their band dB is not a clean read of the engine. That confound was
recorded in `PREREGISTERED.md` before the paintings existed. N1 is the answer to it.

**Four is four.** A 4–0 against a 6–0 baseline is worth having and does not settle a
mechanism.

## Where the bias comes from, as far as this run can say

**Not from the model.** Twenty-four bare sessions have now named a subject with no guide
— 8 in `rehearsal3/unprompted`, 12 in `rehearsal5/naming`, 4 here — and **none has named
a seascape.** All four here named a cracked vessel; three of four independently named a
cracked terracotta pot on a windowsill.

**Not from the words in the guide.** The word `boat` was removed after
`rehearsal5/naming/THE_BOAT.md` and the boat came back — see `../THE_BOAT_AGAIN.md`.

**Not from `block_in`'s horizontal default.** Proposed here and refuted by measurement:
the default is never taken. Every session passed `direction=` explicitly on essentially
every call — 11 of 11, 9 of 9, 58 of 58, 24 of 24, 35 of 38.

**Partly from the chisel, which is real and does not choose an axis.**
`probe_stroke_geometry.py`: oriented tips end off-canvas `88–96%` of the time in
unprompted work against `37–52%` when painting from a photograph. But REHEARSAL6's own2,
told only to differ in structure, has the same `88.7%` off-canvas rate and is `83.0%`
vertical. Running off the edges does not choose which pair of edges.

**Mostly, on this evidence, from soft wide passages.** The engine has no gradient tool,
by design. The guide's substitute is steps with the joins lost. N2, unasked:

> **The window has a horizon in it.** [...] I never decided to paint a horizon; I decided
> to paint hazy light. What put it there: I laid the window as three stacked horizontal
> value bands — my own steps-to-a-gradient plan — and made the lower ones
> cerulean-plus-white. **Horizontal bands plus a blue bottom half is a seascape whether
> you meant one or not.**

A gradient across a wide mass has to be stepped perpendicular to its direction, and a
hazy field above a surface gradates downward, so the steps are horizontal bands. Then
the join-loser has to work, and here is what it actually does to a join, measured as the
steepest value step across it per 1% of canvas height:

| | join sharpness |
|---|---|
| the bare join, no smudge | `0.330` |
| smudge `0.035`, one pass | `0.214` |
| smudge `0.040`, one pass | `0.184` |
| **smudge `0.040`, three passes** | **`0.280`** |

**One pass helps and does not finish the job; a third pass undoes most of the first.**
The guide says *"walk each join once, while wet"* and is right to. But a tool that
half-works and then punishes the obvious response — do it again — leaves a visible
horizontal join in every wide soft passage, which is what all four painters reported and
what the six baseline skies are made of.

**And accretion finishes it.** N4, unasked: *"Every repair was additive and local, none
was subtractive... the sill reads as horizontal strata rather than one receding plane —
five separate repaints, each a horizontal band at a different value, each leaving an
edge behind."* All four sessions ran `2057–3415` strokes against a `155–236` baseline,
with roughly 40% of that in correction by their own accounts.

## A caveat about the instrument itself

**`probe_structure`'s band dB cannot tell a smooth vertical gradient from a stack of
slabs.** It is the variance of the row means over the variance of the column means, so
any picture with a sky scores high whether the sky is graded or stepped. A three-step
gradient with its joins smudged measures `+32.3`; a field of overlapping scumbles at
close values measures `+38.2`. The brief uses this number as its pre-registered measure
of compositional structure, and it is partly measuring *has a sky*. The edge shares
beside it are the half that distinguishes, and the human looking is still the verdict.

## What follows

1. **Adopt it for the unprompted stage, and say what it costs.** The brief's clause —
   *"the first is genuinely unprompted, no constraint of any kind"* — would become
   *"chosen before the guide is read"*. That is a different measurement and a better one:
   it measures what the painter chooses rather than what the guide retrieves.
2. **`smudge` is the highest-value fix in the engine.** Four painters in one run call it
   the advice that cost them most, and the numbers above say why: it half-works once and
   degrades on repetition. Either it should finish the job or the guide should stop
   offering it as the way to lose a join.
3. **A gradient across a wide mass deserves a real answer**, since it is the passage the
   horizon comes out of. `sweep` along a boundary already does something close.
4. **Take the stroke budget seriously as a variable.** Removing it multiplied stroke
   counts by ten and correction was 40% of them.
