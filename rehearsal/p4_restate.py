# Stage 4 -- restate the figure in solid paint over the scumble.
# The scumble is a broken half-load field; anything that has to read as a solid
# mass needs load near 1.0, not the 0.4-0.6 dry-brush window.
p = s.palette
p["fl_lit"]   = p.tint(p.mix("burnt_sienna", "cadmium_red", 0.22), 0.84)   # ~0.75
p["fl_half"]  = p.tint(p.mix("burnt_sienna", "cadmium_red", 0.30), 0.68)   # ~0.60
p["fl_dark"]  = p.tint(p.mix("burnt_sienna", "burnt_umber", 0.45), 0.40)   # ~0.42
p["beard2"]   = p.tint(p.mix("burnt_umber", "ultramarine", 0.20), 0.14)
p["hair2"]    = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.45), 0.26)
p["hair_hi"]  = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.60), 0.55)
p["carton2"]  = p.desaturate(p.mix("cadmium_red", "cadmium_yellow", 0.50), 0.42)
p["coat2"]    = p.mix("ultramarine", "burnt_umber", 0.60)

s.dry()

# -- the face, solid, left edge riding the profile ------------------------------
face = [(0.437, 0.245, 0.115), (0.428, 0.275, 0.135), (0.420, 0.300, 0.150),
        (0.416, 0.325, 0.158), (0.412, 0.348, 0.165), (0.421, 0.372, 0.158),
        (0.430, 0.395, 0.150)]
for lx, y, w in face:
    s.stroke([(lx, y), (lx + w * 0.5, y + 0.004), (lx + w, y - 0.003)],
             "bristle", "fl_lit", size=0.042, pressure="lift_off",
             load=1.0, note="face light")
# the shadow half of the head, right of the lit planes
for x0, y0, x1, y1 in [(0.520, 0.270, 0.585, 0.290), (0.530, 0.310, 0.590, 0.330),
                       (0.535, 0.350, 0.595, 0.372), (0.520, 0.395, 0.585, 0.410)]:
    s.stroke([(x0, y0), (x1, y1)], "bristle", "fl_half", size=0.040,
             pressure="taper", load=0.95, note="face turning away")

# -- brow, eye socket, nose ------------------------------------------------------
s.stroke([(0.424, 0.306), (0.470, 0.300), (0.505, 0.305)], "bristle", "fl_dark",
         size=0.022, pressure="swell", load=1.0, note="brow")
s.dab(0.452, 0.323, "round_hard", p.tint("burnt_umber", 0.05), size=0.010, note="eye")
s.stroke([(0.418, 0.330), (0.414, 0.352), (0.424, 0.370)], "bristle", "fl_half",
         size=0.020, pressure="even", load=1.0, note="nose")

# -- the beard: follows the jaw, not a horizontal bar ----------------------------
for x0, y0, x1, y1 in [(0.428, 0.412, 0.520, 0.455), (0.432, 0.440, 0.545, 0.490),
                       (0.446, 0.478, 0.560, 0.520), (0.470, 0.515, 0.565, 0.548),
                       (0.500, 0.548, 0.560, 0.566)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2 - 0.008, (y0 + y1) / 2 + 0.008), (x1, y1)],
             "bristle", "beard2", size=0.042, pressure="taper",
             load=0.95, note="beard")
s.stroke([(0.437, 0.424), (0.470, 0.430)], "bristle", p.tint("burnt_umber", 0.02),
         size=0.014, pressure="taper", load=1.0, note="mouth")

# -- hair: solid mass, direction following the fall -----------------------------
for x0, y0, x1, y1 in [(0.452, 0.115, 0.520, 0.175), (0.470, 0.085, 0.560, 0.150),
                       (0.520, 0.078, 0.615, 0.165), (0.560, 0.095, 0.650, 0.215),
                       (0.590, 0.135, 0.660, 0.280), (0.585, 0.200, 0.640, 0.340),
                       (0.560, 0.255, 0.612, 0.380), (0.545, 0.150, 0.600, 0.245)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2 + 0.012, (y0 + y1) / 2), (x1, y1)],
             "bristle", "hair2", size=0.058, pressure="taper", load=0.95, note="hair")
for x0, y0, x1, y1 in [(0.500, 0.090, 0.575, 0.130), (0.575, 0.130, 0.630, 0.230)]:
    s.stroke([(x0, y0), (x1, y1)], "bristle", "hair_hi", size=0.026,
             pressure="taper", load=0.6, note="hair lit")

# -- the hand: four fingers with gaps, not a slab -------------------------------
s.dry()
for x, ytop, ybot, w in [(0.212, 0.402, 0.548, 0.030), (0.249, 0.372, 0.548, 0.032),
                         (0.286, 0.380, 0.552, 0.032), (0.321, 0.408, 0.556, 0.030)]:
    s.stroke([(x, ytop), (x + 0.005, (ytop + ybot) / 2), (x - 0.003, ybot)],
             "bristle", "fl_lit", size=w, pressure="taper", load=1.0, note="finger")
for x in (0.2305, 0.2675, 0.3035):
    s.stroke([(x, 0.400), (x, 0.545)], "bristle", "beard2", size=0.012,
             pressure="even", load=0.9, note="between fingers")
s.stroke([(0.205, 0.560), (0.275, 0.575), (0.345, 0.558)], "bristle", "fl_half",
         size=0.045, pressure="swell", load=1.0, note="palm")

# -- knock the carton back; it was shouting -------------------------------------
s.dry()
s.block_in(Region(0.163, 0.782, 0.298, 1.0), "bristle", "carton2",
           density=0.85, size=0.055, direction="vertical", load=0.95, note="carton")
s.stroke([(0.228, 0.768), (0.272, 0.764)], "flat", p.tint("yellow_ochre", 0.80),
         size=0.038, pressure="even", load=1.0, note="carton top")

print("strokes:", s.stroke_count)
print(s.look())
