"""How axis-aligned is a picture? The number behind the human's note.

`HUMAN_NOTES.md` says the paintings show "a lot of very horizontal or vertical
strokes, which really show the edges of those square strokes". That is a judgement
about edges, so measure edges: take every pixel whose gradient is strong, work out
which way the *edge* through it runs, and report the share of them running within
ten degrees of horizontal or vertical.

A photograph of a room full of tables and walls is genuinely quite axis-aligned, so
the number only means something next to its own reference. The comparison that
matters is painting against the thing it was painted from.

Run from the repo root:  python rehearsal3/probe_axis_alignment.py
"""
from __future__ import annotations

import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOLERANCE_DEG = 10.0
STRONG_PERCENTILE = 80.0


def axis_share(path: str, box: tuple[float, float, float, float] | None = None) -> float:
    """Share of strong edges running within TOLERANCE_DEG of an axis, as a percentage.

    Args:
        path: an image file.
        box: optional normalised (x0, y0, x1, y1) crop, so a panel of a sheet can be
            measured on its own.
    """
    im = Image.open(path).convert("L")
    if box is not None:
        w, h = im.size
        im = im.crop((round(box[0] * w), round(box[1] * h),
                      round(box[2] * w), round(box[3] * h)))
    im.thumbnail((900, 900), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float64) / 255.0

    # Sobel, written out: the point of this probe is a number nobody has to trust a
    # library for.
    kx = np.array([[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]])
    ky = kx.T
    gx = _convolve(a, kx)
    gy = _convolve(a, ky)

    mag = np.hypot(gx, gy)
    strong = mag >= np.percentile(mag, STRONG_PERCENTILE)
    if not strong.any():
        return float("nan")

    # The edge runs perpendicular to the gradient. Fold to [0, 90): an edge at 0 is
    # horizontal, at 90 vertical, and both count as axis-aligned.
    edge = (np.degrees(np.arctan2(gy[strong], gx[strong])) + 90.0) % 90.0
    off = np.minimum(edge, 90.0 - edge)
    return 100.0 * float((off < TOLERANCE_DEG).mean())


def _convolve(a: np.ndarray, k: np.ndarray) -> np.ndarray:
    """3x3 convolution on the interior, edges dropped."""
    out = np.zeros_like(a)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            out[1:-1, 1:-1] += k[dy + 1, dx + 1] * a[
                1 + dy: a.shape[0] - 1 + dy, 1 + dx: a.shape[1] - 1 + dx
            ]
    return out


def report(rows: list[tuple[str, str, tuple | None]]) -> None:
    width = max(len(name) for name, _, _ in rows)
    for name, path, box in rows:
        if not os.path.exists(path):
            print(f"  {name:<{width}}  (missing: {path})")
            continue
        print(f"  {name:<{width}}  {axis_share(path, box):5.1f} %")


def panel(i: int, n: int = 4) -> tuple[float, float, float, float]:
    """A panel of the four-up mountain sheet, inset to miss the label bars."""
    left, top = 120, 46
    w, h, gap = 700, 520, 10
    total_w, total_h = 2970, 586
    x0 = (left + gap + i * (w + gap)) / total_w
    return (x0 + 0.004, (top + gap + 20) / total_h,
            x0 + (w - 12) / total_w, (top + h - 10) / total_h)


if __name__ == "__main__":
    tol = f"within {TOLERANCE_DEG:.0f} deg of an axis"
    print(f"Share of strong edges {tol}. Higher means more square.\n")

    print("The references, for scale:")
    report([
        ("Level1 (mug on a table)", "C:/temp/Level1.jpg", None),
        ("Level2 (painted landscape)", "C:/temp/Level2.jpg", None),
        ("Level3 (the sitter)", "C:/temp/Level3.jpg", None),
    ])

    print("\nWhat this engine has produced so far:")
    report([
        ("REHEARSAL2 copy (the sitter)", f"{ROOT}/rehearsal2/copy_final.png", None),
        ("REHEARSAL2 own (estuary)", f"{ROOT}/rehearsal2/own_final.png", None),
        ("REHEARSAL1 copy", f"{ROOT}/rehearsal/copy_final.png", None),
        ("REHEARSAL1 own", f"{ROOT}/rehearsal/own_final.png", None),
    ])

    sheet = f"{HERE}/probe_axis_mountain.png"
    print("\nThe same hillside, four ways (probe_axis_mountain.png):")
    report([
        ("block_in box", sheet, panel(0)),
        ("guide's edge() columns", sheet, panel(1)),
        ("along the slope, tip follows", sheet, panel(2)),
        ("along the slope, tip pinned", sheet, panel(3)),
    ])

    print("\nThis run's paintings:")
    report([
        ("rehearsal3 pass (mug)", f"{HERE}/pass/copy_final.png", None),
        ("rehearsal3 pass (unprompted)", f"{HERE}/pass/own_final.png", None),
        ("rehearsal3 sitter", f"{HERE}/sitter/copy_final.png", None),
        ("rehearsal3 assisted (mug)", f"{HERE}/assisted/copy_final.png", None),
    ])
