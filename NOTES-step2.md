# Step 2 of `PLAN-0.9.0.md`: measure (in progress)

**To understand this, start by reading the plan's status line and section 6's *Answered*
table, then [`answers.md`](paintings/Claude/uktarl_krannoc/answers.md), then
[`scripts/probe_uktarl_session.py`](scripts/probe_uktarl_session.py)'s docstring.**

Branch: `measure-uktarls-room`, off `main` at `f416bcf` (step 1, #101, merged).

---

## What landed so far

| | |
|---|---|
| **`paintings/Claude/uktarl_krannoc/answers.md`** | the painter's answers to `questions-step1.md`, verbatim, written 2026-10-10 in the painting's own session |
| **`paintings/Claude/uktarl_krannoc/evidence/`** | `edges_2x.png` (the edges it would soften), `heads_1to1.png` and `heads_4x.png` (the join on skin), as the answers cite them under `out/` |
| **`PLAN-0.9.0.md`** | the status line, and section 6's *Answered* table: what each answer decides |
| **`scripts/probe_uktarl_session.py`** | `--claims`, `--clip-out`, `--answers`. It registers the painting with `probe_bell_session.py`'s rebuild and reuses its instruments |

## What it measured

- **The rebuild** (`--claims`): 429 records, 410 spent, 0 pixels off the painter's
  `painting.png`, in about 50 s. Landmarks left at the end: `candle`, `lantern`.
- **4A, the exclusion** (`--clip-out`): the backlight's eight calls laid once with
  `clip=wall` and Uktarl's seven prelude shapes excluded, patched into `_clip_cover`:

  | laid | px wholly on him | seam px at y=460/490/520/550 |
  |---|---|---|
  | committed, three typed regions (44 points) | 15 (the glare on the wig: `glow_above` misses the hair's outline) | 6/3/2/1 |
  | `clip_out`, cut on the line | 0 | 4/1/1/0 |
  | `clip_out`, broken into the light (a hold's default) | 0 | 6/3/2/1 |
  | `clip_out`, broken onto him | 523 | 3/0/1/0 |

  Cut on the line is the painter's answer, and the bench agrees: the seam closes, and the
  only pixels it lays on him are his antialiased rim, in proportion to the wall they share.
  The hold's default, broken into the light, is exactly the committed seam. Sheet:
  `out/uktarl/clip_out.png`.
- **The answers' M claims** (`--answers`), each held: 150 of 246 standing lines (61%) word
  for word the report before; *no clear light* in 43 of 46 reports; 39 finding lines; the
  seam at the four rows; the square turned in fractions at 4.5°/93.5° and 23.4°/104.2°,
  sides 94 and 109 px. Of the 39 findings, 11 are *stack of bars* over all 46 reports; the
  painter's 6 count only the runs it filtered.

## Decisions and gotchas

- **`answers.md` is filed verbatim**; its `out/...` paths are the painter's folder. The three
  pictures are copied to `evidence/` under the same names.
- **The painter's 46 reports equal the filed `reports.txt`** (`all_reports.txt` in its
  `out/`), and no script changed since filing.
- **`Session.marks`** holds landmarks, not `_landmarks`.
- **A per-pass spent total sums to 414**, four more than the painting's 410: the signature
  marks are free.
- **A `cat > file` with no input blocks a Bash call** until its timeout. Write files with a
  heredoc, never a bare redirect.

## Next, still step 2

`--soft` (B, the cases in answer B's table, per hold), `--rules` (C1 near-copies on what
landed, C2, C3, C5 standing lines printed on change, over the corpus), `--direction` (G1,
G2, G3 with the stream kept), `--key` (H2 over the corpus's plans with a named light),
`--shares` (F, with answer E's split), `--reading` (I's inventory), and the join's width on
the three faces (P9).
