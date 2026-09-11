# compare() put the bloom a tenth below plan, and it is right for a reason that is not
# arithmetic: the foam on the brush had become the brightest thing in the picture and
# the eye went right, away from the light the picture is about. So the bloom gets a
# concentrated core -- and then the water is laid again over it, because the water is
# in front of the light and a scumble laid on top had put it behind.
core = blob((0.316, 0.448), 0.086, wobble=0.40, seed=29)
print("core scumble:", s.cost({"shape": core, "size": 0.05}))
s.scumble(core, "cyan_hi", "foam", 6)

s.stroke([(0.262, 0.512), (0.340, 0.404), (0.392, 0.398)], "bristle", "foam",
         size=0.030, load=0.70, opacity=0.70, pressure="swell")
s.stroke([(0.288, 0.462), (0.352, 0.436)], "round_hard", "foam_hi",
         size=0.0095, opacity=0.85, pressure=[0.25, 1.0, 0.3])

# the water, back in front of the light
s.stroke([(0.392, 0.352), (0.372, 0.626)], "bristle", "haze",
         size=0.042, opacity=0.38, load=0.65, pressure="taper")
s.stroke([(0.268, 0.352), (0.249, 0.598)], "bristle", "haze",
         size=0.034, opacity=0.30, load=0.55, pressure="lift_off")
print(s.look())
