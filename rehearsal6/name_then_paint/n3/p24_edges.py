import math, random
rng = random.Random(379)
p = s.palette
def at_value(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.tint(base, m)) < target: lo=m
        else: hi=m
    return p.tint(base, (lo+hi)/2)
G = p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.48), 0.28)
p["burn"] = at_value(G, 0.912)
p["burn2"]= at_value(G, 0.888)
s.dry()

# the light burning round the cup's left shoulder
for i in range(7):
    y = 0.470 + i * 0.017 + rng.uniform(-0.005, 0.005)
    xe = 0.243 if y > 0.553 else 0.31
    s.stroke([(-0.16, y + 0.012), (0.08, y), (xe, y - 0.006)], "round_hard",
             "burn" if i % 2 else "burn2", size=rng.choice([0.026, 0.038, 0.019]),
             pressure=[1.0, 0.92, 0.08], load=1.0)
for i in range(4):
    y = 0.575 + i * 0.016
    s.stroke([(-0.14, y), (0.06, y - 0.003), (0.246, y - 0.008)], "round_hard",
             "burn", size=rng.choice([0.020, 0.030]), pressure=[1.0, 0.9, 0.06], load=1.0)

# sharpen the cup's lit edge by laying the light up to it, centre just outside
for dx, sz, col in [(-0.009, 0.016, "burn"), (-0.017, 0.012, "burn2")]:
    s.stroke([(0.296 + dx, 0.578), (0.262 + dx, 0.604), (0.251 + dx, 0.632),
              (0.262 + dx, 0.668)], "round_hard", col, size=sz,
             pressure=[0.25, 1.0, 0.9, 0.2], load=1.0)

# quiet the noisy join at the back of the board
for x, y, L, sz in [(0.075, 0.664, 0.16, 0.020), (0.185, 0.658, 0.12, 0.015),
                    (0.645, 0.652, 0.15, 0.018), (0.845, 0.646, 0.17, 0.022),
                    (0.960, 0.642, 0.11, 0.014)]:
    s.stroke([(x - L/2, y + 0.006), (x + L/2, y - 0.005)], "bristle",
             rng.choice(["sill", "sill_b"]), size=sz, pressure="taper",
             load=rng.uniform(0.75, 1.0), load_falloff=0.25)

# lose the cup's shadow-side edge into the board
s.smudge([(0.533, 0.648), (0.528, 0.672)], size=0.030)
s.smudge([(0.512, 0.742), (0.502, 0.768)], size=0.028)
s.smudge([(0.331, 0.822), (0.352, 0.830)], size=0.026)
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(region="B4:G8", sketch=False))
