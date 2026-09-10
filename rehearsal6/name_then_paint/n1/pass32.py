# Pass 32 - tidy the pot's inside, warm the foliage, mend the table edge.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()
rnd = random.Random(303)

# --- the inside of the pot, warm dark rather than teal ------------------------
s.block_in(ellipse(Region(0.336, 0.650, 0.500, 0.690)).inset(0.006), "flat",
           p.mix(p["pot_in"], "burnt_umber", 0.35), direction=(6, 174), density=1.0,
           size=0.013, load=1.0, pressure="even")
s.stroke([(0.348,0.660),(0.404,0.654),(0.462,0.660)], "round_hard",
         p.mix(p["pot_in"], "burnt_sienna", 0.30), size=0.007, pressure=[0.3,0.85,0.3])
s.stroke([(0.322,0.668),(0.366,0.692),(0.418,0.698),(0.470,0.692),(0.512,0.670)],
         "flat", p.mix(p["terra_mid"], p["terra_hi"], 0.62), size=0.016,
         pressure="even", load=1.0)
s.stroke([(0.330,0.666),(0.376,0.688),(0.422,0.694)], "round_hard", "terra_hi",
         size=0.0055, pressure=[0.45,1.0,0.25])
s.stroke([(0.340,0.686),(0.392,0.708),(0.446,0.712),(0.494,0.700)], "round_hard",
         "terra_sh", size=0.0055, pressure=[0.3,0.9,0.9,0.35])
s.stroke([(0.500,0.664),(0.522,0.676),(0.532,0.694)], "round_hard", "leaf_dk",
         size=0.012, pressure=[0.6,1.0,0.4])

# --- foliage: warm accents and two darks so it is not a flat green ------------
for pts, col, sz, ld in (
        ([(0.404,0.596),(0.446,0.586),(0.484,0.594)], "leaf_wm", 0.011, 0.6),
        ([(0.556,0.600),(0.598,0.612)], "leaf_md", 0.009, 0.55),
        ([(0.462,0.620),(0.512,0.630),(0.548,0.622)], "leaf_wm", 0.008, 0.5),
        ([(0.606,0.620),(0.646,0.636)], "leaf_dk", 0.013, 0.9),
        ([(0.424,0.640),(0.470,0.652)], "leaf_dk", 0.012, 0.9),
        ([(0.372,0.612),(0.398,0.634)], "leaf_md", 0.008, 0.5)):
    s.stroke(pts, "bristle", col, size=sz, load=ld, pressure=[0.4,1.0,0.35])
s.stroke([(0.664,0.626),(0.700,0.658),(0.716,0.692)], "round_hard", "leaf_lt",
         size=0.005, pressure=[0.55,0.8,0.15])

# --- the table's far edge on the right, off the staircase ---------------------
edge = [(0.688,0.640),(0.760,0.648),(0.828,0.644),(0.896,0.654),(0.962,0.650),(1.0,0.658)]
s.stroke([(x, y - 0.016) for x, y in edge], "round_hard", "bg", size=0.030,
         pressure="even", load=1.0)
s.stroke([(x, y + 0.014) for x, y in edge], "round_hard", "tbl", size=0.028,
         pressure="even", load=1.0)
s.stroke([(0.700,0.652),(0.790,0.656),(0.884,0.662)], "bristle",
         p.mix(p["tbl"], p["tbl_lit"], 0.5), size=0.009, load=0.5, pressure="taper")
# and on the left, a touch of light along it
s.stroke([(0.030,0.612),(0.120,0.616),(0.196,0.620)], "bristle",
         p.mix(p["tbl"], p["tbl_lit"], 0.62), size=0.008, load=0.45, pressure="taper")

# --- wood: a few marks that vary, none of them parallel for long --------------
grain = [([(0.052,0.742),(0.176,0.756),(0.238,0.750)], 0.010, 0.45, "tbl_lit"),
         ([(0.196,0.812),(0.296,0.822)], 0.007, 0.35, "tbl_hi"),
         ([(0.058,0.930),(0.152,0.944),(0.214,0.936)], 0.009, 0.40, "tbl_hi"),
         ([(0.560,0.712),(0.642,0.720)], 0.006, 0.30, "tbl_lit"),
         ([(0.268,0.686),(0.312,0.690)], 0.005, 0.30, "tbl_lit"),
         ([(0.128,0.876),(0.176,0.884)], 0.006, 0.35, "tbl_hi"),
         ([(0.836,0.836),(0.912,0.848)], 0.007, 0.30, "tbl"),
         ([(0.396,0.952),(0.486,0.962)], 0.008, 0.35, "tbl_lit")]
for pts, sz, ld, col in grain:
    s.stroke(pts, "bristle", col, size=sz, load=ld, pressure="taper")

print("strokes:", s.stroke_count)
print(s.look(sketch=False))
