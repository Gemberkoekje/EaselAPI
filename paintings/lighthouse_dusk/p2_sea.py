# Pass 2: the sea, over the bottom of the sky. First one straight glow stroke to
# take the wander out of the afterglow's lower edge, then two soft passages rather
# than one, so the rows of swell are fine near the horizon and broad near the
# frame; then one straight stroke along the horizon, because a horizon is the one
# edge in a seascape that may not wander; then the afterglow's reflection as a
# few tapered marks that get shorter, sparser and dimmer coming forward, and two
# dark ripples across them so they lie in the water rather than on it. The first
# version laid the reflection with a starved bristle and it came back as a row of
# dotted rectangles; the second laid six alike and they read as stripes.
s.stroke([(0.40, 0.566), (1.06, 0.566)], "flat", p.mix("glow", "glow_core", 0.4), size=0.022,
         opacity=0.7, load=1.0, load_falloff=0.0, jitter=0.0, size_jitter=0.0,
         pressure=[0.0, 0.6, 1.0], note="glow at the horizon, straight")
mid = p.mix("sea_far", "sea_near", 0.45)
s.scumble(Region(-0.04, 0.573, 1.04, 0.73), "sea_far", mid, 6, brush="flat", size=0.07,
          opacity=0.85, load=1.0, load_falloff=0.0, note="far sea")
s.scumble(Region(-0.04, 0.70, 1.04, 1.05), mid, "sea_near", 6, brush="flat", size=0.13,
          opacity=0.85, load=1.0, load_falloff=0.0, note="near sea")
s.stroke([(-0.05, 0.588), (1.05, 0.588)], "flat", "sea_far", size=0.026, opacity=0.9,
         load=1.0, load_falloff=0.0, jitter=0.0, size_jitter=0.0, pressure="even",
         note="the horizon, straight")
dim = p.mix("sea_lit", "sea_far", 0.45)
marks = [  # (x0, x1, y, size, colour, opacity): tapered, no two alike
    (0.50, 1.06, 0.600, 0.022, "sea_lit", 0.75),
    (0.63, 0.97, 0.616, 0.013, "sea_lit", 0.65),
    (0.71, 0.88, 0.636, 0.011, dim, 0.7),
    (0.67, 0.80, 0.664, 0.010, dim, 0.6),
    (0.77, 0.93, 0.700, 0.010, dim, 0.5),
]
for x0, x1, y, size, colour, op in marks:
    s.stroke([(x0, y), ((x0 + x1) / 2, y + 0.002), (x1, y - 0.001)], "round_hard", colour,
             size=size, opacity=op, load=1.0, load_falloff=0.1, pressure="swell",
             note="reflection")
s.stroke([(0.58, 0.626), (0.74, 0.623), (0.90, 0.627)], "round_hard", mid, size=0.008,
         opacity=0.7, pressure="swell", note="ripple across the reflection")
s.stroke([(0.66, 0.652), (0.80, 0.650)], "round_hard", "sea_near", size=0.007,
         opacity=0.6, pressure="swell", note="ripple, lower")
print(s.look(values=True))
print(s.look())
