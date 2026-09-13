s.dry()
# The coping had quietly become as light as the water it surrounds. The deck falls
# away from the pool into the dark -- broad films, no shape of their own.
dk = p.at_value("deck", 0.22)
for pts, size, op in [([(-0.05, 0.86), (0.12, 0.94), (0.28, 1.04)], 0.30, 0.55),
                      ([(-0.05, 0.52), (0.06, 0.64), (0.13, 0.78)], 0.24, 0.45),
                      ([(0.86, 0.90), (0.98, 0.98), (1.06, 1.05)],  0.26, 0.50),
                      ([(0.04, 0.335), (0.22, 0.365), (0.41, 0.402)], 0.14, 0.40),
                      ([(0.62, 0.395), (0.80, 0.425), (1.03, 0.452)], 0.12, 0.30)]:
    s.glaze(pts, dk, opacity=op, size=size, pressure="swell")

# and what the deck has on it: a wet sheen off the water, broken, and two darks.
# Three marks that describe a surface beat thirty that repeat it, so there is no
# tile grid here and the angles are deliberately not one angle.
sheen = p.at_value("deck", 0.46)
s.stroke([(0.300, 0.968), (0.404, 0.930), (0.489, 0.944)], "bristle", sheen,
         size=0.052, load=0.34, opacity=0.55, load_falloff=0.4, pressure="taper")
s.stroke([(0.876, 0.742), (0.942, 0.796)], "bristle", sheen,
         size=0.038, load=0.28, opacity=0.45, load_falloff=0.5, pressure="swell")
s.stroke([(0.238, 0.640), (0.286, 0.702), (0.318, 0.760)], "bristle", sheen,
         size=0.030, load=0.24, opacity=0.40, load_falloff=0.5, pressure="lift_off")
s.stroke([(0.545, 0.392), (0.640, 0.408)], "bristle", p.at_value("deck", 0.40),
         size=0.026, load=0.30, opacity=0.45, load_falloff=0.5, pressure="taper")
s.stroke([(0.052, 0.890), (0.166, 0.922)], "bristle", p.at_value("deck", 0.24),
         size=0.045, load=0.55, opacity=0.55, load_falloff=0.4, pressure="swell")
s.stroke([(0.930, 0.630), (0.985, 0.700)], "bristle", p.at_value("deck", 0.26),
         size=0.034, load=0.5, opacity=0.50, load_falloff=0.4, pressure="taper")
print(s.look())
