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

# warmer, far less red skin than the first attempt
p["skin_m"] = to_value(p.desaturate(p.mix("burnt_sienna", "yellow_ochre", 0.42), 0.30), 0.37)
p["skin_l"] = to_value(p.desaturate(p.mix("burnt_sienna", "yellow_ochre", 0.55), 0.20), 0.50)
p["skin_v"] = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.25), 0.60)
p["skin_d"] = to_value(p.mix("burnt_sienna", "burnt_umber", 0.50), 0.24)
p["hair_d"] = to_value(p.mix("burnt_umber", "burnt_sienna", 0.35), 0.185)
p["hair_m"] = to_value(p.mix("burnt_umber", "yellow_ochre", 0.60), 0.31)

# the hair without the face: a band round the head
hair2 = polygon([
    (0.421, 0.245), (0.437, 0.195), (0.458, 0.152), (0.490, 0.110), (0.526, 0.082),
    (0.572, 0.100), (0.618, 0.155), (0.660, 0.228), (0.703, 0.320), (0.706, 0.378),
    (0.684, 0.430), (0.648, 0.462), (0.618, 0.484), (0.592, 0.450), (0.575, 0.395),
    (0.565, 0.330), (0.548, 0.272), (0.512, 0.222), (0.470, 0.200), (0.440, 0.208),
])
face = polygon([
    (0.421, 0.242), (0.417, 0.262), (0.412, 0.292), (0.417, 0.313), (0.404, 0.346),
    (0.393, 0.368), (0.403, 0.386), (0.424, 0.408), (0.430, 0.430), (0.428, 0.452),
    (0.436, 0.478), (0.452, 0.520), (0.487, 0.555), (0.522, 0.540), (0.548, 0.500),
    (0.562, 0.440), (0.568, 0.370), (0.570, 0.300), (0.540, 0.248), (0.492, 0.208),
    (0.452, 0.212),
])

s.dry()
n = s.stroke_count
s.block_in(hair2, "bristle", "hair_d", direction=("axis", 68), density=1.0,
           size=0.075, load=1.0)
print("hair reblock", s.stroke_count - n); n = s.stroke_count
s.block_in(face, "flat", "skin_m", direction="axis", density=1.0, size=0.075, load=1.0)
print("face reblock", s.stroke_count - n)
print("total:", s.stroke_count)
print(s.look(region=span("D1", "F5"), reference="ref.jpg"))
