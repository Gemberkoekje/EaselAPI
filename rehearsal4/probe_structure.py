"""Is the second unprompted painting built differently from the first?

The brief constrains the repeat, not the remedy:

    **The second must differ from the first in compositional structure**, and that is
    the only constraint. If the first is built from horizontal bands, the second must
    not be.

and points at `rehearsal3/probe_axis_alignment.py` for the number. That probe answers
"how square is this picture", which is related but not the same question: two pictures
can both be 30% axis-aligned and one be a stack of bands while the other is a grid.
So three numbers here, all of them cheap and all of them from the exported PNG:

**banding** -- the variance of the row means over the variance of the column means, in
dB. A stack of horizontal bands changes a lot going down and little going across, so it
scores high positive; a picture built from vertical divisions scores negative; something
with no dominant direction sits near zero.

**horizontal share / vertical share** -- of the strong edges that are axis-aligned,
which axis. `probe_axis_alignment.py` folds the two together into one number, and the
fold is exactly what this stage needs to see apart.

**mass centroid spread** -- how far the dark mass sits from the picture's centre, as a
fraction of the diagonal, with its direction. A picture whose weight is a low band and
one whose weight is a side column differ here even when their edge statistics match.

None of these is a verdict. The verdict is the human looking at the pair. These are
here so the write-up can say *how* they differ rather than only that they do.

Run from the repo root:  python rehearsal4/probe_structure.py
"""
from __future__ import annotations

import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOLERANCE_DEG = 10.0
STRONG_PERCENTILE = 80.0


def _grey(path: str, longest: int = 900) -> np.ndarray:
    im = Image.open(path).convert("L")
    im.thumbnail((longest, longest), Image.LANCZOS)
    return np.asarray(im, dtype=np.float64) / 255.0


def _convolve(a: np.ndarray, k: np.ndarray) -> np.ndarray:
    out = np.zeros_like(a)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            out[1:-1, 1:-1] += k[dy + 1, dx + 1] * a[
                1 + dy: a.shape[0] - 1 + dy, 1 + dx: a.shape[1] - 1 + dx
            ]
    return out


def banding_db(a: np.ndarray) -> float:
    """Row-mean variance over column-mean variance, in dB. Positive means banded."""
    rows = a.mean(axis=1).var()
    cols = a.mean(axis=0).var()
    tiny = 1e-12
    return 10.0 * float(np.log10((rows + tiny) / (cols + tiny)))


def edge_split(a: np.ndarray) -> tuple[float, float]:
    """Share of all strong edges running near-horizontal, and near-vertical."""
    kx = np.array([[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]])
    gx, gy = _convolve(a, kx), _convolve(a, kx.T)
    mag = np.hypot(gx, gy)
    strong = mag >= np.percentile(mag, STRONG_PERCENTILE)
    if not strong.any():
        return (float("nan"), float("nan"))
    # The edge runs perpendicular to the gradient; fold to [0, 180) then to a
    # signed distance from each axis.
    edge = (np.degrees(np.arctan2(gy[strong], gx[strong])) + 90.0) % 180.0
    horizontal = np.minimum(edge, 180.0 - edge) < TOLERANCE_DEG
    vertical = np.abs(edge - 90.0) < TOLERANCE_DEG
    n = edge.size
    return (100.0 * float(horizontal.sum()) / n, 100.0 * float(vertical.sum()) / n)


def dark_centroid(a: np.ndarray) -> tuple[float, float, float]:
    """Where the dark mass sits: (dx, dy, distance), normalised, origin at centre."""
    weight = 1.0 - a
    total = weight.sum()
    if total <= 0:
        return (0.0, 0.0, 0.0)
    h, w = a.shape
    ys, xs = np.mgrid[0:h, 0:w]
    cx = float((weight * xs).sum() / total) / w - 0.5
    cy = float((weight * ys).sum() / total) / h - 0.5
    return (cx, cy, float(np.hypot(cx, cy)))


def report(rows: list[tuple[str, str]]) -> None:
    width = max(len(n) for n, _ in rows)
    print(f"  {'':<{width}}   band dB    horiz%    vert%    dark mass from centre")
    for name, path in rows:
        if not os.path.exists(path):
            print(f"  {name:<{width}}   (missing)")
            continue
        a = _grey(path)
        band = banding_db(a)
        horizontal, vertical = edge_split(a)
        dx, dy, dist = dark_centroid(a)
        where = f"{dist:.3f}  ({dx:+.3f}, {dy:+.3f})"
        print(f"  {name:<{width}}   {band:+7.2f}   {horizontal:6.1f}   {vertical:6.1f}"
              f"    {where}")


if __name__ == "__main__":
    print("Compositional structure, measured from the exported PNGs.")
    print("band dB: positive = banded across the picture's height (stacked "
          "horizontal bands), negative = divided down its width.\n")

    print("The two unprompted paintings this run:")
    report([
        ("unprompted 1 (no constraint)", f"{HERE}/pass/own1_final.png"),
        ("unprompted 2 (must differ)", f"{HERE}/pass/own2_final.png"),
    ])

    print("\nFor scale - earlier unprompted paintings, and this run's copies:")
    report([
        ("REHEARSAL3 unprompted", f"{ROOT}/rehearsal3/pass/own_final.png"),
        ("REHEARSAL2 unprompted", f"{ROOT}/rehearsal2/own_final.png"),
        ("REHEARSAL1 unprompted", f"{ROOT}/rehearsal/own_final.png"),
        ("REHEARSAL4 copy (mug)", f"{HERE}/pass/copy_final.png"),
        ("REHEARSAL4 copy (sitter)", f"{HERE}/sitter/copy_final.png"),
    ])

    print("\nAnd the references, which nobody composed:")
    report([
        ("Level1 (the mug photo)", "C:/temp/Level1.jpg"),
        ("Level3 (the sitter photo)", "C:/temp/Level3.jpg"),
    ])
