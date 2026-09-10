import random
rng = random.Random(31)
p = s.palette

def at_value(base, target):          # tint ratio that reads `target`
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if p.value_of(p.tint(base, mid)) < target: lo = mid
        else: hi = mid
    return p.tint(base, (lo + hi) / 2)

wood  = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.48), 0.34)
stone = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.34), 0.20)

p["sill_lit"]  = at_value(wood, 0.545)
p["sill_mid"]  = at_value(p.desaturate(wood, 0.25), 0.435)
p["sill_back"] = at_value(stone, 0.395)
p["sill_face"] = at_value(stone, 0.300)
p["under"]     = at_value(p.mix(stone, "burnt_umber", 0.4), 0.215)
p["rail"]      = at_value(p.desaturate(wood, 0.45), 0.365)
for n in ("under", "sill_face", "rail", "sill_back", "sill_mid", "sill_lit"):
    print(f"{n:10s} {p.hex(p[n])}  v={p.value_of(p[n]):.3f}")

top  = polygon([(-0.05, 0.652), (1.05, 0.634), (1.05, 0.882), (-0.05, 0.902)])
face = polygon([(-0.05, 0.882), (1.05, 0.862), (1.05, 0.938), (-0.05, 0.962)])

# the rail of the window sitting behind the sill - strong right, gone left
s.block_in(polygon([(0.30, 0.628), (1.05, 0.604), (1.05, 0.652), (0.30, 0.664)]),
           "flat", "rail", direction=(-2, 26), density=1.0, size=0.035, load=1.0)

# the sill top: one mass, passes along its own run, crossed
s.block_in(top, "flat", "sill_mid", direction=(-1.5, 24), density=1.0, size=0.10, load=1.0)
# the light raking in from the left
for i in range(7):
    y = 0.672 + i * 0.030 + rng.uniform(-0.008, 0.008)
    a, b = (-0.12, y), (0.58 + rng.uniform(-0.10, 0.14), y - 0.014)
    if i % 2: a, b = b, a
    s.stroke([a, b], "flat", "sill_lit", size=rng.choice([0.055, 0.038, 0.070]),
             pressure="even", load=1.0, load_falloff=0.18)
# the cool dusty line where the sill meets the glass
s.block_in(polygon([(-0.05, 0.650), (1.05, 0.632), (1.05, 0.686), (-0.05, 0.706)]),
           "flat", "sill_back", direction=(-1.5, 20), density=0.95, size=0.030, load=1.0)

s.block_in(face, "flat", "sill_face", direction=(-1.2, 22), density=1.0, size=0.045, load=1.0)
s.block_in(polygon([(-0.05, 0.936), (1.05, 0.918), (1.05, 1.05), (-0.05, 1.05)]),
           "flat", "under", direction=(-1, 30), density=1.0, size=0.055, load=1.0)

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
