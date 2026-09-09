"""Probe behind the human's note in HUMAN_NOTES.md: axis-aligned marks and the tip angle.

Two questions, both answered by looking:

1. Can the tip be rotated at all from the public API? `Brush` carries `angle_follow`
   and `angle`, and `stroke(**brush_overrides)` reaches every brush field, but
   `PAINTER.md` documents neither. Sheet 1 puts the same horizontal stroke down with
   the tip following travel and pinned at 0, 45 and 90 degrees, for each tip that has
   an orientation.

2. Does it matter? Sheet 2 paints the same hillside four ways: as a `block_in` box,
   as the guide's own `edge()` recipe (vertical columns), as strokes running along
   the slope with the tip following them, and as strokes along the slope with the
   tip pinned across the form.

Run from the repo root:  python rehearsal3/probe_stroke_axis.py
Then look at rehearsal3/probe_axis_tips.png and rehearsal3/probe_axis_mountain.png.
"""
from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw

from easel import Region, Session

HERE = os.path.dirname(os.path.abspath(__file__))
ORIENTED = ["flat", "knife", "bristle"]
ANGLES = [None, 0.0, 45.0, 90.0]


def label(path: str, rows: list[str], cols: list[str], title: str) -> None:
    """Composite row and column labels onto an exported sheet, for the write-up."""
    im = Image.open(path).convert("RGB")
    pad_l, pad_t = 120, 46
    out = Image.new("RGB", (im.width + pad_l, im.height + pad_t), (24, 24, 26))
    out.paste(im, (pad_l, pad_t))
    d = ImageDraw.Draw(out)
    d.text((10, 12), title, fill=(240, 240, 244))
    for i, name in enumerate(cols):
        x = pad_l + im.width * (i + 0.5) / len(cols) - 30
        d.text((x, pad_t - 16), name, fill=(240, 240, 244))
    for j, name in enumerate(rows):
        y = pad_t + im.height * (j + 0.5) / len(rows) - 6
        d.text((10, y), name, fill=(240, 240, 244))
    out.save(path)


def sheet_tips() -> None:
    """One horizontal stroke per cell: tip following travel, then pinned three ways."""
    s = Session(1400, 900, texture="linen", ground="toned_grey", seed=5)
    for j, tip in enumerate(ORIENTED):
        cy = (j + 0.5) / len(ORIENTED)
        for i, ang in enumerate(ANGLES):
            cx = (i + 0.5) / len(ANGLES)
            over: dict[str, object] = {"size": 0.09}
            if ang is not None:
                over["angle_follow"] = False
                over["angle"] = ang
            s.stroke(
                [(cx - 0.09, cy), (cx, cy - 0.008), (cx + 0.09, cy)],
                tip,
                "titanium_white",
                pressure="even",
                **over,
            )
    out = s.export(os.path.join(HERE, "probe_axis_tips.png"))
    label(
        str(out),
        ORIENTED,
        ["angle_follow (default)", "angle=0", "angle=45", "angle=90"],
        "Sheet 1 - the same horizontal stroke, tip following travel then pinned",
    )
    print(f"  {out}")


def slope(x: float) -> float:
    """A hillside: a ridge down to the right, the thing the note is about."""
    knots = [(0.06, 0.78), (0.30, 0.40), (0.52, 0.26), (0.78, 0.52), (0.96, 0.62)]
    for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return knots[-1][1] if x > knots[-1][0] else knots[0][1]


def paint_mountain(mode: str) -> Session:
    s = Session(700, 520, texture="linen", ground="toned_grey", seed=5)
    s.block_in(Region(0.0, 0.0, 1.0, 0.85, "sky"), "flat", "cerulean", size=0.16,
               density=0.8)
    dark, light = "burnt_umber", "yellow_ochre"

    if mode == "box":
        s.block_in(Region(0.06, 0.26, 0.96, 1.0, "hill"), "flat", dark,
                   direction="horizontal", size=0.10)
    elif mode == "columns":
        # The guide's own recipe from "A region is a rectangle": walk across, and
        # let each stroke start where the edge is. Every stroke is a column.
        x = 0.07
        while x < 0.96:
            s.stroke([(x, slope(x)), (x, 1.02)], "bristle", dark,
                     size=0.09, pressure="lift_off")
            x += 0.031
    else:
        # Strokes that run along the form instead of across the canvas. Each pass is
        # a band parallel to the ridge, stepped down the slope's own normal.
        pin = mode == "pinned"
        for k in range(9):
            off = 0.035 * k
            pts = []
            for i in range(9):
                x = 0.07 + (0.89 * i / 8)
                pts.append((x, min(slope(x) + off + 0.012 * math.sin(3.1 * x), 1.02)))
            if k % 2:
                pts = pts[::-1]
            over: dict[str, object] = {}
            if pin:
                # Hold the blade across the ridge, the way a knife is turned to cut a
                # slope, instead of letting it swing with every wobble of the path.
                over["angle_follow"] = False
                over["angle"] = -34.0
            s.stroke(pts, "flat", dark if k < 6 else light, size=0.10,
                     pressure="even", **over)
    return s


def sheet_mountain() -> None:
    modes = ["box", "columns", "along", "pinned"]
    names = {
        "box": "block_in box",
        "columns": "guide's edge() columns",
        "along": "along the slope, tip follows",
        "pinned": "along the slope, tip pinned",
    }
    panels = []
    for mode in modes:
        s = paint_mountain(mode)
        p = s.export(os.path.join(HERE, f"_mtn_{mode}.png"))
        panels.append(Image.open(str(p)).convert("RGB"))
        print(f"  {mode}: {s.stroke_count} strokes")
    w, h = panels[0].size
    out = Image.new("RGB", (w * len(panels) + 10 * (len(panels) + 1), h + 20),
                    (24, 24, 26))
    for i, im in enumerate(panels):
        out.paste(im, (10 + i * (w + 10), 10))
    path = os.path.join(HERE, "probe_axis_mountain.png")
    out.save(path)
    label(path, ["hillside"], [names[m] for m in modes],
          "Sheet 2 - the same hillside, four ways of laying the mass")
    for mode in modes:
        os.remove(os.path.join(HERE, f"_mtn_{mode}.png"))
    print(f"  {path}")


if __name__ == "__main__":
    print("sheet 1: does the tip angle reach the public API?")
    sheet_tips()
    print("sheet 2: does it matter?")
    sheet_mountain()
