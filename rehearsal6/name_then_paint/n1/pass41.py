# Pass 41 - connect the bud, kill the grey smear under A, tidy A's left edge.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math
p = s.palette
s.dry()

# a stem and a leaf that tie the bud to the bunch
s.stroke([(0.546,0.394),(0.542,0.424),(0.536,0.444)], "round_hard", "stem",
         size=0.0055, pressure=[0.9, 0.7, 0.25])
s.block_in(ribbon([(0.544,0.408),(0.572,0.424),(0.596,0.452)], 0.026, 0.005).inset(0.005),
           "flat", "leaf_dk", direction="axis", density=1.0, size=0.010,
           load=1.0, pressure="even")
s.stroke([(0.548,0.412),(0.574,0.428),(0.590,0.446)], "round_hard", "leaf_md",
         size=0.004, pressure=[0.5, 0.8, 0.2])
s.block_in(ribbon([(0.540,0.398),(0.516,0.386),(0.494,0.392)], 0.022, 0.005).inset(0.004),
           "flat", "leaf_dk", direction="axis", density=1.0, size=0.009,
           load=1.0, pressure="even")

# the grey smear: make it the shadow where A overhangs C
s.block_in(polygon([(0.326,0.482),(0.400,0.478),(0.462,0.490),(0.470,0.512),
                    (0.396,0.514),(0.328,0.508)]), "flat", cool(pc(0.42), 0.14),
           direction=(11, 158), density=1.0, size=0.013, load=1.0, pressure="even")
for pts, v, sz in (([(0.336,0.498),(0.392,0.492),(0.446,0.500)], 0.38, 0.011),
                   ([(0.348,0.486),(0.412,0.482)], 0.46, 0.009),
                   ([(0.360,0.508),(0.424,0.510)], 0.35, 0.010)):
    s.stroke(pts, "bristle", cool(pc(v), 0.15), size=sz, load=0.85, pressure=[0.4,1.0,0.4])
# C's top edge, found again against that shadow
s.stroke(arc(0.398, 0.586, 0.078, 0.066, 1.00, 206, 264, 7), "bristle", warm(pc(0.80), 0.10),
         size=0.012, load=0.9, pressure=[0.4, 1.0, 0.4])
s.stroke(arc(0.398, 0.586, 0.078, 0.066, 1.01, 214, 256, 6), "liner", warm(pc(0.90), 0.08),
         size=0.0036, pressure=[0.25, 1.0, 0.3])
# A's underside, found against it too
s.stroke(arc(0.442, 0.436, 0.100, 0.092, 0.99, 42, 92, 7), "bristle", cool(pc(0.50), 0.13),
         size=0.013, load=0.85, pressure=[0.4, 1.0, 0.4])

# A's left flank, the green wedge gone
s.block_in(polygon([(0.310,0.494),(0.344,0.486),(0.352,0.524),(0.316,0.532)]), "flat",
           "bg", direction=(51, 141), density=1.0, size=0.012, load=1.0, pressure="even")
for t0, t1, f, v in ((140, 178, 1.00, 0.60), (110, 146, 1.02, 0.54)):
    s.stroke(arc(0.442, 0.436, 0.100, 0.092, f, t0, t1, 6), "bristle", warm(pc(v), 0.09),
             size=0.013, load=0.85, pressure=[0.4, 1.0, 0.4])

print("strokes:", s.stroke_count)
print(s.look(sketch=False))
