# Moving the pool and the herons into `paintings/`

**To understand this, start by reading `tests/test_paintings.py`, then `PAINTINGS.md`,
then the three new directories: `paintings/pool_night/`, `paintings/heron_lot/1/` and
`paintings/heron_lot/2/`.**

Three paintings that lived as working directories at the repository root are now under
`paintings/`, which is what `tests/test_paintings.py` governs.

## What the test actually requires

A directory under `paintings/` is a *painting* if it holds any of `painting.png`,
`painting.gif`, `NOTES.md` or `prelude.py`; if it holds none of those it is a *container*
and the paintings are one level in. Every painting owes three files — `painting.png`,
`painting.gif`, `NOTES.md` — and `PAINTINGS.md` must link to all three by path. The
reverse also holds: the page may not link to a directory that is not there. A sixth check
bans the counting phrases the page used before it stopped sizing its own collection.

So the work was: rename each painting's outputs to `painting.png`/`painting.gif`, and
write a section per directory.

## Decisions

- **What moves and what stays.** Only the painting itself: notes, `prelude.py`, the pass
  scripts, the probes, the exercises, and the two outputs. The `.easel` session and the
  `out/` look snapshots stay behind in the root working directory, ignored as regenerable
  intermediates. That is the pattern `laundromat_night/` already set — its root directory
  is still there holding exactly those leftovers.
- **`heron_lot/1/` and `heron_lot/2/`** per the owner's call, which makes `heron_lot/` a
  container. The test already supports this shape (it is how `lighthouse_greenhouse/` is
  laid out) and the page gets one section with a part for each attempt, same as the
  greenhouse.
- **Reproducibility is not claimed for any of the three.** None of them was ever verified
  from a clean session, and the pool's own commit message says so explicitly. The other
  paintings' tables say "byte for byte, verified by sha256"; these say **Not claimed**
  with the reason.

## Gotchas

- **Moving a painting into `paintings/` can falsify a measurement elsewhere.**
  `SUGGESTIONS.md` proves "six of the nine paintings used no pencil" by asserting that
  every `pencil` hit under `paintings/` is a filter-list mention. The pool and both
  herons draw, so that sentence became false the moment they moved. It now carves them
  out explicitly. Grep for the directory name *and* for claims that quantify over
  `paintings/` before moving anything into it.
- **Relative links break silently.** `heron_lot_2/NOTES.md` pointed at
  `../heron_lot/`; from `2/` that is now `../1/`. Nothing tests inter-notes links.
- **`probe_band.py` loads `heron.easel`**, which is not committed and never was. Left as
  it is with a comment saying where the file comes from — changing the string would not
  make it runnable from a clean checkout.
- **Line endings.** `.gitattributes` is `* text=auto eol=lf` and every other painting file
  is LF in the working tree; the heron files were authored CRLF. Normalised on the way in.
- **The page's prose enumerates paintings even though it refuses to count them.** Three
  passages name every picture in turn — the reading-set bullet, the subject-chosen-first
  rule and the unfinished list — so each needed a clause for each new painting. The
  unfinished list also still said "the two greenhouse attempts" when there are three;
  reworded to stop counting, which is the rule the page states for itself.

## File map

| Path | What changed |
|---|---|
| `paintings/pool_night/` | moved from `pool_night/` (tracked files, via `git mv`); `pool_at_night.{png,gif}` → `painting.{png,gif}` |
| `paintings/heron_lot/1/` | moved from `heron_lot/` (was untracked); `heron_dawn.{png,gif}` → `painting.{png,gif}` |
| `paintings/heron_lot/2/` | moved from `heron_lot_2/` (was untracked); `heron_dawn_2.{png,gif}` → `painting.{png,gif}` |
| `PAINTINGS.md` | two new sections (the pool; the heron pair, with a part each and a verdict); clauses added to the three enumerating passages |
| `SUGGESTIONS.md` | path references updated; the pencil measurement's supporting clause corrected |
| `*/NOTES.md` | output links renamed; the herons cross-link each other |

Full suite green.
