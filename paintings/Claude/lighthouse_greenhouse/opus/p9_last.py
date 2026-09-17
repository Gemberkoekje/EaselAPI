# The last marks, and they go where the picture would have had to apologise: the
# shaft, which is a lot of quiet green-grey with three iron arcs across it, and
# the near dark under it. Both get what the picture is actually about rather than
# more finish.
s.dry()

# A creeper that has gone up the outside on its own. It crosses two turns of the
# stair, because a plant does, and stopping politely at each one is what would
# have given it away. Two strokes, different widths and values, neither straight.
s.stroke([(0.1495, 0.742), (0.1560, 0.660), (0.1600, 0.586), (0.1665, 0.508)],
         "bristle", "leaf_dark", size=0.026, load=0.62, opacity=0.9,
         pressure=[1.0, 0.85, 0.55, 0.0], note="subject tower")
s.stroke([(0.1720, 0.706), (0.1810, 0.632), (0.1760, 0.560)], "bristle",
         p.at_value("leaf_mid", 0.285), size=0.016, load=0.6, opacity=0.75,
         pressure="swell", note="subject tower")
s.stroke([(0.1660, 0.664), (0.1950, 0.650), (0.2180, 0.668)], "bristle",
         p.mix("leaf_dark", "tower_mid", 0.30), size=0.010, load=0.45,
         opacity=0.65, pressure=[0.9, 0.6, 0.0], note="subject tower")
s.stroke([(0.1580, 0.598), (0.1750, 0.590)], "bristle", "leaf_lit", size=0.011,
         load=0.8, opacity=0.85, pressure=[0.25, 1.0, 0.15], note="subject tower")

# One window, because the thing is a building and nothing so far has said so.
# Three marks and no more, dark first: the opening, the light along its head, and
# what somebody has put on the sill.
s.stroke([(0.2385, 0.398), (0.2385, 0.428)], "flat", p.at_value("iron", 0.185),
         size=0.019, opacity=1.0, load=1.0, load_falloff=0.0, pressure="even",
         note="subject tower")
s.stroke([(0.2295, 0.3925), (0.2495, 0.3915)], "liner",
         p.at_value("tower_lit", 0.615), size=0.004, opacity=0.9,
         pressure=[0.3, 1.0, 0.4], note="subject tower")
s.stroke([(0.2320, 0.4175), (0.2440, 0.4135)], "bristle", "leaf_mid",
         size=0.009, load=0.7, opacity=0.9, pressure="swell",
         note="subject tower")

# And a clump that has seeded itself in the rock at the foot, so the conversion
# is not confined to the parts somebody is looking after.
s.stroke([(0.412, 0.858), (0.428, 0.840), (0.446, 0.850)], "bristle",
         p.at_value("leaf_dark", 0.235), size=0.014, load=0.7, opacity=0.85,
         pressure="swell", note="rock")
s.stroke([(0.421, 0.845), (0.434, 0.832)], "bristle",
         p.at_value("leaf_mid", 0.315), size=0.007, load=0.8, opacity=0.8,
         pressure=[1.0, 0.2], note="rock")

s.dry()

# The rock's top edge is found the whole way across. One stretch of it goes:
# better one edge lost completely than four half lost.
s.smudge([(0.192, 0.816), (0.244, 0.830), (0.296, 0.842)])
s.stroke([(0.214, 0.806), (0.258, 0.818), (0.296, 0.830)], "bristle",
         p.mix("rock_lit", "sea_near", 0.5), size=0.022, load=0.35, opacity=0.45,
         pressure="swell", note="edges")

# Three last passes on the near dark, at three angles and three values, because
# it is still the flattest passage in the picture.
for path, v, size, load, op in (
        ([(0.48, 0.906), (0.66, 0.962), (0.78, 1.030)], 0.290, 0.016, 0.30, 0.6),
        ([(-0.04, 1.000), (0.22, 1.034), (0.44, 1.008)], 0.180, 0.026, 0.35, 0.6),
        ([(0.70, 0.976), (0.90, 1.012)], 0.325, 0.012, 0.40, 0.7)):
    s.stroke(path, "bristle", p.at_value("rock", v), size=size, load=load,
             opacity=op, pressure="lift_off", note="rock")

print(s.look())
print(s.look(values=True))
print(s.look(region="B3:D7"))
