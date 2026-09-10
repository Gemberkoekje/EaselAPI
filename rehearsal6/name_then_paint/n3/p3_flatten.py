import random
rng = random.Random(11)
p = s.palette
def cool(ratio, t):
    return p.tint(p.mix("ultramarine", "burnt_sienna", ratio), t)

p["sky"]     = cool(0.44, 0.878)     # the field
p["sky_c"]   = cool(0.36, 0.842)     # colder, top right
p["sky_w"]   = cool(0.54, 0.905)     # warmer/lighter, low left
p["sky_hot"] = cool(0.58, 0.946)
for n in ("sky_c", "sky", "sky_w", "sky_hot"):
    print(f"{n:8s} {p.hex(p[n])}  v={p.value_of(p[n]):.3f}")

s.dry()
# one flat field, crossed, big brush - kills the ring
s.block_in(span("A1", "H6"), "flat", "sky", direction=(-22, 58),
           density=1.0, size=0.20, load=1.0)

def band(colour, x0, x1, y0, y1, n, sizes, ang):
    for i in range(n):
        t = i / (n - 1.0)
        y = y0 + (y1 - y0) * t + rng.uniform(-0.02, 0.02)
        xa = x0 + rng.uniform(-0.05, 0.05)
        xb = x1 + rng.uniform(-0.06, 0.06)
        dy = (xb - xa) * ang
        if i % 2:
            xa, xb, dy = xb, xa, -dy
        s.stroke([(xa, y), (xb, y + dy)], "flat", colour,
                 size=rng.choice(sizes), pressure="even",
                 load=1.0, load_falloff=0.12)

band("sky_c", 0.46, 1.04, -0.02, 0.34, 7, [0.16, 0.12, 0.19], -0.13)
band("sky_w", -0.04, 0.62, 0.60, 0.30, 8, [0.15, 0.11, 0.18], -0.10)
band("sky_hot", -0.03, 0.34, 0.56, 0.44, 4, [0.10, 0.07, 0.13], -0.08)
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
