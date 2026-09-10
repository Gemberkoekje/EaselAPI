p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["blade"] = p.desaturate(to_value(p.mix("burnt_umber", "viridian", 0.35), 0.215), 0.45)
p["blade2"] = p.desaturate(to_value(p.mix("burnt_umber", "alizarin", 0.25), 0.185), 0.45)
p["blade_sh"] = to_value(p.mix("burnt_umber", "ultramarine", 0.45), 0.125)
p["blade_lt"] = p.desaturate(to_value(p.mix("yellow_ochre", "burnt_sienna", 0.30), 0.44), 0.35)

c_plan = [
    dict(points=[(0.352, 0.442), (0.436, 0.372), (0.528, 0.302), (0.622, 0.256),
                 (0.706, 0.234)], brush="round_hard", color="blade_sh", size=0.015,
         pressure=[0.15, 0.8, 1.0, 0.7, 0.1], label="C1 shadow"),
    dict(points=[(0.346, 0.436), (0.430, 0.364), (0.522, 0.294), (0.616, 0.248),
                 (0.702, 0.226)], brush="round_hard", color="blade", size=0.012,
         pressure=[0.2, 1.0, 0.9, 0.7, 0.15], label="C1 blade"),
    dict(points=[(0.624, 0.128), (0.578, 0.226), (0.536, 0.330), (0.506, 0.442)],
         brush="round_hard", color="blade2", size=0.010,
         pressure=[0.1, 0.9, 1.0, 0.2], label="C2 blade"),
    dict(points=[(0.452, 0.356), (0.520, 0.302), (0.586, 0.268)], brush="liner",
         color="blade_lt", size=0.0035, pressure=[0.2, 0.9, 0.3], label="C1 lit edge"),
]
print(s.rehearse(c_plan, region=span("C2", "G5")))
print(s.rehearse(c_plan))
