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

p["cartn2"]  = to_value(p.mix("cadmium_red", "cadmium_yellow", 0.50), 0.42)
p["red_pat"] = to_value(p.mix("cadmium_red", "cadmium_yellow", 0.30), 0.36)
p["face2"]   = to_value(p.desaturate(p.mix("burnt_sienna", "yellow_ochre", 0.45), 0.35), 0.38)
p["coat_l"]  = to_value(p.mix("ultramarine", "burnt_umber", 0.48), 0.20)
p["shirt_b"] = to_value(p.mix("cerulean", "ultramarine", 0.30), 0.30)

s.dry()
n = s.stroke_count

# the cheek: the bristle comb left scratches there — lay the plane back over them
s.stroke([(0.516, 0.290), (0.540, 0.350), (0.542, 0.404)], "flat", "skin_m",
         size=0.030, opacity=0.75, pressure="even")
s.stroke([(0.500, 0.330), (0.522, 0.392), (0.528, 0.442)], "flat", "skin_l",
         size=0.022, opacity=0.55, pressure="even")
s.smudge([(0.520, 0.300), (0.534, 0.400)], size=0.040)
print("cheek", s.stroke_count - n); n = s.stroke_count

# the ear, and the neck under the jaw
s.dab(0.5865, 0.3455, "round_hard", "skin_m", size=0.026)
s.dab(0.5885, 0.3510, "round_hard", "skin_d", size=0.011, opacity=0.75)
s.stroke([(0.5240, 0.4980), (0.5480, 0.5560)], "flat", "neck", size=0.028,
         opacity=0.85)
s.stroke([(0.4980, 0.5220), (0.5300, 0.5480)], "flat", "skin_d", size=0.020,
         opacity=0.7)
print("ear/neck", s.stroke_count - n); n = s.stroke_count

# the coat: collar, lapel, the lit shoulder plane, the zip
s.stroke([(0.516, 0.586), (0.539, 0.629), (0.558, 0.685), (0.567, 0.732)],
         "bristle", "coat_l", size=0.020, load=0.7)
s.stroke([(0.648, 0.470), (0.716, 0.452), (0.782, 0.470)], "bristle", "coat_l",
         size=0.045, opacity=0.6, load=0.7)
s.stroke([(0.560, 0.640), (0.596, 0.720), (0.612, 0.820)], "bristle", "coat_l",
         size=0.016, opacity=0.5, load=0.6)
s.stroke([(0.5305, 0.6400), (0.5580, 0.6520)], "round_hard", "shirt_b", size=0.010)
s.dab(0.5655, 0.7200, "round_hard", "coat_l", size=0.008, press=2)
print("coat", s.stroke_count - n); n = s.stroke_count

# the man on the right
s.stroke([(0.766, 0.312), (0.828, 0.314)], "bristle", "deep", size=0.028)
s.dab(0.802, 0.372, "round_hard", "face2", size=0.044)
s.stroke([(0.786, 0.402), (0.824, 0.406)], "bristle", "bgL", size=0.016)
s.stroke([(0.838, 0.428), (0.870, 0.488), (0.878, 0.534)], "bristle", "red_pat",
         size=0.042, load=0.8)
print("right man", s.stroke_count - n); n = s.stroke_count

# the carton, restated over the speckle, duller
carton = polygon([(0.156, 0.790), (0.172, 0.756), (0.224, 0.748), (0.257, 0.772),
                  (0.255, 1.000), (0.154, 1.000)])
s.block_in(carton, "flat", "cartn2", direction="axis", density=1.0, size=0.085, load=1.0)
s.stroke([(0.2380, 0.7560), (0.2400, 0.7950)], "flat", "capwh", size=0.020,
         pressure="even")
print("carton", s.stroke_count - n)

print("total:", s.stroke_count)
print(s.look(reference="ref.jpg"))
