"""Pass F-I - clear the speckle beside the handle, then the things that make
this a particular mug: the tea, the crewmate, the spoon, the teabag tag."""
p = s.palette
s.dry()

# the old handle-shadow pass left a speckled comb; table back over it
s.block_in(ellipse(Region(0.598, 0.408, 0.790, 0.668)), "flat", "table_lit",
           direction=(-74,), density=1.0, size=0.075, load=1.0)
s.block_in(ellipse(Region(0.612, 0.492, 0.716, 0.586), rotate=-14), "flat",
           p.mix(p["shad_pen"], p["table_lit"], 0.42), direction=(-16,),
           density=1.0, size=0.034, load=1.0)
print("right table:", s.stroke_count)

# the tea: an ellipse, not a serrated polygon
tea_shape = ellipse(Region(0.334, 0.136, 0.596, 0.318), rotate=-3)
s.block_in(tea_shape.inset(0.030), "flat", "tea", direction=(-3,),
           density=1.0, size=0.060, load=1.0)
print("tea:", s.stroke_count)

# the crewmate printed on the mug
p["crew"] = "#191210"
p["crew_warm"] = "#2a1c14"
p["visor"] = p.desaturate(p.mix(p.mix("alizarin", "cerulean", 0.6),
                                "titanium_white", 0.65), 0.5)
crew = polygon([(0.372, 0.428), (0.398, 0.407), (0.462, 0.400), (0.500, 0.412),
                (0.511, 0.448), (0.511, 0.487), (0.556, 0.490), (0.556, 0.588),
                (0.512, 0.592), (0.510, 0.640), (0.500, 0.670), (0.470, 0.672),
                (0.462, 0.628), (0.440, 0.628), (0.434, 0.674), (0.398, 0.674),
                (0.378, 0.648), (0.366, 0.560), (0.362, 0.482)])
s.block_in(crew.inset(0.022), "flat", "crew", direction=("axis", 66),
           density=1.0, size=0.044, load=1.0)
print("crew:", s.stroke_count)
# the warmer lit half of him, wet into the dark so it does not sit on top
s.stroke([(0.392, 0.560), (0.404, 0.630)], "bristle", "crew_warm", size=0.040,
         opacity=0.5, load=1.0, note="crew light")
s.stroke([(0.478, 0.470), (0.492, 0.560)], "bristle", "crew_warm", size=0.034,
         opacity=0.45, load=1.0, note="crew light")
# the gap between his legs, cut with the mug's own colour from behind
s.stroke([(0.451, 0.634), (0.452, 0.672)], "flat", "mug_face", size=0.014,
         pressure="even", load=1.0, note="leg gap")
# the visor
s.stroke([(0.378, 0.478), (0.428, 0.466)], "round_hard", "visor", size=0.030,
         pressure="even", load=1.0, note="visor")
print("crew done:", s.stroke_count)

# the spoon, standing in the tea
p["steel_d"] = "#0b0b0e"
p["steel_l"] = p.desaturate(p.mix(p.mix("ultramarine", "burnt_sienna", 0.35),
                                  "titanium_white", 0.72), 0.4)
s.stroke([(0.507, -0.01), (0.513, 0.095), (0.521, 0.185)], "flat", "steel_d",
         size=0.026, pressure="even", load=1.0, note="spoon handle")
s.stroke([(0.524, 0.196), (0.536, 0.245), (0.556, 0.288)], "flat", "steel_l",
         size=0.024, pressure="even", load=1.0, note="spoon bowl")
s.dab(0.529, 0.222, "round_hard", "mug_hi", size=0.012, press=3)
print("spoon:", s.stroke_count)

# the teabag tag out on the table, and its thread
p["tag"] = "#232230"
tag = polygon([(0.816, 0.560), (0.836, 0.536), (0.878, 0.545), (0.890, 0.578),
               (0.884, 0.628), (0.848, 0.648), (0.818, 0.630), (0.810, 0.592)])
s.block_in(tag.inset(0.014), "flat", "tag", direction="axis", density=1.0,
           size=0.028, load=1.0)
s.stroke([(0.632, 0.290), (0.672, 0.352), (0.720, 0.452), (0.775, 0.530),
          (0.812, 0.570)], "liner", "mug_rim", size=0.0035, opacity=0.5,
         note="thread")
s.stroke([(0.812, 0.610), (0.760, 0.660), (0.700, 0.700), (0.640, 0.712)],
         "liner", p["shad_pen"], size=0.003, opacity=0.4, note="thread 2")
print("strokes:", s.stroke_count)
print(s.look())
