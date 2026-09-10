p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["hull_far"] = to_value(p.mix("burnt_sienna", "cerulean", 0.45), 0.46)
p["gut"] = to_value(p.mix("ultramarine", "burnt_umber", 0.60), 0.15)
p["flank"] = to_value(p.mix("burnt_umber", "ultramarine", 0.30), 0.24)
p["shadow"] = to_value(p.mix("burnt_umber", "ultramarine", 0.40), 0.26)
for n in ("hull_far", "gut", "flank", "shadow", "mud_mid", "mud_near"):
    print(f"{n:9s} {p.hex(p[n])}  {p.value_of(p[n]):.2f}")

s.mark("bow", 0.203, 0.661)
s.mark("stern", 0.588, 0.684)

s.dry()

# the shadow on the mud goes first - it is behind the boat
s.block_in(ellipse(span("B7", "F7")).shifted(-0.055, 0.028).scaled(0.86), "bristle",
           "shadow", direction=8, density=0.6, size=0.060, load=0.55,
           pressure="even", opacity=0.55)

hull = polygon([(0.198, 0.645), (0.290, 0.628), (0.400, 0.626), (0.500, 0.640),
                (0.585, 0.663), (0.592, 0.706), (0.578, 0.742), (0.500, 0.780),
                (0.410, 0.788), (0.300, 0.762), (0.235, 0.716), (0.208, 0.678)])
inside = polygon([(0.226, 0.668), (0.290, 0.652), (0.400, 0.650), (0.500, 0.663),
                  (0.568, 0.682), (0.552, 0.694), (0.500, 0.704), (0.420, 0.701),
                  (0.300, 0.686), (0.234, 0.674)])
flank = polygon([(0.220, 0.672), (0.300, 0.684), (0.420, 0.699), (0.520, 0.700),
                 (0.572, 0.678), (0.592, 0.706), (0.578, 0.742), (0.500, 0.780),
                 (0.410, 0.788), (0.300, 0.762), (0.235, 0.716), (0.208, 0.678)])

# far edge, then what is inside, then the near edge
s.block_in(hull, "bristle", "hull_far", direction="axis", density=0.8,
           size=0.030, load=1.0, pressure="even")
s.block_in(inside, "flat", "gut", direction="axis", density=1.0,
           size=0.012, load=1.0, pressure="even")
s.block_in(flank, "bristle", "flank", direction="axis", density=0.9,
           size=0.022, load=1.0, pressure="even")

print("total", s.stroke_count)
print(s.look())
print(s.look(region=span("B5", "F8")))
