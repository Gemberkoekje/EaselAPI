# Stage 2 -- the masses that are still missing, and the face made into a head.
p = s.palette
p["beard"]    = p.tint(p.mix("burnt_umber", "burnt_sienna", 0.35), 0.10)   # ~0.28
p["fl_shade"] = p.tint(p.mix("burnt_sienna", "burnt_umber", 0.35), 0.45)   # ~0.44
p["hair_lit"] = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.55), 0.42)   # ~0.50
p["carton"]   = p.mix("cadmium_red", "cadmium_yellow", 0.55)               # ~0.57
p["glove"]    = p.shade(p.mix("ultramarine", "burnt_umber", 0.45), 0.30)
p["bg_fig"]   = p.tint(p.mix("burnt_umber", "ultramarine", 0.30), 0.12)

# -- cut the face slab back on the right: hair falls over it -------------------
for x0, y0, x1, y1 in [(0.555, 0.16, 0.585, 0.34), (0.575, 0.20, 0.605, 0.40),
                       (0.545, 0.26, 0.575, 0.44), (0.595, 0.24, 0.625, 0.44)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2), (x1, y1)],
             "bristle", "hair", size=0.075, pressure="taper", note="hair over face")

# -- hair across the top of the forehead ---------------------------------------
for x0, y0, x1, y1 in [(0.425, 0.20, 0.50, 0.15), (0.44, 0.235, 0.52, 0.17)]:
    s.stroke([(x0, y0), (x1, y1)], "bristle", "hair", size=0.06,
             pressure="lift_off", note="hairline")

# -- the beard, and the shadow side of the face --------------------------------
s.dry()
for x0, y0, x1, y1 in [(0.445, 0.455, 0.565, 0.480), (0.450, 0.495, 0.570, 0.515),
                       (0.465, 0.530, 0.575, 0.545), (0.487, 0.565, 0.565, 0.570),
                       (0.440, 0.420, 0.500, 0.430)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + 0.006), (x1, y1)],
             "bristle", "beard", size=0.045, pressure="taper", note="beard")
for x0, y0, x1, y1 in [(0.470, 0.300, 0.560, 0.315), (0.480, 0.345, 0.565, 0.360),
                       (0.425, 0.262, 0.500, 0.268)]:
    s.stroke([(x0, y0), (x1, y1)], "bristle", "fl_shade", size=0.035,
             pressure="taper", load=0.55, note="face shadow")

# -- the raised hand, left of the face -----------------------------------------
s.dry()
for x, ytop, ybot in [(0.215, 0.400, 0.560), (0.250, 0.375, 0.560),
                      (0.287, 0.383, 0.560), (0.322, 0.410, 0.560)]:
    s.stroke([(x, ytop), (x + 0.006, (ytop + ybot) / 2), (x - 0.004, ybot)],
             "bristle", "flesh", size=0.038, pressure="taper", note="finger")
s.stroke([(0.20, 0.545), (0.28, 0.560), (0.35, 0.545)], "bristle", "flesh",
         size=0.05, pressure="swell", note="palm")
# the glove below it
for x0, y0, x1, y1 in [(0.195, 0.62, 0.36, 0.66), (0.20, 0.69, 0.37, 0.72),
                       (0.215, 0.755, 0.39, 0.775), (0.30, 0.60, 0.40, 0.70)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2), (x1, y1)],
             "bristle", "glove", size=0.07, pressure="taper", note="glove")

# -- the carton, bottom left ---------------------------------------------------
s.dry()
s.block_in(Region(0.16, 0.775, 0.30, 1.0), "flat", "carton",
           density=0.95, size=0.06, direction="vertical", note="carton")
s.stroke([(0.225, 0.760), (0.275, 0.755)], "flat", p.tint("yellow_ochre", 0.85),
         size=0.045, pressure="even", note="carton top")

# -- background figures --------------------------------------------------------
s.dry()
for x0, y0, x1, y1 in [(0.055, 0.34, 0.175, 0.38), (0.05, 0.45, 0.18, 0.48),
                       (0.06, 0.56, 0.19, 0.60)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2), (x1, y1)],
             "bristle", "bg_fig", size=0.075, pressure="taper", note="figure left")
s.stroke([(0.09, 0.40), (0.135, 0.45)], "bristle", "fl_shade", size=0.045,
         pressure="taper", note="left face")
# the beret -- the darkest note in the background
for x0, y0, x1, y1 in [(0.195, 0.335, 0.335, 0.315), (0.205, 0.385, 0.345, 0.375),
                       (0.23, 0.43, 0.35, 0.43)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 - 0.01), (x1, y1)],
             "bristle", "glove", size=0.065, pressure="taper", note="beret")
# right-hand figure, warm
for x0, y0, x1, y1 in [(0.775, 0.36, 0.88, 0.40), (0.79, 0.45, 0.895, 0.47)]:
    s.stroke([(x0, y0), (x1, y1)], "bristle", "hair_lit", size=0.07,
             pressure="taper", load=0.6, note="figure right")
s.stroke([(0.825, 0.475), (0.895, 0.52)], "bristle", "cadmium_red", size=0.045,
         pressure="taper", load=0.7, note="red pattern")

print("strokes:", s.stroke_count)
print(s.look())
