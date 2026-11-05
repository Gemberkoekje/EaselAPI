"""The candle's planned light, D1:E2 (planned 0.90), read as the checklist reads a place (its median value),
over the whole cell and inside the cut, painted at 1x and at 2x and 4x reduced to 120x300."""
import numpy as np
from PIL import Image
SP = "/tmp/claude-0/-home-user-projects/effc84d7-d7e9-5d60-848f-887f6f888335/scratchpad/"
inside = np.load(SP + "step2/cut/alphas.npz")["candle|c4"] > 0.5
runs = {"1x": Image.open(SP + "q2/candle/candle_rgb.png"),
        "2x reduced": Image.open(SP + "step2/dep/c2x/candle_rgb.png").resize((120, 300), Image.LANCZOS),
        "4x reduced": Image.open(SP + "q2/candle4x/candle_rgb.png").resize((120, 300), Image.LANCZOS)}
for name, im in runs.items():
    V = (np.asarray(im.convert("RGB")).astype(float) / 255) @ [0.2126, 0.7152, 0.0722]
    cell, m = V[0:75, 45:75], inside[0:75, 45:75]
    print(f"{name:11s} D1:E2 median: whole cell {np.median(cell):.2f}, inside the cut {np.median(cell[m]):.2f}  (planned 0.90)")
