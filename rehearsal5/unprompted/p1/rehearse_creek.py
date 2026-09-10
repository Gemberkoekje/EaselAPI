p = s.palette
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["trough"] = to_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.29)
p["thread"] = to_value(p.mix("cerulean", "burnt_sienna", 0.22), 0.60)
p["glint"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.20), 0.84)

path_n = [(0.874, 0.612), (0.836, 0.686), (0.800, 0.790), (0.772, 0.920), (0.758, 1.02)]
path_m = [(0.852, 0.449), (0.862, 0.500), (0.884, 0.548), (0.874, 0.616)]
path_f = [(0.985, 0.383), (0.936, 0.402), (0.884, 0.424), (0.852, 0.452)]

bury = [
    dict(points=[(0.905, 0.600), (0.866, 0.690), (0.828, 0.800), (0.796, 0.960),
                 (0.784, 1.03)], brush="bristle", color="mud_near", size=0.075,
         pressure="even", load=1.0, label="bury near R"),
    dict(points=[(0.845, 0.615), (0.808, 0.700), (0.774, 0.805), (0.746, 0.935),
                 (0.734, 1.03)], brush="bristle", color="mud_near", size=0.070,
         pressure="even", load=1.0, label="bury near L"),
    dict(points=[(0.858, 0.440), (0.868, 0.500), (0.890, 0.552), (0.880, 0.625)],
         brush="bristle", color="mud_far", size=0.048, pressure="even", load=1.0,
         label="bury mid R"),
    dict(points=[(0.840, 0.446), (0.850, 0.502), (0.872, 0.550), (0.862, 0.622)],
         brush="bristle", color="mud_far", size=0.044, pressure="even", load=1.0,
         label="bury mid L"),
    dict(points=[(0.990, 0.372), (0.938, 0.394), (0.886, 0.416), (0.852, 0.444)],
         brush="bristle", color="sheen", size=0.034, pressure="even", load=1.0,
         label="bury far"),
]
relay = [
    dict(points=path_n, brush="bristle", color="trough", size=0.030,
         pressure="even", load=1.0, label="trough"),
    dict(points=[(0.884, 0.628), (0.852, 0.700), (0.822, 0.792)], brush="round_hard",
         color="thread", size=0.006, pressure=[0.9, 0.2], label="lip near"),
    dict(points=path_m, brush="bristle", color="thread", size=0.016,
         pressure="even", load=1.0, label="mid water"),
    dict(points=[(0.856, 0.470), (0.870, 0.522), (0.886, 0.556)], brush="round_hard",
         color="glint", size=0.007, pressure=[0.3, 1.0, 0.4], label="mid glint"),
    dict(points=path_f, brush="round_hard", color="glint", size=0.009,
         pressure=[1.0, 0.55], label="far glint"),
]
print(s.rehearse(bury + relay, region=span("F4", "H8")))
print(s.rehearse(bury + relay))
