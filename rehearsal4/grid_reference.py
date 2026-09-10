"""Overlay the painter's A-H by 1-8 grid on a reference photograph.

`verify_done.py` needs a list of the cells the *object* covers, and that list has to
be read off the photograph rather than guessed. This writes the gridded reference so
it can be looked at.

Run from the repo root:  python rehearsal4/grid_reference.py
"""
from __future__ import annotations

import os

from PIL import Image, ImageDraw

from easel.measure import GRID_COLS, GRID_ROWS

HERE = os.path.dirname(os.path.abspath(__file__))


def grid(src: str, dst: str, width: int = 1000) -> str:
    im = Image.open(src).convert("RGB")
    im.thumbnail((width, width), Image.LANCZOS)
    w, h = im.size
    draw = ImageDraw.Draw(im)
    ncol, nrow = len(GRID_COLS), len(GRID_ROWS)

    for c in range(1, ncol):
        x = round(c * w / ncol)
        draw.line([(x, 0), (x, h)], fill=(255, 60, 60), width=1)
    for r in range(1, nrow):
        y = round(r * h / nrow)
        draw.line([(0, y), (w, y)], fill=(255, 60, 60), width=1)

    for r, row in enumerate(GRID_ROWS):
        for c, col in enumerate(GRID_COLS):
            x = round((c + 0.5) * w / ncol)
            y = round((r + 0.5) * h / nrow)
            label = f"{col}{row}"
            draw.text((x - 7, y - 6), label, fill=(0, 0, 0))
            draw.text((x - 8, y - 7), label, fill=(255, 255, 0))

    im.save(dst)
    return dst


if __name__ == "__main__":
    print(grid("C:/temp/Level1.jpg", f"{HERE}/_ref_grid_mug.png"))
    print(grid("C:/temp/Level3.jpg", f"{HERE}/_ref_grid_sitter.png"))
