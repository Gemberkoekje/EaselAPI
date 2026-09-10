import random

p = s.palette
rng = random.Random(41)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


p["post"] = to_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.20)
p["post_lit"] = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.40), 0.52)
p["wet"] = to_value(p.mix("burnt_sienna", "cerulean", 0.40), 0.66)
p["wet2"] = to_value(p.mix("yellow_ochre", "cadmium_red", 0.30), 0.71)

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

# a line of rotting withies stepping back toward the horizon
POSTS = [(0.930, 0.822, 0.112, 0.014, 0.010),
         (0.879, 0.716, 0.082, 0.011, -0.014),
         (0.851, 0.641, 0.061, 0.009, 0.006),
         (0.816, 0.564, 0.038, 0.007, 0.009),
         (0.799, 0.522, 0.031, 0.006, -0.005),
         (0.766, 0.463, 0.018, 0.005, 0.003),
         (0.752, 0.437, 0.013, 0.004, -0.002)]
posts = []
for x, y, h, w, lean in POSTS:
    posts.append(dict(points=[(x, y), (x + lean, y - h)], brush="round_hard",
                      color="post", size=w, pressure=[1.0, 0.7], label="post"))
for x, y, h, w, lean in POSTS[:3]:
    posts.append(dict(points=[(x + w * 0.5, y - h * 0.15), (x + lean + w * 0.4, y - h * 0.8)],
                      brush="round_hard", color="post_lit", size=w * 0.42,
                      pressure=[0.4, 1.0, 0.5], label="post lit"))
for x, y, h, w, lean in POSTS[:4]:
    posts.append(dict(points=[(x - w * 1.6, y + h * 0.035), (x + w * 3.4, y + h * 0.055)],
                      brush="bristle", color="post", size=w * 0.9, load=0.65,
                      pressure="lift_off", label="post foot"))

# broad thin sheets of water lying on the flats
sheets = []
for cx, cy, ln, sz, col in [(0.255, 0.463, 0.190, 0.020, "wet"),
                            (0.470, 0.447, 0.150, 0.015, "wet2"),
                            (0.360, 0.492, 0.230, 0.026, "wet"),
                            (0.630, 0.470, 0.135, 0.017, "wet2"),
                            (0.135, 0.508, 0.145, 0.022, "wet"),
                            (0.560, 0.517, 0.175, 0.024, "wet")]:
    dy = rng.uniform(-0.008, 0.008)
    sheets.append(dict(points=[(cx - ln / 2, cy), (cx, cy + dy), (cx + ln / 2, cy + dy / 2)],
                       brush="bristle", color=col, size=sz, load=rng.uniform(0.5, 0.8),
                       pressure="swell", label="sheet"))

print(s.rehearse(bury + posts + sheets, region=span("E4", "H8")))
print(s.rehearse(bury + posts + sheets))
