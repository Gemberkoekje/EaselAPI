"""Question D: what size a hand-laid letter needs to read at the size the pack shows a handout.

A 768 x 1024 handout at M on a 1080p projector is drawn 0.59 of its size (M: max-height 56vh).
The same line of capitals and digits is laid six ways -- pencil, liner, round brush, at cap
heights from 32 to 80 px -- each letter one or two strokes along a hand-made path, the way a
stroke-font recipe would lay them. Read at full size and at 604 px on the long side.
"""
import math
from easel import Session

OUT = "."
W, H = 768, 1024
s = Session(W, H, texture="linen", ground="#d9c9a4", seed=5, out_dir=OUT)
s.palette["ink"] = s.palette.at_value(s.palette.mix("burnt_umber", "ultramarine", 0.3), 0.18)


def ellipse_path(cx, cy, rx, ry, a0=0, a1=360, n=16):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


# One or two paths a glyph, in a box one cap-height tall, y down; (paths, smooth, advance).
GLYPHS = {
    "O": ([ellipse_path(0.38, 0.5, 0.36, 0.5)], True, 0.9),
    "W": ([[(0, 0), (0.18, 1), (0.38, 0.35), (0.58, 1), (0.76, 0)]], False, 0.9),
    "E": ([[(0.6, 0), (0, 0), (0, 1), (0.6, 1)], [(0, 0.5), (0.45, 0.5)]], False, 0.75),
    "D": ([[(0, 0), (0, 1)], [(0, 0), (0.3, 0.03), (0.55, 0.2), (0.63, 0.5), (0.55, 0.8),
                               (0.3, 0.97), (0, 1)]], True, 0.8),
    " ": ([], False, 0.45),
    "4": ([[(0.52, 0), (0, 0.68), (0.72, 0.68)], [(0.52, 0.3), (0.52, 1)]], False, 0.85),
    "0": ([ellipse_path(0.33, 0.5, 0.3, 0.5)], True, 0.75),
    "G": ([ellipse_path(0.36, 0.5, 0.34, 0.5, -50, 200, 14) + [(0.66, 0.55), (0.45, 0.55)]],
          True, 0.85),
    "P": ([[(0, 1), (0, 0)], [(0, 0), (0.35, 0.02), (0.55, 0.14), (0.55, 0.36), (0.35, 0.48),
                               (0, 0.5)]], True, 0.7),
}
ROWS = [("pencil", None, 32), ("pencil", None, 56), ("liner", 0.003, 32), ("liner", 0.003, 56),
        ("round_hard", 0.005, 56), ("round_hard", 0.008, 80)]

top = 60
for tool, size, cap in ROWS:
    x = 40
    for ch in "OWED 40 GP":
        paths, smooth, adv = GLYPHS[ch]
        for path in paths:
            pts = [((x + u * cap) / W, (top + v * cap) / H) for u, v in path]
            if tool == "pencil":
                s.pencil(pts, pressure=0.9, smooth=smooth)
            else:
                s.stroke(pts, tool, "ink", size=size, opacity=0.95, load=1.0,
                         load_falloff=0.0, pressure="even", smooth=smooth,
                         note=f"{tool} {cap}px")
        x += (adv + 0.12) * cap
    top += cap + 70

print("strokes charged:", s.stroke_count)
print(s.look(path=OUT + "/letters_full.png"))
print(s.look(scale=604, path=OUT + "/letters_M.png"))
print(s.log(last=200))
