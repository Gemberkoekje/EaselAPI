p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["flank"] = to_value(p.mix("burnt_umber", "ultramarine", 0.22), 0.23)
p["shadow"] = to_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.27)

s.dry()

# kill the speckled film - stopping short of x=0.80 so the withies survive
fix = polygon([(0.00, 0.762), (0.13, 0.744), (0.27, 0.766), (0.41, 0.748),
               (0.55, 0.772), (0.68, 0.752), (0.795, 0.775),
               (0.795, 1.010), (0.00, 1.010)])
s.block_in(fix, "bristle", "mud_near", direction=-6, density=1.0,
           size=0.085, load=1.0, load_falloff=0.22, pressure="even")

# a solid shadow on the mud, softened after - not a low-load scumble
s.block_in(ellipse((0.398, 0.797), 0.205, 0.026), "flat", "shadow",
           direction="axis", density=1.0, size=0.016, load=1.0, pressure="even")
s.smudge([(0.235, 0.812), (0.300, 0.822)], size=0.040)
s.smudge([(0.520, 0.810), (0.585, 0.800)], size=0.040)

# the near flank again, solid, with a brush that keeps the silhouette
flank = polygon([(0.220, 0.672), (0.300, 0.684), (0.420, 0.699), (0.520, 0.700),
                 (0.572, 0.678), (0.592, 0.706), (0.578, 0.742), (0.500, 0.780),
                 (0.410, 0.788), (0.300, 0.762), (0.235, 0.716), (0.208, 0.678)])
s.block_in(flank, "flat", "flank", direction="axis", density=1.0,
           size=0.020, load=1.0, pressure="even")

print("total", s.stroke_count)
print(s.look(region=span("A5", "H8")))
