"""Side-by-side sheets for REHEARSAL3: reference against what each run produced.

Run from the repo root after all three runs have exported their copies:
    python rehearsal3/make_sheets.py
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PANEL_H = 520
PAD = 16
LABEL_H = 26
BG = (28, 28, 30)
FG = (232, 232, 236)


def panel(path: str, label: str) -> tuple[Image.Image, str]:
    im = Image.open(path).convert("RGB")
    w = max(1, round(im.width * PANEL_H / im.height))
    return im.resize((w, PANEL_H), Image.LANCZOS), label


def sheet(items: list[tuple[str, str]], out: str) -> str:
    panels = []
    for path, label in items:
        if not os.path.exists(path):
            print(f"  missing, skipped: {path}")
            continue
        panels.append(panel(path, label))
    if not panels:
        raise SystemExit(f"nothing to put in {out}")
    width = sum(p.width for p, _ in panels) + PAD * (len(panels) + 1)
    height = PANEL_H + LABEL_H + PAD * 2
    canvas = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    x = PAD
    for im, label in panels:
        canvas.paste(im, (x, PAD))
        draw.text((x + 2, PAD + PANEL_H + 6), label, fill=FG)
        x += im.width + PAD
    canvas.save(out)
    print(f"  wrote {out}  ({canvas.width}x{canvas.height})")
    return out


def main() -> int:
    print("mug — own pencil against assisted:")
    sheet(
        [
            ("C:/temp/Level1.jpg", "reference"),
            (f"{HERE}/pass/copy_final.png", "M6 fresh session, own pencil"),
            (f"{HERE}/assisted/copy_final.png", "M6 fresh session, machine sketch"),
        ],
        f"{HERE}/mug_compared.png",
    )
    print("sitter — the same photograph, before M6 and after:")
    sheet(
        [
            ("C:/temp/Level3.jpg", "reference"),
            (f"{ROOT}/rehearsal2/copy_final.png", "M5 fresh session (REHEARSAL2)"),
            (f"{HERE}/sitter/copy_final.png", "M6 fresh session"),
        ],
        f"{HERE}/sitter_compared.png",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
