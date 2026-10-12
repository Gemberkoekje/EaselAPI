# Step 4 of `PLAN-0.9.0.md`: a held edge that is soft

**To understand this, start by reading the plan's section 4B, and section 6's rows P2 and
*Answered after the bench* 4B, then `CALIBRATION.md`'s *A soft hold, as built*, then
[`tests/test_soft_hold.py`](tests/test_soft_hold.py).**

Branch: `ccr-65d1dbee-863bmi`, off `main` at `6e26229` (#105, step 3, merged).

---

## What landed

| | |
|---|---|
| **`src/easel/session.py`** | `soft=` on `stroke`, and so on `dab`, `smudge` and `glaze`, and on `block_in`, `sweep`, `cover` and `scumble`; `_as_softness` reads what a painter hands it into one `_Soft` per edge it loses; `_clip_cover` builds B1 on what it softens (`_soft_hold`), with the softness in the memo's key; a stretch's taper (`_taper`); the record's `"soft"` in the clip's mapping and its replay; `"soft"` left out of a planned mark's brush fields |
| **`PAINTER.md`** | step 6 leads with the soft hold; paid for in the same section (6,689 words, 5 fewer than before) |
| **`RECIPES.md`** | *An edge that is actually lost* leads with the soft hold, in prose; the smudge is for an edge already painted |
| **`REFERENCE.md`** | `soft=` under *Which verb takes which hold*, rule first; a `soft` row; the `feather` row sends a lost edge to `soft=` |
| **`CALIBRATION.md`** | the round's *A soft hold, as built* |
| **`SUGGESTIONS.md`** | the round's row for the held edge, filled in |
| **`scripts/probe_uktarl_session.py`** | `--soft-built` lays every edge of answer B through `soft=` beside the bench's B1, and the painter's far-side stretch; both `_clip_cover` patches take the new argument |
| **`tests/test_soft_hold.py`**, **`tests/test_mcp.py`** | the new behaviour; two planned masses with `soft` priced and painted over the wire |

## Decisions and gotchas

- **As the painter chose**: B1, a smooth ramp inward, in the long side's fraction, per
  hold and per stretch. No `lose()` verb (P2), no `edge="soft"`.
- **What a number softens.** The mass's own outline under `edge="hard"`, with `clip=`
  kept at its edge: every edge in the painter's answer B, and every case the bench laid,
  was that. Without an own outline, a number softens the call's one `clip=`; a call held
  by several places and none its own is refused and told to name one,
  `soft=[(shape, width)]`. **One reading to confirm**: that a bare number never means
  *every hold of the call*, which the painter's batch 1 rejected for a call with two
  holds (*one softness for the whole call would soften the silhouette too*).
- **A stretch** is a run of a hold's own points in order, either way round
  (`shape.closed[i:j]`, or reversed); all the way round, or the very points the hold was
  handed as, is the whole outline. Points that are not a run of any hold are refused.
  **A second reading to confirm: the taper lies past each end of the named stretch**, so
  the stretch named is soft over all of its length, and the softness fades back to the
  held edge over its own width beyond it (answer 2b, *taper back to the hold's edge at
  each end*). The other reading, a taper inside the stretch, would leave a stretch
  shorter than two widths never fully soft.
- **The taper is not counted along the outline.** Counted by arc length, a corner where
  the stretch ends creases: the pixels either side of its bisector belong to different
  sides. Instead a pixel takes the softness by how much further the stretch is from it
  than the outline is: on the line that is the distance back to the stretch's end; a
  pixel `d` in tapers over the width and `d` more, which rounds the corner.
- **On what it softens, `soft=` replaces the feather.** The bench's B1 had no broken
  edge under the ramp, and the built one is the bench's: on a hold softened whole, the
  feather breaks none of it; on a stretch, the rest of the outline keeps it.
- **The bench's second hold is not the engine's.** `--soft-built` finds the softened
  edges identical, and the masks apart only outside a crisp `clip=`'s line: the bench
  broke a second hold on its inside pixels only and left the rim's `0.5` coverage, where
  the engine lets nothing past the line, as 0.8.0. The blanket heap's 451 export pixels
  are that rim's paint carried along the passes.
- **`clip_out=` is never softened** (P1: cut on the line); naming an exclusion is
  refused, with the reason.
- **The `holes` line needs no change**: measured, a soft edge reads as bare nowhere the
  line measures (`CALIBRATION.md`).
- **The record**: `params["clip"]` becomes the mapping step 3 introduced whenever a mark
  is softened, `{"in": [...], "soft": [{"hold", "width", "run"?}]}`, with `"out"` beside
  it when held out too. A width of `0` logs nothing. Tested against `v0.8.0` from `git
  archive` by hand: the session loads, `replay()` raises `KeyError: 0`. The test carries
  0.8.0's reader verbatim, as step 3's does.
- **Recipe code blocks run as `easel demo`'s first panel**: a recipe's first block is the
  one its demo lays as *the recipe*. A `soft=` block first under *An edge that is actually
  lost* would have become the smudge demo's recipe panel, laid on a passage it has nothing
  to do with, so the soft hold leads in prose with its two forms inline.
- **`PAINTER.md`'s cuts**, to stay inside 6,700: *The step most painters so far have
  skipped*, a picture's crisp edges *said as a number* (the `edges:` line says it), and the
  three smudge notices described at length (each says itself at the call).

## Next

Step 5 (C: `habits=` per place, the pass rule leaving the signature out as the closing
audit does, and C5's standing lines printed on change) starts from the plan's section 4C
and *Answered after the bench*. Step 8's
join recipe width waits on nothing now: the soft hold is what P9 named as the other
remedy for a terminator that reads as a facet.
