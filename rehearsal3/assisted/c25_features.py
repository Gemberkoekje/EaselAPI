# Pass 25 — the things that make it a mug of tea rather than a shape: the pale
# rim ring, the handle, the spoon, the teabag and its string.
# The rim goes on as the mass OUTSIDE the tea (brush centred on the ring, laid up
# to where the dark stops) rather than as a line drawn round the hole.
# Run: python -m easel run painting.easel c25_features.py
REF = r"C:\temp\Level1.jpg"
p = s.palette
M, T, D, S = p.mix, p.tint, p.desaturate, p.shade


def at_value(base, target):
    if p.value_of(base) < target:
        lo, hi, f = 0.0, 1.0, T
    else:
        lo, hi, f = 0.0, 1.0, S
    for _ in range(24):
        mid = (lo + hi) / 2
        if (p.value_of(f(base, mid)) < target) == (f is T):
            lo = mid
        else:
            hi = mid
    return f(base, (lo + hi) / 2)


NEUT = D(M("ultramarine", "burnt_umber", 0.40), 0.30)
p["rim_a"] = at_value(NEUT, 0.62)
p["rim_b"] = at_value(NEUT, 0.74)
p["rim_c"] = at_value(NEUT, 0.82)
p["hand"] = at_value(NEUT, 0.76)
p["hand_d"] = at_value(NEUT, 0.52)
p["wood_d"] = at_value(D(M("yellow_ochre", "burnt_umber", 0.50), 0.34), 0.44)
p["steel"] = at_value(D(M("cerulean", "burnt_umber", 0.30), 0.45), 0.66)
p["black"] = S(M("ultramarine", "burnt_umber", 0.45), 1.0)
p["navy"] = S(M("ultramarine", "burnt_umber", 0.25), 1.0)

s.dry()

# --- the rim ring ---------------------------------------------------------
n0 = s.stroke_count
s.stroke([(0.372, 0.120), (0.440, 0.109), (0.510, 0.108), (0.565, 0.122),
          (0.604, 0.148)], "flat", "rim_a", size=0.014, load=1.0, pressure="even")
s.stroke([(0.606, 0.150), (0.624, 0.186), (0.621, 0.222)], "flat", "rim_a",
         size=0.012, load=1.0, pressure="even")
s.stroke([(0.620, 0.224), (0.604, 0.256), (0.566, 0.288)], "flat", "rim_b",
         size=0.016, load=1.0, pressure="even")
s.stroke([(0.566, 0.290), (0.506, 0.312), (0.446, 0.316), (0.402, 0.304)],
         "flat", "rim_c", size=0.019, load=1.0, pressure="even")
s.stroke([(0.400, 0.302), (0.362, 0.278), (0.339, 0.245), (0.332, 0.206),
          (0.343, 0.168), (0.372, 0.142)], "flat", "rim_b", size=0.024,
         load=1.0, pressure="even")
print("rim:", s.stroke_count - n0)

# --- the handle -----------------------------------------------------------
n0 = s.stroke_count
s.stroke([(0.628, 0.250), (0.672, 0.272), (0.697, 0.312)], "flat", "hand",
         size=0.030, load=1.0, pressure="even")
s.stroke([(0.699, 0.316), (0.701, 0.362), (0.682, 0.408)], "flat", "hand",
         size=0.028, load=1.0, pressure="even")
s.stroke([(0.680, 0.412), (0.648, 0.444), (0.618, 0.464)], "flat", "hand",
         size=0.030, load=1.0, pressure="even")
s.dry()
# the wood seen through the handle
s.stroke([(0.648, 0.300), (0.664, 0.330), (0.666, 0.376), (0.652, 0.412)],
         "flat", "wood_d", size=0.030, load=1.0, pressure="even")
s.stroke([(0.646, 0.404), (0.644, 0.340), (0.648, 0.302)], "flat", "wood_d",
         size=0.020, load=1.0, pressure="even")
# a light along the handle's outer edge, and its shaded inner side
s.stroke([(0.688, 0.284), (0.706, 0.330), (0.706, 0.372)], "round_hard",
         "rim_c", size=0.010, load=1.0, pressure="taper")
s.stroke([(0.660, 0.290), (0.676, 0.330), (0.672, 0.390)], "round_hard",
         "hand_d", size=0.009, load=1.0, pressure="taper", opacity=0.7)
print("handle:", s.stroke_count - n0)

# --- the spoon ------------------------------------------------------------
n0 = s.stroke_count
s.stroke([(0.531, 0.004), (0.524, 0.055), (0.515, 0.105)], "flat", "black",
         size=0.042, load=1.0, pressure="even")
s.stroke([(0.514, 0.108), (0.508, 0.175), (0.504, 0.232)], "flat", "black",
         size=0.023, load=1.0, pressure="even")
s.stroke([(0.505, 0.238), (0.518, 0.268), (0.540, 0.288)], "flat", "steel",
         size=0.020, load=1.0, pressure="even")
s.dab(0.529, 0.279, "round_hard", "steel", size=0.014)
s.dab(0.522, 0.262, "round_hard", at_value(NEUT, 0.86), size=0.009)
print("spoon:", s.stroke_count - n0)

# --- the teabag tag and its string ----------------------------------------
n0 = s.stroke_count
for i, (y, lx, rx) in enumerate([(0.560, 0.826, 0.908), (0.585, 0.818, 0.916),
                                 (0.612, 0.824, 0.910), (0.634, 0.840, 0.894)]):
    pts = [(lx, y), (rx, y)]
    s.stroke(pts if i % 2 == 0 else pts[::-1], "flat", "navy", size=0.020,
             load=1.0, pressure="even")
s.dab(0.845, 0.578, "round_hard", at_value(NEUT, 0.88), size=0.011)
s.stroke([(0.642, 0.214), (0.700, 0.290), (0.730, 0.380), (0.742, 0.452),
          (0.790, 0.530), (0.820, 0.560)], "liner", "rim_c", size=0.004,
         load=1.0, pressure="even", opacity=0.8)
s.stroke([(0.716, 0.436), (0.660, 0.560), (0.600, 0.610), (0.520, 0.630)],
         "liner", "wood_d", size=0.003, load=1.0, pressure="even", opacity=0.6)
print("tag+string:", s.stroke_count - n0)

print(s.look(reference=REF))
print("total strokes:", s.stroke_count)
