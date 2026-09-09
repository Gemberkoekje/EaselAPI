"""Generate ``samples/brushes.png`` -- every brush, size and pressure, on every texture.

This sheet is the engine's primary test artefact. Regenerate it after any change to
the brush, stroke, texture or canvas code, and then *actually look at it*. Numbers
in a test suite will not tell you that a stroke has gone mechanical.

    python scripts/make_brush_sampler.py

Things to look for, all of which have been real bugs here:

* regular stripes across a stroke (dab spacing beating against something),
* a halftone dot screen where paint runs out (texture gating gone periodic),
* identical edges on every stroke (no variation in load or wobble),
* beads rather than a continuous mark (spacing too wide for the tip).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from easel.brush import BRUSHES  # noqa: E402
from easel.canvas import Canvas  # noqa: E402
from easel.stroke import paint_stroke  # noqa: E402
from easel.texture import TEXTURES  # noqa: E402

SIZES = [("S", 0.055), ("M", 0.1), ("L", 0.17)]
PRESSURES = ["taper", "press_in", "even"]

CELL_W, CELL_H = 190, 120
LABEL_W = 92
HEADER_H = 26
TITLE_H = 30
PAINT = "#F2EDE4"
GROUND = "toned_grey"


def stroke_path(rng: np.random.Generator) -> list[tuple[float, float]]:
    """A gently curved path across a cell, with a little variation per stroke."""
    wob = rng.uniform(-0.06, 0.06, size=4)
    return [
        (0.08, 0.5 + wob[0]),
        (0.36, 0.42 + wob[1]),
        (0.64, 0.58 + wob[2]),
        (0.92, 0.48 + wob[3]),
    ]


def render_cell(brush_name: str, size: float, pressure: str, texture: str, seed: int) -> Image.Image:
    canvas = Canvas(CELL_W, CELL_H, texture=texture, ground=GROUND, seed=seed)
    b = BRUSHES[brush_name].with_(size=size)
    rng = np.random.default_rng(seed)

    # The smudge brush moves paint rather than adding it, so give it paint to move.
    if b.smudge >= 1.0:
        paint_stroke(canvas, [(0.05, 0.55), (0.5, 0.45), (0.95, 0.55)],
                     BRUSHES["bristle"].with_(size=size * 1.2), PAINT, "even", rng)
    paint_stroke(canvas, stroke_path(rng), b, PAINT, pressure, rng)
    return Image.fromarray(canvas.to_srgb8(), mode="RGB")


def build_panel(texture: str, seed: int) -> Image.Image:
    """One texture: brushes down the side, size/pressure combinations across."""
    names = list(BRUSHES)
    cols = [(s_label, s_val, p) for s_label, s_val in SIZES for p in PRESSURES]

    width = LABEL_W + len(cols) * CELL_W
    height = TITLE_H + HEADER_H + len(names) * CELL_H
    panel = Image.new("RGB", (width, height), (22, 22, 24))
    draw = ImageDraw.Draw(panel)

    draw.text((8, 9), f"texture: {texture}", fill=(255, 235, 190))
    for i, (s_label, _s_val, p) in enumerate(cols):
        x = LABEL_W + i * CELL_W
        draw.text((x + 6, TITLE_H + 7), f"{s_label}  {p}", fill=(190, 190, 200))
        if i % len(PRESSURES) == 0 and i:
            draw.line([(x, TITLE_H), (x, height)], fill=(70, 70, 78), width=1)

    for r, name in enumerate(names):
        y = TITLE_H + HEADER_H + r * CELL_H
        draw.text((8, y + CELL_H // 2 - 4), name, fill=(235, 235, 240))
        for c, (_s_label, s_val, p) in enumerate(cols):
            cell = render_cell(name, s_val, p, texture, seed + r * 31 + c * 7)
            panel.paste(cell, (LABEL_W + c * CELL_W, y))
    return panel


def main() -> int:
    out = Path(__file__).resolve().parents[1] / "samples" / "brushes.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    panels = [build_panel(texture, seed=100 + i * 1000) for i, texture in enumerate(TEXTURES)]
    gap = 10
    width = max(p.size[0] for p in panels)
    height = sum(p.size[1] for p in panels) + gap * (len(panels) - 1)

    sheet = Image.new("RGB", (width, height), (14, 14, 16))
    y = 0
    for p in panels:
        sheet.paste(p, (0, y))
        y += p.size[1] + gap

    sheet.save(out)
    print(f"Wrote {out} ({sheet.size[0]}x{sheet.size[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
