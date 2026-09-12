# The lamp's light, still in the air behind everything the tower is made of: the
# halo round the lantern first, then the beam, then the tower over both of them so
# that the beam's root is cut by the lantern it comes out of.
#
# The beam is a mass of lit fog, not a film over clear sky -- that is the whole
# reason it can be painted at all. Laid as a fan of strokes rather than a
# block_in because what it has to do is *die out*, and a pressure list on a mass
# is read in canvas order, which would grade it the wrong way across.

# The light in the air. color_a is the value the patch meets the fog at: anything
# darker draws a rim round the glow instead of melting into it.
s.scumble(halo(), p.at_value("fog_high", 0.590), "glow", 7, direction="inward",
          note="subject halo")

s.dry()

# Eight rays. No two the same length, value, width or opacity, three of them
# stopping short of the frame where the fog eats them, and every one pressing
# hardest at the lamp and arriving at nothing.
RAYS = [
    (0.145, 0.205, 0.88, 0.665, 0.024, 0.24, [0.70, 0.22, 0.00], -0.003, 0.35),
    (0.150, 0.240, 1.06, 0.700, 0.030, 0.35, [0.80, 0.30, 0.00], +0.004, 0.55),
    (0.158, 0.290, 1.06, 0.745, 0.042, 0.50, [0.95, 0.50, 0.05], -0.006, 0.75),
    (0.167, 0.354, 1.06, 0.765, 0.048, 0.55, [1.00, 0.55, 0.10], +0.005, 0.85),
    (0.176, 0.420, 0.93, 0.755, 0.044, 0.50, [1.00, 0.50, 0.00], -0.007, 0.70),
    (0.184, 0.472, 0.80, 0.725, 0.034, 0.40, [0.95, 0.40, 0.00], +0.006, 0.50),
    (0.191, 0.524, 1.06, 0.695, 0.030, 0.32, [0.85, 0.28, 0.00], -0.005, 0.45),
    (0.197, 0.568, 0.99, 0.675, 0.024, 0.28, [0.80, 0.22, 0.00], +0.004, 0.40),
]
for y0, y1, xe, v, size, op, press, bow, load in RAYS:
    mx = 0.305 + 0.55 * (xe - 0.305)
    my = y0 + 0.55 * (y1 - y0) + bow
    s.stroke([(0.305, y0), (mx, my), (xe, y1)], "bristle",
             p.at_value("beam", v), size=size, opacity=op, load=load,
             load_falloff=0.30, pressure=press, note="subject beam")

# Two short marks at the lamp itself, where the beam is a solid thing before the
# fog has had any distance to take it apart.
s.stroke([(0.296, 0.164), (0.380, 0.180), (0.446, 0.200)], "bristle",
         "beam_core", size=0.021, opacity=0.50, load=0.8, load_falloff=0.65,
         pressure=[1.0, 0.30, 0.0], note="subject beam")
s.stroke([(0.298, 0.176), (0.350, 0.189)], "round_hard", "beam_core",
         size=0.010, opacity=0.55, pressure=[1.0, 0.15], note="subject beam")

# And where it grazes the water far out: lit fog lying on the sea, not a stripe
# on it. Kept under the horizon's own value so it reads as air, not as surf.
s.stroke([(0.78, 0.596), (0.94, 0.604), (1.06, 0.600)], "bristle",
         p.at_value("beam", 0.655), size=0.020, load=0.35, opacity=0.40,
         pressure="swell", note="subject beam")

print(s.look(grid=True))
print(s.look(values=True))
