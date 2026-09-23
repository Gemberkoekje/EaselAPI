# The five questions

Every picture here was made by your own passes, rebuilt through the code `easel run`
uses, on the canvas you had when you laid them: `p04_tower.py` on the canvas after your
headland, `p03_headland.py` on the canvas after your sea, and so on. Each candidate was
patched into the engine for one bench and taken out again. The plan's numbering is kept:
these are questions 10 to 14, after your nine.

---

## Part 1 -- blind: `blind/` and nothing else

### 10a. Which edge reads as paint?

Four renders of the same passes, lettered **A to D in the same order on every sheet**.
One of them is the engine you painted with; the other three are ways of cutting a hard
edge that the plan proposes. `KEY.md` says which is which.

| sheet | what it is |
|---|---|
| `q10_tower_1x.png` | your tower as `p04_tower.py` laid it, at the painting's size, 1:1. **This is the test you set**: *the jaggies are invisible at 1024x768 unless you zoom; the vector-clean edge was the problem* |
| `q10_tower_x3.png` | the middle of the shaft, three times |
| `q10_tower_1440.png` | your passes rebuilt at 1440x960, 1:1 |
| `q10_headland.png` | your headland mass as `p03_headland.py` laid it: the top row on your roughened outline, the bottom row on a plain outline drawn through the same points |
| `q10_ground.png` | a hard-edged mass laid on bare ground, enlarged twice |
| `q10_burial.png` | `cover()` burying a mistake in a worked passage, enlarged three times |

**Rank A to D, most paint-like to least, at the painting's size.** Then: does any of them
read as a painted edge to you? Does any read as blur? Does any read as ragged or damaged?

### 12a. Which starved brush reads as a dry brush?

Five renders, lettered **P to T in the same order on every sheet**. One is the engine you
painted with; the other four are ways of gating a starved brush against the canvas
tooth.

| sheet | what it is |
|---|---|
| `q12_crosser.png` | your sky's first crosser -- `bristle`, `size=0.065`, `opacity=0.40`, `pressure="swell"` -- at loads 0.30, 0.45 and 0.60, one row per letter, on a flat field of your sky's value |
| `q12_exercise3.png` | exercise 3: the same `bristle` stroke at loads 1.0, 0.6, 0.35 and 0.2, `load_falloff=0`, on rough canvas |
| `q12_water.png` | your first water pass as you rehearsed it (the one the check misfired on): the surf and the swells, on your painting |

**Rank P to T, most like a dry brush dragged to least.** Which of them read as dirt?

### 13a. Graded passage, or separate things?

Ten passes from other painters' paintings in the corpus. On each, the line you met
twice fired: *N marks at stepping colours run parallel ... and the narrowest brush laying
them is ... Under 2 the passes stop overlapping and a graded passage comes back as bars*.
On one of the ten, only a narrowed form of the rule fires. In each crop the left half is
the canvas as that pass left it, and the right half is the same with every mark the rule
counted drawn in magenta.

**For each of `crop_01` to `crop_10`**, mark **T** if it is a graded passage coming back
as bars, so the line is right to fire; **F** if it is separate things and not a passage,
so it should not fire; or **?** if you can't tell. Your own two misfires are not among the
ten. They are in `labelled/graded_headland.png` and `labelled/graded_water.png`, drawn
the same way, if you want a reference for F.

**Write Part 1's answers in `answers-step2.md` now, then open `KEY.md`.**

---

## Part 2 -- open: `KEY.md`, `labelled/`, `numbers/`

### 10b. The edge, by name

You said the tower, lantern and cap wanted *crisp-but-painted* edges, which sounded like
A2, and that you would have used `roughen()` for rock. Now that you know the letters,
which candidate do you choose for made things, and at what feather? If none reads as paint
at the painting's size, the plan's fallback is to ship the feather opt-in, at `0`.

What the numbers say, in brief (`numbers/CALIBRATION-...md`, *An edge that is not a
step*):

- **A1 feathered inward at `0.002`** (2 px at 1024 wide) takes the tower's one-pixel step
  from `0.30` to about `0.23`-`0.25`. It moves the `edges:` line only from 77% to 69% on
  a flat field, and halves it only at `0.005`.
- **A2 keeps every pixel crisp and breaks the boundary where the tooth is low**, so
  neither number can see it at all. That is why this question is yours.
- **On the headland, your roughened outline** changes the picture more than any feather
  at `0.002` does: compare the two rows of `q10_headland.png`.

### 11. Should the default reach `clip=`?

Your decision: *feather `edge="hard"` by default; keep `clip=` hard when it is only
containing paint; feather inward or not at all; `feather=0` stays available.* The
engine cannot tell a clip that draws an edge from one that contains paint, so the plan
turned your decision into **`edge="hard"` feathers by default, and `clip=` keeps `0`**.
What the bench found:

- **The default, read that way, moves 5 of your 9 edge-drawing calls**: the headland mass,
  both sea stacks, the cap, and the horizon, your `scumble(sea, ..., edge="hard")`, which
  you wanted ruled.
- **It moves none of the four your verdict named.** The tower, its lit side and the
  lantern, twice, are `stroke(..., clip=...)`, so under the default they are exactly what
  they are today. See the last three panels of `labelled/edges_tower_1024x768.png`, marked
  *default only*.
- **Every feather benched is inward.** It only ever takes paint away inside the line, so
  a feathered clip cannot carry paint past its outline, and the containment you protected
  holds by construction. The risk you named for containment clips -- *the planes would
  leave a lighter fringe around the dark headland* -- was an outward feather's. The
  remaining risk is a rim of the mass beneath showing through the feather's zone, and
  `labelled/edges_containment.png` and `edges_containment_x4.png` show your planes with
  their `clip=headland` feathered. The bench sees no rim; look for yourself.
- **The cost of feathering `clip=` too**: it also moves your 24 containment calls and the
  corpus's other clips (GPT's thirteen), and a script that wants a ruled clip passes
  `feather=0`.

**Options:** (a) as decided: `edge="hard"` feathers, `clip=` does not, and your tower
takes `feather=` by hand; (b) `clip=` feathers too, inward, by default; (c) something
else.

### 12b. The dry brush, by name, and its cost

The candidates: **B1** reads the tooth along the stroke's travel, so what clears the gate
is a run of pixels rather than one. **B2** gives every bristle of the comb its own load,
so some bristles keep their paint and an empty one lays nothing. **B1+B2** is both.
**B3** lays starved paint thinner. Things to weigh:

- **B2 needs a comb**, so it changes nothing on a `flat`. Your five starved ledges in
  `p08_rock.py` are flats; B1 changes them, B2 does not (`labelled/flecks_ledges.png`).
- **B1 and B2 both change how much paint a load lays**, not only its shape: B2 as benched
  lays up to 3.5 times today's paint at `load=0.35` on rough, and B1 up to a fifth more or
  less. The bench's proposal is to tune both until each load lays about what it lays
  today, so the loads the guide recommends for a broken mark (0.35-0.6, which you used)
  keep their meaning and only the shape of the mark moves.

**Which do you choose**, and does "tuned to lay today's amount" match what you meant by
*a dry-brush mark that works*?

### 13b. The graded rule

`KEY.md` has the ten crops by name and a table of which gate silences which. The plan
drew two clauses on your misfires: judge the run by its **median** brush, because your
`0.006` crevice was an accent among planes, and **break** the run where neighbours do not
overlap along the stack, because your ripple sat beside glints. Both together silence
both misfires and keep the recipe's own failure demo firing. The plan's condition for
building them is that they keep every true positive a human calls a passage -- and the
human is you, now, with your T/F from 13a.

**Options:** (a) build the plan's gate, the median brush and a 30% overlap break; (b) the
bench's variant, the narrowest brush at least half the median with a 10% break; (c) leave
the rule as it stands -- it fires on 9 of 337 passes in the corpus and never on a guide
block, and the saved reports (C0, which you asked for) will make any future misfire
reproducible; (d) something else.

### 14. Parallel panels

You had no evidence and said so. The bench:

- One panel of a `vary=` sheet takes **2.8-2.9 s**; four in one process 11.1-11.6 s; four
  in four spawned processes **4.4-4.7 s, 1.6-1.7 times one panel**. The plan's target
  was 1.5 times. The cost is each process loading the session file, about 1.4 s.
- **Your harness's three-band sky variant took 10.4-10.7 s, and 10.2-10.6 s of it is the
  three scumbles themselves.** The fifteen seconds is the paint.

D0 -- scripts rehearsed as side-by-side alternatives, which is what you said would have
replaced your harness -- is built either way. **Is D1 declined**, as the plan says a missed
target is?
