# The sea, still behind everything. In this much fog the water at the horizon is
# nearly the fog's own value and only darkens as it comes toward us, so it is two
# graded passages and no block-in at all -- the ground flecking through them is
# most of what keeps a wide quiet passage from being a slab.
s.scumble(Region(-0.05, 0.592, 1.05, 0.780), p.at_value("sea_far", 0.635),
          p.at_value("sea_far", 0.500), 7, note="sea far")
s.scumble(Region(-0.05, 0.760, 1.05, 1.06), p.at_value("sea_far", 0.500),
          "sea_near", 5, note="sea near")

s.dry()

# The one ruled line in the picture, and it is only half a line: it starts at
# nothing out in the fog and is only found where the water is nearer. Its ends
# run off the canvas so it has no visible termination.
s.stroke([(0.30, 0.5975), (0.70, 0.5985), (1.06, 0.5975)], "flat",
         p.at_value("sea_far", 0.505), size=0.011, opacity=0.85, load=1.0,
         load_falloff=0.0, jitter=0.0, size_jitter=0.0,
         pressure=[0.0, 0.55, 0.85], note="horizon")

# Three marks on the water, no two the same: a long broken light, a shorter one
# that stops, and one dark ripple. All three moved up off the rock's edge, which
# the first rehearsal showed was about to bury two of them.
s.stroke([(0.44, 0.792), (0.72, 0.783), (1.06, 0.796)], "bristle",
         p.at_value("sea_near", 0.575), size=0.026, load=0.50, opacity=0.8,
         pressure="swell", note="water")
s.stroke([(0.62, 0.712), (0.86, 0.706)], "bristle",
         p.at_value("sea_far", 0.585), size=0.016, load=0.35, opacity=0.6,
         pressure="lift_off", note="water")
s.stroke([(0.66, 0.862), (0.90, 0.876), (1.06, 0.868)], "bristle",
         p.at_value("sea_near", 0.315), size=0.019, load=0.65, opacity=0.85,
         pressure=[0.8, 1.0, 0.2], note="water")

print(s.look(grid=True))
print(s.look(values=True))
