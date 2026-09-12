# Pass 8: the surroundings again. The near water gets a few quiet ripples of
# different lengths at slightly different angles so the swell stops being rows;
# one dark ripple crosses the widest reflection bar and two small glints sit
# between the bars, so the reflection is water with light on it rather than
# stripes. The lower sky gets two soft cloud streaks across the glow, tapered at
# both ends, one long and one short, which is what a sunset has and what breaks
# the passage's lobes without adding a band. The first version of this pass laid
# the ripples a step too dark and the clouds as three hard lines, and both read
# as drawn on the picture rather than in it.
p["sea_deep"] = p.at_value("sea_near", 0.32)
p["cloud"] = p.at_value(p.mix("sky_mid", "sky_top", 0.5), 0.50)
ripples = [  # (points, size, colour, opacity)
    ([(0.42, 0.665), (0.55, 0.662)],                    0.005, "sea_far",  0.45),
    ([(0.36, 0.705), (0.47, 0.708), (0.58, 0.703)],     0.006, "sea_deep", 0.45),
    ([(0.66, 0.80), (0.80, 0.797), (0.94, 0.803)],      0.007, "sea_deep", 0.45),
    ([(0.70, 0.90), (0.86, 0.897), (1.02, 0.905)],      0.009, "sea_deep", 0.5),
    ([(0.86, 0.755), (1.03, 0.75)],                     0.006, "sea_deep", 0.4),
]
for pts, size, colour, op in ripples:
    s.stroke(pts, "round_hard", colour, size=size, opacity=op, pressure="swell", note="ripple")
s.stroke([(0.60, 0.604), (0.78, 0.606), (1.0, 0.603)], "round_hard", p.mix("sea_far", "sea_near", 0.45),
         size=0.005, opacity=0.7, pressure="swell", note="ripple across the bar")
s.dab(0.805, 0.643, "round_hard", "sea_lit", size=0.010, press=2, tip_wobble=0.4, note="glint")
s.stroke([(0.845, 0.667), (0.875, 0.668)], "round_hard", "sea_lit", size=0.007, opacity=0.8,
         pressure="swell", note="glint, lower")
clouds = [
    ([(0.44, 0.468), (0.70, 0.462), (0.99, 0.470)], 0.018, [0.0, 1.0, 0.7, 0.0]),
    ([(0.58, 0.508), (0.78, 0.503), (0.93, 0.507)], 0.013, [0.0, 0.9, 0.0]),
]
for pts, size, pr in clouds:
    s.stroke(pts, "round_soft", "cloud", size=size, opacity=0.45, load=1.0, load_falloff=0.0,
             pressure=pr, note="cloud streak")
print(s.look(values=True))
print(s.look())
