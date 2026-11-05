"""alpha_085.png: each cut at 4x over a light and a dark ground -- shipped, the places as a hold at 2x2 and 4x4
samples, and the 4x4 coverage softened to 0.85 px and to 2.5 px."""
import numpy as np
from PIL import Image, ImageDraw
A = "/home/user/projects/the-curator/game/art/easel/"
al = np.load("alphas.npz")
light, dark = (198, 181, 146), (52, 44, 38)          # sampled from the owner's alpha.png grounds
crops = {"doorway wall": (A + "doorway_wall.png", (650, 420, 730, 500)),
         "patron": (A + "patron_default.png", (40, 215, 120, 295)),
         "candle": (A + "candle.png", (25, 2, 95, 52))}
cols = [("shipped", "shipped"), ("hold 2x2", "c2"), ("hold 4x4", "c4"), ("0.85 px", "soft085"), ("2.5 px", "soft25")]
cells = []
for name, (png, box) in crops.items():
    rgb = np.asarray(Image.open(png).convert("RGB")).astype(np.float64)
    for gname, g in (("light", light), ("dark", dark)):
        row = []
        for label, key in cols:
            a = al[f"{name}|{key}"][..., None]
            comp = rgb * a + np.array(g, dtype=np.float64) * (1 - a)
            c = Image.fromarray(np.clip(comp + 0.5, 0, 255).astype(np.uint8)).crop(box)
            c = c.resize((c.size[0] * 4, c.size[1] * 4), Image.NEAREST)
            ImageDraw.Draw(c).text((4, c.size[1] - 12), f"{name} {label} on {gname}", fill=(255, 255, 255))
            row.append(c)
        cells.append(row)
cw = max(c.size[0] for r in cells for c in r) + 8
heights = [max(c.size[1] for c in r) + 8 for r in cells]
sheet = Image.new("RGB", (cw * len(cols), sum(heights)), (24, 24, 24))
y = 0
for r, hgt in zip(cells, heights):
    for i, c in enumerate(r):
        sheet.paste(c, (i * cw, y))
    y += hgt
sheet.save("alpha_085.png")
print(sheet.size)
