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

p["skin_h"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.15), 0.66)
p["hair_h"] = to_value(p.mix("yellow_ochre", "cadmium_yellow", 0.35), 0.68)
p["blur_l"] = to_value(p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.55), 0.4), 0.44)

s.dry()
n = s.stroke_count

# value corrections the table asked for
s.stroke([(0.018, 0.062), (0.112, 0.058)], "flat", "wall_m", size=0.095,
         pressure="even", load=1.0)
s.stroke([(0.018, 0.312), (0.112, 0.308)], "flat", "blur_l", size=0.095,
         pressure="even", load=1.0)
s.stroke([(0.136, 0.148), (0.141, 0.246)], "flat", "wall_l", size=0.052,
         pressure="even", load=1.0)
s.stroke([(0.148, 0.556), (0.204, 0.604)], "bristle", "lowdark", size=0.048,
         load=0.9)
s.stroke([(0.636, 0.792), (0.744, 0.808)], "flat", "coat", size=0.062,
         pressure="even", load=1.0)
s.stroke([(0.648, 0.856), (0.740, 0.862)], "flat", "coat", size=0.048,
         pressure="even", load=1.0)
s.stroke([(0.462, 0.390), (0.492, 0.418), (0.500, 0.448)], "flat", "skin_l",
         size=0.022, opacity=0.8, pressure="even")
s.stroke([(0.478, 0.372), (0.508, 0.386)], "flat", "skin_l", size=0.018,
         opacity=0.7, pressure="even")
print("corrections", s.stroke_count - n); n = s.stroke_count

# the last lights: few, deliberate
s.dab(0.4285, 0.2585, "round_hard", "skin_h", size=0.008, press=2)
s.dab(0.4108, 0.3648, "round_hard", "skin_h", size=0.005, press=2)
s.dab(0.4520, 0.4638, "round_hard", "teeth2", size=0.0034, press=3)
s.stroke([(0.548, 0.108), (0.598, 0.134)], "bristle", "hair_h", size=0.006)
s.smudge([(0.556, 0.086), (0.614, 0.124)], size=0.030)
print("lights", s.stroke_count - n)

print("total:", s.stroke_count)
print(s.look(reference="ref.jpg"))
print(s.compare("ref.jpg"))
