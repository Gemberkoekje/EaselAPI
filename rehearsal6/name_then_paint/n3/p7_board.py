import random
rng = random.Random(53)
p = s.palette

def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if p.value_of(p.tint(base, mid)) < target: lo = mid
        else: hi = mid
    return p.tint(base, (lo + hi) / 2)

wood  = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.44), 0.60)
cool  = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.38), 0.30)
board = p.mix(wood, cool, 0.30)

p["sill"]   = at_value(board, 0.470)
p["sill_a"] = at_value(p.mix(board, wood, 0.6), 0.525)
p["sill_b"] = at_value(p.mix(board, cool, 0.5), 0.425)
p["sill_c"] = at_value(board, 0.585)
p["sill_d"] = at_value(p.mix(board, cool, 0.8), 0.380)
for n in ("sill_d", "sill_b", "sill", "sill_a", "sill_c"):
    print(f"{n:7s} {p.hex(p[n])}  v={p.value_of(p[n]):.3f}")

s.dry()
top = polygon([(-0.05, 0.648), (1.05, 0.630), (1.05, 0.884), (-0.05, 0.906)])
s.block_in(top, "flat", "sill", direction=(-1.6, 27), density=1.0, size=0.105, load=1.0)

# grain: long broken passes that run off both edges, dry brush so they break
for i in range(6):
    y = 0.676 + i * 0.036 + rng.uniform(-0.010, 0.010)
    col = "sill_a" if i % 2 == 0 else "sill_b"
    a, b = (-0.15, y), (1.15, y - rng.uniform(0.010, 0.024))
    if i % 2: a, b = b, a
    s.stroke([a, b], "bristle", col, size=rng.choice([0.022, 0.034, 0.016]),
             pressure="even", load=rng.uniform(0.42, 0.58), load_falloff=0.05)

# worn patches, each at its own angle, low contrast
for i in range(14):
    x = rng.uniform(0.02, 0.99)
    y = rng.uniform(0.678, 0.862)
    lit = rng.random() < (0.82 - 0.60 * x)
    col = rng.choice(["sill_a", "sill_c"]) if lit else rng.choice(["sill_b", "sill_d"])
    L = rng.uniform(0.05, 0.17)
    ang = rng.uniform(-0.55, 0.35)
    s.stroke([(x - L/2, y - ang*L/2), (x + L/2, y + ang*L/2)], "bristle", col,
             size=rng.choice([0.018, 0.026, 0.034]), pressure=rng.choice(["taper","even","lift_off"]),
             load=rng.uniform(0.45, 0.75), load_falloff=0.25)

# break the sill's back edge: glare spilling down over it, sill biting up into it
for x, y, sz in [(0.13, 0.652, 0.030), (0.52, 0.646, 0.024), (0.79, 0.640, 0.020)]:
    s.stroke([(x - 0.05, y - 0.012), (x + 0.06, y + 0.010)], "flat", "sky_w",
             size=sz, pressure="taper", load=0.8)
for x, y in [(0.31, 0.638), (0.66, 0.630), (0.93, 0.626)]:
    s.stroke([(x - 0.04, y + 0.008), (x + 0.05, y - 0.006)], "bristle", "sill_b",
             size=0.016, pressure="taper", load=0.7)

print("strokes:", s.stroke_count)
print(s.look())
