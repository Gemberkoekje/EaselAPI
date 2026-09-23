# The sea: one ramp from the far water (reflecting the sky) to the near water, masked at
# the horizon so the horizon is the one ruled line; then a warm film carrying the glow's
# reflection down toward the viewer (clipped to the water), which the broken pieces will
# sit on later.
s.scumble(sea, "sea_far", "sea_near", 9, direction=1, edge="hard", opacity=0.95,
          jitter=0.01, size_jitter=0.03)
s.dry()
under = s.sample(Region(0.10, 0.60, 0.30, 0.90))
p["film"] = p.at_value(p.mix(under, "glow", 0.4), p.value_of(under) + 0.07)
s.glaze([(0.19, 0.590), (0.21, 0.75), (0.25, 1.03)], "film", opacity=0.10, size=0.22,
        pressure=[0.9, 0.7, 0.45], clip=sea)
s.glaze([(0.19, 0.590), (0.205, 0.74), (0.235, 0.99)], "film", opacity=0.13, size=0.09,
        pressure=[1.0, 0.7, 0.3], clip=sea)
s.dry()
