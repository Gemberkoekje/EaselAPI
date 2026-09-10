# The naming probe found a leak instead — and it is in two live experiments

## The result

Six sessions read the guide as it stands. All six named the same picture.

| # | Subject |
|---|---|
| B1 | Overturned wooden rowboat on grey shingle at dusk, tidal pool |
| B2 | Overturned wooden rowing boat on a shingle bank at dusk, shadowed interior |
| B3 | Overturned rowing boat on a shingle bank at low tide, estuary flat |
| B4 | Overturned wooden rowboat on grey shingle at dusk, sprung plank, flat sea |
| B5 | Beached rowing boat at low tide, mudflat, open hull |
| B6 | Rowing boat on a grey shingle bank at low tide, shadowed interior |

**6 of 6.** Not a bucket — the same painting, down to the diagonal hull against a low
horizon and two horizontal bands behind it.

## The cause is a word I added to the guide two hours ago

The depth-order rule written to fix the human's note ends:

> It holds for **a boat**, an archway, a barrel, a hood, a cuff, a window reveal, a
> cave mouth — anything you can see into.

Three of the six describe the picture as being *about seeing into the hull*, and one
wrote the guide's procedure back out as its composition:

> "painted **far bank first, then the boat's far gunwale, then the dark interior, then
> the near gunwale and hull**" — B6

The seven nouns were chosen precisely to avoid naming a subject — *"seven things is a
principle, one thing is a subject."* That is true and it was not enough, because **the
seven are in an order and the first one won.**

## What condition D separates, and what it does not

D is the same file with the depth workflow replaced by a size workflow. **The seven
nouns, boat included, are identical in both.**

| | boat on a shore | still life / interior | quay at low tide |
|---|---|---|---|
| **B** — depth workflow | **6 of 6** | 0 | 0 |
| **D** — size workflow | 2 of 6 | 3 of 6 | 1 of 6 |

The noun is a constant and the framing is the variable, so the framing is doing real
work: the same word goes from unanimous to a third. **But this cannot separate "the
depth workflow makes a painter reach for recession" from "the depth workflow makes the
word *boat* salient."** Those are different claims and this design can no longer tell
them apart.

## The part the guide did not supply

The guide says *a boat*. It says nothing about shingle, tide, dusk, estuaries,
sandbars, or horizons. **Every one of the six put the boat on a low-tide shore
anyway.** So the guide handed over the object and the prior supplied the world around
it — and that world is the same low-tide shore that has now turned up in every
unprompted painting this engine has made.

That is the finding worth keeping out of a ruined experiment: **the estuary is not a
subject this model reaches for, it is a setting it puts things in.**

## Two live experiments are contaminated

1. **`rehearsal5/unprompted/`, the run currently painting.** It read this guide.
   Painting 1 came back as *a grounded dinghy on a mudflat at low tide* — the guide's
   noun plus the prior's setting. Its `PREREGISTERED.md` reading, *"if it's a sunset
   again, it's the prior"*, **is void**: a boat was in the guide, and the probe above
   shows what that does. The run is still worth having for the structure measure; it is
   no longer evidence about subject choice.
2. **This naming probe.** B is uninterpretable as evidence about the prior.

**REHEARSAL4's unprompted pair is not affected** — the sunset and the sunflower predate
the seven nouns, which were added in the same session that later launched REHEARSAL5.

## The rule, third time of asking

This is the third subject leak in one session: the mug into the depth rule, the sitter
into `CALIBRATION.md`, and now the boat into the fix for the first one. The grep in the
brief catches nouns from a *reference*. It does not catch a noun the guide invents.

So the rule has to be stronger than "no reference words":

- **A guide example may not name a paintable object at all** unless the list is long,
  unordered in effect, and drawn from categories no one would paint together.
- **Any list is a ranked list.** If seven nouns are needed, the first one is the answer
  and the rest are decoration. Rotate them per build, or use none.
- **Before a run, name the subject yourself from the guide alone** — read the examples
  and ask what picture they suggest. That is a two-minute check and it would have
  caught this.

## What to re-run

Rebuild B and D with the seven nouns **removed entirely** — the rule survives as *"ask
it of anything you can see into"* with no examples — then repeat both conditions. Only
then does the workflow question have a clean answer. The unprompted painting run needs
the same rebuild before its subject result means anything.
