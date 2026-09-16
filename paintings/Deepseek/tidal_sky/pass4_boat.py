# Pass 4: the boat -- the one dark thing standing in the light -- and its reflection.
# The near mass goes on top; the catch-light finishes it.
s.block_in(boat_shape(), "flat", "boat_dark", size=0.015, solid=True,
           direction="axis", edge="hard")
s.look(region=span("E5", "G5"), path="pass4_boat_region.png")

# its reflection: broken, fading down
s.stroke([(0.525, 0.610), (0.64, 0.605), (0.745, 0.585)], "bristle", "boat_dark",
         size=0.018, load=0.6, opacity=0.55, pressure="swell")
s.stroke([(0.545, 0.635), (0.655, 0.628)], "bristle", "boat_dark",
         size=0.013, load=0.55, opacity=0.45, pressure="swell")
s.stroke([(0.585, 0.662), (0.675, 0.654)], "bristle", "boat_dark",
         size=0.010, load=0.5, opacity=0.35, pressure="swell")

# the one broken catch-light along the near edge -- the mark that makes it a boat
s.stroke([(0.535, 0.576), (0.63, 0.568), (0.735, 0.558)], "round_hard", "gold",
         size=0.0085, opacity=0.95, load=1.0, load_falloff=0.0,
         pressure=[0.05, 0.55, 1.0, 0.45])
s.look(region=span("E5", "G5"), path="pass4_boat_after.png")
s.look(values=True, path="pass4_values.png")
