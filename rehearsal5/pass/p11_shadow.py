REF = "C:/temp/Level1.jpg"
p = s.palette

def dv(base, target, dark):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if p.value_of(p.mix(base, dark, mid)) > target:
            lo = mid
        else:
            hi = mid
    return p.mix(base, dark, (lo + hi) / 2)

warm_dark = p.mix("ultramarine", "burnt_umber", 0.72)
wood = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.38), 0.22)
p["shad_pen"]   = dv(wood, 0.315, warm_dark)
p["shad_core"]  = dv(wood, 0.180, warm_dark)
p["shad_heart"] = warm_dark
for n in ("shad_pen", "shad_core", "shad_heart"):
    print(f"{n:<11} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")

core = polygon([(0.400, 0.545), (0.345, 0.600), (0.316, 0.668), (0.336, 0.755),
                (0.388, 0.815), (0.443, 0.843), (0.505, 0.826), (0.560, 0.766),
                (0.594, 0.690), (0.614, 0.600), (0.600, 0.545)])

s.block_in(core.scaled(1.09).inset(0.040), "flat", "shad_pen", direction=18,
           density=0.8, size=0.080, load=1.0, note="penumbra")
print("pen", s.stroke_count)

s.block_in(core.inset(0.042), "flat", "shad_core", direction=25,
           density=0.85, size=0.085, load=1.0, note="shadow core")
print("core", s.stroke_count)

heart = ellipse(span("C6", "E6")).scaled(0.82).shifted(0.012, 0.012)
s.block_in(heart.inset(0.026), "flat", "shad_heart", direction=-8,
           density=0.9, size=0.052, load=1.0, note="shadow heart")
print("heart", s.stroke_count)

ring = ribbon([(0.607, 0.548), (0.655, 0.520), (0.702, 0.545),
               (0.714, 0.580), (0.678, 0.602), (0.632, 0.592)], 0.030)
s.block_in(ring, "flat", "shad_pen", direction="axis", density=0.9,
           size=0.020, load=1.0, note="handle shadow ring")
print("ring", s.stroke_count)

print(s.look(reference=REF))
print(s.look(region=span("C5", "G7"), reference=REF))
print(s.compare(REF))
