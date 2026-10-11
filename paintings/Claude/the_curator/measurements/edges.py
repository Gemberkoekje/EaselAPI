import json, math, sys
import numpy as np
from PIL import Image
A = "/home/user/projects/the-curator/game/art/easel/"
S = "/tmp/claude-0/-home-user-projects/effc84d7-d7e9-5d60-848f-887f6f888335/scratchpad/"

def perim(poly):
    return sum(math.dist(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly)))

def report(name, path, edge_len):
    a = np.asarray(Image.open(path).convert("RGBA"))[:, :, 3].astype(int)
    n = a.size
    zero, full, part = (a == 0).sum(), (a == 255).sum(), ((a > 0) & (a < 255)).sum()
    band = ((a >= 26) & (a <= 229)).sum()   # 10%-90% of full alpha
    print(f"{name:16s} {a.shape[1]}x{a.shape[0]}  transparent {zero / n:6.1%}  partial {part:6d} px  "
          f"partial/edge {part / edge_len:4.2f} px  10-90% band/edge {band / edge_len:4.2f} px  (edge ~{edge_len:.0f} px)")
    return a

def profile(a, y, x0, x1):
    return [int(v) for v in a[y, x0:x1]]

# patron: hood + cloak outlines (pixels); the union's edge is shorter than the sum, so this overstates the edge and understates width
o = json.load(open(S + "art/patron/outline.json"))
pa = report("patron_default", A + "patron_default.png", sum(perim(o[k]) for k in o))
c = json.load(open(S + "cand/outline.json"))
ca = report("candle", A + "candle.png", sum(perim(c[k]) for k in c))
# arch: half circle r=260 plus two sides from y=400 to the bottom (720)
wa = report("doorway_wall", A + "doorway_wall.png", math.pi * 260 + 2 * 320)
print("arch row 600, x 694..706:", profile(wa, 600, 694, 707))
print("arch row 600, x 1214..1226:", profile(wa, 600, 1214, 1227))
# a near-vertical stretch of each sprite's side
def side(a, y):
    row = a[y]
    xs = np.nonzero((row > 0) & (row < 255))[0]
    return xs
for nm, a, ys in (("patron", pa, (300, 400)), ("candle", ca, (100, 180))):
    for y in ys:
        xs = side(a, y)
        if len(xs):
            x0 = xs[0]
            print(f"{nm} row {y}, x {x0 - 1}..{x0 + 5}:", profile(a, y, x0 - 1, x0 + 6))
