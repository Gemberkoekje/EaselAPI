# Pass 45 - break the remaining rectangles; set the bud back.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()
rnd = random.Random(45)
p["bg_c"] = p.tint(p.mix(p.mix("ultramarine","burnt_umber",0.72),"yellow_ochre",0.10), 0.058)
print("bg_c", p.hex(p["bg_c"]), round(p.value_of(p["bg_c"]), 3))

# --- soften the pale patch's boundary in the upper left -----------------------
bnd = [(0.06,0.06),(0.20,0.045),(0.36,0.05),(0.44,0.13),(0.50,0.22),(0.43,0.31),
       (0.34,0.40),(0.22,0.39),(0.10,0.36),(0.055,0.22)]
for i in range(len(bnd)):
    a = bnd[i]; b = bnd[(i + 1) % len(bnd)]
    mx, my = (a[0]+b[0])/2, (a[1]+b[1])/2
    for k in (-1, 1):
        s.stroke([(a[0] + k*0.018*rnd.uniform(0.3,1.4), a[1] + k*0.016*rnd.uniform(0.3,1.4)),
                  (mx + k*0.024*rnd.uniform(0.2,1.2), my + k*0.020*rnd.uniform(0.2,1.2)),
                  (b[0] + k*0.016*rnd.uniform(0.3,1.4), b[1] + k*0.018*rnd.uniform(0.3,1.4))],
                 "bristle", ("bg_c" if k < 0 else "bg_a"),
                 size=rnd.uniform(0.026, 0.050), load=rnd.uniform(0.55, 0.85),
                 pressure=[0.4, 1.0, 0.5])

# --- the table's far edge on the left, off the ruler ---------------------------
lft = [(0.0,0.600),(0.062,0.606),(0.128,0.598),(0.196,0.608),(0.262,0.602),(0.322,0.610)]
s.stroke([(x, y - 0.017) for x, y in lft], "round_hard", "bg", size=0.030,
         pressure="even", load=1.0)
s.stroke([(x, y + 0.015) for x, y in lft], "round_hard", "tbl", size=0.028,
         pressure="even", load=1.0)
s.stroke([(0.030,0.612),(0.128,0.610),(0.230,0.618)], "bristle",
         p.mix(p["tbl"], p["tbl_lit"], 0.55), size=0.008, load=0.45, pressure="taper")

# --- break the rectangles left on the table -----------------------------------
for pts, col, sz, ld in (
        ([(0.868,0.690),(0.900,0.740),(0.884,0.800)], "tbl", 0.030, 0.8),
        ([(0.906,0.812),(0.938,0.872),(0.920,0.930)], "tbl_dk", 0.028, 0.8),
        ([(0.548,0.780),(0.578,0.842),(0.560,0.900)], "tbl_far", 0.026, 0.75),
        ([(0.556,0.920),(0.620,0.946)], "tbl_far", 0.024, 0.7),
        ([(0.760,0.756),(0.820,0.778)], "tbl_far", 0.022, 0.6),
        ([(0.324,0.900),(0.392,0.918),(0.452,0.906)], "tbl_lit", 0.020, 0.5),
        ([(0.470,0.960),(0.560,0.972)], "tbl", 0.018, 0.5)):
    s.stroke(pts, "bristle", col, size=sz, load=ld, pressure=[0.4, 1.0, 0.45])

# --- the bud, smaller and dimmer ----------------------------------------------
s.block_in(polygon([(0.492,0.292),(0.640,0.288),(0.652,0.400),(0.556,0.436),(0.498,0.402)]),
           "flat", "bg", direction=(43, 133), density=1.0, size=0.018, load=1.0, pressure="even")
head(0.550, 0.360, 0.036, 0.030, 63, 0.470, 0.140, 0.008, lit=240.0, heart=False)
for t0, t1, f, v in ((180, 244, 1.00, 0.58), (244, 306, 0.98, 0.52), (306, 10, 1.00, 0.44),
                     (10, 76, 0.98, 0.40), (76, 142, 1.00, 0.38), (142, 182, 1.02, 0.48)):
    s.stroke(arc(0.550, 0.360, 0.036, 0.030, f*rnd.uniform(0.97, 1.05), t0, t1, 6), "bristle",
             (warm(pc(v), 0.10) if v > 0.50 else cool(pc(v), 0.12)),
             size=rnd.uniform(0.007, 0.011), load=rnd.uniform(0.7, 0.95),
             pressure=[0.4, 1.0, 0.4])
s.stroke(arc(0.550, 0.360, 0.036, 0.030, 1.00, 200, 250, 6), "liner", warm(pc(0.68), 0.09),
         size=0.0030, pressure=[0.25, 1.0, 0.3])
s.stroke([(0.548,0.392),(0.542,0.418),(0.536,0.442)], "round_hard", "stem",
         size=0.0050, pressure=[0.9, 0.7, 0.25])
s.block_in(ribbon([(0.544,0.402),(0.572,0.420),(0.594,0.448)], 0.024, 0.005).inset(0.005),
           "flat", "leaf_dk", direction="axis", density=1.0, size=0.009,
           load=1.0, pressure="even")
s.block_in(ribbon([(0.542,0.394),(0.518,0.382),(0.498,0.388)], 0.020, 0.005).inset(0.004),
           "flat", "leaf_dk", direction="axis", density=1.0, size=0.008,
           load=1.0, pressure="even")

print("strokes:", s.stroke_count)
print(s.look())
