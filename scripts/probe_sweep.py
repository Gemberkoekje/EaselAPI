"""What `sweep()` costs and what it buys, measured on one shaped mass.

`s.sweep()` replaced a fifteen-line recipe. The claim behind both is
that a mass with a silhouette wants passes swept along its boundary, and that a box
drawn round it is a box for good. This measures that on one arbitrary boundary,
three ways -- a `block_in` over the bounding rectangle, a sweep, and a sweep crossed
-- and writes the sheet to look at beside the numbers.

**Is it the shape you asked for?**

* **Axis-aligned edges**: the share of strong edges running within ten degrees of
  horizontal or vertical. Higher is squarer. It is the number behind the human's
  note that every mass in these paintings was laid along the canvas's own axes.
* **Paint outside the shape**: the share of painted pixels that landed more than
  half a brush on the wrong side of the boundary. A rectangle's corners are all
  outside a shape that has a silhouette, and no later work takes them out again.

**Is it a mass or a set of strings?** Measured over the band one to three
part-brushes inside the boundary, which is the mass itself and not its edge:

* **Value and spread**: a single sweep leaves the mass stringy, because a bristle
  brush covers about three-quarters of its width. This is how much, and how much of
  it `cross=` takes out. The spread must not reach zero: a mass with no variation
  left in it is a flat fill, which is the loudest tell there is.

Run from the repo root:  python scripts/probe_sweep.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from easel import Region, Session  # noqa: E402

OUT = ROOT / "out"
SIZE = (520, 400)
#: An arbitrary boundary with a peak in it, and not a subject. Its bounding box
#: covers a great deal of ground the shape itself does not, which is the point.
EDGE = [(-0.03, 0.72), (0.24, 0.50), (0.50, 0.66), (0.77, 0.44), (1.03, 0.58)]
DEPTH = 0.34
BRUSH = 0.13
#: One part-brush, the step `sweep` and `block_in` both space their passes by.
STEP = BRUSH * (1.0 - 0.45)


def axis_share_fn():
    """The Sobel metric from the M6 probe, imported rather than written out twice."""
    path = ROOT / "rehearsal3" / "probe_axis_alignment.py"
    spec = importlib.util.spec_from_file_location("_easel_axis", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.axis_share


def session() -> Session:
    s = Session(*SIZE, texture="linen", ground="toned_grey", seed=9, timelapse=False)
    s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
    return s


def boxed() -> tuple[Session, int]:
    """What the mass costs as a rectangle: the bounding box of the same boundary."""
    s = session()
    top = min(y for _, y in EDGE)
    records = s.block_in(Region(0.0, top, 1.0, min(top + DEPTH, 1.0)),
                         "bristle", "dark", size=BRUSH)
    return s, len(records)


def swept(**kw) -> tuple[Session, int]:
    s = session()
    records = s.sweep(EDGE, "bristle", "dark", into="down", depth=DEPTH, size=BRUSH, **kw)
    return s, len(records)


def depth_into_mass(s: Session) -> np.ndarray:
    """How far each pixel lies inside the boundary, in fractions of the canvas height.

    Negative is outside the shape. Measured against the knots the painter gave, not
    against the smoothed curve the strokes follow, so a couple of thousandths of the
    difference between the two is in every number here.
    """
    ys = np.arange(s.canvas.height)[:, None] / s.canvas.height
    xs = np.arange(s.canvas.width)[None, :] / s.canvas.width
    boundary = np.interp(xs, [p[0] for p in EDGE], [p[1] for p in EDGE])
    return ys - boundary


def measure(s: Session, before: np.ndarray) -> tuple[float, float, float]:
    """Paint outside the shape, and the value and spread of the mass itself."""
    into = depth_into_mass(s)
    painted = np.abs(s.canvas.rgb - before).max(axis=2) > 1e-3
    # Half a brush, in the units y is measured in: `size` is a fraction of the long
    # side, and this canvas is wider than it is tall.
    half_brush = 0.5 * BRUSH * s.canvas.width / s.canvas.height
    outside = float((painted & (into < -half_brush)).sum()) / max(int(painted.sum()), 1)

    band = (into >= STEP) & (into <= 3.0 * STEP)
    lum = s.canvas.rgb.mean(axis=2)[band]
    return 100.0 * outside, float(lum.mean()), float(lum.std())


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    axis_share = axis_share_fn()
    before = session().canvas.rgb.copy()

    versions = [
        ("block_in over the bounding box", *boxed()),
        ("sweep along the boundary", *swept()),
        ("sweep, crossed at 26 deg", *swept(cross=26)),
    ]

    print(f"One boundary, {len(EDGE)} points, depth {DEPTH}, bristle at {BRUSH}, "
          f"on a {SIZE[0]}x{SIZE[1]} canvas.\n")
    print(f"{'':32s} {'strokes':>7s} {'square':>7s} {'outside':>8s} "
          f"{'value':>7s} {'spread':>7s}")
    tiles = []
    for name, s, strokes in versions:
        path = OUT / f"sweep_{name.split()[0]}_{strokes}.png"
        s.export(path, impasto=False)
        outside, mean, std = measure(s, before)
        print(f"{name:32s} {strokes:7d} {axis_share(str(path)):6.1f}% {outside:7.1f}% "
              f"{mean:7.3f} {std:7.4f}")
        tiles.append(Image.open(path))

    sheet = Image.new("RGB", (SIZE[0] * len(tiles), SIZE[1]), (24, 24, 24))
    for i, tile in enumerate(tiles):
        sheet.paste(tile, (i * SIZE[0], 0))
    sheet.save(OUT / "sweep_sheet.png")
    print(f"\nWrote {OUT / 'sweep_sheet.png'} -- look at it before believing any of that.")

    # How far a sweep can be asked to go before it stops on its own.
    theta = np.linspace(0.0, 2.0 * np.pi, 16, endpoint=False)
    blob = [(0.5 + 0.20 * np.cos(t), 0.5 + 0.20 * np.sin(t)) for t in theta]
    print("\nA closed boundary of radius 0.20, swept deeper than it is wide:")
    for depth in (0.10, 0.20, 0.40, 0.90):
        s = session()
        laid = len(s.sweep(blob, "bristle", "dark", closed=True, depth=depth, size=BRUSH))
        print(f"  depth {depth:.2f}: {round(depth / STEP):2d} passes asked for, "
              f"{laid:2d} laid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
