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

p["hand"]   = to_value(p.desaturate(p.mix("burnt_sienna", "cadmium_red", 0.25), 0.45), 0.44)
p["glove"]  = to_value(p.mix("ultramarine", "burnt_umber", 0.42), 0.16)
p["farman"] = to_value(p.desaturate(p.mix("burnt_sienna", "yellow_ochre", 0.4), 0.35), 0.31)
p["capwh"]  = to_value(p.mix("yellow_ochre", "cerulean", 0.25), 0.72)

hand = polygon([
    (0.202, 0.424), (0.214, 0.388), (0.224, 0.388), (0.232, 0.420), (0.245, 0.389),
    (0.255, 0.394), (0.254, 0.430), (0.267, 0.409), (0.278, 0.418), (0.274, 0.454),
    (0.290, 0.446), (0.301, 0.482), (0.302, 0.552), (0.288, 0.614), (0.252, 0.668),
    (0.205, 0.655), (0.172, 0.596), (0.164, 0.520), (0.180, 0.456),
])
glove = polygon([
    (0.278, 0.560), (0.318, 0.548), (0.352, 0.590), (0.364, 0.680), (0.346, 0.760),
    (0.304, 0.784), (0.272, 0.742), (0.266, 0.650),
])
carton = polygon([
    (0.156, 0.790), (0.172, 0.756), (0.224, 0.748), (0.257, 0.772), (0.255, 1.000),
    (0.154, 1.000),
])
farman = polygon([
    (0.098, 0.352), (0.140, 0.336), (0.176, 0.360), (0.180, 0.440), (0.164, 0.500),
    (0.128, 0.512), (0.100, 0.470),
])

s.dry()
n = s.stroke_count
s.block_in(farman, "flat", "farman", direction="axis", density=1.0, size=0.075, load=1.0)
print("farman", s.stroke_count - n); n = s.stroke_count

s.block_in(hand, "flat", "hand", direction=("axis"), density=1.0, size=0.075, load=1.0)
print("hand", s.stroke_count - n); n = s.stroke_count

# the gaps between the fingers, drawn as the dark BEHIND, not as outlines
s.stroke([(0.232, 0.418), (0.222, 0.470)], "liner", "glove", size=0.010, pressure=[1, 0])
s.stroke([(0.253, 0.428), (0.246, 0.482)], "liner", "glove", size=0.010, pressure=[1, 0])
s.stroke([(0.274, 0.452), (0.268, 0.498)], "liner", "glove", size=0.009, pressure=[1, 0])

s.block_in(glove, "bristle", "glove", direction="axis", density=1.0, size=0.07, load=1.0)
print("glove", s.stroke_count - n); n = s.stroke_count

s.block_in(carton, "flat", "cartn", direction="axis", density=1.0, size=0.075, load=1.0)
s.dab(0.240, 0.766, "round_hard", "capwh", size=0.030, press=3)
print("carton", s.stroke_count - n); n = s.stroke_count

# two glass tumblers, bottom left: pale verticals, nothing more
s.stroke([(0.068, 0.880), (0.070, 1.000)], "flat", "capwh", size=0.038,
         opacity=0.45, pressure="even")
s.stroke([(0.118, 0.900), (0.120, 1.000)], "flat", "capwh", size=0.032,
         opacity=0.40, pressure="even")
print("glass", s.stroke_count - n)

print("total:", s.stroke_count)
print(s.look(reference="ref.jpg"))
