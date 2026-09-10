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

p["hair_d"] = to_value(p.mix("burnt_umber", "burnt_sienna", 0.40), 0.19)
p["hair_m"] = to_value(p.mix("burnt_umber", "yellow_ochre", 0.55), 0.33)
p["hair_l"] = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.28), 0.53)
p["hair_h"] = to_value(p.mix("yellow_ochre", "cadmium_yellow", 0.30), 0.70)
p["skin_d"] = to_value(p.mix("burnt_sienna", "burnt_umber", 0.45), 0.23)
p["skin_m"] = to_value(p.desaturate(p.mix("burnt_sienna", "cadmium_red", 0.30), 0.18), 0.38)
p["skin_l"] = to_value(p.mix("burnt_sienna", "yellow_ochre", 0.50), 0.52)
p["skin_h"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.20), 0.68)
p["beard"]  = p.mix("burnt_umber", "ultramarine", 0.30)
p["coat_l"] = to_value(p.mix("ultramarine", "burnt_umber", 0.45), 0.21)

coat = polygon([
    (0.290, 1.000), (0.330, 0.860), (0.378, 0.720), (0.428, 0.620), (0.470, 0.578),
    (0.512, 0.592), (0.545, 0.600), (0.572, 0.582), (0.600, 0.548), (0.630, 0.492),
    (0.672, 0.418), (0.706, 0.372), (0.722, 0.392), (0.756, 0.435), (0.794, 0.482),
    (0.827, 0.532), (0.855, 0.581), (0.869, 0.630), (0.878, 0.690), (0.882, 0.760),
    (0.900, 0.870), (0.920, 1.000),
])

hair = polygon([
    (0.421, 0.245), (0.437, 0.195), (0.458, 0.152), (0.490, 0.110), (0.526, 0.082),
    (0.572, 0.100), (0.618, 0.155), (0.660, 0.228), (0.703, 0.320), (0.706, 0.378),
    (0.684, 0.430), (0.648, 0.462), (0.618, 0.484), (0.560, 0.440), (0.500, 0.360),
    (0.455, 0.300),
])

face = polygon([
    (0.421, 0.242), (0.417, 0.262), (0.412, 0.292), (0.417, 0.313), (0.404, 0.346),
    (0.393, 0.368), (0.403, 0.386), (0.424, 0.408), (0.430, 0.430), (0.428, 0.452),
    (0.436, 0.478), (0.452, 0.520), (0.487, 0.555), (0.522, 0.540), (0.548, 0.500),
    (0.562, 0.440), (0.568, 0.370), (0.570, 0.300), (0.540, 0.248), (0.492, 0.208),
    (0.452, 0.212),
])

beard = polygon([
    (0.406, 0.398), (0.443, 0.384), (0.487, 0.397), (0.520, 0.418), (0.543, 0.455),
    (0.548, 0.492), (0.532, 0.524), (0.503, 0.550), (0.470, 0.548), (0.444, 0.512),
    (0.428, 0.468), (0.419, 0.428),
])

n0 = s.stroke_count
s.block_in(coat, "flat", "coat", direction=("axis", 62), density=1.0,
           size=0.14, load=1.0)
print("coat:", s.stroke_count - n0)

n0 = s.stroke_count
s.block_in(hair, "bristle", "hair_d", direction=("axis", 74), density=1.0,
           size=0.09, load=1.0)
print("hair:", s.stroke_count - n0)

n0 = s.stroke_count
s.block_in(face, "flat", "skin_m", direction="axis", density=1.0,
           size=0.085, load=1.0)
print("face:", s.stroke_count - n0)

n0 = s.stroke_count
s.block_in(beard, "bristle", "beard", direction=("axis", 80), density=1.0,
           size=0.055, load=1.0)
print("beard:", s.stroke_count - n0)

print("total:", s.stroke_count)
print(s.look(reference="ref.jpg"))
print(s.look(reference="ref.jpg", values=True))
