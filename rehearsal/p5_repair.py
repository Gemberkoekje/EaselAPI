# Stage 5 -- repairs, painted over rather than undone.
# The face went chalky pink and the fingers came out as a barcode.
p = s.palette
p["skin"]    = p.desaturate(p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.40), 0.74), 0.25)
p["skin_h"]  = p.desaturate(p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.55), 0.58), 0.30)
p["skin_s"]  = p.desaturate(p.tint(p.mix("burnt_sienna", "burnt_umber", 0.40), 0.36), 0.25)
p["hairm"]   = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.40), 0.22)
p["cart"]    = p.desaturate(p.mix("cadmium_red", "cadmium_yellow", 0.55), 0.50)
p["bg_near"] = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.30), 0.20)

s.dry()

# -- repaint the face in a muted skin, warm not pink ----------------------------
face = [(0.437, 0.243, 0.112), (0.429, 0.268, 0.130), (0.421, 0.292, 0.146),
        (0.416, 0.316, 0.156), (0.413, 0.340, 0.162), (0.417, 0.364, 0.156),
        (0.427, 0.388, 0.146)]
for lx, y, w in face:
    s.stroke([(lx, y), (lx + w * 0.55, y + 0.005), (lx + w, y - 0.004)],
             "bristle", "skin", size=0.040, pressure="lift_off", load=1.0,
             note="face repaint")
for x0, y0, x1, y1 in [(0.505, 0.262, 0.578, 0.286), (0.515, 0.302, 0.588, 0.326),
                       (0.520, 0.342, 0.592, 0.368), (0.508, 0.386, 0.578, 0.404)]:
    s.stroke([(x0, y0), (x1, y1)], "bristle", "skin_h", size=0.038,
             pressure="taper", load=1.0, note="face shadow side")
# brow, socket, nose, mouth -- small and few
s.stroke([(0.425, 0.302), (0.468, 0.296), (0.502, 0.302)], "bristle", "skin_s",
         size=0.020, pressure="swell", load=1.0, note="brow")
s.dab(0.450, 0.320, "round_hard", p.tint("burnt_umber", 0.04), size=0.009, note="eye")
s.stroke([(0.419, 0.326), (0.4135, 0.350), (0.425, 0.368)], "bristle", "skin_h",
         size=0.019, pressure="even", load=1.0, note="nose")
s.stroke([(0.432, 0.420), (0.466, 0.426)], "bristle", p.tint("burnt_umber", 0.02),
         size=0.013, pressure="taper", load=1.0, note="mouth")

# -- hair: cover the helmet edge, let it break into the background --------------
for x0, y0, x1, y1 in [(0.448, 0.108, 0.522, 0.168), (0.474, 0.080, 0.566, 0.146),
                       (0.526, 0.072, 0.620, 0.162), (0.566, 0.092, 0.656, 0.212),
                       (0.596, 0.132, 0.664, 0.278), (0.588, 0.198, 0.642, 0.338),
                       (0.562, 0.252, 0.614, 0.376)]:
    s.stroke([(x0, y0), ((x0 + x1) / 2 + 0.014, (y0 + y1) / 2), (x1, y1)],
             "bristle", "hairm", size=0.055, pressure="taper", load=0.9, note="hair")
# stray locks, dry brush, breaking the silhouette
for x0, y0, x1, y1 in [(0.560, 0.082, 0.640, 0.052), (0.612, 0.140, 0.690, 0.116),
                       (0.470, 0.078, 0.520, 0.048), (0.628, 0.212, 0.700, 0.230)]:
    s.stroke([(x0, y0), (x1, y1)], "bristle", "hairm", size=0.020,
             pressure="lift_off", load=0.45, note="stray hair")

# -- the hand: cover the stripes, restate as one light shape -------------------
s.dry()
s.block_in(Region(0.198, 0.375, 0.345, 0.560), "bristle", "skin",
           density=0.9, size=0.048, direction="vertical", load=1.0, note="hand")
# only two gaps, soft, and the fingertips at different heights
for x, ytop in [(0.245, 0.372), (0.300, 0.386)]:
    s.stroke([(x, ytop + 0.02), (x + 0.002, 0.520)], "bristle", "skin_s",
             size=0.014, pressure="taper", load=0.75, note="finger gap")
s.stroke([(0.213, 0.398), (0.222, 0.372)], "bristle", "bg_near", size=0.022,
         pressure="taper", load=0.9, note="above fingertip")
s.stroke([(0.318, 0.404), (0.330, 0.386)], "bristle", "bg_near", size=0.022,
         pressure="taper", load=0.9, note="above fingertip")
s.stroke([(0.205, 0.556), (0.278, 0.572), (0.348, 0.552)], "bristle", "skin_h",
         size=0.042, pressure="swell", load=1.0, note="palm")

# -- the carton: one solid muted block, no stripes ------------------------------
s.dry()
s.block_in(Region(0.160, 0.778, 0.300, 1.0), "flat", "cart",
           density=1.0, size=0.07, direction="horizontal", load=1.0, note="carton")
s.stroke([(0.226, 0.770), (0.274, 0.766)], "flat", p.tint("yellow_ochre", 0.78),
         size=0.036, pressure="even", load=1.0, note="carton top")

print("strokes:", s.stroke_count)
print(s.look())
