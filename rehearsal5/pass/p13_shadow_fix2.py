REF = "C:/temp/Level1.jpg"
p = s.palette

def tv(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if p.value_of(p.mix(base, "titanium_white", mid)) < target:
            lo = mid
        else:
            hi = mid
    return p.mix(base, "titanium_white", (lo + hi) / 2)

wood = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.38), 0.22)
print("wood raw value", round(p.value_of(wood), 3))     # the clamp that bit me
p["shad_pen"]  = tv(wood, 0.335)
p["shad_core"] = tv(wood, 0.170)
p["shad_ring"] = tv(wood, 0.350)
for n in ("shad_pen", "shad_core", "shad_ring", "shad_heart"):
    print(f"{n:<11} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")

core = polygon([(0.400, 0.545), (0.345, 0.600), (0.316, 0.668), (0.336, 0.755),
                (0.388, 0.815), (0.443, 0.843), (0.505, 0.826), (0.560, 0.766),
                (0.594, 0.690), (0.614, 0.600), (0.600, 0.545)])

s.dry()
s.block_in(core.scaled(1.14).inset(0.030), "flat", "shad_pen", direction=-20,
           density=0.85, size=0.065, load=1.0, note="penumbra 2")
print("pen", s.stroke_count)
s.block_in(core.inset(0.038), "flat", "shad_core", direction=32,
           density=1.0, size=0.078, load=1.0, note="shadow core 2")
print("core", s.stroke_count)

# a deeper pool where the mug meets the table - strokes, not a block, so it
# keeps a broken edge instead of a rectangle
for pts, size in [([(0.352, 0.640), (0.430, 0.672), (0.520, 0.660)], 0.052),
                  ([(0.540, 0.688), (0.450, 0.702), (0.360, 0.684)], 0.048),
                  ([(0.380, 0.718), (0.470, 0.728), (0.545, 0.712)], 0.040),
                  ([(0.500, 0.745), (0.430, 0.752), (0.395, 0.742)], 0.030)]:
    s.stroke(pts, "bristle", "shad_heart", size=size, load=1.0, pressure="swell",
             load_falloff=0.1, note="shadow pool")
print("pool", s.stroke_count)

# the fringe the dry strokes speckled, put wood back
for a, b, size in [((0.276, 0.612), (0.292, 0.790), 0.038),
                   ((0.404, 0.876), (0.520, 0.858), 0.034)]:
    s.stroke([a, b], "flat", "wood_field", size=size, pressure="even",
             load=1.0, load_falloff=0.0, note="clean fringe")

# the handle's cast shadow: three round marks, no axis to print
for pts, size in [([(0.598, 0.556), (0.618, 0.542), (0.645, 0.539), (0.668, 0.549)], 0.015),
                  ([(0.668, 0.549), (0.679, 0.566), (0.674, 0.586)], 0.013),
                  ([(0.672, 0.589), (0.650, 0.601), (0.622, 0.600), (0.603, 0.588)], 0.015)]:
    s.stroke(pts, "round_hard", "shad_ring", size=size, pressure="swell",
             load=1.0, note="handle shadow")
print("ring", s.stroke_count)

print(s.look(region=span("C5", "G7"), reference=REF))
print(s.look(reference=REF))
print(s.compare(REF))
