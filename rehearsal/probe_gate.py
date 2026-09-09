import numpy as np
from PIL import Image
import easel.canvas as C
from easel import Session

# A scumble like the one that printed a dot screen, at several grain weights.
tiles = []
for hw, gw in [(0.72, 0.28), (0.62, 0.38), (0.52, 0.48), (0.42, 0.58)]:
    C._TOOTH_HEIGHT_W, C._TOOTH_GRAIN_W = hw, gw
    s = Session(340, 240, texture="linen", ground="umber_wash", seed=7, timelapse=False)
    s.block_in((0, 0, 1, 1), "bristle", s.palette.tint("yellow_ochre", 0.4),
               density=0.7, size=0.30, direction="horizontal")
    s.dry()
    s.block_in((0, 0, 1, 1), "bristle",
               s.palette.tint(s.palette.mix("burnt_umber", "ultramarine", 0.35), 0.10),
               density=0.55, size=0.30, direction="horizontal", load=0.55)
    img = np.asarray(s.canvas.to_srgb8())
    lab = Image.fromarray(img)
    tiles.append((f"h{hw:.2f}/g{gw:.2f}", lab))

W = sum(t[1].width for t in tiles)
sheet = Image.new("RGB", (W, tiles[0][1].height), "white")
x = 0
for _, im in tiles:
    sheet.paste(im, (x, 0)); x += im.width
sheet.save("rehearsal/gate_weights.png")
print("labels:", [t[0] for t in tiles])
