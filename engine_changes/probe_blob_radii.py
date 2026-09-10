"""`blob(region, radius)` was a horizontal sausage. Item 1 of `ENGINE_CHANGES.md`.

The two branches of `_centre_and_radii` disagreed. Given a *point* and one radius
you got a circle; given a *region* and one radius the radius set the width and the
height silently stayed at the region's own half-height. The guide's own example,
`blob(cell("D5"), 0.22, wobble=0.3, seed=2)`, came out 4.1 : 1 and the height never
moved however large the radius got.

This prints the reproduction under both rules and draws the picture, because the
number 4.1 does not look like anything and a mass four cells wide over a grid does::

    python engine_changes/probe_blob_radii.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO / "src") not in sys.path:
    sys.path.insert(0, str(_REPO / "src"))

from easel import Session, blob, cell  # noqa: E402

CELL = cell("D5")
WOBBLE = dict(wobble=0.3, seed=2)


def old_rule(radius):
    """What the region branch used to build: the radius across, the cell's own down."""
    if radius is None:
        return blob(CELL, **WOBBLE)
    return blob(CELL, radius, CELL.height * 0.5, **WOBBLE)


def new_rule(radius):
    """What it builds now: one radius is a circle wherever the shape is put."""
    return blob(CELL, **WOBBLE) if radius is None else blob(CELL, radius, **WOBBLE)


def table() -> None:
    print(f"cell(\"D5\") is {CELL.width:.3f} x {CELL.height:.3f}")
    print(f"{'radius':>8}  {'old: w x h':>17}  {'ratio':>6}   {'new: w x h':>17}  {'ratio':>6}")
    for radius in (0.02, 0.05, 0.10, 0.22, 0.26, None):
        row = f"{'(none)' if radius is None else f'{radius:.2f}':>8}  "
        for rule in (old_rule, new_rule):
            s = rule(radius)
            row += f"{s.width:8.4f} x {s.height:6.4f}  {s.width / s.height:6.2f}   "
        print(row.rstrip())
    print()
    print("The guide shows blob(cell(\"D5\"), 0.22) as \"an irregular mass filling a "
          "cell\".")
    print("Under either rule it is not: 0.22 is a radius, so the mass is "
          f"{new_rule(0.22).width / CELL.width:.1f} cells")
    print("across. Only the no-radius call fills the cell "
          f"({new_rule(None).width:.3f} x {new_rule(None).height:.3f}).")


def panel(shape, title: str) -> tuple[str, Image.Image]:
    """The mass painted over the grid, so its size is read off the canvas."""
    s = Session(420, 420, ground="toned_grey", seed=3, timelapse=False,
                out_dir=_REPO / "out")
    s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
    s.block_in(shape, "bristle", "dark", density=0.7, size=0.05, direction="axis")
    return title, s.look_image(grid=True, scale=420)


def build() -> Image.Image:
    made = [
        panel(old_rule(0.22), "before: blob(cell(\"D5\"), 0.22) -- 4.1 : 1, four cells wide"),
        panel(new_rule(0.22), "after:  blob(cell(\"D5\"), 0.22) -- round, still four cells wide"),
        panel(new_rule(None), "after:  blob(cell(\"D5\")) -- the call that fills the cell"),
    ]
    label_h = 20
    width = sum(img.size[0] for _, img in made) + 2 * len(made)
    sheet = Image.new("RGB", (width, made[0][1].size[1] + label_h), (18, 18, 20))
    draw = ImageDraw.Draw(sheet)
    x = 0
    for title, img in made:
        draw.text((x + 6, 5), title, fill=(250, 238, 200))
        sheet.paste(img, (x, label_h))
        x += img.size[0] + 2
    return sheet


def main(argv: list[str]) -> int:
    table()
    out = Path(argv[0]) if argv else Path(__file__).parent / "blob_radii.png"
    sheet = build()
    sheet.save(out)
    print(f"\nWrote {out} ({sheet.size[0]}x{sheet.size[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
