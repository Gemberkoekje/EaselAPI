# Running log — assisted run, rehearsal3

Every time I wanted to look at the source or a signature, I write it down here
instead, with what I did instead. Written as I go, not from memory.

## 0. How do I persist a session between `python` scripts?

- **Wanted:** `Session.save()` / `Session.load()`. PAINTER.md's API list
  (lines 727-749) has no save/load at all. The only persistence the guide
  describes is the CLI section at the very bottom: `easel new painting.easel`,
  `easel run painting.easel pass1.py`.
- **Expected:** since the guide says "Save the session as the guide describes",
  I expected a documented `s.save(path)`.
- **Did instead:** used the documented CLI form
  `python -m easel run painting.easel cN.py`, which is still "run with python"
  and does persist. Each pass script is therefore written for `easel run`
  (where `s`, `palette`, `cell`, `span`, ... are already in scope).
- **Would add to PAINTER.md:** one line in "The rest of the API" saying that a
  `Session` built in a plain script is *not* persistent, and that
  `easel run <file>.easel <script>.py` is the only way to continue a painting
  across processes.

---

## How the rest of this record was kept

Entry 0 above was written before the first mark. From `c3_sketch.py` onward I
wrote each one **into the header comment of the pass script where it bit**, at the
moment it bit, rather than into this file — so the record is distributed across
`c3`, `c12`, `c13`, `c14b`, `c16`, `c17`, `c19`, `c20`, `c23`, `c24`, `c26`, `c27`
and `c28`, each script's comment saying what I expected, what happened, and what I
did instead. `LOG.md` consolidates all of them into one numbered table
("What the guide cost me, in the order it bit"). The index:

| # | Pass where it bit | One line |
|---|---|---|
| 1 | before painting | no documented `Session.save()`; had to infer `easel run` |
| 2 | `c3_sketch.py` | `prep.merge(a, b)` — which number survives is undocumented; `KeyError` |
| 3 | `c3_sketch.py` | `s.sketch()` returns the whole StrokeRecord list; printing it is 35 KB |
| 4 | `c2_areas.py` | `prepare()` numbers areas but nothing draws the numbers; `region(n)` is a bbox |
| 5 | `c12_lines.py` | the background block-in buried the entire underdrawing |
| 6 | `c13_redraw.py` | `erase()` does not remove lines from `sketch_lines()` — engine defect |
| 7 | `c17_tea2.py` | `s.log()` returns a string, not records |
| 8 | `c17_tea2.py` | `tint(c, 0.80)` is a mix ratio, not a value — landed at 0.648 |
| 9 | `c16`→`c23` | a small brush does not cover in one pass the way `block_in` does |
| 10 | `c23`→`c24` | `block_in` overhang (0.35 x brush) ate the mug's right edge |
| 11 | `c26`, `c28` | `compare()` flags cells below the palette floor as if they were fixable |
| 12 | `t1_coverage.py` | a throwaway Session overwrites `out/look_00N.png` of the real one |
| 13 | `c27_final.py` | `smudge`/`dab`/`glaze` all count against `stroke_count`; unstated |
