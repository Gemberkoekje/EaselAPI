# The headland: the whole mass dark and masked to its silhouette, the planes that tile it
# (each along a side of its own, clipped to the mass), two small rocks off the tip, and
# broken warm light scraped down the west slope.
headland_mass()
headland_planes()
s.block_in(stack_a, "flat", "land", size=0.010, solid=True, edge="hard", direction=15)
s.block_in(stack_b, "flat", "cliff", size=0.008, solid=True, edge="hard", direction=-20)
s.stroke([(0.462, 0.598), (0.472, 0.612), (0.478, 0.628)], "bristle", "lit",
         size=0.026, load=0.4, opacity=0.5, pressure="swell", clip=headland)   # scrape down the slope
s.stroke([(0.545, 0.567), (0.556, 0.585), (0.561, 0.600)], "bristle", "lit",
         size=0.020, load=0.35, opacity=0.45, pressure="taper", clip=headland)
