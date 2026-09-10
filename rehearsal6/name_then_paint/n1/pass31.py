# Pass 31 - fallen petals with a round tip, so they taper instead of ending square.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math
p = s.palette
s.dry()
s.block_in(polygon([(0.556,0.788),(0.856,0.766),(0.862,0.938),(0.634,0.948),(0.550,0.878)]),
           "flat", "tbl_far", direction=(9, 160), density=1.0, size=0.030,
           load=1.0, pressure="even")
s.block_in(polygon([(0.766,0.772),(0.862,0.768),(0.866,0.906),(0.776,0.916)]),
           "flat", "tbl_dk", direction=(23, 142), density=1.0, size=0.024,
           load=1.0, pressure="even")

def petal(cx, cy, a, b, rot, v, vlit, curl=1.0):
    r = math.radians(rot); dx, dy = math.cos(r), math.sin(r); nx, ny = -math.sin(r), math.cos(r)
    s.stroke([(cx - a*0.75*dx + 0.005 + nx*b*1.15, cy - a*0.75*dy + 0.007 + ny*b*1.15),
              (cx + a*0.80*dx + 0.010 + nx*b*1.05, cy + a*0.80*dy + 0.009 + ny*b*1.05)],
             "round_hard", p.mix(p["cast"], "burnt_umber", 0.62), size=b*1.7,
             pressure=[0.4, 1.0, 0.35])
    s.stroke([(cx - a*dx - nx*b*0.10, cy - a*dy - ny*b*0.10),
              (cx + nx*b*0.16*curl, cy + ny*b*0.16*curl),
              (cx + a*dx - nx*b*0.06, cy + a*dy - ny*b*0.06)],
             "round_hard", warm(pc(v), 0.14), size=b*2.1, pressure=[0.28, 1.0, 0.30])
    s.stroke([(cx - a*0.74*dx - nx*b*0.42, cy - a*0.74*dy - ny*b*0.42),
              (cx - nx*b*0.60, cy - ny*b*0.60),
              (cx + a*0.70*dx - nx*b*0.26, cy + a*0.70*dy - ny*b*0.26)],
             "liner", warm(pc(vlit), 0.10), size=0.0040, pressure=[0.25, 1.0, 0.30])
    s.stroke([(cx + a*0.26*dx + nx*b*0.52, cy + a*0.26*dy + ny*b*0.52),
              (cx + a*0.80*dx + nx*b*0.18, cy + a*0.80*dy + ny*b*0.18)],
             "round_hard", cool(pc(max(0.33, v - 0.22)), 0.14), size=0.0038, pressure=[0.85, 0.15])

petal(0.610, 0.838, 0.030, 0.0125, -13, 0.63, 0.81, 1.0)
petal(0.700, 0.892, 0.034, 0.0135,  10, 0.57, 0.73, -0.8)
petal(0.789, 0.808, 0.032, 0.0120, -28, 0.67, 0.85, 0.7)

print("strokes:", s.stroke_count)
print(s.look(region=span("E6","H8"), sketch=False))
