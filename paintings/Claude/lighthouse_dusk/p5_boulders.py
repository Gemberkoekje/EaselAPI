# Pass 5: the near rocks, in front of the tower's base, so the tower stands in the
# headland rather than on it. One angular boulder mass with a clean edge, its top
# taking the sky's light, its right side the glow's; the dark where it meets the
# ridge; then the water's edge, where the sea breaks against the seaward face:
# three broken pale marks with a starved brush on the water side of the boundary,
# no two alike. (The first version put them on the rock, where they read as
# scribbles.)
p["foam"] = p.at_value(p.mix("sea_far", "titanium_white", 0.5), 0.66)
s.block_in(boulders(), "flat", "rock", size=0.03, density=1.0, solid=True,
           direction="axis", edge="clean", note="boulders")
s.stroke([(0.25, 0.63), (0.30, 0.622), (0.335, 0.636)], "flat", "rock_cool", size=0.016,
         opacity=1.0, load=1.0, load_falloff=0.0, pressure="even", note="boulder top")
s.stroke([(0.338, 0.645), (0.348, 0.675), (0.34, 0.70)], "flat", "rock_warm", size=0.013,
         opacity=1.0, load=1.0, load_falloff=0.0, pressure="lift_off", note="boulder, lit side")
s.stroke([(0.225, 0.70), (0.29, 0.718), (0.345, 0.712)], "round_hard", "rock_deep", size=0.011,
         opacity=0.85, pressure="swell", note="under the boulders")
s.stroke([(0.525, 0.715), (0.56, 0.765)], "round_hard", "foam", size=0.009, load=0.45,
         opacity=0.8, pressure="taper", note="water's edge")
s.stroke([(0.595, 0.835), (0.625, 0.89), (0.645, 0.94)], "round_hard", "foam", size=0.011,
         load=0.4, opacity=0.75, pressure="swell", note="water's edge, lower")
s.stroke([(0.655, 0.955), (0.71, 0.978)], "round_hard", "foam", size=0.008, load=0.4,
         opacity=0.7, pressure="lift_off", note="water's edge, the point")
print(s.look(values=True))
print(s.look())
