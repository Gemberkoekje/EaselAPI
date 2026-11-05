"""The candle's finest texture: painted at 1x on linen, at 1x on a smooth canvas, and at 2x and 4x reduced
(Lanczos) to 120x300. Texture = the standard deviation, in 8-bit levels of value, of the value image minus
its Gaussian blur (sigma 0.7 and 2 px), over the inside of the base and of the wax body (3 px in from the
outline)."""
import json
import numpy as np
from PIL import Image, ImageDraw
SP = "/tmp/claude-0/-home-user-projects/effc84d7-d7e9-5d60-848f-887f6f888335/scratchpad/"
O = json.load(open(SP + "cand/outline.json"))
def value(im):
    return (np.asarray(im.convert("RGB")).astype(np.float64)) @ [0.2126, 0.7152, 0.0722]
def gauss(a, s):
    r = int(np.ceil(4 * s)); x = np.arange(-r, r + 1); k = np.exp(-x * x / (2 * s * s)); k /= k.sum()
    p = np.pad(a, r, mode="reflect")
    p = np.apply_along_axis(lambda v: np.convolve(v, k, "valid"), 1, p)
    return np.apply_along_axis(lambda v: np.convolve(v, k, "valid"), 0, p)
def inside(name, inset=3):
    m = Image.new("L", (120, 300), 0); ImageDraw.Draw(m).polygon([tuple(p) for p in O[name]], fill=255)
    a = np.asarray(m) > 0
    for _ in range(inset):
        a = a & np.roll(a, 1, 0) & np.roll(a, -1, 0) & np.roll(a, 1, 1) & np.roll(a, -1, 1)
    return a
regions = {"base": inside("base"), "wax body": inside("body")}
runs = {"1x linen": Image.open(SP + "q2/candle/candle_rgb.png"),
        "1x smooth canvas": Image.open(SP + "step2/dep/smooth/candle_rgb.png"),
        "2x reduced": Image.open(SP + "step2/dep/c2x/candle_rgb.png").resize((120, 300), Image.LANCZOS),
        "4x reduced": Image.open(SP + "q2/candle4x/candle_rgb.png").resize((120, 300), Image.LANCZOS)}
print(f"{'':18s}" + "".join(f"{r + ' ' + str(s):>16s}" for r in regions for s in (0.7, 2.0)))
for name, im in runs.items():
    V = value(im)
    cells = []
    for r, m in regions.items():
        for s in (0.7, 2.0):
            cells.append(f"{(V - gauss(V, s))[m].std():16.2f}")
    print(f"{name:18s}" + "".join(cells))
# a sheet: the base and the top of the wax, each run at 3x
tiles = []
for name, im in runs.items():
    t = im.convert("RGB").crop((20, 150, 100, 300)).resize((240, 450), Image.NEAREST)
    ImageDraw.Draw(t).text((4, 4), name, fill=(0, 0, 0))
    tiles.append(t)
sheet = Image.new("RGB", (250 * len(tiles), 450), (24, 24, 24))
for i, t in enumerate(tiles):
    sheet.paste(t, (i * 250, 0))
sheet.save("texture_sheet.png")

# The same, over stretches that no hand-laid stroke crosses: the base's middle (x 25-75, y 270-288) and the
# wax between the shade and the lit face (x 54-62, y 80-230).
clean = {"base middle": (slice(270, 289), slice(25, 76)), "wax between strokes": (slice(80, 231), slice(54, 63))}
print()
print(f"{'':18s}" + "".join(f"{r + ' ' + str(s):>24s}" for r in clean for s in (0.7, 2.0)))
for name, im in runs.items():
    V = value(im)
    print(f"{name:18s}" + "".join(f"{(V - gauss(V, s))[sl].std():24.2f}" for sl in clean.values() for s in (0.7, 2.0)))
