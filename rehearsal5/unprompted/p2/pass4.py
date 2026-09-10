p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["rent_a"] = p.desaturate(to_value(p.mix("cerulean", "burnt_sienna", 0.15), 0.82), 0.25)
p["rent_b"] = p.desaturate(to_value(p.mix("cerulean", "alizarin", 0.20), 0.70), 0.30)
p["rent_c"] = p.desaturate(to_value(p.mix("yellow_ochre", "cadmium_red", 0.22), 0.74), 0.22)
p["rent_d"] = p.desaturate(to_value(p.mix("cerulean", "burnt_umber", 0.35), 0.55), 0.30)
for n in ("rent_a", "rent_b", "rent_c", "rent_d"):
    print(f"{n} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

s.dry()

L1 = hull([(0.618, 0.108), (0.672, 0.056), (0.752, 0.082), (0.760, 0.148),
           (0.700, 0.186), (0.634, 0.166)])
L2 = blob((0.576, 0.264), 0.066, 0.050, wobble=0.45, seed=21)
L3 = hull([(0.404, 0.360), (0.482, 0.352), (0.512, 0.406), (0.460, 0.452),
           (0.398, 0.428)])
L4 = blob((0.322, 0.524), 0.046, 0.036, wobble=0.45, seed=23)
L5 = blob((0.238, 0.646), 0.030, 0.024, wobble=0.45, seed=25)
BR = hull([(0.560, 0.296), (0.664, 0.330), (0.742, 0.392), (0.630, 0.384),
           (0.556, 0.344)])
BL = hull([(0.556, 0.212), (0.478, 0.168), (0.418, 0.184), (0.500, 0.232)])
I1 = blob((0.302, 0.806), 0.036, 0.026, wobble=0.42, seed=7)
I2 = blob((0.786, 0.548), 0.022, 0.016, wobble=0.42, seed=11)
I3 = blob((0.148, 0.372), 0.030, 0.021, wobble=0.42, seed=13)

# dimmest first, brightest last, so the light stays clean
for sh, col, sz in ((I3, "rent_d", 0.011), (I2, "rent_d", 0.009), (I1, "rent_d", 0.012),
                    (L5, "rent_d", 0.012), (BL, "rent_b", 0.020), (L4, "rent_b", 0.018),
                    (BR, "rent_c", 0.024), (L3, "rent_b", 0.024), (L2, "rent_a", 0.026),
                    (L1, "rent_a", 0.030)):
    s.block_in(sh, "bristle", col, direction="axis", density=1.0, size=sz,
               load=1.0, pressure="even")

# the necks between the pools - one stroke each, running along the chain
s.stroke([(0.658, 0.170), (0.622, 0.212)], "bristle", "rent_b", size=0.022,
         load=1.0, pressure="swell")
s.stroke([(0.540, 0.312), (0.500, 0.348)], "bristle", "rent_b", size=0.018,
         load=1.0, pressure="swell")
s.stroke([(0.412, 0.438), (0.368, 0.482)], "bristle", "rent_b", size=0.014,
         load=0.9, pressure="swell")
s.stroke([(0.292, 0.560), (0.258, 0.614)], "bristle", "rent_d", size=0.011,
         load=0.9, pressure="taper")
s.stroke([(0.222, 0.676), (0.192, 0.732), (0.170, 0.784)], "bristle", "rent_d",
         size=0.008, load=0.85, pressure="lift_off")

print("strokes", s.stroke_count)
print(s.look())
