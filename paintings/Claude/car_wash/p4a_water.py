# Water sheeting down the glass. One value, `haze`, does two jobs: over the dark
# tunnel it lightens, over the bloom it darkens -- which is what a film of water does.
# Clustered to the left and absent from a whole passage on the right, because a grain
# that repeats evenly across a field is a stack of bands with another name.
W = dict(brush="bristle", color="haze")
s.stroke([(0.168, 0.295), (0.145, 0.660), (0.163, 0.900)], size=0.055,
         opacity=0.40, load=0.75, pressure="taper", **W)
s.stroke([(0.223, 0.462), (0.205, 0.825)], size=0.034,
         opacity=0.32, load=0.55, pressure="lift_off", **W)
s.stroke([(0.268, 0.238), (0.247, 0.552)], size=0.070,
         opacity=0.26, load=0.85, pressure="swell", **W)
s.stroke([(0.392, 0.378), (0.371, 0.882)], size=0.045,
         opacity=0.35, load=0.65, pressure="taper", **W)
s.stroke([(0.556, 0.548), (0.545, 0.842)], size=0.027,
         opacity=0.30, load=0.45, pressure="press_in", **W)
s.stroke([(0.638, 0.202), (0.621, 0.438)], size=0.021,
         opacity=0.36, load=0.60, pressure="taper", **W)
print(s.look())
