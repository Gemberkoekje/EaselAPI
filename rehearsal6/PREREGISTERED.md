# Written before the paintings existed

`rehearsal6/pass/` and `rehearsal6/sitter/` held a reference photograph and nothing
else when this file was written. Everything below is decided here so that no reading
of a result can be chosen after seeing it.

## Pre-run checks the brief requires

The brief makes two checks a precondition of the pass, not a formality: the guide may
not name anything in the reference, and somebody must read the guide's examples and
try to name a subject. Both were run against `PAINTER.md` at `8e83459`.

**1. The grep.** Clean on both references. No `mug`, `cup`, `teacup`, `teabag`,
`spoon`, `saucer`, `crewmate`; no `face`, `portrait`, `sitter`, `hair`, `beard`,
`glove`, `coat`. `table` occurs nine times and every one is a table *of numbers*
(`the mean colour is in the table too`, `a table of each one's share`). `hand`
occurs once, as `the hand working down`. `hull` and `window` occur as API terms.

**2. Naming the subject.** All 49 python blocks in the guide were extracted and every
quoted name in them read: `dark`, `shadow`, `light`, `far`, `near`, `mid`, `base`,
`lit`, `top_l`, `top_r`, `edge`, `corrected_colour`, plus brushes and pigments.
**No block names a paintable object.** The seven nouns REHEARSAL5 found are gone and
nothing replaced them.

**3. The first of two borderline items, recorded rather than fixed.** `PAINTER.md:622` reads *"a
painter reaches for the texture of what it is — grain, weave, brick, ripple"*, and the
paragraph then works its example on grain: *"if a surface has a grain, the grain
varies: it breaks, it crosses, it disappears for a whole passage."* The mug
photograph's largest mass is a wooden table whose texture is grain. By the letter of
the leak rule — any list is a ranked list, and its first item is the answer — this is
a four-item list whose first item is the thing the reference's background is made of.

It is left standing, for the reason `NOTES.md` item 0c gives: guide changes are made
and no more are to be made before the next run. It is not a subject and it carries a
rule rather than a picture (*the grain varies*, which is an instruction to break it up,
not to paint one). **But it is on the record here, before the run, and if the table
comes out well it is the first thing to suspect.**

**4. The second, on the other reference.** `PAINTER.md:240` reads *"this is the whole
method at that scale — a knuckle, a hinge, a fold, a catchlight"*. The sitter
photograph's foreground is a pair of gloved hands held up beside the face, knuckles
forward, and *knuckle* is the first item of that four-item list.

It is left standing for the same reason as item 3, and it bites less: the sitter run is
the reach measure, not the pass, so no pass criterion depends on it. It is recorded
because the leak rule's whole point is that a leak *in* hides — the only symptom is that
the number improves — and because two lists in one guide, each with a reference's own
material at the head of it, is a pattern rather than an accident. **If the run's hands
come out better than its face, this is the first thing to suspect.**

**What both items say about the rule as written.** The brief's remedy for the boat was
"a guide example may not name a paintable object at all". Neither of these names an
object: a knuckle is a scale, a grain is a texture. Both are nonetheless the first word
of a list, and both happen to be the material of a reference. Whether the rule needs to
reach lists of non-objects is a question for after this run, and it is asked here so
that asking it later cannot look like a result-shaped conclusion.

## The unprompted pair

The measurement is `probe_structure.py`, and the baseline below was measured before
either painting existed. Seven unprompted paintings and the two references:

```
                            band dB    horiz%    vert%    dark mass from centre
  REHEARSAL5 unprompted 1    +23.83     31.5      6.2    0.055  (-0.004, +0.055)
  REHEARSAL2 unprompted      +16.60     41.3      5.9    0.093  (-0.014, +0.092)
  REHEARSAL3 unprompted      +13.51     36.1      6.8    0.044  (-0.007, +0.043)
  REHEARSAL1 unprompted      +10.93     25.4      6.6    0.104  (-0.028, +0.100)
  REHEARSAL4 unprompted 1     +8.37     29.8      7.4    0.070  (-0.016, +0.068)
  REHEARSAL4 unprompted 2     +0.09      8.4      9.0    0.010  (+0.006, +0.008)
  REHEARSAL5 unprompted 2     -3.00     18.4      9.8    0.002  (-0.001, +0.002)

  Level1 (the mug photo)      -8.40     10.4     12.4    0.017  (-0.016, -0.005)
  Level3 (the sitter photo)   +1.51     13.5     17.8    0.034  (-0.005, +0.034)
```

Five *first* unprompted paintings, five stacks of horizontal bands: `+8.4` to `+23.8`
dB, with four to six times as many near-horizontal strong edges as near-vertical.
Both *second* paintings, made under the differ-in-structure constraint, sit at `+0.1`
and `-3.0`. The constraint has moved the number twice; the question is whether it
does it a third time, and whether the first painting is a band-stack a third time.

**What would count**, decided in advance and unchanged from REHEARSAL4:

- A **break** is the second painting landing at least `8` dB below the first *and*
  reversing or levelling the edge split — near-vertical strong edges at least as
  common as near-horizontal, or the two within a factor of `1.5`.
- A **partial break** is one of those without the other, or a band-dB gap between `4`
  and `8`.
- **No break** is a gap under `4` dB with the edge split unchanged in character.

The first painting is not being judged. If it lands at `+14` dB like its five
predecessors that is a finding about the guide, not a failure by the painter.

## The two numbers on the copy, and the procedural rule

REHEARSAL5's painter met the value criterion by laying a bar of dark it knew was bad,
and said so. The brief's answer is a second number and a rule, and both apply here for
the first time:

- **`compare()`**: no cell on the object more than `0.10` out. Told to the painter, in
  the brief's own words, as REHEARSAL4 told it.
- **`probe_human_notes.py`'s containment**: the share of the dark mass's paint that
  lands where the reference has nothing like it. **Not told to the painter.** No single
  mark can improve this and the value number at once, which is the whole point of it.
- **The last ten strokes of a copy may not be value corrections**, and the log must say
  what they were for. Told to the painter, because nothing else carries it: it is a
  protocol rule and `PAINTER.md` does not mention it.

## What is deliberately not in the prompts

**The signature.** `PAINTER.md:1263` tells a painter to sign a finished picture and
what the mark may not be. The prompts say nothing about it, so an unsigned painting is
a finding about whether the guide's instruction lands — which is the only reason to put
an instruction in a guide rather than in a prompt.

**Everything the probes measure.** Neither prompt contains the words band, axis,
horizontal, vertical, containment, structure, escape, or any instruction about marks.
Neither painter is told what changed in the guide, that anything changed, that this run
is compared against an earlier one, or that these baselines exist.

## What this cannot tell anyone

The two painters are fresh contexts in the same container as the session that launched
them, not two separate Claude Code sessions on two machines as in REHEARSAL4. They were
given the guide, the reference and the prompt below and nothing else, and the honesty of
"do not open the source" is theirs as it was in every earlier run — but the difference
in mechanism is real and is stated here rather than in a footnote.

The human looking at the paintings is still the verdict. Everything here says only how
they differ.
