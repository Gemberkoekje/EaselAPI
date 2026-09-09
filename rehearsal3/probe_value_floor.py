"""How dark can this palette actually go, and is the guide's 0.10 rule reachable?

Two fresh sessions of the M6 pass independently stopped and reported the same thing:
`compare()` asks them to bring every cell within 0.10 of the reference, the palette
bottoms out somewhere near 0.23, and a low-key photograph has cells far below that.
They each spent strokes finding it out. Neither could check it, because checking it
means reading the palette, which they were not allowed to do.

So check it from outside, the way they would have if the guide had told them how.
Values are read off the exported PNG, not out of the engine — gotcha 0 in NOTES.md:
measure the picture the painter actually sees.

Run from the repo root:  python rehearsal3/probe_value_floor.py
"""
from __future__ import annotations

import os

import numpy as np
from PIL import Image

from easel import Region, Session

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "_floor.png")
PATCH = Region(0.15, 0.15, 0.85, 0.85, "patch")


def patch_value(s: Session) -> float:
    """Mean sRGB value of the middle of the canvas, from the exported PNG."""
    s.export(SCRATCH)
    a = np.asarray(Image.open(SCRATCH).convert("L"), dtype=np.float64) / 255.0
    h, w = a.shape
    return float(a[int(0.3 * h): int(0.7 * h), int(0.3 * w): int(0.7 * w)].mean())


def flat(color, passes: int = 1, ground: str = "toned_grey") -> float:
    s = Session(320, 320, texture="smooth", ground=ground, seed=3)
    for _ in range(passes):
        s.block_in(PATCH, "flat", color, size=0.30, density=1.0)
        s.dry()
    return patch_value(s)


def glazed(color, coats: int) -> float:
    s = Session(320, 320, texture="smooth", ground="toned_grey", seed=3)
    s.block_in(PATCH, "flat", color, size=0.30)
    s.dry()
    for _ in range(coats):
        s.glaze([(0.1, 0.35), (0.9, 0.35)], color, opacity=0.6)
        s.glaze([(0.1, 0.5), (0.9, 0.5)], color, opacity=0.6)
        s.glaze([(0.1, 0.65), (0.9, 0.65)], color, opacity=0.6)
        s.dry()
    return patch_value(s)


def reference_cells(path: str) -> np.ndarray:
    """Per-cell reference values, straight out of the painter's own compare()."""
    s = Session(400, 300, ground="toned_grey", seed=1)
    return np.array([c.ref for c in s.compare(path).cells])


if __name__ == "__main__":
    pal = Session(64, 64, seed=1).palette
    pigments = sorted(set(pal.pigment_names))
    print(f"{len(pigments)} pigments, one flat pass each on a toned grey ground:\n")
    rows = sorted(((n, flat(n)) for n in pigments), key=lambda r: r[1])
    for name, v in rows:
        print(f"  {name:<18} {v:.3f}")

    dark, floor = rows[0]
    print(f"\nDarkest single pigment: {dark} at {floor:.3f}")

    print("\nDoes piling it on go darker?")
    for n in (1, 2, 4, 8):
        print(f"  {n} dried pass(es)      {flat(dark, n):.3f}")

    print("\nDoes glazing it over itself go darker?")
    for n in (1, 2, 4):
        print(f"  {n} glaze round(s)      {glazed(dark, n):.3f}")

    print("\nDoes mixing the darks together go darker?")
    names = [n for n, _ in rows[:5]]
    for i in range(2, len(names) + 1):
        mixed = pal.mix_many([pal[n] for n in names[:i]])
        print(f"  {' + '.join(names[:i]):<50} {flat(mixed):.3f}")

    print("\nTwo passes of the darkest pigment, per ground:")
    for ground in ("white", "toned_grey", "cool_grey", "umber_wash", "burnt_sienna"):
        print(f"  {ground:<16} {flat(dark, 2, ground=ground):.3f}")

    print("\nWhat the references ask for (compare()'s own per-cell numbers):")
    for name in ("Level1", "Level2", "Level3"):
        vals = reference_cells(f"C:/temp/{name}.jpg")
        unreachable = int((vals < floor - 0.10).sum())
        print(
            f"  {name}.jpg  cells {vals.min():.3f}-{vals.max():.3f}   "
            f"{unreachable} of {vals.size} cells cannot be brought within 0.10"
        )

    if os.path.exists(SCRATCH):
        os.remove(SCRATCH)
