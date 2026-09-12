# Pass 7: the rock again, named as the weakest passage. The seaward face was a
# staircase of slabs: two cracks cut across the strata and two starved bristle
# strokes run down the slope over them. The mid plane's lower edge was a ruled
# line: one smudge along it (a straight boundary is two points) and one dry
# stroke across it lose it. The top strip gets two notches so it is a ridge and
# not a ribbon, and a second, smaller boulder goes in beside the first so the
# near rocks are two of a kind rather than one lump -- lit from the other side.
s.stroke([(0.545, 0.75), (0.575, 0.80), (0.59, 0.86)], "round_hard", "rock_deep", size=0.010,
         opacity=0.9, pressure="taper", note="crack across the strata")
s.stroke([(0.505, 0.71), (0.535, 0.735)], "round_hard", "rock_deep", size=0.008,
         opacity=0.85, pressure="lift_off", note="crack, upper")
s.stroke([(0.49, 0.69), (0.55, 0.78), (0.61, 0.90)], "bristle", "rock_mid2", size=0.028,
         load=0.45, opacity=0.6, pressure="taper", note="down the face, dry")
s.stroke([(0.52, 0.73), (0.585, 0.83), (0.625, 0.94)], "bristle", "rock_warm", size=0.022,
         load=0.35, opacity=0.5, pressure="taper", note="down the face, dry, warm")
s.smudge([(-0.02, 0.705), (0.46, 0.785)], size=0.05, note="lose the mid plane's edge")
s.stroke([(0.08, 0.77), (0.24, 0.735), (0.38, 0.775)], "bristle", "rock", size=0.035,
         load=0.4, opacity=0.6, pressure="taper", note="across the join, dry")
s.stroke([(0.095, 0.567), (0.105, 0.60)], "round_hard", "rock_deep", size=0.008,
         opacity=0.85, pressure="lift_off", note="notch in the ridge")
s.stroke([(0.36, 0.612), (0.375, 0.645)], "round_hard", "rock_deep", size=0.007,
         opacity=0.85, pressure="lift_off", note="notch in the ridge, right")
small = blob((0.19, 0.645), 0.032, wobble=0.4, points=8, seed=3, aspect=s.aspect)
s.block_in(small, "flat", "rock", size=0.014, density=1.0, solid=True, direction="axis",
           edge="clean", note="second boulder")
s.stroke([(0.168, 0.632), (0.195, 0.625), (0.212, 0.634)], "flat", "rock_cool", size=0.009,
         opacity=1.0, load=1.0, load_falloff=0.0, pressure="even", note="second boulder, top")
print(s.look(values=True))
print(s.look())
