import random
rng = random.Random(41)
p = s.palette

def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if p.value_of(p.tint(base, mid)) < target: lo = mid
        else: hi = mid
    return p.tint(base, (lo + hi) / 2)

wood  = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.46), 0.42)
stone = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.36), 0.22)

p["sill"]     = at_value(wood, 0.470)
p["sill_lit"] = at_value(wood, 0.575)
p["sill_dk"]  = at_value(p.mix(wood, stone, 0.5), 0.395)
p["ledge"]    = at_value(stone, 0.265)
p["ledge_lo"] = at_value(p.mix(stone, "burnt_umber", 0.45), 0.205)
p["rail"]     = at_value(p.desaturate(wood, 0.5), 0.340)
for n in ("ledge_lo", "ledge", "rail", "sill_dk", "sill", "sill_lit"):
    print(f"{n:9s} {p.hex(p[n])}  v={p.value_of(p[n]):.3f}")

s.dry()
# one dark below, one mid above: two masses, not four stripes
s.block_in(polygon([(-0.05, 0.878), (1.05, 0.856), (1.05, 1.06), (-0.05, 1.06)]),
           "flat", "ledge", direction=(-1.4, 30), density=1.0, size=0.075, load=1.0)
s.block_in(polygon([(-0.05, 0.958), (1.05, 0.940), (1.05, 1.06), (-0.05, 1.06)]),
           "flat", "ledge_lo", direction=(-1.2, 26), density=1.0, size=0.045, load=1.0)
s.block_in(polygon([(-0.05, 0.648), (1.05, 0.630), (1.05, 0.884), (-0.05, 0.906)]),
           "flat", "sill", direction=(-1.6, 27), density=1.0, size=0.105, load=1.0)

# worn board: patches, at their own angles, not full-width stripes
for i in range(16):
    x = rng.uniform(0.02, 0.98)
    y = rng.uniform(0.690, 0.860)
    lit = rng.random() < (0.80 - 0.55 * x)          # light rakes in from the left
    col = "sill_lit" if lit else "sill_dk"
    L = rng.uniform(0.06, 0.22)
    ang = rng.uniform(-0.16, 0.10)
    sz = rng.choice([0.030, 0.045, 0.060, 0.022])
    s.stroke([(x - L / 2, y - ang * L / 2), (x + L / 2, y + ang * L / 2)],
             "round_hard", col, size=sz, pressure="even", load=1.0, load_falloff=0.3)

# the window rail behind the sill, right side only, dying away to the left
s.block_in(polygon([(0.38, 0.640), (1.05, 0.604), (1.05, 0.652), (0.44, 0.664)]),
           "flat", "rail", direction=(-3, 24), density=1.0, size=0.030, load=1.0)

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
