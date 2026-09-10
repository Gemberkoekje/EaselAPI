# Pass 39 - last repairs, petal notches, and the highlights.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math
p = s.palette
s.dry()

# the black lozenge under B, given foliage instead
s.block_in(polygon([(0.458,0.582),(0.522,0.586),(0.548,0.618),(0.520,0.648),(0.462,0.640)]),
           "flat", "leaf_dk", direction=(29, 143), density=1.0, size=0.016,
           load=1.0, pressure="even")
for pts, col, sz, ld in (([(0.470,0.600),(0.508,0.596),(0.532,0.606)], "leaf_md", 0.010, 0.6),
                         ([(0.478,0.624),(0.514,0.632)], "leaf_wm", 0.008, 0.5),
                         ([(0.492,0.584),(0.524,0.592)], "leaf_md", 0.007, 0.45),
                         ([(0.464,0.614),(0.490,0.626)], "leaf_dk", 0.011, 0.9)):
    s.stroke(pts, "bristle", col, size=sz, load=ld, pressure=[0.4, 1.0, 0.35])
s.stroke([(0.474,0.594),(0.506,0.590)], "round_hard", "leaf_lt", size=0.004,
         pressure=[0.6, 0.15])

# the dark arc hanging over the bud
s.block_in(polygon([(0.448,0.316),(0.528,0.306),(0.540,0.344),(0.470,0.360)]), "flat",
           "bg", direction=(47, 137), density=1.0, size=0.015, load=1.0, pressure="even")
for t0, t1, f, v in ((186, 244, 1.00, 0.62), (244, 296, 0.99, 0.56), (152, 190, 1.02, 0.50)):
    s.stroke(arc(0.556, 0.370, 0.045, 0.039, f, t0, t1, 6), "bristle", warm(pc(v), 0.10),
             size=0.009, load=0.9, pressure=[0.4, 1.0, 0.4])

# notches where one petal laps over another at the rim
for cx, cy, rx, ry, th, f0, f1, v, w in (
        (0.442,0.436,0.100,0.092, 202, 1.03, 0.80, 0.66, 0.005),
        (0.442,0.436,0.100,0.092, 266, 1.02, 0.84, 0.62, 0.0045),
        (0.640,0.520,0.112,0.100, 186, 1.03, 0.82, 0.62, 0.005),
        (0.640,0.520,0.112,0.100, 232, 1.02, 0.82, 0.68, 0.0045),
        (0.640,0.520,0.112,0.100, 296, 1.02, 0.86, 0.58, 0.004),
        (0.398,0.586,0.078,0.066, 232, 1.02, 0.80, 0.58, 0.004)):
    s.stroke([at(cx, cy, rx, ry, f0, th), at(cx, cy, rx, ry, (f0+f1)/2, th+4),
              at(cx, cy, rx, ry, f1, th - 3)], "round_hard", cool(pc(v), 0.13),
             size=w, pressure=[1.0, 0.6, 0.2])

# --- the highlights: five marks -----------------------------------------------
s.dab(0.394, 0.394, "round_hard", "titanium_white", size=0.009, press=3)
s.dab(0.421, 0.373, "round_hard", p.mix("titanium_white", "yellow_ochre", 0.10),
      size=0.007, press=3)
s.dab(0.588, 0.472, "round_hard", "titanium_white", size=0.008, press=3)
s.dab(0.366, 0.556, "round_hard", p.mix("titanium_white", "yellow_ochre", 0.08),
      size=0.006, press=3)
s.dab(0.778, 0.800, "round_hard", p.mix("titanium_white", "yellow_ochre", 0.14),
      size=0.0045, press=3)

print("strokes:", s.stroke_count)
print(s.look(sketch=False))
