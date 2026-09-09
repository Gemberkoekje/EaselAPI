# Stage 7 -- edges, then the few highlights. Nothing large from here.
p = s.palette
p["cart"]   = p.desaturate(p.mix("cadmium_red", "cadmium_yellow", 0.60), 0.30)
p["hi"]     = p.tint(p.mix("yellow_ochre", "cadmium_red", 0.15), 0.90)
p["skin_h"] = p.desaturate(p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.55), 0.58), 0.30)

s.dry()
# -- the carton, restated warm instead of pink ---------------------------------
s.block_in(Region(0.150, 0.780, 0.298, 1.0), "flat", "cart",
           density=1.0, size=0.065, direction="vertical", load=1.0, note="carton")
s.stroke([(0.224, 0.772), (0.272, 0.768)], "flat", p.tint("yellow_ochre", 0.82),
         size=0.034, pressure="even", load=1.0, note="carton top")
s.stroke([(0.152, 0.800), (0.158, 0.980)], "bristle", p.shade(p["cart"], 0.45),
         size=0.022, pressure="taper", load=0.9, note="carton shadow edge")

# -- edges: lost and found -----------------------------------------------------
s.smudge([(0.345, 0.400), (0.352, 0.560)], size=0.055)          # hand into background
s.smudge([(0.196, 0.396), (0.194, 0.560)], size=0.048)          # and its other side
s.smudge([(0.560, 0.300), (0.572, 0.400)], size=0.060)          # face into hair -- lost
s.smudge([(0.640, 0.230), (0.700, 0.300)], size=0.075)          # hair into the wall
s.smudge([(0.300, 0.640), (0.400, 0.690)], size=0.070)          # glove into the coat
s.smudge([(0.470, 0.600), (0.560, 0.640)], size=0.065)          # beard into the coat

# -- highlights: few, small, deliberate ----------------------------------------
s.stroke([(0.392, 0.300), (0.388, 0.330)], "round_hard", "hi",
         size=0.009, pressure="taper", load=1.0, note="forehead edge")
s.stroke([(0.388, 0.352), (0.386, 0.368)], "round_hard", "hi",
         size=0.008, pressure="taper", load=1.0, note="nose edge")
s.dab(0.425, 0.336, "round_hard", p.tint("titanium_white", 0.9), size=0.005, note="eye")
s.dab(0.418, 0.404, "round_hard", "hi", size=0.007, note="lip")
s.stroke([(0.208, 0.392), (0.214, 0.430)], "round_hard", "hi",
         size=0.008, pressure="taper", load=1.0, note="fingertip")
s.stroke([(0.330, 0.400), (0.336, 0.436)], "round_hard", "hi",
         size=0.007, pressure="taper", load=1.0, note="fingertip")
s.dab(0.246, 0.786, "round_hard", p.tint("titanium_white", 0.85), size=0.010, note="carton lid")
s.stroke([(0.606, 0.108), (0.648, 0.150)], "bristle",
         p.tint(p.mix("burnt_umber", "yellow_ochre", 0.6), 0.50),
         size=0.016, pressure="taper", load=0.5, note="hair catching light")

print("strokes:", s.stroke_count)
print(s.look())
