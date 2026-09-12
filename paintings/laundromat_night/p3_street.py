# Pass 3, nearer than the building: the street it stands in.
s.dry()

# The road, graded: lighter up by the kerb where it is further off and catching more
# of the lamp, darker in the foreground under the viewer. A scumble, so it arrives
# graded for the six strokes a block-in would have cost anyway. The vertical streaks
# a wet road actually has are strokes of their own, two passes from now -- laying
# this mass vertically would step 24 passes across the canvas's whole width.
s.scumble(road(), p.at_value("asphalt", 0.275), p.at_value("asphalt", 0.185), 6,
          size=0.075, load=1.0, load_falloff=0.0, opacity=0.95, note="road")

# The sidewalk: damp concrete, lighter than the asphalt, and it keeps its own axis
# so the two planes do not both run with the canvas.
s.block_in(sidewalk(), "flat", p.at_value("kerb", 0.295), density=1.0, solid=True,
           size=0.028, direction="axis", note="sidewalk")

# The kerb face, where the two planes meet: broken, and brighter toward the lamp.
s.stroke([(0.32, 0.7855), (0.70, 0.7745), (1.06, 0.7605)], "bristle",
         p.at_value("kerb", 0.375), size=0.012, load=0.9, load_falloff=0.10,
         opacity=0.85, pressure=[0.25, 0.9, 1.0], note="kerb")
s.stroke([(-0.06, 0.7935), (0.16, 0.7885), (0.36, 0.7845)], "bristle",
         p.at_value("kerb", 0.315), size=0.010, load=0.55, opacity=0.6,
         pressure="swell", note="kerb")
print(s.budget_line())

# The road came back as wavy horizontal strata -- the scumble's own pass structure,
# and a stack of bands is a composition whether or not one was meant there. The
# reflection will break the middle two passes from now; these break the thirds that
# it will not reach. No two alike, none of them horizontal. Exercise 3's lesson
# applied: below about 0.6 of load this texture takes almost nothing.
s.stroke([(0.015, 1.04), (0.085, 0.895), (0.155, 0.800)], "bristle",
         p.at_value("kerb", 0.300), size=0.030, load=0.85, opacity=0.60,
         pressure="swell", note="road wet")
s.stroke([(0.995, 0.830), (0.915, 0.945), (0.865, 1.05)], "bristle",
         p.at_value("asphalt", 0.170), size=0.042, load=0.85, opacity=0.60,
         pressure=[0.2, 1.0, 0.5], note="road dry patch")
s.stroke([(0.705, 1.05), (0.675, 0.930), (0.690, 0.855)], "bristle",
         p.at_value("kerb", 0.285), size=0.022, load=0.80, opacity=0.55,
         pressure="taper", note="road wet")

# The sidewalk is one flat band, so it gets a crack across it and a damp patch.
s.stroke([(0.238, 0.708), (0.292, 0.748), (0.326, 0.793)], "round_hard",
         p.at_value("asphalt", 0.205), size=0.006, load=0.9, opacity=0.75,
         jitter=0.04, pressure=[0.3, 1.0, 0.45], note="sidewalk crack")
s.stroke([(0.795, 0.735), (0.868, 0.748), (0.905, 0.742)], "bristle",
         p.at_value("kerb", 0.255), size=0.026, load=0.80, opacity=0.55,
         pressure="swell", note="sidewalk damp")
print(s.budget_line())
