# Nothing in this picture was moving: the brush stood beside the glass rather than
# acting on it. Six small marks were tried here first and vanished at picture scale --
# being careful, not being quiet. Four bigger ones instead, thrown up into the arch
# where there is already activity rather than across the quiet passage lower down.
s.stroke([(0.728, 0.212), (0.648, 0.168), (0.572, 0.152)], "bristle", "foam",
         size=0.030, load=0.50, opacity=0.72, pressure="lift_off")
s.stroke([(0.734, 0.352), (0.672, 0.330)], "bristle", "foam",
         size=0.020, load=0.42, opacity=0.60, pressure="taper")
s.stroke([(0.716, 0.252), (0.628, 0.208)], "liner", "foam_hi",
         size=0.0045, pressure=[1.0, 0.12])
s.stroke([(0.556, 0.146), (0.528, 0.140)], "liner", "foam",
         size=0.0035, opacity=0.65, pressure="lift_off")
print(s.look())
