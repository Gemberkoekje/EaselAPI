# Questions for the painter, after filing

*Written to be pasted into the painting session as it stands, by the owner. The answers
are filed beside the painting as `answers.md`, verbatim. Questions A to E are
`PLAN-0.8.0.md`'s question 2 (its follow-up), 5, 6, 7 and 8; its questions 1 and 3 were
answered from the painting session's transcript and are not asked. Kept as it was put:
one sentence in it is wrong, and the painter's answers correct it — the glint in the
picture is the glaze, and the ember under it did not land either.*

---

Your painting and your verdict are filed in the EaselAPI repository, with the pack's
details left out, and the next release acts on the verdict — every point you raised has a
proposed answer. The owner's ruling is that the tool is for painters, so where a proposal
turns on a choice about how the tool should behave, the choice is yours. Four of those can
be asked now; three more — the thumbnail's size, the candidates for a turning edge, and a
darker dark — will come later, with pictures to compare blind.

Please answer each with your evidence where you have it, say so where you have none, and
label each answer **M** (you measured it), **O** (you observed it) or **R** (you reasoned
it).

**First, two things your own session showed when the painting was filed**, because one of
them changes a question:

- **The highlights at `0.52` instead of `0.64`.** The details pass's second rehearsal
  read the head's top plane at `0.52` on the `lightest:` line, before the two `s.dry()`
  calls were added; its third rehearsal, after them, read it at `0.52` again — and at the
  time you put the reading down to the eye inside the plane. The `0.64` was the value you
  mixed the plane at. The `0.52` is the plan's reading of the whole plane with the eye in
  it: by its median the plane reads `0.61`, and 14% of its pixels are under `0.35`.
- **The spark in the eye did not land.** The last mark of the finishing pass, a
  `round_hard` dab at `size=0.0028`, changed two pixels, by at most 21 levels of 255;
  `easel log` lists it as *NO PAINT LANDED*. The glint in the picture is the ember under
  it.

**Question A.** Given the above: is there any other place — in this painting, a
rehearsal, or the exercises — where you saw a light land dull in wet paint? If there is
none, the warning you suggested has no case yet, and the round records that rather than
building it.

**Question B — what a planned place reads.** Today every planned place is read by its
mean, which is how the eye pulled the head's top down to `0.52`. The candidates: **(1)**
its median, one number for both the `plan:` and the `lightest:` lines — the head's top
reads `0.61`, inside its plan; **(2)** its brightest part (the 75th or 90th percentile,
`0.62` or `0.63`) for `lightest:` alone, keeping the mean for `plan:`. The one other
painting with a plan keeps every verdict under all of them. Which should it be? And
should a place split between two values say so — *head top reads 0.61, 14% of it under
0.35*?

**Question C — declaring a key.** A plan would take `key="low"` (or `"high"`), as it
takes `ground="buried"`. The `values:` line would stop saying *no clear light* — it said
so on 25 of your 27 reports — and ask the question it never reaches for a dark picture:
whether its clusters are a light, a mid and a dark *inside* the key, or two of them read
as one (your bottom two were `0.07` apart). What should `key="low"` hold you to: **(1)**
the top twentieth of the picture staying under the palette's middle, `0.54`; **(2)** a
top you name, `key=("low", 0.40)`; or **(3)** only the clusters inside the key, and no
ceiling?

**Question D — the documentation.** The proposal takes your eighth suggestion: move the
commentary on the documents and the anecdotes out of `PAINTER.md` into `CALIBRATION.md`
and `LESSONS.md`, keeping beside each rule only the one sentence of evidence that
persuades, and leave a first page someone could start painting from alone. The anecdotes
in the file today include *one painter chose the underside of a pier*, *one painting lost
eighty strokes to four near-parallel fingers*, *one painter redrew an arrangement three
times*, *one painter finished a whole picture without opening any of the other four*,
*one painting spent about eighty strokes on four treatments*, and four sentences that
begin *every painter so far*. **Which of them persuaded you** — which should stay beside
their rule? And **did the card alone carry what you needed to start**? (Your session
shows you read `PAINTER.md` to line 700 of 754, `REFERENCE.md` to line 520 of 723 and
twelve of `RECIPES.md`'s twenty-one entries.)

**Question E — what a pass cost, call by call.** Under a pass's total, a line would name
the calls that cost more than one stroke, each with its strokes, its verb and the line of
your script it was called from. On your committed subject pass it would read:

```
Rehearsed p04_gargoyle.py: 102 strokes of the 210 left. Nothing committed.
  dearest: 23 block_in at p04_gargoyle.py:40 (lay_body), 22 at :38, 20 at :36, 14 at :18 -- 79 of the 102
```

Should it come after every pass, or only after rehearsed and counted ones? Should it
name the script line, the function, or both? And three calls, or four?
