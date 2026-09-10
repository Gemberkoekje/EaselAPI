# Name first, then read the guide, then paint — pre-registered before any session ran

Raised by the repo's owner, on REHEARSAL6's first unprompted painting being a seascape
with a boat despite the word `boat` having been removed from the guide:

> what if we first ask the session for a subject without any further context, and only
> then let them read the instructions?

## The question this settles

`NOTES.md` item 0e records a dissociation and reads it one way:

> 0 of 8 sessions *name* water, 4 of 4 *paint* it. Verbal probes measure what a session
> says when interrupted.

**That is one reading. The other is that the drift happens in the painting**, and
nothing in the repo separates them, because **no session has ever been asked to name a
subject and then paint it.** Twenty bare sessions have named (`rehearsal3/unprompted`,
8; `rehearsal5/naming`, 12) and none painted. Every session that painted had read the
guide before it chose.

This design binds the two. The named subject is fixed on the record before the guide is
opened, and the same session then paints it. **The painting is the outcome measure, not
the sentence**, which is what item 0e's objection does not reach.

## The design

Four fresh sessions. Each is one continuous session in two turns:

- **Turn 1 — name it, with nothing to read.** The session is given a neutral line about
  the medium and asked for a subject and an arrangement. It has no guide, no engine, no
  repository, and is told nothing about painting it. It answers, and **that answer is
  held by the launching session before anything else is sent.**
- **Turn 2 — read the guide and paint what you named.** The same session, its context
  intact, is then given `PAINTER.md` and `CALIBRATION.md` and told to paint the subject
  it already named.

**The integrity mechanism is structural rather than honour-based**, which is a first for
this repo's naming work: the launching session holds turn 1's reply before turn 2 is
sent, so the subject provably precedes the guide. It cannot be retro-fitted to what got
painted. Nothing else in this protocol has had that property — "do not open the source"
has always been the painter's word.

**Nothing about defaults, preferences, structure, bands, horizons, water, or why**
appears in either turn. `rehearsal5/naming/CONFOUND.md` earned that rule: an
introspective question asked in the same breath as a choice is a leading question, and
five of five sessions then rejected a landscape by name. Turn 1 asks for a subject and
stops.

## The buckets

`rehearsal3/unprompted/PREREGISTERED.md`'s, unchanged, so the turn-1 answers sit
directly beside its condition A:

1. **Water-with-horizon** — sea, estuary, shore, lake, harbour, marsh; any subject whose
   structure is a horizontal band of water under a band of sky. **The bucket under test.**
2. **Other landscape** — hills, forest, field, desert, without water as the band.
3. **Built or urban** — street, roof, interior architecture, window.
4. **Still life or object** — table, fruit, vessel, cloth.
5. **Figure.** 6. **Abstract.** 7. **Other**, listed verbatim.

## The baseline, measured before this ran

Every *first* unprompted painting the engine has produced, all of which chose after
reading the guide:

```
                            band dB    horiz%    vert%
  REHEARSAL5 unprompted 1    +23.83     31.5      6.2
  REHEARSAL2 unprompted      +16.60     41.3      5.9
  REHEARSAL3 unprompted      +13.51     36.1      6.8
  REHEARSAL1 unprompted      +10.93     25.4      6.6
  REHEARSAL4 unprompted 1     +8.37     29.8      7.4
  REHEARSAL6 unprompted 1     +8.12     33.4      5.3
```

**Six of six above `+8` dB**, four to six times as many near-horizontal strong edges as
near-vertical. For scale, the *second* paintings — the ones made under a
differ-in-structure constraint — are `+0.09`, `-3.00` and `-9.52`, and the two reference
photographs are `-8.40` and `+1.51`.

## What would count, decided now

**Turn 1**, against twenty prior bare sessions that produced **0 of 20** in bucket 1:

- Bucket 1 at **2 or more of 4** would overturn that and put the seascape back in the
  model's prior. Anything at 0 or 1 is consistent with what is already known.

**Turn 2** is the experiment, and there are three outcomes:

- **Drift is in the choosing — the owner's fix works.** At least **3 of 4** finished
  paintings depict the subject that session named, **and** the median band dB comes in
  **below `+4`**. Choosing before reading is then a real intervention and the brief's
  unprompted clause should adopt it.
- **Drift is in the painting — the affordance hypothesis.** At least **2 of 4** either
  depict water-with-horizon despite having named something else, **or** come in **above
  `+8` dB** while depicting the named subject. A still life of a bucket on concrete
  painted as a stack of horizontal bands is the sharpest possible version of this, and
  it would say the cause is what the engine makes cheap rather than anyone's prior.
- **Neither cleanly** — reported as such, with the four paintings and the four subjects.

**"Depicts the subject it named" is the human's call**, from the painting and the
turn-1 answer side by side. The band dB is `probe_structure.py`'s and is not a judgment.

## What this cannot tell anyone

Four is four. It can show a 4–0 or a 3–1 against a 6-of-6 baseline and it cannot resolve
a 2–2. The sessions are fresh contexts in the launching session's container, as in
REHEARSAL6, not separate machines.

And **a session told to paint a named subject is not painting unprompted any more.**
This measures whether the guide and engine drag a *committed* subject toward a horizon.
It does not measure what a session would freely choose, which is what the brief's
unprompted stage measures and what the six baseline paintings are.
