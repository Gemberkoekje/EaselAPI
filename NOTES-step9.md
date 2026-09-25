# Step 9 of `PLAN-0.7.0.md`: three sentences, and the round's record

**To understand this, start by reading the plan's workstream G and section 4H, then
*A volume of lit air* and *A passage brightening toward one side* in `RECIPES.md`, and
*Pressure* and *The fade and the wet bands* in `CALIBRATION.md` -- and read
`NOTES-step8.md` first if you have not.**

Branch: `claude/v0-7-plan-ayggw7`, off `main` at `a6b8517` (#84).

---

## What this step was for

The painter's three documentation findings the round had not yet answered, and the
record. Finding 11: one sentence of prose was backwards -- *the one factual error I found
was in prose*. Finding 10: a caveat lived a file away from its rule, so a painter who read
the recipe alone could not know how late a pressure list's fade arrives. Finding 8, the
seam it withdrew, left a real number behind -- the wet layering -- that no page carried.
And finding 9, the weight of the documentation, which the painter ruled *watch*: recorded,
nothing cut.

## What landed

| | |
|---|---|
| **G1** | *A volume of lit air*: `[1.0, ..., 0.1]` is wide and bright at the source and narrow and gone at the far end, the core and the body thinning away from the light; the wide faint film runs the other way. Cites *Pressure* in `CALIBRATION.md`. The block and its demo are untouched |
| **G2** | *A passage brightening toward one side*: **the fade arrives late** -- at the recipe's own `opacity=0.5` a quarter pressure moves the value over half as far as full pressure does and a tenth still a quarter as far; the painter's band reads `0.41` over its last third and `0.19` over its last twentieth -- and the reason named where it lives, *`opacity` does not thin a long stroke* in `PAINTING.md` |
| **G4** | `CALIBRATION.md`, under *`scumble`*: *Ramps laid over one another, wet or dried between* -- a number for choosing, not a rule |
| **The numbers** | `CALIBRATION.md`: the share of its step a pass lays at one pressure, under *Pressure*; the index row; *Written, in step 9* in the round's section, with the lit-air films' widths; the right third's pressure corrected where it stood |
| **The probe** | `probe_handover_session.py --pressure`: `probe_lit_air` (the recipe's own three films, each laid alone), `_painters_band` and `_recipes_passage` (the recipe laid from its own block, its pressure and opacity replaced), and the share-of-step table |
| **The record** | `LESSONS.md` (*Nor is a measurement*; *a painter told where to start reads what it likes*; the index's one data point; the numpy papercut; one line under the tenth round's prediction); `SUGGESTIONS.md` (the three rows, the round closed, the cohort's open item revisited); #70's line; `README.md` and `llms.txt` (thirty notices, the round no longer open, the rebuild claim, the sizes); `CHANGELOG.md` |

## Decisions and gotchas

**1. G2's number was the plan's own, and wrong.** The plan drafted the recipe's sentence as
*a quarter pressure still lays a quarter of the step, because dabs overlap* -- reasoned
from the painter's thirds, never measured, and the one claim of the round nobody checked
because the planner made it. Measured, a pass laid at one pressure along its whole length:

| pressure | the recipe's six `flat` strokes, `opacity=0.5` | at `0.9` | the painter's `scumble`, `opacity=0.5` | at `0.9` |
|---|---|---|---|---|
| 0.50 | 0.85 | 1.00 | 0.76 | 0.92 |
| 0.25 | 0.56 | 0.82 | 0.43 | 0.67 |
| 0.10 | 0.24 | 0.43 | 0.15 | 0.28 |

A quarter pressure lays two-thirds of the step on the painter's band, not a quarter.
Behind it, the round's own `CALIBRATION.md` section said the painter's right third
*still averages a quarter pressure*; the band's passes are cut at the frame and run from
the canvas's first column to its last, and the third averages `0.135`, which the table
puts at `0.37` of the step -- the band reads `0.365`. Both are corrected where they stood,
in the plan, `CALIBRATION.md` and `SUGGESTIONS.md`, and the recipe carries the measured
numbers: the recipe's own strokes at its own opacity for the law, the painter's band for
what the end of a pass reads. `LESSONS.md` already says this (*check the painters'
numbers*); it applies to the plan's.

**2. G4's home did not exist by the name the plan gave it.** The plan put the wet ramps
*under the graded-field recipe's measurement*, and `CALIBRATION.md` has no section of that
name: the recipe's band and brush are measured under *`scumble`* (*The band, and the brush
that closes its joins*, *The load a band is laid at*), which the index points the recipe's
rules at. So the ramps are a subsection at the end of *`scumble`*, beside them, and no
index row, because a number for choosing is not a rule.

**3. The painter's band reads higher in the canvas's last column than just inside it** --
`0.189` against `0.171` at `x=0.99`, at opacity 0.9 -- an effect of the frame, not of the
fade. The probe printed it on its first run and does not now; nothing quotes it. The last
twentieth and the last 4%, as the painter read them, are what the pages say.

**4. The signposts' sizes had gone stale, most of them before this round.** The card was
901 words at 0.4.0, when *under a thousand words* was true; it is 1,369 now, against its
1,400 ceiling, and six places still said a thousand or under -- the README twice,
`llms.txt`, the CLI's `guide` help, the MCP `guide` tool's description, and a comment in
`docs.py`. `llms.txt`'s sizes for the documents were older still: `REFERENCE.md` at 3,600
words is 8,820, 1,188 of them this round's, and the README said `llms.txt` itself is 850
words where it is 1,510. The plan asked for the README and `llms.txt` *where a count or a
claim moves*; the painter's finding was the weight, and a signpost that understates it by
a third is the wrong place to leave a stale count, so every size says what it is. Counted
with `wc -w`, and the card and `PAINTER.md` with `tests/test_guide.py`'s own count. The
notices went from twenty-nine to thirty with `older-engine` in step 4, in both files.

**5. The README's rebuild claim was stronger than the goldens.** It said *the log replays
byte for byte* and that this *holds everywhere*. The lighthouse handover's rebuild holds
to the stroke and misses the painter's export by 729 pixels at one level, from `2.4e-7` in
one mixture between two numpy builds -- and the golden tests had known it since CI's 3.13
jobs: `close_enough` takes ±1 on 2% of pixels for exactly that kind of noise. The README
says *to the stroke*, and to the byte on one machine.

**6. #70's line is posted**, as
[a comment](https://github.com/Gemberkoekje/EaselAPI/issues/70#issuecomment-5824300375):
the cross-machine rebuild, and that `llms.txt`'s two worked examples -- `car_wash`,
`lighthouse_dusk` -- claim a byte-for-byte rebuild as `PAINTINGS.md`'s rows do. **Those
two sentences are not changed here**: they are per-painting claims, which are #70's, and
#70 already knows `car_wash` comes back five marks over.

**7. The data points went where their questions were.** The plan asked for them in
`LESSONS.md`'s protocol section; there are two. The reading, the three rules broken and
the painter's instruction for a cut are a bullet under *The protocol, if a run is ever
repeated*; `explain` and `diagnose` going uncalled is the answer to the open item under
*About the protocol* that asked for it; and the tenth round's prediction -- *the session
reaches its subject earlier, because it spent less of its first hour reading* -- gains one
line pointing at the first. *A measurement is not a method* is a paragraph under *Warning
is not method*, whose rule it extends.

## The numbers

On this machine, `probe_handover_session.py --pressure`, on the engine as the round
built it:

| | |
|---|---|
| **The lit-air films, each laid alone** | the core 49 px near the light, peak `0.30`, and 16 where it gives out, `0.02`; the body 97 and 60; the wide faint film 90 and **159**, the one that opens the cone |
| **The painter's band**, `0.149` field | `0.858` / `0.787` / `0.408` by thirds at opacity 0.9, `0.188` over the last twentieth, `0.183` over the last 4%; at 0.5, `0.800` / `0.644` / `0.291`, `0.170`, `0.167` -- every one as step 2 measured it on 0.6.0 |
| **The recipe's own passage** | `0.162` at its no-pressure end on a `0.150` field, `0.466` at the other |
| **Three ramps, wet and dried between** | 16% of the canvas moved over two levels of value and 5% over eight; 34% and 13% in colour; median column jump `0.0002` both ways |

## What step 9 did *not* touch

What any mark lays: nothing under `src/easel/` changed but the card's size, in a line each
of the `guide` help, the MCP `guide` tool's description and a comment in `docs.py`.
`PAINTER.md` is untouched, and so is every guide
block; `check_guide_blocks.py` runs them as before. `LESSONS.md`'s older running counts --
*thirty claims re-measured*, the pytest total and the guide-block count under *Verifying a
change* -- are stale from before this round and are left, as 0.6.0 left them. And the
round's *what it left open* is step 10's, with this plan and the step notes, as 0.6.0's
was.

## File map

| File | What changed |
|---|---|
| `RECIPES.md` | G1, G2 |
| `CALIBRATION.md` | the table under *Pressure* and the index row; *Ramps laid over one another* under *`scumble`*; *Written, in step 9*, and the right third corrected |
| `scripts/probe_handover_session.py` | `probe_lit_air`, `_painters_band`, `_recipes_passage`, the share table; `--pressure`'s help |
| `LESSONS.md` | *Nor is a measurement*; the protocol bullet; the index's data point; the tenth round's prediction; the numpy papercut |
| `SUGGESTIONS.md` | the three documentation rows, their left column corrected where it stood; the round closed; the cohort's code-to-symptom item revisited |
| `README.md`, `llms.txt` | thirty notices; no round open; the rebuild claim to the stroke; the sizes |
| `src/easel/cli.py`, `mcp_server.py`, `docs.py` | the card's size, in the `guide` help, the MCP `guide` tool and a comment |
| `CHANGELOG.md` | `[Unreleased]`: this step's section |
| `PLAN-0.7.0.md` | status; row 10, G2 and G4 corrected where they stand; 4G and 4H marked written; the order of work |
| `NOTES-step9.md` | this file |

## Next

Step 10, the cut: the version in `pyproject.toml`, `src/easel/__init__.py` and both
entries in `server.json`; `[Unreleased]` becomes `[0.7.0]` under an introduction to the
round, **without the claim**, and `tests/test_version.py` run with the tags fetched; the
tag; then the claim. This plan and the step notes leave in the PR that adds the claim, as
`PLAN-0.6.0.md`'s did, and what the round left open and is written nowhere else goes to
`SUGGESTIONS.md` first, in a short section at the end of the round's, as 0.6.0's cut
wrote one for the cohort. Read the plan's section 6 and `git show 3d6fe74` first.
