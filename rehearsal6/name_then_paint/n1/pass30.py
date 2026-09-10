# Pass 30 - break the slab between the heads; the fallen petals as three marks each.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()
rnd = random.Random(77)

# A's right flank, in shadow, running behind B
for t0, sp, f, v in ((300, 40, 1.02, 0.50), (326, 44, 0.96, 0.56), (352, 40, 1.04, 0.47),
                     (14, 36, 0.98, 0.43), (338, 30, 1.10, 0.52), (310, 28, 1.09, 0.46)):
    s.stroke(arc(0.442, 0.436, 0.100, 0.092, f, t0, t0+sp, 6), "bristle",
             cool(pc(v + rnd.uniform(-0.03, 0.03)), 0.10), size=rnd.uniform(0.011, 0.019),
             load=rnd.uniform(0.6, 0.9), pressure=[0.4, 1.0, 0.4])
# B's left edge over it
for t0, sp, f, v in ((150, 40, 1.00, 0.58), (176, 36, 0.97, 0.63), (200, 32, 1.02, 0.68)):
    s.stroke(arc(0.640, 0.520, 0.112, 0.100, f, t0, t0+sp, 6), "bristle",
             warm(pc(v), 0.09), size=rnd.uniform(0.012, 0.018), load=0.85,
             pressure=[0.4, 1.0, 0.4])
# soften the bud's underside
for t0, sp, f, v in ((60, 44, 1.02, 0.44), (96, 40, 0.98, 0.40), (34, 34, 1.05, 0.47)):
    s.stroke(arc(0.556, 0.370, 0.045, 0.039, f, t0, t0+sp, 5), "bristle",
             cool(pc(v), 0.12), size=0.009, load=0.65, pressure=[0.4, 1.0, 0.35])

# --- the fallen petals again: one body stroke, one lit edge, one dark under ----
s.block_in(polygon([(0.560,0.796),(0.850,0.772),(0.856,0.930),(0.640,0.940),(0.556,0.876)]),
           "flat", "tbl_far", direction=(9, 160), density=1.0, size=0.030,
           load=1.0, pressure="even")
s.block_in(polygon([(0.762,0.776),(0.856,0.772),(0.860,0.900),(0.772,0.910)]),
           "flat", "tbl_dk", direction=(23, 142), density=1.0, size=0.024,
           load=1.0, pressure="even")

def petal(cx, cy, a, b, rot, v, vlit):
    r = math.radians(rot); dx, dy = math.cos(r), math.sin(r); nx, ny = -math.sin(r), math.cos(r)
    s.stroke([(cx - a*dx + 0.004 + nx*b*0.9, cy - a*dy + 0.006 + ny*b*0.9),
              (cx + a*dx + 0.009 + nx*b*0.9, cy + a*dy + 0.008 + ny*b*0.9)],
             "flat", p.mix(p["cast"], "burnt_umber", 0.6), size=b*1.5, pressure="even", load=1.0)
    s.stroke([(cx - a*0.92*dx, cy - a*0.92*dy), (cx, cy), (cx + a*0.92*dx, cy + a*0.92*dy)],
             "flat", warm(pc(v), 0.14), size=b*2.0, pressure="swell", load=1.0)
    s.stroke([(cx - a*0.80*dx - nx*b*0.45, cy - a*0.80*dy - ny*b*0.45),
              (cx - nx*b*0.62, cy - ny*b*0.62),
              (cx + a*0.74*dx - nx*b*0.30, cy + a*0.74*dy - ny*b*0.30)],
             "liner", warm(pc(vlit), 0.10), size=0.0042, pressure=[0.3, 1.0, 0.35])
    s.stroke([(cx + a*0.30*dx + nx*b*0.5, cy + a*0.30*dy + ny*b*0.5),
              (cx + a*0.86*dx + nx*b*0.2, cy + a*0.86*dy + ny*b*0.2)],
             "round_hard", cool(pc(max(0.33, v - 0.20)), 0.14), size=0.004, pressure=[0.8, 0.2])

petal(0.612, 0.838, 0.032, 0.014, -13, 0.63, 0.80)
petal(0.702, 0.892, 0.036, 0.015,   9, 0.58, 0.74)
petal(0.790, 0.808, 0.034, 0.014, -27, 0.66, 0.83)

print("strokes:", s.stroke_count)
print(s.look(region=span("E6","H8"), sketch=False))
