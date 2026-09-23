# The glow broken down the water toward the viewer (on the film laid in the sea pass):
# thin slivers, densest under the horizon; rows further apart, wider and fainter as they
# come nearer, no two pieces one length; then the water's own dark laid back across.
# Then surf where the sea meets the rock: few marks, low contrast, hugging the rock.
import random
rng = random.Random(5)
p["glint"] = p.at_value(p.mix("film", "core", 0.5), 0.64)
s.dry()
cx = lambda y: 0.19 + (y - 0.59) * 0.12            # the film's own centre line
y, gap, spread, op, sz = 0.592, 0.0105, 0.012, 0.75, 0.0045
while y < 0.93:
    pieces = 2 if y < 0.64 else 1
    for k in range(pieces):
        x = cx(y) + rng.gauss(0, spread) + (k * rng.choice((-1, 1)) * rng.uniform(0.03, 0.06))
        n = rng.uniform(0.018, 0.060)
        s.stroke([(x - n / 2, y + 0.0015), (x + n * 0.1, y - 0.0015), (x + n / 2, y + 0.001)],
                 "round_hard", "glint", size=sz, opacity=op * rng.uniform(0.8, 1.0),
                 tip_wobble=0.5, pressure=[0.15, 1.0, 0.35])
    y, gap, spread, op, sz = y + gap, gap * 1.22, spread * 1.22, op * 0.84, sz * 1.07
s.stroke([(0.16, 0.655), (0.215, 0.652), (0.26, 0.657)], "round_hard", "sea_near",
         size=0.005, opacity=0.7, pressure=[0.2, 1.0, 0.3])
s.stroke([(0.17, 0.795), (0.24, 0.790), (0.30, 0.797)], "round_hard", "sea_near",
         size=0.006, opacity=0.7, pressure=[0.3, 1.0, 0.2])

p["foam"] = p.at_value(p.mix("pale", "sea_far", 0.4), 0.52)
p["foam_warm"] = p.at_value(p.mix("foam", "glow", 0.3), 0.58)
s.stroke([(0.382, 0.641), (0.398, 0.646), (0.417, 0.644)], "bristle", "foam_warm",
         size=0.028, load=0.75, opacity=0.6, pressure="swell")           # at the tip
s.stroke([(0.342, 0.647), (0.356, 0.649), (0.368, 0.646)], "round_hard", "foam_warm",
         size=0.006, opacity=0.65, tip_wobble=0.6, pressure=[0.2, 1.0, 0.3])   # round the stack
s.stroke([(0.470, 0.668), (0.505, 0.684), (0.540, 0.699)], "round_hard", "foam",
         size=0.007, opacity=0.55, tip_wobble=0.5, pressure=[0.1, 1.0, 0.4, 0.1])
s.stroke([(0.612, 0.746), (0.640, 0.765), (0.662, 0.786)], "round_hard", "foam",
         size=0.009, opacity=0.5, tip_wobble=0.5, pressure=[0.3, 1.0, 0.2])
s.stroke([(0.742, 0.862), (0.762, 0.892), (0.776, 0.925)], "bristle", "foam",
         size=0.030, load=0.8, opacity=0.4, pressure="swell")
s.dry()
