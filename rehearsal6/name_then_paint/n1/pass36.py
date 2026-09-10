# Pass 36 - put the turn back into each head, and clean what escaped.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()
rnd = random.Random(613)

def flank(cx, cy, rx, ry, lit, vbase, vamp, sz):
    for k, (off, sp, f, mul) in enumerate([(96, 62, 0.62, -0.72), (118, 66, 0.80, -0.86),
                                           (140, 58, 0.96, -0.96), (86, 48, 1.04, -0.90),
                                           (162, 46, 0.88, -0.80), (108, 50, 0.44, -0.62)]):
    	pass
    for k, (off, sp, f, mul) in enumerate([(96, 62, 0.62, -0.72), (118, 66, 0.80, -0.86),
                                           (140, 58, 0.96, -0.96), (86, 48, 1.04, -0.90),
                                           (162, 46, 0.88, -0.80), (108, 50, 0.44, -0.62)]):
        v = max(0.33, vbase + vamp*mul)
        s.stroke(arc(cx, cy, rx, ry, f*rnd.uniform(0.96, 1.04), lit+off, lit+off+sp, 7),
                 "bristle", cool(pc(v + rnd.uniform(-0.03, 0.03)), 0.15),
                 size=sz*rnd.uniform(0.85, 1.30), load=rnd.uniform(0.8, 1.0),
                 pressure=[0.45, 1.0, 0.5])

flank(0.442, 0.436, 0.100, 0.092, 228, 0.700, 0.205, 0.022)
flank(0.640, 0.520, 0.112, 0.100, 218, 0.645, 0.220, 0.024)
flank(0.398, 0.586, 0.078, 0.066, 236, 0.575, 0.195, 0.018)
flank(0.556, 0.370, 0.045, 0.039, 242, 0.505, 0.150, 0.012)

clean(0.442, 0.436, 0.100, 0.092, [(140, 348, "bg")], sz=0.024, rr=1.16)
clean(0.640, 0.520, 0.112, 0.100, [(250, 424, "bg"), (48, 128, "bg")], sz=0.026, rr=1.15)
clean(0.556, 0.370, 0.045, 0.039, [(214, 452, "bg")], sz=0.016, rr=1.24)
clean(0.398, 0.586, 0.078, 0.066, [(186, 300, "bg")], sz=0.020, rr=1.20)
s.block_in(polygon([(0.520,0.392),(0.566,0.400),(0.578,0.446),(0.548,0.470),(0.512,0.446)]),
           "flat", cool(pc(0.44), 0.14), direction=(58, 148), density=1.0, size=0.012,
           load=1.0, pressure="even")

print("strokes:", s.stroke_count)
print(s.look(region=span("C3","G6"), sketch=False))
print(s.look(values=True, sketch=False))
