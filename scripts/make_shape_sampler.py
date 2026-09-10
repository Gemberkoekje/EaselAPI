"""Generate ``samples/shapes.png`` -- every way of building a mass that is not a box.

The companion to ``brushes.png`` for M8. That sheet answers "what does this brush
do"; this one answers "what does a mass with a silhouette look like when the engine
fills it", which is the question the milestone exists for.

    python scripts/make_shape_sampler.py

Down the side: the five ways to build a shape. Across: the sweep directions, ending
with the rectangle the mass would have been before shapes existed -- that last
column is the comparison the sheet is for.

Things to look for:

* a silhouette that reads as the shape, not as a box with corners knocked off,
* passes that stop *at* the edge instead of fading out short of it,
* the notch in the concave shape still open after the fill,
* ``axis`` sweeping along the mass and not along the canvas,
* the ragged half-brush of spill past the boundary being spill, not a second edge.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from easel.regions import blob, ellipse, hull, polygon, ribbon  # noqa: E402
from easel.session import Session  # noqa: E402

CELL_W, CELL_H = 260, 200
LABEL_W = 96
HEADER_H = 26
TITLE_H = 30
GROUND = "toned_grey"
TEXTURE = "linen"

#: name -> the shape, built the way the guide tells a painter to build it.
SHAPES = {
    "ellipse": ellipse((0.5, 0.5), 0.34, 0.30),
    "blob": blob((0.5, 0.5), 0.34, 0.30, wobble=0.28, seed=6),
    "hull": hull([(0.12, 0.86), (0.30, 0.16), (0.72, 0.24), (0.90, 0.78)]),
    "ribbon": ribbon([(0.08, 0.80), (0.42, 0.30), (0.92, 0.52)], 0.30, end_width=0.10),
    "concave": polygon([(0.10, 0.12), (0.90, 0.12), (0.90, 0.90), (0.62, 0.90),
                        (0.62, 0.48), (0.38, 0.48), (0.38, 0.90), (0.10, 0.90)]),
}

#: label -> (direction, whether to fill the shape or the box it sits in).
COLUMNS = [
    ("horizontal", ("horizontal", False)),
    ("axis", ("axis", False)),
    ("cross", (("axis", 90.0), False)),
    ("its box", ("horizontal", True)),
]


def render_cell(shape, direction, as_box: bool, seed: int) -> Image.Image:
    s = Session(CELL_W, CELL_H, texture=TEXTURE, ground=GROUND, seed=seed,
                timelapse=False)
    s.palette["mass"] = s.palette.mix("ultramarine", "burnt_umber", 0.4)
    place = shape.box if as_box else shape
    s.block_in(place, "bristle", "mass", direction=direction, density=1.0, size=0.16)
    return Image.fromarray(s.canvas.to_srgb8(), mode="RGB")


def build_sheet() -> Image.Image:
    width = LABEL_W + len(COLUMNS) * CELL_W
    height = TITLE_H + HEADER_H + len(SHAPES) * CELL_H
    sheet = Image.new("RGB", (width, height), (22, 22, 24))
    draw = ImageDraw.Draw(sheet)
    draw.text((8, 9), f"shaped masses -- block_in, bristle 0.16, {TEXTURE}",
              fill=(255, 235, 190))

    for c, (label, _) in enumerate(COLUMNS):
        x = LABEL_W + c * CELL_W
        draw.text((x + 6, TITLE_H + 7), label, fill=(190, 190, 200))
        if c:
            draw.line([(x, TITLE_H), (x, height)], fill=(70, 70, 78), width=1)

    for r, (name, shape) in enumerate(SHAPES.items()):
        y = TITLE_H + HEADER_H + r * CELL_H
        draw.text((8, y + CELL_H // 2 - 4), name, fill=(235, 235, 240))
        for c, (_label, (direction, as_box)) in enumerate(COLUMNS):
            cell = render_cell(shape, direction, as_box, seed=200 + r * 37 + c * 11)
            sheet.paste(cell, (LABEL_W + c * CELL_W, y))
    return sheet


def main() -> int:
    out = Path(__file__).resolve().parents[1] / "samples" / "shapes.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet = build_sheet()
    sheet.save(out)
    print(f"Wrote {out} ({sheet.size[0]}x{sheet.size[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
