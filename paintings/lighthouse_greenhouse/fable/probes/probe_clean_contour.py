"""edge="clean" arches the contour of a mass with few corners.

The clean contour is swept along the shape's SMOOTHED outline; through two sparse
corners the spline bows outward. ragged (which has no contour pass) stops correctly at
half a brush. Subdividing the sides gives the spline collinear points and fixes it.

Run: .venv/bin/python probes/probe_clean_contour.py
"""
import numpy as np
from PIL import Image

from easel import Session, polygon


def subdivide(points, n=6):
    out = []
    for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1], strict=True):
        for i in range(n):
            t = i / n
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    return out


def top_above(shape, top_edge, ground, **block_kw):
    """px of paint standing above `top_edge` in the shape's x-band."""
    s = Session(1024, 768, texture="linen", ground=ground, seed=3)
    s.block_in(shape, "flat", "burnt_umber", size=0.02, density=1.0, solid=True,
               direction=90, **block_kw)
    s.export("_contour.png", impasto=False)
    a = np.asarray(Image.open("_contour.png").convert("RGB")).astype(int)
    bg = np.median(a[:30].reshape(-1, 3), axis=0)
    xs = shape.box
    band = (np.abs(a - bg).sum(axis=2) > 40)[:, int(xs.x0 * 1024):int(xs.x1 * 1024)]
    rows = np.nonzero(band.any(axis=1))[0]
    return (top_edge - rows.min() / 768) * 768


def report(name, pts, top_edge, ground):
    print(f"  {name}")
    print(f"    ragged             : {top_above(polygon(pts), top_edge, ground, edge='ragged'):5.0f}px above the top edge")
    print(f"    clean              : {top_above(polygon(pts), top_edge, ground, edge='clean'):5.0f}px above the top edge")
    print(f"    clean, subdivided  : {top_above(polygon(subdivide(pts)), top_edge, ground, edge='clean'):5.0f}px above the top edge")


if __name__ == "__main__":
    print("A tall four-cornered tower, top edge at y=0.20:")
    report("fresh tower", [(0.30, 0.90), (0.40, 0.90), (0.38, 0.20), (0.32, 0.20)], 0.20, "toned_grey")
    print("\nThe dusk example's own tower() polygon, top edge at y=0.165 (its committed PNG predates this):")
    report("lighthouse_dusk tower", [(0.228, 0.630), (0.312, 0.630), (0.297, 0.165), (0.243, 0.165)], 0.165, "burnt_sienna")
    print("\nExpected: ragged ~2-4px (correct half-brush), clean ~45-67px (the arch), subdivided ~6px (fixed).")
