# Pass 29 - close the gash between A and B; the three fallen petals.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math
p = s.palette
s.dry()

# smooth the sawtooth above B and the wedge between the heads
s.block_in(polygon([(0.530,0.300),(0.640,0.296),(0.664,0.336),(0.590,0.372),(0.522,0.352)]),
           "flat", "bg", direction=(41, 131), density=1.0, size=0.020, load=1.0, pressure="even")
s.block_in(polygon([(0.508,0.340),(0.556,0.352),(0.572,0.424),(0.542,0.470),(0.508,0.442)]),
           "flat", cool(pc(0.42), 0.14), direction=(64, 154), density=1.0, size=0.014,
           load=1.0, pressure="even")
for t0, f, v in ((300, 1.00, 0.60), (326, 0.96, 0.66), (352, 0.98, 0.58), (272, 1.02, 0.55)):
    s.stroke(arc(0.640, 0.520, 0.112, 0.100, f, t0, t0+34, 6), "bristle",
             warm(pc(v), 0.10), size=0.013, load=0.8, pressure=[0.4, 1.0, 0.4])
for t0, f, v in ((338, 1.00, 0.64), (10, 0.98, 0.55), (300, 1.02, 0.70)):
    s.stroke(arc(0.442, 0.436, 0.100, 0.092, f, t0, t0+30, 6), "bristle",
             warm(pc(v), 0.10), size=0.012, load=0.75, pressure=[0.4, 1.0, 0.4])
s.stroke(arc(0.556, 0.370, 0.045, 0.039, 1.02, 74, 150, 6), "bristle",
         cool(pc(0.44), 0.12), size=0.010, load=0.7, pressure=[0.4, 1.0, 0.4])

# --- the three fallen petals ---------------------------------------------------
fallen = [(0.612, 0.838, 0.034, 0.017, -14, 0.54, 0.70),
          (0.702, 0.892, 0.038, 0.018,   8, 0.50, 0.65),
          (0.790, 0.808, 0.036, 0.017, -26, 0.57, 0.74)]
for cx, cy, a, b, rot, v, vlit in fallen:
    r = math.radians(rot)
    dx, dy = math.cos(r), math.sin(r)
    nx, ny = -math.sin(r), math.cos(r)
    # the shadow it throws, first: it is under the petal
    s.stroke([(cx - a*0.8*dx + 0.006, cy - a*0.8*dy + b*0.9),
              (cx + a*0.9*dx + 0.010, cy + a*0.9*dy + b*1.0)],
             "round_hard", p.mix(p["cast"], "burnt_umber", 0.55), size=0.012,
             pressure=[0.5, 1.0, 0.4])
    el = ellipse(Region(cx-a, cy-b, cx+a, cy+b), rotate=rot)
    s.block_in(el.inset(0.0035), "flat", cool(pc(v), 0.08), direction="axis",
               density=1.0, size=0.007, load=1.0, pressure="even")
    # the lit upper edge, and the curl at one end
    s.stroke([(cx - a*0.85*dx + nx*b*0.35, cy - a*0.85*dy + ny*b*0.35),
              (cx + nx*b*0.75, cy + ny*b*0.75),
              (cx + a*0.8*dx + nx*b*0.3, cy + a*0.8*dy + ny*b*0.3)],
             "liner", warm(pc(vlit), 0.12), size=0.0045, pressure=[0.3, 1.0, 0.3])
    s.stroke([(cx + a*0.62*dx - nx*b*0.5, cy + a*0.62*dy - ny*b*0.5),
              (cx + a*1.02*dx - nx*b*0.15, cy + a*1.02*dy - ny*b*0.15)],
             "round_hard", pc(min(0.86, vlit + 0.10)), size=0.005, pressure=[0.9, 0.2])
    s.stroke([(cx - a*0.35*dx - nx*b*0.6, cy - a*0.35*dy - ny*b*0.6),
              (cx + a*0.45*dx - nx*b*0.45, cy + a*0.45*dy - ny*b*0.45)],
             "round_hard", cool(pc(max(0.34, v - 0.16)), 0.14), size=0.004, pressure=[0.4, 0.9, 0.3])

print("strokes:", s.stroke_count)
print(s.look(region=span("E6","H8"), sketch=False))
print(s.look(sketch=False))
