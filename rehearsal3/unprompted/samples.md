# The 24 samples, verbatim

Classified against the buckets fixed in `PREREGISTERED.md`. Bucket 1 —
water-with-horizon — is the one under test: the two paintings that prompted the
question are both bucket 1.

## Condition A — bare, no guide

| # | Subject named | Bucket |
|---|---|---|
| A1 | rain-wet asphalt street at night, red traffic light smeared down the puddles | 3 built/urban |
| A2 | rain-wet asphalt street at night from above, neon sign broken across puddles | 3 built/urban |
| A3 | rain-wet asphalt street at night, low angle, shopfront sign reflected, sign cropped out | 3 built/urban |
| A4 | a dented tin watering can on a wet stone step after rain | 4 still life |
| A5 | rain-wet asphalt street at night from above, streetlight and red signal in puddles | 3 built/urban |
| A6 | rain-wet asphalt street at night close up, streetlights and a traffic signal | 3 built/urban |
| A7 | an enamel basin of water on a windowsill at dusk | 4 still life |
| A8 | an overturned enamel mug on a bare table by a window, tea dried to a ring | 4 still life |

**A: built/urban 5, still life 3, water-with-horizon 0.**

## Condition B — the guide as the sessions read it

| # | Subject named | Bucket |
|---|---|---|
| B1 | rain-wet cobbled street at dusk, one warm lit window reflected down the stones | 3 built/urban |
| B2 | an overturned enamel mug on a bare table by a window, water spreading | 4 still life |
| B3 | rain-wet city street at dusk, figure with umbrella, pale strip of sky, reflection below | 3 built/urban |
| B4 | **low horizon at dusk over wet tidal flats, a groyne post off centre, broken reflection** | **1 water-with-horizon** |
| B5 | rain-wet cobbled street at dusk head-on, lit shop window smeared across the stones | 3 built/urban |
| B6 | a tall window in a dim room, light falling on a bare floor | 3 built/urban |
| B7 | **a bare tree at the edge of a flooded winter field at dusk, low band of pale sky, doubled in the water** | **1 water-with-horizon** |
| B8 | rain-wet city street at dusk from a low doorway, warm window reflected in the pavement | 3 built/urban |

**B: built/urban 5, still life 1, water-with-horizon 2.**

B4 is the estuary almost exactly: tidal flats, a post, a broken reflection, a low
horizon at dusk. Its stated reason names the guide — "large quiet masses laid with a
big brush", "a clean light/mid/dark separation", "edges that can be lost".

## Condition C — the same guide, five landscape clauses neutralised

| # | Subject named | Bucket |
|---|---|---|
| C1 | rain-wet cobbled street at dusk from a low doorway, one warm window | 3 built/urban |
| C2 | rain-wet cobbled street at dusk head-on, lit shop window smeared on the stones | 3 built/urban |
| C3 | rain-soaked cobbled street at dusk, lit shop window, rest into blue-grey mist | 3 built/urban |
| C4 | a window ledge in late afternoon, chipped enamel jug and a fallen pear | 4 still life |
| C5 | rain-wet cobbled street at dusk, lit shop window down the wet stones | 3 built/urban |
| C6 | rain-wet city street at dusk, figure with umbrella against shop-window light | 3 built/urban |
| C7 | a tall window in a dim room, light across an empty chair and floorboards | 3 built/urban |
| C8 | rain-wet cobbled street at dusk, lit window, a figure walking away | 3 built/urban |

**C: built/urban 7, still life 1, water-with-horizon 0.**

---

# The tally

| Condition | built/urban | still life | **water-with-horizon** |
|---|---|---|---|
| **A** bare, no guide | 5 | 3 | **0 of 8** |
| **B** the guide as read | 5 | 1 | **2 of 8** |
| **C** guide, landscape words removed | 7 | 1 | **0 of 8** |

## Against the thresholds fixed beforehand

- *"A at 5 or more → the model's prior; the guide is exonerated and REHEARSAL3.md is
  wrong as stated."* **A = 0.** The estuary is not the model's default.
- *"A low, B at 5 or more → the guide nudges; REHEARSAL3.md stands."* **B = 2.**
  Well below. **REHEARSAL3.md does not stand as written.**
- *"B high and C low, a drop of 4 or more → the words are the lever."* Drop of 2.
  Below threshold. Fisher exact on B vs C is p ≈ 0.47 — directionally consistent,
  statistically nothing.
- *"All three low → happenstance."* This is the outcome closest to what happened.

**So the claim in `REHEARSAL3.md` — "a painter reading that and asked to paint
anything at all will paint a horizontal landscape, because that is the only kind of
picture the vocabulary describes" — is not supported and has been corrected.** Six
of eight sessions that read the real guide named a street or an interior.

## The finding that is much larger than the one being tested

Seventeen of the twenty-four sessions — **71%, in every condition alike** — named a
rain-wet street at dusk or night with a lit window or sign smeared across the wet
ground. Several are near-verbatim matches to each other. Whatever "unprompted"
means here, it does not mean unconstrained: the subject is close to determined
before the guide is opened, and the guide barely moves it.

That is a real answer to the question asked, and it is not the answer this repo had
written down.

## The puzzle the naming task cannot solve

Both real runs painted estuaries. Naming produces streets 71% of the time and
estuaries 8%. Two estuaries in two tries, at 2-in-8 per try, is about a 1-in-16
coincidence — possible, and not comfortable.

The two differ in one large way, and `PREREGISTERED.md` names it as this design's
weakness: **the real sessions had each just spent 250 to 300 strokes painting a
copy.** They had *felt* the engine — the bristle comb, the rectangle that `block_in`
fills, the value floor, the run-out — where these twenty-four have only read about
it. A painter that knows what its hands can do chooses differently from one that has
only read the manual.

That is hypothesis 3, affordances, and the naming design cannot see it. Condition D
below tests it directly.

---

# Condition D — added after the first 24, and labelled as post-hoc

**Not pre-registered.** `PREREGISTERED.md` named "naming is not painting" as this
design's weakness, and the first 24 samples made that weakness the live
explanation, so D tests it: the same guide as B, plus the seven mechanical facts a
session knows only after painting a long copy — the bristle comb above `size=0.12`,
three-quarters coverage, `block_in` filling a rectangle and overshooting it, the
region vocabulary being all rectangles, run-out on long strokes, the `0.23` floor
and no black, and marks below `size=0.003` being unreliable.

Every one of those is a mechanical fact. None of them names a subject, a landscape,
or anything in the world.

| # | Subject named | Bucket |
|---|---|---|
| D1 | **a low winter estuary at dusk, wet tidal flats, dark headland from the right, a pale hull grounded on the mud with its reflection** | **1 water-with-horizon** |
| D2 | rain-wet asphalt street at dusk, streetlamp and its long smeared reflection | 3 built/urban |
| D3 | an overturned wooden chair on a bare floor in a large empty room | 3 built/urban |
| D4 | rain-wet asphalt road head-on to a low horizon, sodium lamp and reflection | 3 built/urban |
| D5 | rain-wet road between hedgerows running into a low bright band of sky | 2 other landscape |
| D6 | **a low wide estuary in late afternoon, broad wet mudflat, dark headland from the left third, a small warm-lit hull far out** | **1 water-with-horizon** |
| D7 | rain-wet asphalt intersection at dusk, streetlight and smeared reflection | 3 built/urban |
| D8 | rain-wet asphalt street at dusk, road filling the lower two-thirds, low wet-grey sky | 3 built/urban |

**D: built/urban 5, other landscape 1, water-with-horizon 2.**

D1 and D6 are the estuary in detail — tidal flats, a headland pushing in from one
side, a small hull, a broken reflection — produced by a prompt containing no
landscape word at all.

---

# The whole result

| Condition | built/urban | still life | other landscape | **water-with-horizon** |
|---|---|---|---|---|
| **A** bare, no guide | 5 | 3 | 0 | **0 of 8** |
| **B** the guide as read | 5 | 1 | 0 | **2 of 8** |
| **C** guide, landscape words removed | 7 | 1 | 0 | **0 of 8** |
| **D** guide + what painting teaches | 5 | 0 | 1 | **2 of 8** |

## 1. The pre-registered claim fails

`REHEARSAL3.md` said a painter given this guide "will paint a horizontal landscape,
because that is the only kind of picture the vocabulary describes". The threshold
fixed beforehand was 5 of 8. **B is 2 of 8**, and six of the eight named a street or
an interior. The claim is wrong as written and has been corrected in
`REHEARSAL3.md`.

## 2. The estuary is not the model's prior either

**A is 0 of 8.** Whatever makes these sessions paint estuaries, it is not something
they would have done anyway. That rules out the comfortable explanation.

## 3. Every estuary in the experiment came from a condition containing the words

Pooling the two conditions that carry the guide's landscape clauses against the two
that do not — **post-hoc pooling, so weigh it accordingly**:

| | water-with-horizon | other |
|---|---|---|
| words present (B + D) | **4** | 12 |
| words absent (A + C) | **0** | 16 |

Fisher exact, two-tailed: **p ≈ 0.10**. Not significant at any conventional bar, and
the direction is perfectly clean across 32 samples: five clauses of prose, totalling
about thirty words in a 981-line document, are the only thing separating four
estuaries from none. Suggestive. Not proven. Worth its own pre-registered test with
a real n before anyone acts on it.

## 4. The larger effect is on composition, not subject

This is the finding worth keeping, and it is **post-hoc** — read it as a hypothesis
that earned a test, not as a result.

Count the samples whose stated reason explicitly invokes horizontal bands or
axis-aligned rectangles as *why the subject was chosen*:

- **A** (no guide): 0 of 8 — none of them can, they have not been told anything.
- **B** (guide): about 2 of 8, and vaguely — "large quiet masses", "a pale strip of
  sky".
- **D** (guide + what painting teaches): **6 of 8, explicitly.**

> D2: "the whole subject is bands and horizontals — so the rectangular regions are
> working for me instead of against me."
> D8: "two big quiet horizontal masses that `flat` and crossed passes handle well
> and that `block_in` can actually fill honestly (they genuinely are bands, not
> silhouettes)."
> D1: "horizontal bands are honest rectangles for `flat` block-ins."

**Telling a painter what the engine is bad at makes it choose pictures made of
horizontal bands, and say so in as many words.** The noun varies — estuary, street,
road, empty room — but the *composition* converges, and composition is what the
human's eye caught and what `probe_axis_alignment.py` measures. A wet street at dusk
chosen because "the road and sky are two big quiet horizontal masses" is the same
painting as an estuary chosen for the same reason.

That is hypothesis 3, affordances, and it is a better account of the axis-alignment
numbers than the subject nouns ever were.

## 5. So: how unprompted is unprompted?

**Barely, but not for the reason this repo had written down.**

- Twenty of thirty-two sessions — **63%, in every condition alike** — named a
  rain-wet street or road at dusk with a light smeared across the wet ground, often
  in near-identical words. The subject is close to determined before the guide is
  opened. The unprompted stage is not measuring an unprompted choice, and it never
  was.
- The estuary specifically is *not* that prior. It appears only alongside the
  guide's landscape words, 4 times in 16, never in 16 without them.
- And the thing that actually transfers from the tool to the picture is not the
  subject at all. It is the **band**.

The two paintings that started this were not happenstance and were not the model
talking to itself. They are what happens when a painter that has learned this
engine's limits picks a picture those limits can carry — which is the same finding
as the human's first note, arrived at from the other end.
