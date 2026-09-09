# Stage 6 -- corrections read off the shared grid, not guessed.
# Reference vs canvas, cell by cell:
#   A1-C2  reference is dark; mine is bright orange       -> knock it down hard
#   G1-H2  reference is the lightest wall in the picture   -> keep it, warm it
#   D3-D5  the face runs three rows; mine stops at D4      -> push it down
#   B4-C6  the hand runs to row 6; mine stops at row 5     -> extend it
#   B4     the beret is the darkest note left of the head  -> restate it
p = s.palette
p["bg_dark"] = p.tint(p.mix("burnt_umber", "ultramarine", 0.30), 0.06)
p["bg_lit"]  = p.desaturate(p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.30), 0.52), 0.20)
p["skin"]    = p.desaturate(p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.40), 0.74), 0.25)
p["skin_h"]  = p.desaturate(p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.55), 0.58), 0.30)
p["beard2"]  = p.tint(p.mix("burnt_umber", "ultramarine", 0.20), 0.14)
p["hairm"]   = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.40), 0.22)

s.dry()

# -- A1-C2: the dark upper left. Knock it down, crossing the earlier marks. -----
s.block_in(Region(0.0, 0.0, 0.375, 0.30), "bristle", "bg_dark",
           density=0.85, size=0.13, direction="diagonal", load=0.9, note="dark upper left")
s.block_in(Region(0.0, 0.24, 0.24, 0.62), "bristle", "bg_dark",
           density=0.7, size=0.12, direction="horizontal", load=0.8, note="dark left")

# -- G1-H2: let the light wall stay the lightest thing behind him ---------------
s.block_in(Region(0.735, 0.0, 1.0, 0.30), "bristle", "bg_lit",
           density=0.6, size=0.14, direction="diagonal", load=0.75, note="lit wall")

# -- B4: the beret ---------------------------------------------------------------
s.dry()
for x0, y0, x1, y1 in [(0.152, 0.372, 0.300, 0.352), (0.160, 0.408, 0.308, 0.398),
                       (0.180, 0.442, 0.312, 0.440), (0.205, 0.470, 0.310, 0.472)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 - 0.010), (x1, y1)],
             "bristle", "beard2", size=0.052, pressure="taper", load=0.95, note="beret")

# -- the face: down half a cell, and running the full three rows ---------------
s.dry()
face = [(0.404, 0.292, 0.108), (0.397, 0.318, 0.126), (0.392, 0.342, 0.140),
        (0.390, 0.366, 0.148), (0.394, 0.390, 0.146), (0.402, 0.412, 0.138)]
for lx, y, w in face:
    s.stroke([(lx, y), (lx + w * 0.55, y + 0.005), (lx + w, y - 0.004)],
             "bristle", "skin", size=0.038, pressure="lift_off", load=1.0, note="face")
for x0, y0, x1, y1 in [(0.480, 0.308, 0.552, 0.330), (0.492, 0.348, 0.562, 0.372),
                       (0.486, 0.392, 0.552, 0.412)]:
    s.stroke([(x0, y0), (x1, y1)], "bristle", "skin_h", size=0.036,
             pressure="taper", load=1.0, note="shadow side")
s.stroke([(0.398, 0.348), (0.392, 0.372), (0.404, 0.390)], "bristle", "skin_h",
         size=0.018, pressure="even", load=1.0, note="nose")
s.stroke([(0.402, 0.322), (0.446, 0.316), (0.478, 0.322)], "bristle",
         p.tint(p.mix("burnt_sienna", "burnt_umber", 0.4), 0.34),
         size=0.019, pressure="swell", load=1.0, note="brow")
s.dab(0.428, 0.338, "round_hard", p.tint("burnt_umber", 0.04), size=0.0085, note="eye")

# -- the beard: D4 to E5, big and connected to the coat -------------------------
for x0, y0, x1, y1 in [(0.406, 0.432, 0.508, 0.470), (0.410, 0.462, 0.536, 0.508),
                       (0.424, 0.500, 0.552, 0.546), (0.452, 0.538, 0.556, 0.578),
                       (0.486, 0.572, 0.560, 0.598)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2 - 0.008, (y0 + y1) / 2 + 0.010), (x1, y1)],
             "bristle", "beard2", size=0.044, pressure="taper", load=0.95, note="beard")
s.stroke([(0.410, 0.444), (0.444, 0.450)], "bristle", p.tint("burnt_umber", 0.02),
         size=0.012, pressure="taper", load=1.0, note="mouth")

# -- the hand: down to row 6 ----------------------------------------------------
s.dry()
s.block_in(Region(0.196, 0.382, 0.342, 0.600), "bristle", "skin",
           density=0.9, size=0.046, direction="vertical", load=1.0, note="hand")
for x, ytop in [(0.243, 0.390), (0.298, 0.400)]:
    s.stroke([(x, ytop + 0.02), (x + 0.002, 0.545)], "bristle", "skin_h",
             size=0.013, pressure="taper", load=0.7, note="finger gap")
s.stroke([(0.200, 0.600), (0.272, 0.618), (0.344, 0.598)], "bristle", "skin_h",
         size=0.040, pressure="swell", load=1.0, note="palm")
# the glove, dark, under the hand
for x0, y0, x1, y1 in [(0.196, 0.652, 0.360, 0.678), (0.204, 0.706, 0.372, 0.728),
                       (0.222, 0.756, 0.386, 0.778)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2), (x1, y1)],
             "bristle", "beard2", size=0.062, pressure="taper", load=0.95, note="glove")

print("strokes:", s.stroke_count)
print(s.look())
