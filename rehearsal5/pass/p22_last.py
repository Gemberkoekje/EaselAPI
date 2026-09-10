REF = "C:/temp/Level1.jpg"

# the band under the lip was a slab of light; knock it back a step
s.stroke([(0.356, 0.352), (0.440, 0.378), (0.520, 0.374), (0.566, 0.356)],
         "flat", "mug_lit", size=0.052, pressure="even", load=1.0,
         note="knock the band back")
# and restate the lip itself as one thin line
s.stroke([(0.366, 0.310), (0.424, 0.338), (0.482, 0.345), (0.542, 0.332)],
         "liner", "mug_spec", size=0.007, pressure="swell", load=1.0,
         note="the lip")
print("lip", s.stroke_count)

# sharpen the crewmate by painting the wall on the other side of its edge
s.stroke([(0.344, 0.428), (0.350, 0.592)], "flat", "mug_mid", size=0.032,
         pressure="even", load=1.0, note="cut the left edge")
s.stroke([(0.376, 0.392), (0.440, 0.388), (0.498, 0.394)], "flat", "mug_lit",
         size=0.022, pressure="even", load=1.0, note="cut the top edge")
s.stroke([(0.573, 0.452), (0.575, 0.546)], "flat", "mug_dark", size=0.026,
         pressure="even", load=1.0, note="cut the pack edge")
print("figure", s.stroke_count)

# the opening still shows a pale ring on the right and along the front
s.stroke([(0.578, 0.212), (0.596, 0.252), (0.588, 0.292)], "flat", "tea",
         size=0.030, pressure="even", load=1.0, note="opening right")
s.stroke([(0.370, 0.292), (0.420, 0.312), (0.470, 0.320)], "flat", "tea",
         size=0.024, pressure="even", load=1.0, note="opening front")
print("tea", s.stroke_count)

# the mug sits into its shadow
s.stroke([(0.398, 0.684), (0.470, 0.698), (0.528, 0.684)], "round_hard",
         "shad_pool", size=0.032, pressure="swell", load=1.0, note="under the base")

# the tag is a tag, not a lobe
s.stroke([(0.820, 0.578), (0.904, 0.596)], "flat", "tag", size=0.052,
         pressure="even", load=1.0, note="tag")

# join the two dark bars on the far table into one falling-away field
s.stroke([(0.758, 0.174), (0.876, 0.152)], "bristle", "wood_far", size=0.055,
         pressure="even", load=1.0, load_falloff=0.0, note="far table")
print("last", s.stroke_count)

print(s.look(reference=REF))
print(s.look(reference=REF, values=True))
print(s.look())
print(s.compare(REF))
