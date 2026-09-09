# How the samples were taken

Twenty-four fresh sessions, eight per condition, each asked to name a subject and
nothing else. Each was told not to read any file in the repo other than the guide
variant it was handed, and not to paint.

- **A — bare**: no guide, only a neutral one-line description of the medium.
- **B — guide as read**: `guide_B_as_read.md`, which is `git show HEAD:PAINTER.md` —
  the exact text the REHEARSAL3 session read before it painted its estuary.
- **C — guide neutralised**: `guide_C_neutralised.md`, byte-for-byte the same file
  with five clauses changed. `a field of sky` -> `a panel of ceiling`; `a wall, a
  sky, a tabletop, a coat` -> `a wall, a door, a tabletop, a coat`; `a band of water
  blocked in under a headland` -> `a band of carpet blocked in under a cabinet`; and
  `horizon()` renamed `band_at()` in its two mentions. Same length, same advice, same
  API surface otherwise. The rename makes the C guide inaccurate about one function
  name, which costs nothing here because condition C never runs any code.

Landscape-noun count: B has 7 in 981 lines, C has 0.
