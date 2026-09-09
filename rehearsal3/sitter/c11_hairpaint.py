# Pass 11: paint the winning hair plan (rehearsal C, darkened one notch at the back).
REF = "C:/temp/Level3.jpg"
p = s.palette
p["h_a"] = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.30), "titanium_white", 0.06)
p["h_b"] = p.mix("burnt_umber", "ultramarine", 0.10)
p["h_c"] = p.mix(p.mix("yellow_ochre", "burnt_umber", 0.55), "titanium_white", 0.12)
p["h_d"] = p.mix(p.mix("burnt_umber", "yellow_ochre", 0.18), "titanium_white", 0.04)
p["h_hi"] = p.mix(p.mix("yellow_ochre", "burnt_umber", 0.34), "titanium_white", 0.34)
s.dry()

MASS = [
    [(0.500, 0.090), (0.455, 0.140), (0.428, 0.202), (0.424, 0.250)],
    [(0.524, 0.082), (0.474, 0.132), (0.444, 0.200), (0.440, 0.262)],
    [(0.540, 0.080), (0.504, 0.128), (0.474, 0.200), (0.468, 0.272)],
    [(0.554, 0.086), (0.534, 0.142), (0.514, 0.214), (0.510, 0.288)],
    [(0.566, 0.092), (0.564, 0.154), (0.554, 0.234), (0.550, 0.308)],
    [(0.580, 0.102), (0.598, 0.164), (0.604, 0.244), (0.600, 0.322)],
    [(0.594, 0.112), (0.628, 0.178), (0.643, 0.258), (0.643, 0.336)],
    [(0.604, 0.126), (0.651, 0.198), (0.668, 0.278), (0.666, 0.366)],
    [(0.608, 0.148), (0.662, 0.228), (0.675, 0.314), (0.662, 0.406)],
    [(0.600, 0.174), (0.652, 0.258), (0.667, 0.354), (0.652, 0.446)],
    [(0.584, 0.204), (0.632, 0.294), (0.647, 0.384), (0.630, 0.464)],
    [(0.560, 0.234), (0.606, 0.324), (0.622, 0.404), (0.610, 0.470)],
]
SIZES = [0.052, 0.044, 0.060, 0.054, 0.064, 0.048, 0.064, 0.070, 0.068, 0.074,
         0.068, 0.058]
COLS = ["h_a", "h_a", "h_d", "h_a", "h_d", "h_a", "h_d", "h_d", "h_d", "h_b",
        "h_b", "h_b"]
PRESS = ["taper", "lift_off", "taper", "swell", "taper", "lift_off", "taper",
         "swell", "taper", "lift_off", "taper", "swell"]

n0 = s.stroke_count
for pts, sz, c, pr in zip(MASS, SIZES, COLS, PRESS):
    s.stroke(pts, "bristle", c, size=sz, load=1.0, pressure=pr)
print("mass:", s.stroke_count - n0)

n0 = s.stroke_count
LIT = [
    ([(0.508, 0.098), (0.548, 0.088), (0.588, 0.110)], "h_hi", 0.011),
    ([(0.566, 0.122), (0.610, 0.170), (0.634, 0.228)], "h_hi", 0.009),
    ([(0.604, 0.202), (0.644, 0.264), (0.659, 0.324)], "h_c", 0.015),
    ([(0.474, 0.122), (0.446, 0.172), (0.434, 0.218)], "h_c", 0.011),
    ([(0.624, 0.312), (0.652, 0.374), (0.650, 0.430)], "h_c", 0.013),
    ([(0.494, 0.106), (0.470, 0.152), (0.452, 0.204)], "h_hi", 0.008),
]
for pts, c, sz in LIT:
    s.stroke(pts, "bristle", c, size=sz, load=1.0, pressure="taper")
print("lit:", s.stroke_count - n0)

print("head:", s.look(region=span("D1", "G5"), reference=REF))
print("TOTAL strokes:", s.stroke_count)
