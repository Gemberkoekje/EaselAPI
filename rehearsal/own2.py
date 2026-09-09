# Edges, incident in the dark, then a very few accents.
p = s.palette
p["deep2"] = p.shade(p.mix("ultramarine", "burnt_umber", 0.62), 0.35)
p["lift"]  = p.tint(p.mix("burnt_sienna", "yellow_ochre", 0.55), 0.30)
p["glow"]  = p.tint(p.mix("yellow_ochre", "cadmium_yellow", 0.40), 0.72)

s.dry()
# 1. kill the hard vertical seam on the left: carry the light across it, broken
for y0, y1, sz, ld in [(0.06, 0.10, 0.10, 0.9), (0.17, 0.14, 0.07, 0.75),
                       (0.28, 0.24, 0.05, 0.6), (0.36, 0.33, 0.045, 0.5)]:
    s.stroke([(0.44, y0), (0.22, y1), (-0.02, y1 + 0.02)], "bristle", "pale",
             size=sz, load=ld, pressure="lift_off")
s.smudge([(0.30, 0.02), (0.29, 0.30)], size=0.075)

# 2. incident in the dark mass -- it was one flat field
for x0, y0, x1, y1, sz in [(0.05, 0.62, 0.30, 0.70, 0.055),
                           (0.36, 0.72, 0.62, 0.66, 0.045),
                           (0.62, 0.84, 0.92, 0.90, 0.060),
                           (0.14, 0.88, 0.44, 0.94, 0.038),
                           (0.70, 0.70, 0.99, 0.78, 0.032)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 - 0.02), (x1, y1)],
             "bristle", "deep2", size=sz, load=0.55, pressure="taper")
for x0, y0, x1, y1 in [(0.10, 0.55, 0.26, 0.60), (0.50, 0.60, 0.66, 0.64),
                       (0.80, 0.70, 0.95, 0.73)]:
    s.stroke([(x0, y0), (x1, y1)], "knife", "lift", size=0.022,
             load=0.75, pressure="dab")

# 3. edges: one hard, one soft, one lost
s.stroke([(0.30, 0.523), (0.44, 0.492), (0.50, 0.464)], "round_hard", "deep2",
         size=0.010, load=1.0, pressure="taper")            # found
s.smudge([(0.66, 0.655), (0.80, 0.615)], size=0.055)        # soft
s.smudge([(0.86, 0.60), (0.99, 0.735)], size=0.090)         # lost

# 4. accents. Few, and that is the point.
s.dab(0.735, 0.245, "round_hard", "glow", size=0.016)
s.stroke([(0.760, 0.300), (0.788, 0.330)], "round_hard", "glow",
         size=0.008, load=1.0, pressure="taper")
s.dab(0.176, 0.352, "round_hard", p.tint("titanium_white", 0.85), size=0.007)
s.stroke([(0.44, 0.487), (0.52, 0.470)], "round_hard", p.tint("yellow_ochre", 0.80),
         size=0.006, load=1.0, pressure="lift_off")

print("strokes:", s.stroke_count)
print(s.look())
