# REHEARSAL6 — the definition of done, run end to end again

**To understand this, start by reading the brief's *Definition of done* section
(`painting-api-brief.md`), then `rehearsal6/PREREGISTERED.md` (written before the
paintings existed, and it decides how the unprompted pair is read), then this file,
then `rehearsal6/pass/LOG.md` and `rehearsal6/sitter/LOG.md` — each painter in its own
words. `rehearsal6/launch_note.md` holds both prompts in full.**

Two fresh sessions, launched in parallel, each given `PAINTER.md` and `CALIBRATION.md`
and nothing else: no `src/`, no `NOTES.md`, no `REVIEW.md`, no brief, no earlier
rehearsal, no docstrings, no `help()`. Neither was told what changed in the guide, that
anything had changed, or that anything was being measured.

**This is the first run measured on two numbers rather than one**, the first under the
rule that the last ten strokes of a copy may not be value corrections, and the first
where a signed painting was expected. All three exist because REHEARSAL5's painter met
the value criterion by laying a bar of dark it knew was bad, and said so.

Every number below is re-measured from the exported PNGs and the saved sessions by
`rehearsal6/verify_done.py`, which imports REHEARSAL4's checks by path rather than
re-implementing them, so the two runs come out of the same instrument. Where a
painter's log and a script disagree, the script wins.

| Run | Reference | Stage |
|---|---|---|
| `rehearsal6/pass/` | `Level1.jpg`, a mug on a table | The copy, then the two unprompted paintings |
| `rehearsal6/sitter/` | `Level3.jpg`, the sitter | How far the tools reach |

Both references are byte-identical to REHEARSAL4's, so the runs are on the same
photographs.

---

## The verdict first

**Every criterion in the brief is met, including the one REHEARSAL4 failed, and the
unprompted pair broke its own composition by the widest margin any run has managed.**
The three additions the brief made after REHEARSAL5 all did what they were added to do.

| Criterion | Result |
|---|---|
| Recognisable copy of an ordinary object | **Pass.** A pale mug of black tea, spoon, handle, cast shadow, teabag tag on its string, and the printed figure on the mug's front legible. |
| Under 300 strokes | **Pass.** 291 charged on the mug, 298 on the sitter. |
| Without touching source code | **Pass.** `git status` clean across `src/`, `tests/`, `scripts/`, `examples/`, both guide files. |
| No cell **on the object** more than `0.10` out | **Pass.** 0 of 64 cells out on the mug — the whole picture, not just the object. Worst `0.0987`. |
| Strokes rejected in `preview()`/`rehearse()` **before painting them** | **Pass, and not narrowly.** 5 previews and 11 rehearsals on the pass run, 2 and 6 on the sitter. Eight marks on the mug alone were judged and accepted or refused before they were paid for. **This is the criterion REHEARSAL4 failed.** |
| Headline run without `sketch(reference)` | **Pass**, from the engine's own record: `assisted=[]` on all four sessions. |
| Two unprompted paintings | **Pass.** 203 and 155 strokes. |
| The second not repeating the first's composition | **Pass**, on both pre-registered clauses, by the widest margin of any run. |
| Every finished painting signed | **Pass.** All four, 1–2 marks each, neither prompt having mentioned it. |
| The last ten strokes not value corrections | **Pass** on both copies, and see below — the sitter run declined the temptation explicitly. |
| All exports plus time-lapses exist | **Pass.** 8 of 8. |
| Golden-image tests still pass | **Pass.** 279 passed, 3 skipped, no golden regenerated. |
| The sitter: how far do the tools reach? | Answered below. Not a pass criterion. |

**And the ticks are worth less than three things that are not in the table.**

1. **The dark still leaves the cup.** Containment `13.2%`, against REHEARSAL5's `16.3`
   and REHEARSAL4's `17.5` — an improvement, and still two orders of magnitude worse
   than REHEARSAL3's `0.1`. This is the third consecutive run in which the guide's
   depth-order paragraph has not done its job.
2. **Two independent painters found the same false promise in the guide**, and one of
   them lost a mark from a finished painting to it.
3. **The value criterion is saturated and has been for three runs.** Worst cell
   `0.0987`, `0.0961`, `0.0985` on the last three mugs against a `0.10` threshold. A
   criterion that three different painters clear by a thousandth is not measuring
   anything any more.

---

## The three additions, and whether they worked

### The second number: it moved, and not enough

`probe_human_notes.py`'s containment — the share of the dark mass's paint that lands
where the reference has nothing like it.

| | containment | worst excursion |
|---|---|---|
| REHEARSAL3 | **0.1 %** | 0.046 of the width |
| REHEARSAL4 | 17.5 % | 0.150 |
| REHEARSAL5 | 16.3 % | 0.279 |
| **REHEARSAL6** | **13.2 %** | **0.140** |

The excursion is half REHEARSAL5's and the share is the best of the three post-M6
runs, but the tea still runs over the rim on the left and you can see it in the
painting. **The brief's reason for adding this number is confirmed**: the value
criterion reports 0 of 64 cells out on this picture, and a defect a human can see at a
glance is invisible to it. The second number caught what the first cannot.

What it does not do is fix the paragraph. Three runs have now read the guide's far
edge / inside / near edge rule and painted the liquid over the rim anyway. **The rule
is not operative as written**, and REHEARSAL5's two readings have become one: this is
no longer one painter's habits.

### The procedural rule: it worked, and it was tested

Both copies pass. The pass run's last ten were the visor and its light core, the rim
light, the lip accent, the tag, its label, the string, the stray hair on the table,
and two smudges deliberately losing the shadow's edge and the mug's left silhouette —
sizes `0.004` to `0.052`, and its own account is that it finished all value work at
`#294` and checked `compare()` came back clean before starting them.

**The sitter run is the one that matters, because it was tempted and said so.** It
found cell E4 out of tolerance with `compare(region=cell("E4"))` in its closing marks,
and painted a cheek plane rather than the number:

> If I had been chasing the number I would have painted the pale stripe in rehearsal
> 034, which would have fixed E4 and ruined the jaw.

That rehearsal is kept, at `rehearsal6/sitter/rejected/copy_03_pale_stripe_would_fix_E4_and_ruin_the_jaw.png`.
**This is REHEARSAL5's failure mode arriving and being declined**, on the record, by a
painter that did not know the rule existed for that reason. It cost nothing to enforce,
exactly as the brief predicted.

### The signature: it landed, and the guide lies about it

All four paintings are signed, by two painters, neither of whom was told to. The guide
carried it on its own, which is the whole argument for putting a thing in a guide
rather than in a prompt.

**And the exemption it promises does not exist.** `PAINTER.md:1265`:

> **Up to five marks, and they do not come out of your stroke budget**, so long as
> each one carries `note="signature"`.

`History.stroke_count` (`src/easel/history.py:87`) counts every record whose kind is
not `dry`, `look`, `pencil` or `erase`. A signature mark is a `stroke`. Both painters
found this independently, from opposite directions:

- The **pass** painter watched `stroke_count` go `291 → 292` and wrote: *"the exemption
  is bookkeeping for a human reader, not for the counter. It did not cost me anything
  here, but somebody planning to 299 will lose."*
- The **sitter** painter *was* planning to 299. Two signature strokes took it to 301,
  and it undid, dropped **the mole on the sitter's neck** — a real, specific feature of
  that particular face — and re-signed with one mark.

The exemption exists in exactly one place: `SIGNATURE_ALLOWANCE` in
`rehearsal4/verify_done.py`, a verification script no painter ever sees. **A guide that
promises a budget the engine does not honour costs a painting a mark**, and this run is
how that was found out.

---

## The five questions REHEARSAL5 asked, one run later

| | R4 | R5 | **R6** | |
|---|---|---|---|---|
| 1. Dark stayed inside its container | 17.5 %, 0.150 wide | 16.3 %, 0.279 | **13.2 %, 0.140** | **better, still failing** |
| 2. Finished work buried by later masses | 117.7 %, 18 marks | 46.6 %, 15 | **16.1 %, 11** | **better again** |
| 3. Axis-aligned edges (photo 22.8 %) | 26.2 % | 37.3 % | **26.9 %** | **the backfire is gone** |
| 4. Marks judged before payment | 1 preview, 0 rehearse | 4, 5 | **5 preview, 11 rehearse** | **best of the three** |
| 5. Value criterion | 0 of 64, worst 0.0985 | 0 of 64, worst 0.0961 | **0 of 64, worst 0.0987** | **holds, saturated** |

**Question 3 is the one to read carefully.** REHEARSAL5's background rewrite made the
picture *squarer* — 37.3% against a photograph's 22.8% — and the fix was to add the
missing half, *"and the marks inside it are not parallel lines"*. This run came in at
26.9%, back to REHEARSAL4's level. The table on the mug is broken, varied grain rather
than a field of horizontal streaks. **That is one run and one painter**, and the same
caution REHEARSAL5 stated applies here in full: this is an observation, not an effect.

**Question 2 keeps improving and the burying that remains is one habit.** Five of the
eleven marks are the same `block-in A1:C8 22.0` — the left third repainted over
finished work, four times. The whole-canvas repaint is gone; the whole-*column* repaint
is not.

---

## The unprompted pair

**The author of the engine has not seen these two paintings.** They were built, measured
and handed to the human unopened, as the brief requires. What follows is the numbers and
the painter's own words about them.

`PREREGISTERED.md` fixed the reading before they existed. A **break** is the second
painting landing at least `8` dB below the first *and* reversing or levelling the edge
split.

```
                                     band dB    horiz%    vert%    dark mass from centre
  REHEARSAL6 unprompted 1 (free)       +8.12     33.4      5.3    0.034  (-0.016, -0.030)
  REHEARSAL6 unprompted 2 (differ)     -9.52      9.4     30.5    0.014  (-0.006, -0.013)
```

- **Band gap `17.6` dB**, against a threshold of 8.
- **The edge split reversed**, not merely levelled: near-vertical strong edges are
  `3.2×` as common as near-horizontal, where the first painting had the opposite ratio
  at `6.3×`.

**A full break on both clauses, and the widest of any run.** For scale: REHEARSAL4
broke by `8.28` dB with a levelled split (8.4 / 9.0); REHEARSAL5 broke on band dB by
`26.8` but kept a horizontal-dominant split (18.4 / 9.8), which is a partial break by
these criteria. REHEARSAL6 is the first to reverse the axis outright.

**The first painting is a stack of bands for the sixth time running.** `+8.12` dB with
five times as many horizontal strong edges as vertical, which is the same shape as
REHEARSAL1 through 5. The brief said this would not be a failure by the painter, and it
is not. It is a fact about what this model reaches for unprompted, and
`rehearsal5/naming/` has already settled that it is not a thing sessions *name*.

The painter's own account of how it made the second one differ, which is the part being
measured:

> own1 is banded, diagonal, deep-space, landscape, focal point on the right third.
> own2 is its structural opposite: portrait, axial, near-symmetric, radiating from one
> point on the centre line, shallow, subject cropped top and bottom, no focal object at
> all.

Nothing in the prompt said axis, band, structure, or anything about marks. Working out
what "compositional structure" meant was the thing being observed, and it enumerated
six axes and inverted all of them.

Both are signed. Both have time-lapses. `rehearsal6/unprompted_pair.png` is the sheet.

---

## Reach: the sitter

**Recognisable as the photograph, not as the person**, which is the painter's own
answer and matches the picture. Pose, key, composition and the whole value map are
there; the face is a mask with a dot for an eye.

- **Got there:** the head's silhouette and the hair mass, the brow-nose-lip profile,
  the beard as a mass with a lit jaw plane above it, the open mouth, the eye's
  *position*, and the value structure.
- **Defeated it:** the eye itself — *"this photograph is a picture of a man's stare,
  and I got a dot and a smudge with no lids and no gaze"* — the moustache and nostril,
  the face's proportion (a landmark on the bridge rather than the tip, found at 6× with
  thirty strokes left), hair as strands, the hands, and the four other people.

**The axis probe is not diagnostic on this reference and that is worth recording.** The
copy reads 30.5% against the photograph's own 31.3%, because the photograph is a room
full of axis-aligned edges. On the mug, where the photo is 22.8%, the probe still
separates a square painting from a square subject. On the sitter it cannot, and a
number that agrees with the reference here means nothing.

**The reason the face is unfinished is arithmetic, and the guide has no rule for it.**
176 of 299 strokes were spent before the subject existed. The guide warns about
spending too much on detail and too little on structure; this is the opposite failure
and nothing covers it. The painter's proposed rule is the right one: **decide what
fraction of the budget the subject gets before the first stroke, and spend the
background out of what remains.**

---

## What the guide got wrong, checked rather than believed

Every claim below was reproduced against the engine before it was written down. None
of it is fixed here — the run's own criterion is that no source was touched, and
`NOTES.md` item 0c forbids guide edits before a run, not after one.

| # | Claim | Checked |
|---|---|---|
| 1 | **Signature marks are charged.** `PAINTER.md:1265` promises they are not. | Confirmed at `src/easel/history.py:87` and reproduced: `stroke_count` `1 → 2` on a mark noted `signature`. Found independently by both painters; cost the sitter a real mark. |
| 2 | **`block_in` on a curved `ribbon` costs its box, not its width.** The guide says both "the passes are counted across the mass, not over its area" and "a shaped mass costs what its box costs", and for a curved ribbon those disagree. | Confirmed and sharper than reported. A ribbon `0.029` wide at brush `0.015` costs **19 passes** curved and **3 straight** — same width, same brush. The painter budgeted 4 and paid 21, which is 7% of the budget on one call. |
| 3 | **`inset()` on a concave shape takes far more than a rim.** The guide offers "`inset()` the shape by half the brush size" unqualified; CALIBRATION's 99%-coverage figure is measured on a convex blob. | Confirmed. On the sitter's own 15-point coat outline, `inset(0.052)` keeps **62.7%** of the area. The block-in then covered 98.4% of the inset shape and **76.2% of the actual coat**, with the near arm at 15.5%. The painter did not find the hole until `compare()` showed it twenty strokes later. |
| 4 | **Exercise 1's `at_value()` only searches upward.** The guide hands a painter that function and does not say so. | Confirmed. Asked for a value below the base it returns ratio `0.000` and hands back the base. The sitter painter painted a field at 0.41 having asked for 0.30. |
| 5 | **`sweep(cross=0)` raises**, while omitting `cross` works and CALIBRATION tabulates an uncrossed sweep as an option. | Confirmed: `ValueError`. The message is a good one; nothing in the guide warns the argument is not zeroable. |
| 6 | **`undo(n)` counts log entries, not paid marks.** | Confirmed: `undo(2)` over a stroke and a pencil line gives back one stroke. |

And five more from the logs, not separately reproduced here, each of which cost its
painter strokes:

- **Nothing in the guide says how to bury something.** *"'When something is wrong,
  paint over it' — with what?"* A bristle leaves the old paint showing between streaks,
  a flat leaves a rectangle, a round tip leaves a capsule. The pass painter spent about
  fifteen strokes across three paintings arriving at the answer, and it belongs in the
  guide: a long stroke, solid tip, `load=1.0`, full opacity, run along the grain of
  what is there so its own ends fall outside the repair.
- **The brush table needs its converse warnings.** It says a short `flat` is a
  rectangle; it does not say a short `round_hard` is a capsule, which is as loud a tell.
- **`smudge` works along a boundary and fails across one** — and the guide demonstrates
  it across.
- **`look(region=)` pads the crop** beyond the span asked for, which broke two rounds
  of the sitter painter's pixel arithmetic.
- **The two closing rules pull against each other.** "Spend the last third of your
  strokes on what is around the thing you measured" and "the last ten may not be value
  corrections": every near mass laid late knocked a cell back out, so the pass painter
  had to stop correcting early and deliberately. The guide does not say which wins.

---

## What this run cannot tell anyone

**The two painters were fresh contexts launched into the same container, not two
separate Claude Code sessions on a machine as in REHEARSAL4.** Each began with its
prompt and no other history, and "do not open the source" was honoured by the painter
rather than enforced — as in every earlier run. The difference in mechanism is real and
is stated here rather than in a footnote.

**Two borderline leak items were recorded before the run and neither fired.**
`PREREGISTERED.md` flagged that *grain* heads a list in the background paragraph while
the mug's table is wood grain, and that *knuckle* heads a list at detail scale while
the sitter's foreground is a pair of hands. The prediction written down in advance was
that if either mass came out unusually well, the list was the reason. The table came out
well and the hands came out worst in the picture — so the *knuckle* item is answered no.
The *grain* item is not cleanly answered: the table improved from REHEARSAL5, and so did
the background rule that was rewritten between the runs, and one run cannot separate
them. It stays on the record.

**One painter is not a sample, and the caution REHEARSAL4 stated has not expired.**
Both of this run's painters reached for `rehearse` unprompted, and both produced
better-judged pictures than REHEARSAL4's pass session, which never did and produced
most of REHEARSAL4's defects. That is an argument for the tool, not evidence about any
guide edit — a single session's habits still swamp a guide change, and two sessions are
two sessions.

---

## What to do next, in order

1. **Fix the signature exemption in the engine, not in the checker.** `stroke_count`
   should not count marks noted `signature`, up to the guide's five, and past five they
   should all be charged so the exemption cannot be spent on painting. Right now the
   only honest alternative is to delete the promise from the guide, and the promise is
   the better half — a painter that has to pay for its signature will not sign.
2. **The depth-order paragraph has now failed three runs and should be rewritten**, and
   `NOTES.md` item 0c's reason for leaving it alone has expired: one session was not
   evidence, three are. What is certain is that stating the rule, giving it a runnable
   three-mass example and putting it in the checklist is not sufficient.
3. **Retire or re-scale the value criterion.** Three consecutive painters have cleared
   `0.10` by a thousandth on the mug. Containment caught what it missed on all three.
4. **The ribbon and the concave inset are engine-or-guide questions and go before M9**,
   because both change what a painter should be told about what a mass costs.
5. **Then M9 — the MCP server**, as `NOTES.md` has it.
