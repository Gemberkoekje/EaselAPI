# Pass 28 - the bud back at half-light; then lose some edges.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()

s.block_in(ellipse(Region(0.494, 0.312, 0.622, 0.432)), "flat", "bg",
           direction=(38, 128), density=1.0, size=0.022, load=1.0, pressure="even")
head(0.556, 0.370, 0.045, 0.039, 63, 0.535, 0.150, 0.010, lit=242.0, heart=False)
clean(0.556, 0.370, 0.045, 0.039, [(212, 448, "bg")], sz=0.014, rr=1.22)
ruffle(0.556, 0.370, 0.045, 0.039, 64, 0.535, 0.150, 4, 0.006, lit=242.0)

# --- lose edges where the flowers meet the dark -------------------------------
rnd = random.Random(5)
def lose(cx, cy, rx, ry, t0, t1, v, n=5, sz=0.013):
    for i in range(n):
        a0 = t0 + (t1 - t0) * i / n
        a1 = a0 + (t1 - t0) / n * 1.4
        f = rnd.uniform(0.94, 1.06)
        s.stroke(arc(cx, cy, rx, ry, f, a0, a1, 5), "bristle",
                 cool(pc(v + rnd.uniform(-0.04, 0.04)), 0.12),
                 size=sz*rnd.uniform(0.8, 1.3), load=rnd.uniform(0.45, 0.7),
                 pressure=[0.4, 1.0, 0.35])

lose(0.398, 0.586, 0.078, 0.066, 20, 130, 0.36, 5, 0.014)     # C into the foliage
lose(0.640, 0.520, 0.112, 0.100, 46, 128, 0.34, 5, 0.016)     # B into the table dark
lose(0.442, 0.436, 0.100, 0.092, 8, 66, 0.40, 4, 0.014)       # A into the gap behind B

# darks in the gaps between the heads, so the bouquet has depth
for pts, v, sz in (([(0.520,0.470),(0.548,0.492),(0.556,0.520)], 0.30, 0.014),
                   ([(0.336,0.520),(0.352,0.548)], 0.32, 0.012),
                   ([(0.494,0.596),(0.520,0.608)], 0.28, 0.013),
                   ([(0.592,0.418),(0.606,0.448)], 0.33, 0.011)):
    s.stroke(pts, "bristle", cool(pc(v), 0.14), size=sz, load=0.8, pressure=[0.5,1.0,0.4])

print("strokes:", s.stroke_count)
print(s.look(sketch=False))
