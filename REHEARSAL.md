# M5 — the rehearsal

**To understand this, start by reading `painting-api-brief.md` (what M5 is for), then
this file, then the diff to `PAINTER.md` (which is the actual deliverable), then
`REVIEW.md` findings 15–18 (the engine defects this turned up).**

The protocol, run as written: take a reference photograph and `PAINTER.md`, paint a
copy using nothing else, then paint something unprompted. Every reach for the source
or for knowledge a fresh session would not have counts as a gap in the guide.

Reference: a photograph of a man in profile in a dim interior, gesturing — a harder
subject than the brief's "ordinary object", which made it a better test.

---

## The verdict first

**The copy does not meet the definition of done.** At 256 strokes it has a defensible
value structure, a painterly surface and masses in roughly the right places, and it
is *not* a recognisable likeness. The head reads as a head-shaped mass; the hand
reads as a pale rectangle. A viewer given both would see corresponding masses, not a
copy.

**The unprompted painting went far better** — 78 strokes, a clear light/mid/dark
structure, a real painted silhouette, varied edges. That gap is itself the finding:
the engine and the guide serve unprompted painting much better than they serve
copying, and copying is the half of the experiment that runs first.

Both are in `rehearsal/`, with their time-lapses.

The single largest cause was that **the painter had no shared vocabulary with the
reference.** The guide's whole answer to "you cannot reason in pixels" is the
labelled grid — and the grid was drawn only on the canvas, never on the reference
beside it. So every coordinate came out of the model's head, which is exactly the
faculty the brief says is unreliable. Half this painting was made before that was
fixed and half after; the difference was not subtle, and it is why the new *Working
from a reference* section is the most important thing in this diff.

## What the rehearsal cost, in order of when it bit

| # | What happened | Fixed in |
|---|---|---|
| 1 | Guide exercise 2 showed six pressure profiles that looked identical | `PAINTER.md`, exercise rewritten |
| 2 | Guide exercise 4 demonstrated the opposite of its own lesson | `PAINTER.md`, exercise rewritten |
| 3 | A block-in aimed at the middle of the canvas smeared across all of it | engine — REVIEW 15 |
| 4 | Blocked in rectangles because a region *is* a rectangle; no advice for a silhouette | `PAINTER.md`, new snippet |
| 5 | Planned values with `value_of` and got mush; the number contradicted the picture | engine — REVIEW 16 |
| 6 | No idea the palette cannot go below value 0.23 | `PAINTER.md` |
| 7 | Scumbled at `load=0.55` and silkscreened the canvas weave over everything | engine — REVIEW 17 |
| 8 | Laid a "painterly" half-load pass and then could not get anything solid on top | `PAINTER.md` |
| 9 | Could not put the grid on the reference; could not compare values against it | engine — REVIEW 18 |
| 10 | Three `knife` marks read as strips of tape stuck to the painting | `PAINTER.md` |

Items 3, 5, 7 and 9 are engine defects, written up as REVIEW.md findings 15–18 with
the measurements. Finding 17 is the one REVIEW finding 11 explicitly deferred to this
milestone "with the sampler and a real painting as the evidence" — the rehearsal
produced both, and it turned out to be real.

## What changed in the guide

- **New section, *Working from a reference*.** How to use one grid across both
  panels: name the big masses by cell before painting, compare cell against cell,
  correct by cell. Compare values as often as colours. Get the value map right
  before the drawing, then stop measuring.
- **Value planning as numbers.** `value_of` was a row in a table; it is now part of
  workflow step 2, with the warning that two mixtures within `0.10` will not read as
  separate masses.
- **The palette's real range, `0.23`–`0.96`.** There is no near-black, so contrast is
  built by pushing the lights up, not the darks down. Nothing said this before, and
  a painter aiming at a dark mass will otherwise fight the palette for a long time.
- **Load is not only a dry-brush control.** Brushes start at `0.9`–`1.0` and anything
  that must read as solid wants to stay there. The `0.4`–`0.6` window is for
  deliberately broken marks.
- **Don't lay one broken pass across the whole canvas.** One load edge to edge prints
  the surface's own texture as an even field under everything painted afterwards.
- **A region is a rectangle; almost nothing you paint is.** With a working snippet
  that sweeps strokes along a boundary to build a real silhouette.
- **Wetness, quantified.** Paint lands at ~`0.7` and loses ~6% per stroke made
  anywhere — half gone in about eleven strokes. And one `block_in` is ten to thirty
  strokes, so a mass is mostly dry by the time the next one is finished.
- **What pressure actually does** (opacity, not width) and therefore that varying
  mark width is the painter's own job.
- **The `knife` warning**, and where `look()` writes its files.

`examples/exercises.py` was updated in step with the two rewritten exercises, so the
runnable copies do not drift from the printed ones.

## Gotchas for the next session

1. **The grid is the whole game when copying.** `look(reference=..., grid=True)` now
   labels both panels identically. Read the reference *out loud* by cell before
   painting — "the coat fills E5 to H8" — and correct by cell afterwards. Errors of
   placement are invisible when you look at your own painting alone, because it
   looks internally consistent.
2. **Assert on the canvas, not the return value** — still true, and it is what caught
   findings 15 and 16. The block-in reported a normal-looking set of records while
   painting a third of the canvas it was never asked to touch.
3. **The right instrument matters as much as the measurement.** The first attempt at
   finding 17 measured the height map's autocorrelation, improved it, and did not fix
   the visible artefact, because the artefact comes from the *gate*, not the texture.
   That change was reverted. Look at deposited paint.
4. **A quality fix can break a different quality.** Rebalancing the tooth gate cleared
   the halftone screen and flattened the difference between the three surfaces;
   `test_surfaces_break_up_at_their_own_scale` caught it. The real fix was to make the
   grain's *scale* follow the surface, not to loosen the test.
5. **`Region` and the whole API are in scope inside an `easel run` script** without
   imports, as documented. `s.canvas.rgb` and `s.canvas.wetness` are readable and were
   useful for probing, but a fresh painter should not need them — where this rehearsal
   needed them, that is recorded above as a gap.

## Still open

- **Pressure does not modulate stroke width.** Measured, evidenced and deliberately
  not fixed — see REVIEW.md *Open, with evidence*. It would improve mark variety and
  it would change every stroke in the engine, which is not a thing to do by eye at the
  end of a milestone.
- **The copy is not a likeness.** The guide is materially better than it was, but
  nothing here proves a fresh session would now clear the bar. The honest next step is
  to re-run the protocol with a genuinely fresh session and the revised guide, and to
  treat *that* result as the measurement — this one was made by someone who had by
  then read the source.
- Golden-image tests still do not exist; the property tests catch behaviour, not
  appearance.
- The MCP server, now M8 in the brief.

## File map

```
rehearsal/
  p1_masses.py … p7_finish.py   the copy, one script per pass
  copy_final.png                the copy, 256 strokes
  copy_timelapse.gif
  own1.py own2.py own3.py       the unprompted painting
  own_final.png                 78 strokes
  own_timelapse.gif
  ex*.py                        the guide's six exercises, run verbatim
  probe_*.py                    the measurements behind REVIEW 15-18
  check_guide_blocks.py         executes every python block in PAINTER.md
```

Changed outside `rehearsal/`: `PAINTER.md` (the deliverable), `REVIEW.md`
(findings 15–18), `examples/exercises.py`, `src/easel/{session,palette,canvas,look}.py`,
`tests/test_engine.py` (+11 tests, 89 total), and `samples/brushes.png` regenerated.
