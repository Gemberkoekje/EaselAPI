"""`inset()` on a concave shape and on a spiky one. Item 3 of `ENGINE_CHANGES.md`.

One session reported `inset()` shrinking a mass by 2.7 times what it asked for. The
maintainer could not reproduce it on a convex square, where the offset is exact, and
guessed it would be real on a concave shape or a thin one. Both halves are here, and
they are two different things:

**The 2.7x is real, reproducible and correct.** A mitre offset moves every *edge* in
by the amount asked, so a *tip* has to move in by ``amount / sin(half-angle)`` -- which
is exactly where a brush of that reach has to stop. On a five-pointed star an
``inset(0.045)`` takes 0.24 off the width, not 0.09. That is the offset doing its job.
`scaled()` is the call that takes a fixed fraction off a mass. The arithmetic is not
touched; the docstring now says this.

**The concave case was a defect, and a different one.** The fold check asked whether
the offset shape's *centre* was still inside the original. A horseshoe does not
contain its own centroid -- the centroid sits in the gap -- so the check failed for a
reason that had nothing to do with the offset, threw away a perfectly good mitre, and
fell back to scaling about a point outside the mass. The result had half its points
*outside* the shape it had been asked to shrink. The check now tests containment of
the points, which is the invariant that was actually wanted.

Run it::

    python engine_changes/probe_inset.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO / "src") not in sys.path:
    sys.path.insert(0, str(_REPO / "src"))

from easel.regions import Polygon, _offset_ring, _try_polygon, polygon  # noqa: E402

AMOUNT = 0.045

HORSESHOE = polygon([(0.2, 0.2), (0.8, 0.2), (0.8, 0.35), (0.35, 0.35),
                     (0.35, 0.65), (0.8, 0.65), (0.8, 0.8), (0.2, 0.8)], name="horseshoe")
STAR = polygon([(0.5 + (0.25 if i % 2 == 0 else 0.0875) * math.cos(i * math.pi / 5),
                 0.5 + (0.25 if i % 2 == 0 else 0.0875) * math.sin(i * math.pi / 5))
                for i in range(10)], name="star")
SQUARE = polygon([(0.3, 0.3), (0.7, 0.3), (0.7, 0.7), (0.3, 0.7)], name="square")
BLOB_LIKE = polygon([(0.50, 0.14), (0.72, 0.26), (0.86, 0.50), (0.70, 0.72),
                     (0.50, 0.86), (0.28, 0.70), (0.16, 0.50), (0.30, 0.28)], name="lobed")


def old_inset(shape: Polygon, amount: float) -> Polygon:
    """The check as it was: the offset shape's *centre* had to be inside the original."""
    a = float(amount)
    pts = np.asarray(shape.points, dtype=np.float64)
    smaller = a > 0
    best = None
    for cand in (_offset_ring(pts, a), _offset_ring(pts, -a)):
        made = _try_polygon(cand, shape.name, shape.traced)
        if made is None or (made.area < shape.area) != smaller:
            continue
        if best is None or (made.area < best.area) == smaller:
            best = made
    if best is not None:
        sane = (best.area >= 0.05 * shape.area and shape.contains(*best.center)) if smaller \
            else (best.area >= 0.95 * shape.area and best.contains(*shape.center))
        if sane:
            return best
    return shape._toward_centre(a)


def outside(shape: Polygon, made: Polygon) -> int:
    """How many of the inset shape's points left the shape it was shrinking."""
    pts = np.asarray(made.points, dtype=np.float64)
    return int((~shape.inside(pts[:, 0], pts[:, 1])).sum())


def table() -> None:
    print(f"inset({AMOUNT}) -- 'shrink the silhouette all the way round'")
    print(f"{'shape':10s} {'centroid':>9s}  {'old area':>8s} {'out':>4s}   "
          f"{'new area':>8s} {'out':>4s}   {'width taken off':>15s}")
    for shape in (SQUARE, BLOB_LIKE, STAR, HORSESHOE):
        old, new = old_inset(shape, AMOUNT), shape.inset(AMOUNT)
        took = shape.width - new.width
        print(f"{shape.name:10s} {'in' if shape.contains(*shape.center) else 'OUTSIDE':>9s}  "
              f"{old.area:8.4f} {outside(shape, old):4d}   "
              f"{new.area:8.4f} {outside(shape, new):4d}   "
              f"{took:8.3f} = {took / (2 * AMOUNT):.2f}x asked")
    print()
    print("'out' is how many of the inset shape's own points ended up outside the")
    print("shape it was asked to shrink. Four of eight, on the shape that does not")
    print("contain its own centroid, was the defect.")
    print()
    print("The star's 2.7x is not: every edge moved in by exactly 0.045, and a tip")
    print("of that sharpness has to retreat further for that to be true. scaled() is")
    print("the call for taking a fixed fraction off a mass.")


PANEL, PAD = 300, 10
_ORIG = (150, 150, 160)
_OLD = (240, 130, 110)
_NEW = (140, 230, 170)


def panel(shape: Polygon, title: str) -> tuple[str, Image.Image]:
    img = Image.new("RGB", (PANEL, PANEL), (24, 24, 28))
    draw = ImageDraw.Draw(img)

    def px(poly):
        return [(PAD + x * (PANEL - 2 * PAD), PAD + y * (PANEL - 2 * PAD))
                for x, y in poly.closed]

    draw.polygon(px(shape), fill=(52, 52, 60), outline=_ORIG)
    draw.line(px(old_inset(shape, AMOUNT)), fill=_OLD, width=2)
    draw.line(px(shape.inset(AMOUNT)), fill=_NEW, width=2)
    return title, img


def build() -> Image.Image:
    made = [panel(HORSESHOE, "horseshoe: centroid in the gap"),
            panel(BLOB_LIKE, "lobed: unchanged"),
            panel(STAR, "star: 2.7x, and correct"),
            panel(SQUARE, "square: exact, unchanged")]
    label_h, foot = 20, 22
    sheet = Image.new("RGB", (len(made) * (PANEL + 2), PANEL + label_h + foot),
                      (18, 18, 20))
    draw = ImageDraw.Draw(sheet)
    for i, (title, img) in enumerate(made):
        draw.text((i * (PANEL + 2) + 6, 5), title, fill=(250, 238, 200))
        sheet.paste(img, (i * (PANEL + 2), label_h))
    draw.text((6, label_h + PANEL + 5),
              f"grey: the shape.   red: inset({AMOUNT}) as it was.   "
              f"green: inset({AMOUNT}) now.", fill=(210, 210, 215))
    return sheet


def main(argv: list[str]) -> int:
    table()
    out = Path(argv[0]) if argv else Path(__file__).parent / "inset_shapes.png"
    sheet = build()
    sheet.save(out)
    print(f"\nWrote {out} ({sheet.size[0]}x{sheet.size[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
