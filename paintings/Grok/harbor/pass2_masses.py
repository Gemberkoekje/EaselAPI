# Pass 2: three big masses, biggest brush, ground still breathing.
s.block_in(sky_whole(), "bristle", "dusk_high", density=0.8, size=0.18, direction=8)
s.block_in(water_far(), "bristle", "water", density=0.8, size=0.18, direction=4)
s.block_in(water_near_shape(), "bristle", "water_near", density=0.8, size=0.16, direction=5)
s.look(values=True, path="pass2_values.png")
s.look(path="pass2_colour.png")
