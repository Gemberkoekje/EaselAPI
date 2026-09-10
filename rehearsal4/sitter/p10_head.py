p = s.palette

def to_value(base, target):
    other = "titanium_white" if p.value_of(base) < target else "burnt_umber"
    lo, hi = 0.0, 1.0
    for _ in range(28):
        mid = (lo + hi) / 2.0
        v = p.value_of(p.mix(base, other, mid))
        if (v < target) == (other == "titanium_white"):
            lo = mid
        else:
            hi = mid
    return p.mix(base, other, (lo + hi) / 2.0)

p["neck"]   = to_value(p.desaturate(p.mix("burnt_sienna", "cadmium_red", 0.2), 0.3), 0.30)
p["skin_v"] = to_value(p.mix("burnt_sienna", "yellow_ochre", 0.55), 0.58)

s.dry()
n = s.stroke_count

# ---- the hair, following its own flow ----------------------------------
H = [
    ([(0.435, 0.230), (0.462, 0.170), (0.495, 0.128)], "hair_m", 0.030),
    ([(0.470, 0.190), (0.505, 0.135), (0.545, 0.108)], "hair_l", 0.026),
    ([(0.505, 0.115), (0.560, 0.100), (0.605, 0.130)], "hair_l", 0.032),
    ([(0.545, 0.098), (0.600, 0.125), (0.645, 0.185)], "hair_h", 0.022),
    ([(0.580, 0.115), (0.635, 0.175), (0.672, 0.245)], "hair_l", 0.036),
    ([(0.615, 0.160), (0.662, 0.235), (0.690, 0.315)], "hair_m", 0.040),
    ([(0.640, 0.210), (0.682, 0.290), (0.697, 0.370)], "hair_l", 0.028),
    ([(0.660, 0.270), (0.688, 0.350), (0.672, 0.428)], "hair_m", 0.034),
    ([(0.618, 0.330), (0.650, 0.400), (0.638, 0.470)], "hair_d", 0.030),
    ([(0.555, 0.170), (0.590, 0.240), (0.600, 0.320)], "hair_m", 0.026),
    ([(0.520, 0.150), (0.545, 0.215), (0.560, 0.285)], "hair_d", 0.024),
    ([(0.560, 0.300), (0.575, 0.360), (0.578, 0.412)], "hair_d", 0.020),
]
for path, col, sz in H:
    s.stroke(path, "bristle", col, size=sz, pressure="taper", load=0.95)
print("hair strokes", s.stroke_count - n); n = s.stroke_count

# loose strands, at the scale of a strand
s.stroke([(0.492, 0.140), (0.455, 0.185), (0.432, 0.228)], "liner", "hair_d",
         size=0.006, pressure=[1, 0.4])
s.stroke([(0.478, 0.126), (0.448, 0.168)], "liner", "hair_d", size=0.005,
         pressure=[0.8, 0.2])
s.stroke([(0.518, 0.086), (0.548, 0.062)], "liner", "hair_m", size=0.004,
         pressure=[0.7, 0.1])
s.stroke([(0.698, 0.328), (0.718, 0.358)], "liner", "hair_m", size=0.005,
         pressure=[0.9, 0.2])
print("strands", s.stroke_count - n); n = s.stroke_count

# ---- the face, as planes ------------------------------------------------
F = [
    ([(0.425, 0.268), (0.462, 0.242), (0.492, 0.230)], "flat", "skin_l", 0.030),
    ([(0.430, 0.246), (0.476, 0.224)],                 "flat", "skin_l", 0.020),
    ([(0.470, 0.330), (0.505, 0.390), (0.522, 0.440)], "flat", "skin_l", 0.038),
    ([(0.452, 0.332), (0.494, 0.350)],                 "flat", "skin_l", 0.024),
    ([(0.520, 0.272), (0.548, 0.330), (0.556, 0.392)], "flat", "skin_m", 0.034),
    ([(0.428, 0.292), (0.470, 0.288)],                 "flat", "skin_d", 0.017),
    ([(0.416, 0.318), (0.403, 0.350), (0.397, 0.366)], "flat", "skin_v", 0.014),
    ([(0.414, 0.338), (0.416, 0.374)],                 "flat", "skin_m", 0.013),
    ([(0.404, 0.390), (0.424, 0.402)],                 "flat", "skin_m", 0.012),
    ([(0.528, 0.498), (0.556, 0.560)],                 "flat", "neck",   0.030),
    ([(0.498, 0.520), (0.536, 0.546)],                 "flat", "skin_d", 0.022),
]
for path, br, col, sz in F:
    s.stroke(path, br, col, size=sz, pressure="taper", load=1.0)
print("face planes", s.stroke_count - n)

print("total:", s.stroke_count)
print(s.look(region=span("D1", "F5"), reference="ref.jpg"))
