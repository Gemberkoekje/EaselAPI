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

p["eyew"]  = to_value(p.desaturate(p.mix("cerulean", "yellow_ochre", 0.45), 0.55), 0.50)
p["iris"]  = p.mix("burnt_umber", "ultramarine", 0.35)
p["lip"]   = to_value(p.desaturate(p.mix("cadmium_red", "burnt_sienna", 0.40), 0.25), 0.40)
p["teeth"] = to_value(p.desaturate(p.mix("yellow_ochre", "cerulean", 0.3), 0.45), 0.62)
p["hair_l"] = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.30), 0.50)

beard_marks = [
    dict(points=[(0.408, 0.398), (0.440, 0.388), (0.472, 0.394)], brush="bristle",
         color="beard", size=0.018),
    dict(points=[(0.424, 0.446), (0.432, 0.492), (0.454, 0.528)], brush="bristle",
         color="beard", size=0.026),
    dict(points=[(0.444, 0.508), (0.478, 0.546), (0.510, 0.540)], brush="bristle",
         color="beard", size=0.030),
    dict(points=[(0.494, 0.520), (0.524, 0.492), (0.542, 0.454)], brush="bristle",
         color="beard", size=0.028),
    dict(points=[(0.468, 0.432), (0.500, 0.448), (0.524, 0.472)], brush="bristle",
         color="beard", size=0.024),
    dict(points=[(0.478, 0.410), (0.514, 0.430)], brush="bristle",
         color="hair_d", size=0.014, load=0.5),
]

planes = [
    dict(points=[(0.424, 0.272), (0.452, 0.250), (0.482, 0.238)], brush="flat",
         color="skin_l", size=0.024),
    dict(points=[(0.466, 0.336), (0.496, 0.388), (0.512, 0.434)], brush="flat",
         color="skin_l", size=0.030),
    dict(points=[(0.426, 0.296), (0.462, 0.292)], brush="flat",
         color="skin_d", size=0.015),
    dict(points=[(0.524, 0.282), (0.550, 0.340), (0.552, 0.398)], brush="flat",
         color="skin_d", size=0.026, opacity=0.55),
    dict(points=[(0.414, 0.320), (0.401, 0.352)], brush="flat",
         color="skin_v", size=0.011),
    dict(points=[(0.402, 0.388), (0.422, 0.400)], brush="flat",
         color="skin_l", size=0.010),
]

feats = [
    dict(points=[(0.421, 0.279), (0.446, 0.271), (0.468, 0.267)], brush="liner",
         color="hair_d", size=0.008, pressure=[1, 0.4]),
    dict(points=[(0.449, 0.303), (0.470, 0.302)], brush="liner",
         color="hair_d", size=0.005),
    dict(points=[(0.434, 0.450), (0.464, 0.457)], brush="round_hard",
         color="iris", size=0.013),
    dict(points=[(0.438, 0.469), (0.464, 0.471)], brush="round_hard",
         color="lip", size=0.009),
]

hairlight = [
    dict(points=[(0.500, 0.112), (0.548, 0.100), (0.590, 0.118)], brush="bristle",
         color="hair_l", size=0.012),
    dict(points=[(0.548, 0.104), (0.598, 0.134), (0.634, 0.184)], brush="bristle",
         color="hair_m", size=0.014),
    dict(points=[(0.600, 0.148), (0.646, 0.212), (0.672, 0.276)], brush="bristle",
         color="hair_m", size=0.013),
    dict(points=[(0.636, 0.204), (0.674, 0.280), (0.688, 0.350)], brush="bristle",
         color="hair_l", size=0.010),
    dict(points=[(0.460, 0.186), (0.492, 0.140), (0.530, 0.112)], brush="bristle",
         color="hair_m", size=0.011),
    dict(points=[(0.664, 0.300), (0.680, 0.372), (0.664, 0.430)], brush="bristle",
         color="hair_m", size=0.012),
]

print(s.rehearse(beard_marks + planes + feats, reference="ref.jpg",
                 region=span("D3", "E5")))
print(s.rehearse(hairlight, reference="ref.jpg", region=span("D1", "F4")))
