# The picture never said the glass was a plane, or that the brush was touching it --
# the brush could have been three metres away. Where it presses, foam is smeared flat
# against the screen: nearer than everything else, so harder-edged and in focus while
# the mass behind it is not.
#
# First attempt was three elongated marks and made four bright horizontal streaks
# stacked down the leading edge with the throw above them. The contact has to differ in
# character from the throw, not just in position: the throw is a sweep, this is
# compressed, so it is short and broad where they are long and thin.
s.stroke([(0.686, 0.369), (0.733, 0.359)], "bristle", "foam",
         size=0.026, load=0.80, opacity=0.82, pressure="swell")
s.stroke([(0.681, 0.377), (0.739, 0.366)], "round_hard", "foam_hi",
         size=0.008, opacity=0.88, pressure=[0.35, 1.0, 0.25])
print(s.look())
