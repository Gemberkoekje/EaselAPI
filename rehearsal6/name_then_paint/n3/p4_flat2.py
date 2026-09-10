import random
rng = random.Random(23)
p = s.palette
def cool(ratio, t):
    return p.tint(p.mix("ultramarine", "burnt_sienna", ratio), t)

p["sky"]   = cool(0.44, 0.885)
p["sky_c"] = cool(0.37, 0.862)
p["sky_w"] = cool(0.52, 0.912)
p["sky_h"] = cool(0.58, 0.938)
for n in ("sky_c", "sky", "sky_w", "sky_h"):
    print(f"{n:6s} {p.hex(p[n])}  v={p.value_of(p[n]):.3f}")

s.dry()
s.block_in(span("A1", "H6"), "flat", "sky", direction=(-22, 58),
           density=1.0, size=0.20, load=1.0)

def veil(colour, y_lo, y_hi, n, sizes, slope):
    """long shallow passes that begin and end off the canvas, so no end shows"""
    for i in range(n):
        y = y_lo + (y_hi - y_lo) * (i / (n - 1.0)) + rng.uniform(-0.025, 0.025)
        d = rng.uniform(0.7, 1.3) * slope
        a, b = (-0.18, y), (1.18, y + d)
        if i % 2:
            a, b = b, a
        s.stroke([a, b], "flat", colour, size=rng.choice(sizes),
                 pressure="even", load=1.0, load_falloff=0.10)

veil("sky_w", 0.68, 0.26, 9, [0.17, 0.13, 0.20, 0.11], -0.12)
veil("sky_c", 0.30, -0.05, 6, [0.15, 0.19, 0.12], -0.16)
veil("sky_h", 0.62, 0.46, 4, [0.12, 0.09, 0.15], -0.09)
print("strokes:", s.stroke_count)
print(s.look())
