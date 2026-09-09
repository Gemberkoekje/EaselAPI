# How unprompted is unprompted? — pre-registered before the data came in

Raised by the repo's owner, looking at the two unprompted paintings side by side:

> These are the 2 unprompted paintings that were made in the earlier M5 and this M5.
> They are obviously not the same, but it is similar. So just as like an adversarial
> check: How unprompted is unprompted? Did they get to the same result by pure
> happenstance, or is something nudging them?

`REHEARSAL3.md` already asserts an answer — *The guide chooses the subject* — on the
strength of two paintings and a reading of the guide's vocabulary. Two is not a
sample and a reading is not a measurement. This is the check.

**Written before the results, so the analysis cannot be fitted to them.**

## What is already known, and what it rules out

- **n = 2.** REHEARSAL2's fresh session and REHEARSAL3's `pass/` session, months and
  contexts apart, both painted an estuary at low tide with mooring posts.
- **The reference is not the nudge.** The two sessions copied entirely different
  photographs first — a dim interior with a man gesturing, and a mug on a table —
  and both then painted the same subject. Whatever is steering them, it is not what
  they had just been practising.
- **The subject and the artefact match.** Both paintings are the squarest things in
  the repo (47.2 % and 42.9 % axis-aligned edges, against 22.8-31.3 % for the
  references). A horizontal-band seascape is exactly the picture that an
  axis-aligned toolset paints well.

## The four hypotheses

1. **The guide nudges.** Its vocabulary and worked examples steer the choice.
2. **The model's own prior.** Claude asked to paint anything reaches for a
   landscape regardless of tooling, and the guide is innocent.
3. **The affordances nudge.** What is *easy* to paint gets painted, independent of
   the words: `block_in` on rectangles makes bands, so bands get chosen.
4. **Happenstance.** n = 2.

Hypotheses 1 and 3 both indict the tool; they differ in whether the fix is words or
capability. Hypothesis 2 exonerates it. These are not exclusive and the interesting
outcome is a mixture.

## The experiment

Fresh sessions, one sample each, asked only to **name** a subject. No painting: the
choice is what is being measured, and naming is cheap enough to run a real sample.
Every agent is told not to read any other file in the repo.

| Condition | What it gets | Isolates |
|---|---|---|
| **A — bare** | A neutral one-line description of the medium. No guide. | The model's prior (hypothesis 2) |
| **B — guide** | `PAINTER.md` in full, as a real run gets it | Prior + guide (1) |
| **C — guide, neutralised** | `PAINTER.md` with every landscape noun in its prose and examples swapped for a non-landscape one, and `horizon()` renamed. Same API, same advice, same length. | Whether the *words* are the lever (1 vs 3) |

Eight samples per condition.

C is the discriminating condition. If B floods with seascapes and C does not, the
examples are the lever and the fix is a rewrite. If C floods too, the words are not
the lever and the fix is in the API's shape — hypothesis 3, which is a milestone,
not an edit.

## Classification, fixed now

Each answer goes in exactly one bucket, by its primary subject:

1. **Water-with-horizon** — sea, estuary, shore, lake, harbour, marsh, any subject
   whose structure is a horizontal band of water under a band of sky. **This is the
   bucket under test.**
2. **Other landscape** — hills, mountains, forest, field, desert, without water as
   the organising band.
3. **Built or urban** — street, roof, interior architecture, window.
4. **Still life or object** — table, fruit, vessel, cloth.
5. **Figure** — a person or animal as the subject.
6. **Abstract or non-representational.**
7. **Other** — anything that fits none of the above; listed verbatim in the results.

A "sky and cloud study" with no water and no land counts as **other**, not 1.
A shoreline seen from a cliff is **1**, because the band structure is the criterion.

## The threshold, fixed now

The two paintings that prompted this are bucket 1. Treat the null as "bucket 1 is
one option among roughly seven", so chance is on the order of 1-2 of 8.

- **Condition A at 5 or more of 8** → the model's prior. The guide is largely
  exonerated and `REHEARSAL3.md`'s claim is wrong as stated.
- **A low, B at 5 or more** → the guide nudges. `REHEARSAL3.md` stands.
- **B high and C low** (a drop of 4 or more) → the words are the lever.
- **B high and C also high** → the affordances are the lever, not the words.
- **All three low** → happenstance, and two paintings agreeing was luck.

Whatever comes back gets written up, including the outcome where the claim already
in `REHEARSAL3.md` turns out to be wrong.

## Weaknesses of this design, stated up front

- **Naming is not painting.** A session that names "a harbour" might paint something
  else once it has the brushes in its hands. This measures the choice, which is what
  the question is about, but it is not the same act.
- **n = 8 per cell** is enough to separate 1-of-8 from 6-of-8 and not enough to
  argue about 3 versus 5.
- **The neutralised guide is my rewrite**, so condition C tests my idea of which
  words matter. If C comes back low, the honest claim is "these particular words
  mattered", not "words in general".
- **One sample per session, and the sessions share a model.** This measures the
  system as it is actually run, not a property of guides in general.
