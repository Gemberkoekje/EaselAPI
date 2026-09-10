# Pass 46 - cover the chalk outline solidly; make the background quiet.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()
rnd = random.Random(46)

s.block_in(polygon([(0.0,0.0),(0.62,0.0),(0.62,0.235),(0.50,0.295),(0.375,0.325),
                    (0.30,0.40),(0.262,0.52),(0.0,0.545)]), "flat", "bg_a",
           direction=(37, 127), density=1.0, size=0.055, load=1.0, pressure="even")
s.block_in(polygon([(0.03,0.06),(0.30,0.045),(0.42,0.16),(0.34,0.29),(0.14,0.31),(0.05,0.20)]),
           "flat", p.mix(p["bg_a"], p["bg_c"], 0.55), direction=(23, 113), density=1.0,
           size=0.045, load=1.0, pressure="even")

# bloom A's top edge, found again
for t0, t1, f, v in ((188, 236, 1.00, 0.88), (236, 282, 0.99, 0.84), (282, 320, 0.99, 0.74),
                     (160, 192, 1.02, 0.76)):
    s.stroke(arc(0.442, 0.436, 0.100, 0.092, f*rnd.uniform(0.98, 1.03), t0, t1, 7), "bristle",
             warm(pc(v), 0.11), size=rnd.uniform(0.014, 0.022), load=rnd.uniform(0.85, 1.0),
             pressure=[0.45, 1.0, 0.45])
s.stroke(arc(0.442, 0.436, 0.100, 0.092, 1.00, 196, 244, 6), "liner", warm(pc(0.92), 0.07),
         size=0.0038, pressure=[0.25, 1.0, 0.3])
s.stroke([(0.386,0.400),(0.395,0.393),(0.404,0.386)], "round_hard", "titanium_white",
         size=0.0085, pressure=[0.3, 1.0, 0.3])

# the boxes still on the table
for pts, col, sz in (([(0.856,0.676),(0.884,0.734),(0.870,0.796),(0.892,0.856)], "tbl", 0.036),
                     ([(0.916,0.700),(0.946,0.766),(0.930,0.836)], "tbl_dk", 0.034),
                     ([(0.982,0.706),(0.996,0.790)], "tbl_dk", 0.030),
                     ([(0.884,0.900),(0.940,0.946)], "tbl_dk", 0.028),
                     ([(0.548,0.784),(0.576,0.846),(0.558,0.906)], "tbl_far", 0.030),
                     ([(0.640,0.930),(0.720,0.952)], "tbl_far", 0.026)):
    s.stroke(pts, "flat", col, size=sz, load=1.0, pressure="even")
s.stroke([(0.866,0.712),(0.906,0.760),(0.888,0.818)], "bristle",
         p.mix(p["tbl"], p["tbl_dk"], 0.5), size=0.018, load=0.55, pressure="taper")

print("strokes:", s.stroke_count)
print(s.look())
