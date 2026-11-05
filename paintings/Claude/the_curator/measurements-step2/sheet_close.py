"""alpha_085_close.png: the patron's shoulder over the light ground and the candle's top corner over the dark,
at 8x, across the five edges (run after cut_edges.py, beside its alphas.npz)."""
import numpy as np
from PIL import Image, ImageDraw
A = "/home/user/projects/the-curator/game/art/easel/"
al = np.load("alphas.npz")
light, dark = (198, 181, 146), (52, 44, 38)
cols = [("shipped", "shipped"), ("hold 2x2", "c2"), ("hold 4x4", "c4"), ("0.85 px", "soft085"), ("2.5 px", "soft25")]
rows = [("patron", A + "patron_default.png", (55, 255, 95, 290), light), ("candle", A + "candle.png", (30, 20, 60, 45), dark)]
out = []
for name, png, box, g in rows:
    rgb = np.asarray(Image.open(png).convert("RGB")).astype(np.float64)
    row = []
    for label, key in cols:
        a = al[f"{name}|{key}"][..., None]
        c = Image.fromarray(np.clip(rgb * a + np.array(g, float) * (1 - a) + 0.5, 0, 255).astype(np.uint8)).crop(box)
        c = c.resize((c.size[0] * 8, c.size[1] * 8), Image.NEAREST)
        ImageDraw.Draw(c).text((4, 4), label, fill=(255, 255, 255) if g == dark else (0, 0, 0))
        row.append(c)
    out.append(row)
w = max(c.size[0] for r in out for c in r) + 6
h = [max(c.size[1] for c in r) + 6 for r in out]
sheet = Image.new("RGB", (w * 5, sum(h)), (24, 24, 24))
y = 0
for r, hh in zip(out, h):
    for i, c in enumerate(r):
        sheet.paste(c, (i * w, y))
    y += hh
sheet.save("alpha_085_close.png")
