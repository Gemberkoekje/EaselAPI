# Surroundings. The glow is broad, so its reflection is too: a few fainter, shorter glints
# spread sideways under it near the horizon (fewer, fainter the further from the core).
# The one surf mark that reads as a scratch knocked back with a film of the water. The
# near water given a little size: a few long low swells (films, not paint), larger
# toward the viewer, with a thin lit crest on two of them.
import random
rng = random.Random(21)
p["glint_dim"] = p.at_value(p.mix("film", "glint", 0.5), 0.56)
for x, y, n, op in ((0.055, 0.600, 0.030, 0.45), (0.335, 0.598, 0.024, 0.40),
                    (0.405, 0.612, 0.020, 0.30), (0.02, 0.628, 0.036, 0.30),
                    (0.300, 0.640, 0.040, 0.28)):
    s.stroke([(x - n / 2, y + 0.0012), (x + n * 0.15, y - 0.0012), (x + n / 2, y + 0.0008)],
             "round_hard", "glint_dim", size=0.0038 + 0.0015 * (y - 0.59) / 0.05, opacity=op,
             tip_wobble=0.5, pressure=[0.15, 1.0, 0.3])
s.dry()
water = s.sample(Region(0.55, 0.78, 0.62, 0.83))
s.glaze([(0.608, 0.742), (0.638, 0.764), (0.664, 0.789)], water, opacity=0.35, size=0.016)
near = s.sample(Region(0.0, 0.82, 0.60, 1.0)); vn = p.value_of(near)
p["swell_dark"] = p.at_value(p.mix(near, "zenith", 0.15), vn - 0.05)
p["swell_lit"]  = p.at_value(p.mix("sea_far", "pale", 0.3), 0.36)
s.glaze([(-0.04, 0.905), (0.18, 0.897), (0.40, 0.908), (0.58, 0.902)], "swell_dark",
        opacity=0.45, size=0.026, pressure=[0.5, 1.0, 0.8, 0.3])
s.stroke([(0.02, 0.884), (0.21, 0.879), (0.37, 0.887)], "round_hard", "swell_lit",
         size=0.006, opacity=0.5, pressure=[0.1, 0.8, 1.0, 0.2])
s.glaze([(0.33, 0.968), (0.55, 0.958), (0.74, 0.972)], "swell_dark",
        opacity=0.45, size=0.034, pressure=[0.3, 1.0, 0.4])
s.glaze([(0.08, 0.790), (0.22, 0.786), (0.33, 0.792)], "swell_dark",
        opacity=0.4, size=0.018, pressure=[0.3, 1.0, 0.3])
s.stroke([(0.44, 0.945), (0.60, 0.939), (0.70, 0.946)], "round_hard", "swell_lit",
         size=0.007, opacity=0.45, pressure=[0.2, 1.0, 0.4])
s.dry()
