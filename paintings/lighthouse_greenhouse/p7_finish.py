# Pass 7: finishing. Lose one edge on purpose (the tower's shadow side into
# the fog near the top -- the haziest part of the picture, and a silhouette
# that is hard everywhere is the single most common way this goes wrong), a
# few quiet texture touches on the rock's plainer left side, a soft
# foreground mist in front of the waterline, and then the highlights last,
# smallest brush, fewest marks -- the lamp's brightest point, a glint where
# the beam grazes the water, one catch of light on a boulder.
s.smudge([(0.400, 0.34), (0.393, 0.24), (0.386, 0.155)], note="lose the tower's shadow edge into the mist")
s.stroke([(0.05, 0.79), (0.12, 0.775), (0.19, 0.795)], "bristle", "rock_mid", size=0.022,
         load=0.3, opacity=0.5, pressure="taper", note="texture, rock left")
s.stroke([(0.02, 0.835), (0.10, 0.85)], "bristle", "rock_warm", size=0.018, load=0.25,
         opacity=0.45, pressure="lift_off", note="texture, rock left, warmer")

# a soft mist at the waterline, in front of everything -- the nearest thing
# in the picture, and it is air
s.glaze([(-0.05, 0.735), (0.30, 0.715), (0.65, 0.745), (1.05, 0.72)], "mist",
        opacity=0.16, size=0.14, pressure="swell", note="mist at the waterline")
s.glaze([(0.55, 0.77), (0.85, 0.76), (1.05, 0.78)], "mist", opacity=0.14, size=0.10,
        pressure="swell", note="mist, lower, thinning right")

s.dab(0.444, 0.099, "round_hard", "titanium_white", size=0.006, press=2,
      note="brightest point, the lamp through the leaves")
s.stroke([(0.80, 0.565), (0.90, 0.578), (0.99, 0.588)], "round_hard", "beam", size=0.008,
         opacity=0.6, load=0.6, pressure="swell", note="glint, where the beam meets the water")
s.dab(0.475, 0.700, "round_hard", "rock_warm", size=0.007, press=2,
      note="catch of light, boulder top")
print(s.look(values=True))
print(s.look())
print(s.look(diff=True))
