"""Burnt umber with ultramarine at 18-35%, brought by at_value to the values my scripts used them at, each beside a
neutral grey of the same value; with each mixture's Oklab hue and chroma."""
import math
import numpy as np
from PIL import Image, ImageDraw
from easel import Session
s = Session(16, 16, ground="toned_grey", seed=1, out_dir="."); p = s.palette
def oklab(hx):
    c = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    q = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L, A, B = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * q, 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * q, 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * q
    return L, math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360
def neutral(v):                       # the grey whose luma is v
    g = int(round(v * 255)); return "#%02x%02x%02x" % (g, g, g)
for name in ("burnt_umber", "ultramarine"):
    L, C, h = oklab(p.hex(name)); print(f"{name:12s} Oklab hue {h:5.1f}  chroma {C:.3f}")
shares, values = (0.18, 0.25, 0.30, 0.35), (0.14, 0.18, 0.34, 0.44)
img = Image.new("RGB", (len(shares) * 170 + 70, len(values) * 90 + 30), (24, 24, 24))
d = ImageDraw.Draw(img)
for j, t in enumerate(shares):
    d.text((70 + j * 170, 8), f"{int(t * 100)}% ultramarine", fill=(230, 230, 230))
for i, v in enumerate(values):
    d.text((8, 30 + i * 90 + 35), f"value {v}", fill=(230, 230, 230))
    for j, t in enumerate(shares):
        hx = p.hex(p.at_value(p.mix("burnt_umber", "ultramarine", t), v))
        L, C, h = oklab(hx)
        print(f"{int(t * 100):2d}% at value {v:.2f}: {hx}  Oklab hue {h:5.1f}  chroma {C:.3f}")
        x, y = 70 + j * 170, 30 + i * 90
        d.rectangle([x, y, x + 74, y + 80], fill=hx)
        d.rectangle([x + 76, y, x + 150, y + 80], fill=neutral(v))
img.save("umber_ultramarine_vs_neutral.png")
