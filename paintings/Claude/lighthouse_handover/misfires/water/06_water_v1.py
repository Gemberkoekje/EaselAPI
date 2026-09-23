# The water pass exactly as rehearsed at rehearse_011 (later replaced).
import random
rng = random.Random(5)
p["glint"] = p.at_value(p.mix("core", "glow", 0.4), 0.74)
s.dry()
cx = lambda y: 0.19 + (y - 0.59) * 0.12            # the film's own centre line
y, gap, spread, op, sz = 0.596, 0.013, 0.010, 0.85, 0.0075
while y < 0.97:
    x, n = cx(y) + rng.gauss(0, spread), rng.uniform(0.016, 0.048)
    s.stroke([(x - n / 2, y + 0.002), (x, y - 0.002), (x + n / 2, y + 0.001)],
             "round_hard", "glint", size=sz, opacity=op, tip_wobble=0.6,
             pressure=[0.05, 1.0, 0.4])
    y, gap, spread, op, sz = y + gap, gap * 1.22, spread * 1.25, op * 0.86, sz * 1.06
s.stroke([(0.15, 0.662), (0.215, 0.659), (0.26, 0.664)], "round_hard", "sea_near",
         size=0.006, opacity=0.75, pressure=[0.2, 1.0, 0.3])
s.stroke([(0.17, 0.842), (0.25, 0.836), (0.31, 0.845)], "round_hard", "sea_near",
         size=0.007, opacity=0.75, pressure=[0.3, 1.0, 0.2])

# surf: pale sky-grey where the water breaks on the rock, warmer toward the tip
p["foam"] = p.at_value(p.mix("pale", "sea_far", 0.3), 0.57)
p["foam_warm"] = p.at_value(p.mix("foam", "glow", 0.3), 0.62)
s.stroke([(0.385, 0.640), (0.400, 0.645), (0.418, 0.643)], "bristle", "foam_warm",
         size=0.030, load=0.55, opacity=0.6, pressure="swell")           # at the tip
s.stroke([(0.340, 0.646), (0.358, 0.648), (0.372, 0.644)], "round_hard", "foam_warm",
         size=0.008, opacity=0.7, tip_wobble=0.7, pressure=[0.2, 1.0, 0.3])   # round the stack
s.stroke([(0.505, 0.683), (0.535, 0.695), (0.560, 0.707)], "bristle", "foam",
         size=0.024, load=0.45, opacity=0.55, pressure="swell")
s.stroke([(0.622, 0.748), (0.655, 0.770), (0.672, 0.787)], "bristle", "foam",
         size=0.034, load=0.5, opacity=0.5, pressure="taper")
s.dab(0.735, 0.858, "round_hard", "foam", size=0.014, press=3, tip_wobble=0.7)
s.stroke([(0.775, 0.905), (0.792, 0.935), (0.808, 0.975)], "bristle", "foam",
         size=0.040, load=0.45, opacity=0.45, pressure="swell")
s.dry()
