# Pass 2: the three big separations, still thin enough for the ground to breathe.
s.block_in(sky_upper(), "bristle", "sky_high", density=0.80, size=0.18, direction=7)
s.block_in(sky_low(), "bristle", "sky_mid", density=0.78, size=0.16, direction=5)
s.block_in(sea_far(), "bristle", "sea", density=0.80, size=0.17, direction=3)
s.block_in(sea_near(), "bristle", "sea_deep", density=0.78, size=0.15, direction=6)
s.look(values=True, path="pass2_values.png")
s.look(path="pass2_colour.png")
