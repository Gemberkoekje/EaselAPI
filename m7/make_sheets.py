"""Render the four marks M7 changes, for whichever engine is installed.

The brief says every change in this milestone is judged on the sampler *and* on a
real painting, never on a hash. The sampler shows one stroke per cell, so it cannot
show the thing M7 is mostly about -- whether the *next* stroke prints the same
streaks. These four panels can:

1. **The comb, stroke to stroke.** Five bristle strokes, one brush. Do they print
   the same streaks?
2. **The comb, against size.** The same brush at four sizes. Do the streaks get
   fatter as the brush gets bigger, or just more numerous?
3. **Pressure.** One round tip, the six named profiles and a hand-written taper.
   Does anything change width, or only how much paint lands?
4. **Dabs.** One mark, stamped once to four times. Does a catchlight read?

Run it under both engines and join the two sheets::

    PYTHONPATH=/path/to/pre-m7/src python m7/make_sheets.py m7/_before.png
    python m7/make_sheets.py m7/_after.png
    python m7/make_sheets.py --join m7/_before.png m7/_after.png m7/marks_compared.png

The `--join` step is separate so that the two halves are rendered by two different
interpreters, each with its own `easel` on the path.
"""

from __future__ import annotations

import inspect
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from easel.session import Session

W, H = 900, 200
CANVAS = dict(texture="linen", ground="toned_grey", seed=5, timelapse=False)
INK = "titanium_white"


def _session(height: int = H) -> Session:
    # Nothing here calls look(); out_dir only decides where one would land.
    return Session(W, height, out_dir=Path(__file__).resolve().parents[1] / "out", **CANVAS)


def panel_comb_repeats() -> tuple[str, Image.Image]:
    """Five strokes of one brush. The streaks used to be identical on all five."""
    s = _session()
    for i in range(5):
        y = 0.12 + i * 0.19
        s.stroke([(0.05, y), (0.35, y - 0.01), (0.65, y + 0.01), (0.95, y)],
                 "bristle", INK, pressure="even", size=0.10)
    return "1. five bristle strokes, one brush -- do they print the same streaks?", _image(s)


def panel_comb_scales() -> tuple[str, Image.Image]:
    """One brush at four sizes. A bristle has a width; a bigger brush holds more."""
    s = _session()
    for i, size in enumerate((0.02, 0.05, 0.10, 0.18)):
        y = 0.13 + i * 0.24
        s.stroke([(0.05, y), (0.5, y - 0.015), (0.95, y)], "bristle", INK,
                 pressure="even", size=size)
    return "2. bristle at 0.02 / 0.05 / 0.10 / 0.18 -- do the streaks get fatter?", _image(s)


def panel_pressure() -> tuple[str, Image.Image]:
    """The six named profiles plus one written by hand, on a round tip."""
    s = _session(260)
    profiles = ["even", "taper", "press_in", "lift_off", "swell", "dab", [1.0, 0.0]]
    for i, p in enumerate(profiles):
        y = 0.08 + i * 0.135
        s.stroke([(0.06, y), (0.5, y), (0.94, y)], "round_hard", INK,
                 pressure=p, size=0.035)
    return ("3. round_hard: even, taper, press_in, lift_off, swell, dab, [1, 0] "
            "-- does anything taper?"), _image(s)


def panel_dabs() -> tuple[str, Image.Image]:
    """One mark stamped once to four times -- and what that cost before `press`."""
    s = _session(150)
    stamped = "press" in inspect.signature(Session.dab).parameters
    for i in range(4):
        x = 0.14 + i * 0.24
        if stamped:
            s.dab(x, 0.5, brush="round_hard", color=INK, size=0.05, press=i + 1)
        else:
            for _ in range(i + 1):
                s.dab(x, 0.5, brush="round_hard", color=INK, size=0.05)
    how = "press=1..4, one stroke each" if stamped else "1..4 separate dabs (no press)"
    return f"4. a dab at size 0.05, {how} -- {s.stroke_count} strokes spent", _image(s)


def _image(s: Session) -> Image.Image:
    return Image.fromarray(s.canvas.to_srgb8(), mode="RGB")


PANELS = (panel_comb_repeats, panel_comb_scales, panel_pressure, panel_dabs)
_LABEL_H = 20


def build() -> Image.Image:
    made = [p() for p in PANELS]
    height = sum(img.size[1] + _LABEL_H for _, img in made) + 8
    sheet = Image.new("RGB", (W, height), (18, 18, 20))
    draw = ImageDraw.Draw(sheet)
    y = 4
    for title, img in made:
        draw.text((6, y + 5), title, fill=(250, 238, 200))
        y += _LABEL_H
        sheet.paste(img, (0, y))
        y += img.size[1]
    return sheet


def join(before: Path, after: Path, out: Path) -> Path:
    """Stack two sheets, labelled, so the same marks can be looked at side by side."""
    a, b = Image.open(before), Image.open(after)
    gap, head = 14, 24
    sheet = Image.new("RGB", (a.size[0] + b.size[0] + gap,
                              max(a.size[1], b.size[1]) + head), (18, 18, 20))
    draw = ImageDraw.Draw(sheet)
    draw.text((8, 7), "BEFORE  (main, before M7)", fill=(255, 220, 160))
    draw.text((a.size[0] + gap + 8, 7), "AFTER  (main + M7)", fill=(180, 255, 190))
    sheet.paste(a, (0, head))
    sheet.paste(b, (a.size[0] + gap, head))
    sheet.save(out)
    return out


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--join":
        out = join(Path(argv[1]), Path(argv[2]), Path(argv[3]))
        print(f"Wrote {out}")
        return 0
    out = Path(argv[0]) if argv else Path(__file__).parent / "marks.png"
    sheet = build()
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"Wrote {out} ({sheet.size[0]}x{sheet.size[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
