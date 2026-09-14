s.dry()
# The sparkle by the near lamp had stacked up over three passes into the densest
# texture in the picture -- static, next to the thing it was meant to sit beside.
# Two films take it back without removing it.
s.glaze([(0.190, 0.690), (0.270, 0.732), (0.352, 0.774)], p.at_value("water", 0.60),
        opacity=0.38, size=0.085, pressure="swell", note="subject")
s.glaze([(0.300, 0.930), (0.420, 0.958), (0.520, 0.968)], p.at_value("water", 0.56),
        opacity=0.30, size=0.075, pressure="taper", note="subject")
print(s.look(region="B5:E8"))
