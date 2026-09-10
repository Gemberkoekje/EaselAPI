REF = "C:/temp/Level1.jpg"
p = s.palette
WARM_DARK = p.mix("ultramarine", "burnt_umber", 0.72)

def val(target, base):
    other = "titanium_white" if p.value_of(base) < target else WARM_DARK
    up = p.value_of(base) < target
    lo, hi = 0.0, 1.0
    for _ in range(26):
        mid = (lo + hi) / 2
        if (p.value_of(p.mix(base, other, mid)) < target) == up:
            lo = mid
        else:
            hi = mid
    return p.mix(base, other, (lo + hi) / 2)

p["tag"] = val(0.150, p.mix("ultramarine", "burnt_umber", 0.30))
print("tag", p.hex(p["tag"]), round(p.value_of(p["tag"]), 3))

# cross the columns: that is what closes a mass up
for y, x0, x1, size in [(0.436, 0.376, 0.500, 0.046),
                        (0.497, 0.370, 0.505, 0.048),
                        (0.556, 0.372, 0.503, 0.046),
                        (0.586, 0.378, 0.498, 0.030)]:
    s.stroke([(x0, y), (x1, y - 0.004)], "round_hard", "fig_dark",
             size=size, pressure="even", load=1.0, note="close the crewmate")
s.stroke([(0.516, 0.492), (0.552, 0.496)], "round_hard", "fig_pack",
         size=0.046, pressure="even", load=1.0, note="close the backpack")
print("figure", s.stroke_count)

# the teabag tag on the table
s.stroke([(0.828, 0.562), (0.898, 0.578)], "round_hard", "tag",
         size=0.045, pressure="even", load=1.0, note="tag")
s.stroke([(0.822, 0.612), (0.892, 0.626)], "round_hard", "tag",
         size=0.042, pressure="even", load=1.0, note="tag")
s.dab(0.845, 0.596, "round_hard", "mug_spec", size=0.010, press=3)
print("tag", s.stroke_count)

# the few lights that are allowed to be sharp
s.stroke([(0.330, 0.180), (0.372, 0.148), (0.428, 0.128), (0.492, 0.126)],
         "round_hard", "mug_hi", size=0.013, pressure="swell", load=1.0,
         note="rim light")
s.stroke([(0.362, 0.312), (0.420, 0.340), (0.478, 0.347), (0.540, 0.334)],
         "round_hard", "mug_spec", size=0.010, pressure="swell", load=1.0,
         note="lip light")
s.stroke([(0.586, 0.468), (0.592, 0.540), (0.578, 0.588)], "round_hard",
         "mug_spec", size=0.011, pressure="swell", load=1.0, note="specular")
s.dab(0.708, 0.392, "round_hard", "mug_spec", size=0.011, press=3)
print("lights", s.stroke_count)

print(s.look(reference=REF))
print(s.look(region=span("C3", "F6"), reference=REF))
print(s.compare(REF))
