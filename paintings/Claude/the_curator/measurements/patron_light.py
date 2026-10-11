"""Is the top of the patron's value range paint, or the ground the cut throws away? And how much of the rim landed?"""
import numpy as np
from PIL import Image
A = "/home/user/projects/the-curator/game/art/easel/"
RGB = "/tmp/claude-0/-home-user-projects/effc84d7-d7e9-5d60-848f-887f6f888335/scratchpad/cand/patron_rgb.png"   # patron_default.py 99, uncut
V = (np.asarray(Image.open(RGB).convert("RGB")).astype(float) / 255) @ [0.2126, 0.7152, 0.0722]   # Easel's value
a = np.asarray(Image.open(A + "patron_default.png").convert("RGBA"))[:, :, 3]
inside, outside = V[a == 255], V[a == 0]
print(f"inside the cut: max {inside.max():.2f}, 99.9th {np.percentile(inside, 99.9):.2f}, 99th {np.percentile(inside, 99):.2f}")
print(f"cut-away: median {np.median(outside):.2f}")
H, W = V.shape
cell, ca = V[0:int(3 * H / 8), int(3 * W / 8):int(5 * W / 8)], a[0:int(3 * H / 8), int(3 * W / 8):int(5 * W / 8)]
top = lambda v: np.sort(v.ravel())[-max(1, v.size // 20):].mean()
print(f"D1:E3 brightest twentieth: whole cell {top(cell):.2f}, inside the cut {top(cell[ca == 255]):.2f}")
for lo, hi in ((1, 254), (255, 255)):
    m = (a >= lo) & (a <= hi)
    print(f"alpha {lo}-{hi}: {m.sum()} px, pixels over value 0.40: {(V[m] > 0.40).sum()}")
