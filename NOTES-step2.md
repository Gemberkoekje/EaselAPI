# Step 2 of `PLAN-0.8.0.md`: the measuring probe

**To understand this, start by reading the plan's section 4 (the workstreams) and
[`scripts/probe_bell_session.py`](scripts/probe_bell_session.py)'s docstring, then
[`CALIBRATION.md`](CALIBRATION.md)'s *The bell-warden's round* -- and then look at the
sheets the probe writes under `out/bell/`, because three of the round's questions are the
eye's and not a number's.**

Branch: `measure-bell-round`, off `main` at `a180395` (#89, step 1's second half).

---

## What this step was for

*Measure before building*, the plan's rule 1: every candidate of workstreams A to E, H and I
benched on the two paintings' own canvases and over the corpus before any of it is built,
with the output deciding which rows are built as written -- and the candidates the painter
has to judge by eye rendered at the painting's size, with its questions 4, 9 and 10 put to
it as a blind package.

## What landed

| | |
|---|---|
| **`scripts/probe_bell_session.py`** | new. Rebuilds both paintings through the CLI's own `run_script` -- the Bell-Warden in its recorded order -- keeping a copy after each pass and every call's script line and function; re-measures sections 3 and 3b; benches A1, A2, A3, A4, A5, B1-B4, C, D, E1-E4, F7, H2, H4 and I2; replays the corpus once with this round's watcher, kept in `out/bell/corpus.pkl`; writes the sheets |
| **`CALIBRATION.md`** | *The bell-warden's round*: the stub's opening replaced, and seventeen sections of the probe's numbers; its row in the index at the top |
| **`PLAN-0.8.0.md`** | the status line; a *Step 2* note under every workstream it benched; section 5's rows 1 and 6 settled; section 6's questions put; step 2's *as built*; the file map |
| **`paintings/Claude/bell_warden/questions-step2/`** | new: the package questions 4, 9, 10, D and 5f went to the painter in -- `README.md`, `QUESTIONS.md`, `KEY.md`, a form, and `make_package.py`, which lays the probe's sheets out under their letters and refuses to if the letters no longer match `KEY.md` |

## What the probe decided, row by row

| Row | Built as written? | What the probe says |
|---|---|---|
| **A1** guides on any ground | **yes: the cased line** | Today's line leaves a median 88% of its pixels under a step of `0.25` over 35 grounds, and over the room the second drawing went on, 96% under `0.05`. The casing -- opaque or at 150 -- leaves none under `0.25` anywhere. A per-pixel ink fails at its own switch. Which casing is question 4b |
| **A2** a shape to `guide()`, `pencil()` | **yes** | Both raise `TypeError` on a `Polygon` and a `Region`; the spline puts 99% of the plinth's path outside it, up to 21.6 px |
| **A3** the thumbnail | **yes**; size and signature: question 4 | 14 to 36 ms an arrangement. The ears read from 128 px, the arch's band from 192. **The plan's own places draw no creature**: this plan named none of it, so the default is asked |
| **A4** a silhouette from parts | **the recipe; no `ribbon(width=[...])`** | A union of lobes along a member swells as a width per point would; unsmoothed it has 51 notches, `.smooth()` 3 |
| **A5** pixels and groups | **as decided** | One painting of 24 wrote a pixel helper, two moved points about a centre by hand. And a ribbon's width is not a size (F7) |
| **B1-B3** the lit silhouette | **as written**; the painter reads the candidates blind (question 9) | The join widens each terminator's step from under a pixel to about ten and leaves the silhouette a step; a feather does not, until it breaks the silhouette at `0.03`. On the abstract form the join's size is the turn's width. A join's end blots against the silhouette: taper it |
| **B4** a head toward a light | **as written, with its ratio** | The face that worked lights 74% of itself (81% of a row); the strip 24%, the copies 35% |
| **C** the dearest line | **as decided** | Printed on 43% of the corpus's painted passes, a median 67 characters, naming a median 76% of its pass |
| **D** a mark that lands short | **narrowed: a round dab that lands nothing**; the rest is question D | The shortfall has no gap and would speak on 14% to 39% of passes. A round dab that lands nothing is a pixel cliff -- 6.5 px at `press=1`, 5.6 at 2, 2-3 at 3 -- predicting 56 of the corpus's 57, on 3.2% of passes and no guide block. A starved bristle landing nothing is on 9.7%, and on one guide block: *A mass built of planes*'s dry-brush stroke lays nothing on the check's canvas, the recipe's to fix. The wet has no case left |
| **E1** `key="low"` | **as decided: clusters printed, not judged** | Silent on 72 of the 74 low-key passes, and speaks when the pier leaves its key. A fixed `0.10` gap would judge 61 of 74; a scaled one none |
| **E2** the median | **as decided** | It holds a detail either way to 45% of a place and flips past half; the upper percentiles give way to a light detail at 10-30%. It changes a verdict once in the three plans, the handover's tower pass, for the better |
| **E3** a black | **not proposed**; question 10 | The darks move down together: the Bell-Warden's two planned darks stay `0.01` apart. Its room wanted a plan with its darks apart |
| **E4** the named light | **as decided** | Every named light is under a fiftieth of its canvas and clears the top twentieth by `0.17`-`0.28` at its 95th. No verdict changes; the number does |
| **F7** units | **the rows, measured** | A ribbon's width is the canvas's coordinate across its line: 38, 52 or 45 px for `0.05` at 1024x768 as it lies level, upright or at 45 degrees |
| **H2** a rebound prelude name | **narrowed, then built** | 20 of 284 passes rebind one: 17 to the same thing, 3 a loop's variable. Narrowed to a name the prelude assigned, bound to something else: none |
| **H4** a place laid over | **declined; the decline stands** | Finds the fist and the pool's water; speaks on subjects being built; sees the Bell-Warden's head only after the rule already had, the headland never |
| **I2** the rings | **no count; the recipe is F8's strokes** | An inward scumble on a dark ground reads as rings at every count from 4 to 20 |

## Decisions and gotchas

**1. The corpus replay is the corpus probe's, not a copy of it.** `SiteWatcher` subclasses
`probe_cohort_session.Watcher` and replaces its three judging hooks: the site of each call
(the first frame outside the engine and the probes), what each hand-laid mark landed at,
and an 8-by-8-pixel footprint of what each call moved. The old round's candidates are left
out -- they were most of that replay's time -- and `cohort.Watcher` is swapped for the
length of a replay, so `cohort.replay` builds this one. The cache is a plain dict: pickled
as the dataclass, it could only be read back by a process where the probe was `__main__`.

**2. A call's site is its line in the painter's script -- or in the prelude.** `run_script`
compiles the prelude as `prelude.py` and each pass under its path, so a helper defined in the
prelude is reported at its own line there, with its name: *8 scumble at prelude.py:117
(sea_mass)*. That is the frame `_one_call` would see too; whether the line should name the
pass's call of the helper instead is the build's to decide.

**3. Variants of a pass are the painter's source with one line changed**, run under the
pass's own name, so each call keeps its line. `_sub` refuses a change that does not match
exactly the number of times it expects. A helper a variant needs -- B2's `terminator` -- is
put in the pass's scope for the bench by adding it to `easel.__all__`, which is what
`run_script` builds a scope from (`offered`).

**4. `plan()` merges, and a rehearsal copy carries its plan.** As in step 1: a version
rehearsed before the prelude declared `ground=` reports *buried* on a copy of the finished
canvas. None of this step's benches read the ground line.

**5. The terminator's rise is measured, not looked at, and has a reach.** Twelve pixels
either side along the normal: a lit rim narrower than that is read across (the abstract
form's shift of `0.008` reads 18.5). The join's number is honest only where the zones are
wider than the reach, which at the painter's shifts they are.

**6. `ribbon()`'s width is in the canvas's coordinates across its line**, not a fraction of
the long side and not round in pixels -- found building A4's bench, when a union of lobes
sized from the same widths came out wider than the ribbon it was compared with. `ellipse`
and `blob` radii are the width's across and the height's down, round only with `aspect=`.

**7. A thumbnail recorded from passes run with nothing laid** reads `s.sample()` off a bare
canvas, so a film mixed from a sample is mixed from the ground. Films are not masses, and the
thumbnail takes no film, so nothing in it moves.

**8. The floor was re-laid by patching `Session._resolve_color`**, the one place a stroke's
colour is resolved: every colour darker than `0.20` has its linear light scaled so the span
from the box's floor to `0.20` runs from `0.07`. It is the same painting with deeper darks,
not a painter's choice of where to put a dark.

**9. The repaint count needed the rehearsals' order**, which the version READMEs give and
`VERSION_RUNS` records; the Bell-Warden's eleven unfiled rehearsals (room, plinth, finish,
glow) are not in it, and none of them was a subject pass.

**10. Timings only on a quiet machine.** The first corpus replay and the floor bench ran at
the same time; their seconds are not quoted.

**11. On this machine, again**: a Bash `cd` moves the session's working directory; a quoted
heredoc feeding Python turns `\\n` into a newline (make edits carrying escapes with the
editor); and `cat > file` with no heredoc attached waits on standard input forever.

## Questions out

To the first painter, through the owner, as
[`paintings/Claude/bell_warden/questions-step2/`](paintings/Claude/bell_warden/questions-step2/README.md)
-- a zip `make_package.py` builds from the probe's sheets:

- **4a, 4b** (blind): the thumbnail at four sizes; the guide candidates over its room.
- **9a** (blind): its subject's pass laid seven ways, at two sizes.
- **10a** (blind): its painting and the same with the darks under the floor.
- **4c, 4d, 9b, 10b** (open): the thumbnail's signature and default, the drawing over it and
  the drawing alone, the terminator by name, a darker dark.
- **D** (open): whether the post-pass check names the marks that landed nothing.
- **5f** (open): the median for `lightest:` when the lit part is under a tenth of its place.

Nothing goes to the second painter from this step.

## What step 2 did *not* touch

The engine. Nothing under `src/` changed; every candidate is patched in for one bench and put
back.

## File map

| File | What changed |
|---|---|
| `scripts/probe_bell_session.py` | new: the round's benches |
| `CALIBRATION.md` | *The bell-warden's round*: the probe's numbers; its index row |
| `PLAN-0.8.0.md` | status; *Step 2* notes; sections 5, 6, 7 and 9 |
| `paintings/Claude/bell_warden/questions-step2/` | new: the package and its builder |
| `NOTES-step2.md` | this file |

## Next

- **The painter's answers** to 4, 9, 10, D and 5f, filed as
  `paintings/Claude/bell_warden/answers-step2.md` and re-measured, as step 1's were.
- **Step 3** can start before them: A1 (the cased line -- its casing's opacity is 4b's), A2,
  and A5 as decided.
- **For step 9 (F)**: *A mass built of planes*'s dry-brush stroke lays nothing on the guide
  check's canvas; F7's rows are measured here; B4's ratio is *about three quarters*.
- **The owner's to confirm, still**: the plan proposes that this round takes the two
  verdicts it has, and that a third painting against 0.7.0 is recorded but planned after
  0.8.0 (section 8). *Answered 2026-09-27 (O8): new paintings are painted on 0.8.0.*

---

## The painter's answers, 2026-09-27

**To understand this, read the painter's
[`answers-step2.md`](paintings/Claude/bell_warden/answers-step2.md), then `CALIBRATION.md`'s
*The painter's answers to the package, measured again*, then the plan's status line and its
section 6.**

Branch: `file-bell-answers-step2`, off `main` at `da02328` (step 3, #91).

The package was never sent after this step. The owner asked for it on 2026-09-27, and it was
built again from `main` at `da02328` -- only `numbers/CALIBRATION-the-bell-wardens-round.md`
and `scripts/probe_bell_session.py` differ from the 26th's build, by step 3's additions; the
blind and labelled sheets are the same bytes -- and unpacked beside the painting, for the
owner to point the painting session at. The painter answered the same day.

| Question | Its answer | What it decides |
|---|---|---|
| 4a | 192 px; two cells read otherwise than the bench | A3's default size |
| 4b | G blind, then E once it had read the 35 grounds; the notes' boxes pile up | A1 as built; the boxes kept apart, in step 4 |
| 4c | the plan's places and the masses laid so far; a clip as part of a place; `easel run --thumbnail` | A3's signature, and a second way in, in step 6 |
| 4d | never the drawing over a thumbnail; no look of the drawing alone | 4G declined |
| 9a, 9b | F, the join; a soft brush held hard is held hard; B3's sentence says what to do, and *fur* | B1 to B3 |
| 10a, 10b | P, blind; a darker dark, yes, with a hue it cannot name | E3 recorded, not built |
| D | name them after the pass; `dab()` lacks its two-touch figure | D as both a fact and a line; F3 |
| 5f | the 95th percentile for `lightest:`, beside the median | E4, as the second painter asked |

**Measured again (`--answers`), and holding**: B against C, 18, 4, 42 and 9 pixels over
12/255; Q's darkest `0.140` and its 5th to 95th percentile `0.160` to `0.349`, P's 12.5% under
`0.14`, the plinth's side `0.266` in both; every place reading in 5f; the script lines it
cites; that `dab()` gives one touch and three; that neither painter ran `easel log` while
painting -- the Bell-Warden's session names it first on 2026-09-26 at 09:27 UTC, in the
pasted questions, and Wenna Brask's first runs it at 11:44 UTC that day, answering; and the
saved reports' silence, 27 and 32 of them. **Not holding**, both reasoned: the line D asks for
speaks on 14.7% of painted passes, not one in ten; and a floor at `0.07` leaves room for three
planned values `0.10` apart under `0.35`, not four.

**Found measuring them**: `dab()`'s one touch, *about a quarter of the way*, reaches a tenth,
at the brightest pixel as at the median, from 7 px to 25 -- a sentence written 2026-09-10
(#6); the notes' boxes overlap on 8 of the Bell-Warden's 17 and 6 of Wenna Brask's 25; and
under `feather=0.012` the band just inside the outline is nearly three times as grainy as
painted, which the rise *across* the outline could not see.

### Decisions and gotchas

**1. E3 is not built this round, and the painter's yes is recorded.** The question said the
plan proposes no black this round and asked only whether a hue was wrong; the painter agreed
the hue is right and named no pigment. What it wanted is met without one: the `0.13` it asked
for is burnt umber alone, and P's `0.10` accents are a supplied dark, and `at_value`'s new
error names both.

**2. D is built as both**: the fact at the call for a round dab under its cliff, which met the
four conditions, and the line after the pass for every mark that landed nothing. The
painter's own example line names the spark as well; the fact says it as it happens.

**3. The second painter needs no question D.** The flour was the reason to put D to it, and
the first painter answered D with the flour as its case.

**4. The package's `KEY.md` is in this repository**, and so are the step notes that name every
letter, so a painter that opens the repository during Part 1 reads the key. The owner's
message said not to, and this painter did not. A later package could keep its key out of the
repository until the answers are in.

**5. `values_of_rgb` returns values in `0..1`, and the terminator bench's crops are the
export's pixels at the canvas's size**, so a shape's mask lines up with them through the
crop's own box -- `TERMINATOR_BOXES`, now a module constant both benches read.

### File map

| File | What changed |
|---|---|
| `paintings/Claude/bell_warden/answers-step2.md` | new: the painter's answers, verbatim |
| `paintings/Claude/bell_warden/questions-step2/README.md` | when it was sent, and the one wrong sentence |
| `scripts/probe_bell_session.py` | `--answers`; `TERMINATOR_BOXES` |
| `CALIBRATION.md` | *The painter's answers to the package, measured again*; one sentence on `dab()`; the index row |
| `PLAN-0.8.0.md` | the status; A1, A3, A5, B, D, E3, E4, F3 and G; section 6's answers, O8 and O9; sections 7, 8 and 9 |
| `SUGGESTIONS.md`, `PAINTINGS.md` | the answers named; the guide row's 4b |
| `NOTES-step2.md`, `NOTES-step3.md` | this section; step 3's decisions 1 and 6 settled |

### Next

**Step 4**: C, H1, H2 and H3 -- and two small things from the answers, a guide note's box moved
off the boxes already drawn, and the error a one-number `s.px(r)` raises naming the oval.
