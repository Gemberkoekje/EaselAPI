"""Build the guide variants the naming probe hands out.

`rehearsal3/unprompted/` tested whether the guide's landscape *nouns* were what made
fresh sessions reach for an estuary. They were not: condition C removed five clauses
and moved water-with-horizon from 2 of 8 to 0 of 8, a drop of 2 against a
pre-registered threshold of 4 (Fisher p ~ 0.47, statistically nothing).

The guide's *procedure* was never tested, and it is a landscape recipe whether or not
the word sky appears in it: "the far mass, then the middle one, then the near one --
background, middle distance, foreground, in that order, every time." That is what this
builds a control for.

- **B** is the guide exactly as it stands, snapshotted so this run stays reproducible
  after the next edit to `PAINTER.md`.
- **D** is the same file with the depth-ordered workflow replaced by a size-ordered
  one: largest mass first, smallest last, nothing about what is in front of what.
  Same length, same API surface, same advice *quality* -- painting large to small is a
  real method, not a straw man. What it does not carry is recession.

Everything else is byte-for-byte identical. The replacement list is printed on every
run and any clause that fails to match is reported, so a silent miss cannot happen.

Run from the repo root:  python rehearsal5/naming/make_guides.py
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
GUIDE = f"{ROOT}/PAINTER.md"

#: (what it says now, what D says instead). Order matters: the longest, most specific
#: clauses go first so a short one cannot eat part of a long one.
SWAPS: list[tuple[str, str]] = [
    # -- the heading and the rule itself -------------------------------------
    ("### 2. Paint from back to front",
     "### 2. Paint from the largest mass to the smallest"),
    ("""**Lay the furthest thing first and let each nearer thing be painted over it.** The
far mass, then the middle one, then the near one, then the small shape standing in
front of all of them. Background, middle distance, foreground, in that order, every
time.""",
     """**Lay the largest mass first and let each smaller one be painted over it.** The
biggest area, then the next biggest, then the small one, then the little shape that
sits on top of all of them. Largest, large, small, smallest, in that order, every
time."""),
    # -- the worked example --------------------------------------------------
    ("""s.palette["far"]  = s.palette.tint("cerulean", 0.55)
s.palette["near"] = s.palette.desaturate(s.palette["far"], 0.4)

s.block_in("upper-half", "flat", "far", size=0.18)          # furthest
s.block_in(span("A4", "H6"), "flat", "near", size=0.16)     # nearer
s.stroke([(0.3, 0.42), (0.3, 0.78)], "bristle", "dark", size=0.03)   # in front""",
     """s.palette["big"]   = s.palette.tint("cerulean", 0.55)
s.palette["small"] = s.palette.desaturate(s.palette["big"], 0.4)

s.block_in("upper-half", "flat", "big", size=0.18)          # largest
s.block_in(span("A4", "H6"), "flat", "small", size=0.16)    # next
s.stroke([(0.3, 0.42), (0.3, 0.78)], "bristle", "dark", size=0.03)   # smallest"""),
    ("""The narrow shape's edges are now real edges — the place where its paint stops and
the mass behind it is still showing — and you drew none of them. Paint it first and
the only way to get the same edges is to cut the mass behind it carefully around
it,""",
     """The narrow shape's edges are now real edges — the place where its paint stops and
the larger mass is still showing — and you drew none of them. Paint it first and
the only way to get the same edges is to cut the larger mass carefully around
it,"""),
    # -- the three consequences ----------------------------------------------
    ("""- **Draw the near things after the far masses are down.** A pencil line laid on the
  ground and then blocked over is gone — paint buries graphite in proportion to how
  much lands, and a full-strength block-in lands all of it. Landmarks go down before
  anything; the pencil goes down after the far masses; the near masses go on top.
- **Let the near mass overlap.** Run it a little into the far one. A silhouette
  that stops exactly on a boundary was measured; one that overlaps was painted.
- **A mistake in the background is cheap while the foreground is not there yet.**
  It stops being cheap the moment something is standing in front of it.""",
     """- **Draw the small things after the large masses are down.** A pencil line laid on the
  ground and then blocked over is gone — paint buries graphite in proportion to how
  much lands, and a full-strength block-in lands all of it. Landmarks go down before
  anything; the pencil goes down after the large masses; the small masses go on top.
- **Let the smaller mass overlap.** Run it a little into the larger one. A silhouette
  that stops exactly on a boundary was measured; one that overlaps was painted.
- **A mistake in a large mass is cheap while the small ones are not there yet.**
  It stops being cheap the moment something is sitting on top of it."""),
    ("""The exception is the ground itself, which is behind everything and goes on first by
definition. Everything after that is in depth order.""",
     """The exception is the ground itself, which is under everything and goes on first by
definition. Everything after that is in order of size."""),
    # -- the nested-mass paragraph, rebuilt on size rather than depth ---------
    ("""**Anything with an inside has its own depth order, and it is the one most often got
wrong.** A hollow thing is not one mass. It is three, at three depths, and all three
belong to the same object: **the far edge, then what is inside, then the near edge.**""",
     """**Anything with a part inside it has its own order of size, and it is the one most
often got wrong.** Such a thing is not one mass. It is three, at three sizes, and all
three belong to the same object: **the whole of it, then the part within, then the
mark that sits on that.**"""),
    ("""far  = ellipse(span("D2", "F3"))          # what stands behind the inside
near = polygon([(0.36, 0.31), (0.64, 0.31), (0.62, 0.72), (0.38, 0.72)])

s.block_in(far, "flat", "pale", size=0.04)                 # behind the inside
s.block_in(far.inset(0.015), "flat", "dark", size=0.04)    # the inside
s.block_in(near, "flat", "light", size=0.06)               # in front of the inside""",
     """whole = ellipse(span("D2", "F3"))         # the whole of the thing
mark  = polygon([(0.36, 0.31), (0.64, 0.31), (0.62, 0.72), (0.38, 0.72)])

s.block_in(whole, "flat", "pale", size=0.04)               # the whole of it
s.block_in(whole.inset(0.015), "flat", "dark", size=0.04)  # the part within
s.block_in(mark, "flat", "light", size=0.06)               # the mark on that"""),
    ("""Painted in that order, the inside's near edge is a real edge — the place where the
near mass's paint stops and the dark behind it still shows. Painted the other way
round there is nothing for the inside to stop against, so it runs out over the near
edge and no later mark puts it back: you would be cutting the near mass in around a
dark that is already outside it, which is painting up to a line.

It holds for a boat, an archway, a barrel, a hood, a cuff, a window reveal, a cave
mouth — anything you can see into. Ask it before the first stroke: **what is behind
the inside, what is the inside, and what is in front of it?**""",
     """Painted in that order, the smaller mass's edge is a real edge — the place where the
smaller mass's paint stops and the larger one still shows. Painted the other way
round there is nothing for the small mass to stop against, so it runs out over the
larger one and no later mark puts it back: you would be cutting the larger mass in
around a small one already outside it, which is painting up to a line.

It holds for a boat, an archway, a barrel, a hood, a cuff, a window reveal, a cave
mouth — anything built of parts. Ask it before the first stroke: **what is the whole
of it, what is the part within, and what sits on that?**"""),
    # -- the three references elsewhere in the document -----------------------
    ("""The order, in one sentence: **landmarks before anything, pencil after the far
masses are down, near masses on top.** Landmarks are points, and paint cannot bury
them. The pencil can be buried, so it goes on over the far masses and under the
near ones — that is what back to front buys you here.""",
     """The order, in one sentence: **landmarks before anything, pencil after the large
masses are down, small masses on top.** Landmarks are points, and paint cannot bury
them. The pencil can be buried, so it goes on over the large masses and under the
small ones — that is what largest-to-smallest buys you here."""),
    ("Then, once the far masses are down, draw with the pencil through the points:",
     "Then, once the large masses are down, draw with the pencil through the points:"),
    ("""either: the silhouette is where this mass's paint stops and the mass behind it still
shows, which is why the far masses go down first.""",
     """either: the silhouette is where this mass's paint stops and the larger mass still
shows, which is why the large masses go down first."""),
    ("""band and wrong for a mass that meets another at the *same* depth, where it lands on
its neighbour. Painting back to front is the real answer — the far mass spilling into
where the near one is going does no harm, because the near one goes on over it next.
For two masses at the same depth, pass `overhang=0` or inset the place by half the
brush size.""",
     """band and wrong for a mass that meets another of the *same* size, where it lands on
its neighbour. Painting largest to smallest is the real answer — the large mass
spilling into where the small one is going does no harm, because the small one goes
on over it next. For two masses of the same size, pass `overhang=0` or inset the
place by half the brush size."""),
    ("""- Was it painted back to front? An edge you had to cut carefully around something
  is a mass that went on in the wrong order.
- **Anything with an inside — is its far edge under its contents, and its contents
  under its near edge?** Something that has escaped the thing containing it, or a
  small mass sitting *on* a bigger one rather than *in* it: the same mistake twice.""",
     """- Was it painted largest to smallest? An edge you had to cut carefully around
  something is a mass that went on in the wrong order.
- **Anything built of parts — is the whole of it under its parts, and its parts
  under the marks on them?** Something that has escaped the thing containing it, or a
  small mass laid before the big one it belongs to: the same mistake twice."""),
]

#: Words that would give the manipulation away or reintroduce recession. Reported,
#: not fixed, so a leftover is a decision rather than a silent pass.
TELLTALES = ("back to front", "middle distance", "foreground", "depth order",
             "furthest", "nearer thing", "same depth", "far mass",
             "near mass", "behind it", "in front of")


def build() -> int:
    original = open(GUIDE, encoding="utf-8").read()
    variant = original
    misses = 0
    print(f"{len(SWAPS)} replacements:")
    for old, new in SWAPS:
        count = variant.count(old)
        head = old.strip().splitlines()[0][:56]
        if count != 1:
            misses += 1
            print(f"  MISS ({count} matches)  {head}")
            continue
        variant = variant.replace(old, new)
        print(f"  ok                  {head}")

    b_path, d_path = f"{HERE}/guide_B_as_read.md", f"{HERE}/guide_D_size_order.md"
    open(b_path, "w", encoding="utf-8", newline="\n").write(original)
    open(d_path, "w", encoding="utf-8", newline="\n").write(variant)

    print(f"\n  B  {len(original.split()):>6} words  {b_path}")
    print(f"  D  {len(variant.split()):>6} words  {d_path}")
    print(f"  difference: {len(variant.split()) - len(original.split()):+d} words")

    print("\nTelltales left in D (each one would leak the manipulation):")
    for word in TELLTALES:
        n = variant.lower().count(word)
        print(f"  {word:<16} {n}" + ("   <-- LEFTOVER" if n else ""))
    return misses


if __name__ == "__main__":
    sys.exit(1 if build() else 0)
