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

p["wall_58"] = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.20), 0.60)
p["wall_44"] = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.36), 0.46)
p["deep"]    = p.mix("ultramarine", "burnt_umber", 0.55)
p["lowdark"] = to_value(p.mix(p["deep"], "burnt_sienna", 0.30), 0.18)
p["cartn"]   = to_value(p.mix("cadmium_red", "cadmium_yellow", 0.58), 0.50)
p["glass"]   = to_value(p.desaturate(p.mix("viridian", "yellow_ochre", 0.45), 0.45), 0.36)
p["phone"]   = to_value(p.desaturate(p.mix("ultramarine", "yellow_ochre", 0.55), 0.55), 0.32)

s.dry()

# lit wall, right — the coat's spill ate it
s.block_in(span("H2", "H3"), "flat", "wall_58", direction=98, size=0.10,
           density=1.0, load=1.0)
s.block_in(cell("H2"), "flat", "wall_h", direction=88, size=0.08,
           density=1.0, load=1.0)

# re-cut the shoulder: background painted back down TO the coat's edge
wedge = polygon([(0.722, 0.376), (0.878, 0.376), (0.878, 0.585), (0.845, 0.556),
                 (0.806, 0.498), (0.762, 0.440)])
s.block_in(wedge, "flat", "rightbg", direction="axis", density=1.0,
           size=0.075, load=1.0)

# deep shadow behind the raised hand
s.block_in(span("C2", "C3"), "flat", "deep", direction=22, size=0.10,
           density=1.0, load=1.0)

# lower left: dark below the far figures, light on the table front
s.block_in(span("A6", "C7"), "flat", "lowdark", direction=-8, size=0.12,
           density=1.0, load=1.0)
s.block_in(span("A8", "C8"), "flat", "glass", direction=-5, size=0.10,
           density=0.9, load=1.0)

# warm ceiling band, top left
s.block_in(span("A1", "C1"), "flat", "wall_44", direction=6, size=0.10,
           density=0.95, load=1.0)
s.block_in(ribbon([(0.128, 0.010), (0.140, 0.250)], 0.055), "flat", "wall_58",
           direction="axis", density=1.0, size=0.05, load=1.0)   # lit post

print("bg fixes:", s.stroke_count)
print(s.look(reference="ref.jpg"))
