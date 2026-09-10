# Written before the paintings existed

The brief's second unprompted painting is "partly a capability probe rather than a
free choice", and a probe whose reading is chosen after seeing the result measures
nothing. So the baseline and what would count as a break are written down here first,
at a point where `rehearsal4/pass/` held one empty session file and no exports.

## The baseline

`probe_structure.py`, run before either painting existed. Every unprompted painting
this engine has produced so far, and the two references for scale:

```
                              band dB    horiz%    vert%    dark mass from centre
  REHEARSAL3 unprompted       +13.51     36.1      6.8    0.044  (-0.007, +0.043)
  REHEARSAL2 unprompted       +16.60     41.3      5.9    0.093  (-0.014, +0.092)
  REHEARSAL1 unprompted       +10.93     25.4      6.6    0.104  (-0.028, +0.100)

  Level1 (the mug photo)       -8.40     10.4     12.4    0.017  (-0.016, -0.005)
  Level3 (the sitter photo)    +1.51     13.5     17.8    0.034  (-0.005, +0.034)
```

Three independent unprompted paintings, three stacks of horizontal bands: `+10.9` to
`+16.6` dB, with four to seven times as many near-horizontal strong edges as
near-vertical ones. Neither photograph is anything like that. The thing the brief is
asking about is real and it is large.

## What would count

**The first painting is not being judged.** It is unconstrained, and if it lands at
`+14` dB like its three predecessors that is a finding about the guide, not a failure
by the painter.

**For the second**, decided in advance:

- A **break** is the second painting landing at least `8` dB below the first *and*
  reversing or levelling the edge split — near-vertical strong edges at least as
  common as near-horizontal, or the two within a factor of `1.5`.
- A **partial break** is one of those two without the other, or a band-dB gap between
  `4` and `8`.
- **No break** is a gap under `4` dB with the edge split unchanged in character: the
  second painting is another stack of bands, whatever it is a picture of.

`probe_axis_alignment.py` is reported alongside because the brief names it, but it
folds the two axes together and cannot see a picture swapping one for the other. That
is why `probe_structure.py` exists, and why it was written before the paintings.

## What this cannot tell anyone

A number that goes the right way because the painter aimed at the number would be
worth nothing, which is why the painters were told the constraint in the brief's own
words -- "differ in compositional structure" -- and were not told that anything gets
measured, what gets measured, or that these baselines exist. Neither prompt contains
the words band, axis, horizontal, vertical, structure-the-measurement, or any
instruction about marks. The prompts are in `launch_note.md`, in full.

The human looking at the pair is still the verdict. This only says how they differ.
