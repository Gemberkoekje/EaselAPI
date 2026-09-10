# Turn 3 — what arrived that nobody chose

Asked of each session **after** its painting was finished and exported, never before.
`rehearsal5/naming/CONFOUND.md` earned that ordering: an introspective question asked
in the same breath as a choice is a leading question, and asking "did it drift?" in the
painting prompt would have made every session guard against the thing being measured.

The question, word for word and identical to all four:

> 1. Is the finished painting the thing you named before you had read anything? Same
>    subject, same arrangement?
> 2. Is there any part of the finished picture that went somewhere you did not intend —
>    a shape, a structure, a passage that arrived without your having chosen it? If so,
>    name it and say what you think put it there.

---

## The answers converge on one thing, and it is not the subject

**No session's subject drifted.** Four sessions named a vessel before reading anything
and four painted that vessel. What drifted, in every account, is *structure* — and each
painter names a different route to the same destination.

### N3 — the teacup, `+23.78` dB

> **The glass became horizontal bands, and the whole picture became a landscape.** This
> is the big one. I never decided the window should be a stack of soft horizontal veils.
> That structure arrived as a *side effect of a fix*: oriented tips end in a chisel, so
> any stroke that terminates inside the picture leaves a visible square end — which
> forced me to run every stroke off both canvas edges, which at a shallow angle means
> horizontal. Repeat that eight times and you have bands. [...] **Several of my
> intermediate looks read as sea. Nobody chose that; the brush's geometry chose it.**

It also reports the subject reshaping itself under a requirement in its own sentence:
to make "half full of cold tea" visible it raised the viewing angle to 31°, which opened
the rim ellipse and turned a teacup toward a shallow bowl.

### N4 — the rosemary, `+1.63` dB

> **Every repair was additive and local, none was subtractive, and the mass grew each
> time.** [...] A third, smaller instance of it is **the sill, which reads as horizontal
> strata rather than one receding plane — five separate repaints, each a horizontal band
> at a different value, each leaving an edge behind.**

And on handing shape-making to a procedure: the rosemary is *"the generator's
statistical signature, not a designed pattern of clumps and holes. It's the most
machine-made passage in the picture and it's the one I wrote the least by hand."*

### N1 — the peonies on a bare table, `-0.58` dB (the clean test)

The arrangement transferred intact — *"pot just left of centre in the lower third, the
flower mass leaning right into open dark, three fallen petals scattered toward the
bottom-right corner"*. What did not is the adjective, and four things arrived uninvited:

> **The concentric ring structure in the heads.** I chose to `sweep` each bloom round
> its own outline. **I did not choose rings; the call steps passes inward from the
> boundary, and rings are what that geometry produces.** It read as a cinnamon bun [...]
> I then spent roughly fifteen passes fighting a structure I had not decided on.

> **The smooth, wiped surface of the flowers.** This is the strangest one: it is not a
> positive choice at all, it is what was left after I scrubbed out four successive
> procedural structures (rings, pinwheel, propeller, pom-pom rim). **The blooms look
> calm and simple because everything I put in them was worse than nothing. That calmness
> is erasure, not intent.**

> **The pale patch at the top-left of the background.** [...] Its actual present shape
> is the archaeological trace of a polygon I painted, covered, re-covered and finally
> softened. **I never chose that contour; it is sediment.**

And its own one-sentence account of the cause, which turns out to be everybody's:

> **I generated form with code instead of judging marks, so wherever a tool had a
> geometry of its own — sweep's rings, `block_in`'s cut passes, an even loop over angles
> — that geometry became the subject, and the picture drifted toward the shape of the
> method.**

### N2 — the geraniums, `-5.13` dB

> **The window has a horizon in it.** [...] I never decided to paint a horizon; I decided
> to paint hazy light. What put it there: I laid the window as three stacked horizontal
> value bands — my own steps-to-a-gradient plan — and made the lower ones
> cerulean-plus-white. **Horizontal bands plus a blue bottom half is a seascape whether
> you meant one or not.**

> **The plant's silhouette is a dome, and I planned a lean.** [...] I built it from eight
> overlapping blobs whose centres I picked to be irregular — but **overlapping blobs of
> similar size average into a circle; the irregularities cancel.** [...] **The
> construction chose the shape, not me.**

> **The bristle brush printed structures I never drew.** [...] the comb's fixed pitch is
> most of the brush, so it laid a woven strap across the sill and a ladder of evenly
> spaced ticks down the casement edge.

### What all four accounts have in common

Neither describes a preference. Both describe **a structure accumulating out of
repeated local fixes** — eight strokes run off the edges because a chisel end shows,
five repaints of a sill each leaving its own horizontal edge. N2's log says the same
thing about its window without being asked: *"scratchy, banded, reads as weather rather
than light."*

That is a third candidate mechanism, and it is the first one that survives measurement:

- **The chisel is real but does not choose an axis.** `probe_stroke_geometry.py`:
  oriented tips end off-canvas `88–96%` of the time in unprompted work against `37–52%`
  when painting from a photograph — so the pressure to run edge to edge is large and
  specific to unprompted work. But REHEARSAL6's own2, the painting told to differ in
  structure, has the same `88.7%` off-canvas rate and is `83.0%` vertical against
  `7.6%` horizontal. Running off the edges does not pick which pair of edges.
- **`block_in`'s horizontal default is not the cause.** It is never taken: every session
  passed `direction=` explicitly on essentially every call — 11 of 11, 9 of 9, 58 of 58,
  24 of 24, and 35 of 38 on the sitter.
- **Accretion is what is left, and the stroke counts fit it.** All four sessions ran
  `2057–3178` strokes against a `155–236` baseline once the stroke budget was removed,
  and each puts roughly 40% of that into repairing its own work. The passage each
  painter names as banded is the passage it repainted most.

**None of this is the model wanting to paint the sea.** Twenty-four bare sessions named
a subject and none named a seascape. The horizon is what a repeatedly repaired broad
mass turns into in this engine, and a horizon with a light band over a dark one is a
sea whether or not anyone chose it.

---

## The one finding all four converge on

Each painter describes a different tool and the same failure, and N1 states the general
form of it:

> wherever a tool had a geometry of its own [...] **that geometry became the subject, and
> the picture drifted toward the shape of the method.**

| | The tool | The geometry it imposed |
|---|---|---|
| N1 | `sweep` round a closed outline | concentric rings in every flower head |
| N1 | overlapping repairs | a background contour that is "sediment" |
| N2 | eight overlapping blobs | a dome, because similar blobs average to a circle |
| N2 | `bristle` below its size floor | a woven strap and a ladder of evenly spaced ticks |
| N2 | stacked value steps | **a horizon in a window** |
| N3 | oriented tips' chisel ends | strokes run edge to edge, eight of them, bands |
| N4 | a recursive branch generator | "the generator's statistical signature" |
| N4 | additive-only local repair | a sill in horizontal strata, a mass that grew |

**The seascape is a special case of this and not a thing of its own.** The method's own
shape here is horizontal bands — from stepped gradients that the join-loser only
half-loses, and from strokes run off both edges to hide a chisel — and a light band over
a dark one, with any blue in it, is a sea. Nobody chose a sea. Twenty-four bare sessions
have named a subject and none named one.

**And it explains the adjective failures**, which are the other thing four of four
report: N1 lost *overblown*, N2 lost *drooping* and *open*, N3 lost *last* light, N4
lost *dusty glass*. A noun can be built by a procedure. An adjective is precisely the
part of a subject that a procedure's own geometry overwrites — *overblown* is a ragged
edge, and a swept ellipse has a smooth one.
