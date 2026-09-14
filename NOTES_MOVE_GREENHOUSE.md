# Moving the two greenhouse paintings into `paintings/`

**To understand this, start by reading `tests/test_paintings.py`, then the two new
sections in `PAINTINGS.md`, then `paintings/greenhouse_winter/` and
`paintings/fogged_glass/`.** The previous move is written up in `NOTES_MOVE.md` and its
procedure was followed; this file records only what was different.

Two paintings that lived as working directories at the repository root are now under
`paintings/`:

- `greenhouse_winter/` — a Fable session: a greenhouse interior, looking straight down
  the aisle at a low sun behind the fogged end wall.
- `fogged_glass/` — an Opus session: the *outside* of a greenhouse wall in late winter,
  the glass fogged from within.

## The one decision worth recording: two paintings, not one subject

They were nearly filed as `paintings/greenhouse_winter/{fable,opus}/`, on the reading
that this was a matched pair with the subject held constant by accident. **That was
wrong, and the owner corrected it.** A subdirectory under `paintings/` means *the same
brief handed to more than one painter* — which is what `lighthouse_greenhouse/` is (one
written brief, three painters, unchanged) and what `heron_lot/` is (one subject, one
painter, twice). These two are neighbouring subjects independently chosen, not one
subject. An interior looking down an aisle and an exterior wall of misted glass are not
the same picture, and the container would have asserted a control that nobody ran.

So they are two top-level directories with a section each, and `PAINTINGS.md` now says
explicitly that this is *not a held subject and is not a control* — the distinction
matters because the page's whole argument for the lighthouse round is that holding the
subject still is what makes the differences attributable to the painters.

**What survived the correction is one convergence that is checkable.** Both painters
refused a frontal elevation on the closing checklist's layer-cake warning, and both
answered it by writing a metric perspective projection before drawing a line —
`P(xm, hm, dm)`, the same three arguments in the same order, in each one's `prelude.py`,
neither having read the other. That is in both new sections and in `SUGGESTIONS.md`,
recorded as two painters reaching the same helper off the same sentence rather than as
evidence from a pair.

## Gotchas

- **The move falsified a claim on the page, and in the interesting direction.**
  `PAINTINGS.md` criticised its own pass-script convention with *`pool_night` is the only
  one that redrew mid-painting*. `greenhouse_winter/p4_staging.py` redraws every pot and
  plant in graphite on top of the paint and says why in a comment, which is the guide's
  order followed rather than the convention's — so the page now names two, and points at
  the greenhouse as the clearer example of the thing to copy. Recounted rather than
  guessed: **seven** paintings still drew no line at all, and landmarks went from one
  painting to two (`pool_night` and `fogged_glass`). The counts are phrased without
  totals, per the page's own rule and the test that enforces it.
- **"The greenhouse painters" stopped being unambiguous.** That phrase meant the
  lighthouse-conversion round; with a winter greenhouse and a fogged greenhouse wall on
  the page it now reads three ways. Renamed to *the lighthouse-greenhouse painters*
  where it appears in `PAINTINGS.md`. `SUGGESTIONS.md`'s section is left alone because
  its first sentence already names the lighthouse.
- **The register and the gallery no longer have the same count**, and someone will check.
  `paintings/` holds one picture more than `SUGGESTIONS.md` has rounds, because the
  winter greenhouse session filed no items. Said outright in the register's opening
  paragraph rather than left to be discovered.
- **An abandoned draft was in the pass sequence.** `fogged_glass/p9_leaf_fix.py` was a
  first attempt at a repair, superseded by `p9_repair.py`; running both would apply the
  repair twice. Moved to `scratch/`.
- **Line endings**, as last time: ten files authored CRLF by scripted edits on Windows,
  normalised to LF for `.gitattributes`.
- **Reproducibility is not claimed for either**, and each says why in its own table.
  Neither was ever rebuilt from a clean session; `fogged_glass` additionally ran its
  drawing pass twice and interleaved measuring scripts between painting passes, and a
  mark's texture is seeded from its place in the log.

## What moved and what stayed

Only the painting: notes, `prelude.py`, the pass scripts, the probes, the exercises and
the two outputs. The `.easel` sessions and the `out/` look snapshots are regenerable
intermediates and stayed behind, in `greenhouse_winter_out/` and `fogged_glass_out/` —
the pattern `laundromat_night/` set and `NOTES_MOVE.md` documents. Both are gitignored.

## File map

| Path | What changed |
|---|---|
| `paintings/greenhouse_winter/` | moved from `greenhouse_winter/` (was untracked) |
| `paintings/fogged_glass/` | moved from `fogged_glass/` (was untracked); `p9_leaf_fix.py` → `scratch/` |
| `greenhouse_winter_out/`, `fogged_glass_out/` | the `.easel` session and `out/` snapshots, left behind and ignored |
| `PAINTINGS.md` | two new sections; the convention criticism recounted and its claim corrected; clauses added to the subject-chosen rule, the reading-set bullet and the unfinished list; *the greenhouse painters* disambiguated |
| `SUGGESTIONS.md` | the open section reframed from *a matched pair* to two neighbouring subjects, with the projection convergence kept; paths updated; the round/painting count difference stated |

`tests/test_paintings.py` green: 55 checks over twelve paintings.
