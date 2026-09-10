import random
rng = random.Random(127)
p = s.palette
s.dry()
SZ = 0.036
left  = polygon([(-0.06, 0.672), (0.238, 0.664), (0.246, 0.720), (0.286, 0.790),
                 (0.316, 0.846), (0.330, 0.912), (-0.06, 0.912)])
right = polygon([(0.552, 0.660), (1.06, 0.646), (1.06, 0.912), (0.486, 0.912),
                 (0.490, 0.848), (0.506, 0.790), (0.526, 0.738), (0.542, 0.694)])
under = polygon([(0.24, 0.856), (0.56, 0.850), (0.56, 0.912), (0.24, 0.912)])
for shp in (left, right, under):
    s.block_in(shp.inset(0.014), "flat", "sill", direction=(-2, 25), density=1.0,
               size=SZ, load=1.0)

# the pale slabs still sitting on the back of the sill
for x, y in [(0.13, 0.652), (0.505, 0.648), (0.815, 0.642)]:
    for k in range(4):
        yy = y + (k - 1.5) * 0.009
        s.stroke([(x - 0.075, yy + 0.010), (x + 0.075, yy - 0.009)], "bristle",
                 rng.choice(["sill", "sill_b", "sill_d"]), size=0.014,
                 pressure="even", load=1.0, load_falloff=0.15)

# grain back into the reset board
for i in range(16):
    x0 = rng.choice([rng.uniform(-0.08, 0.16), rng.uniform(0.56, 0.98)])
    y = rng.uniform(0.690, 0.884)
    L = rng.uniform(0.08, 0.26)
    a, b = (x0, y), (x0 + L, y - rng.uniform(0.003, 0.022))
    if i % 2: a, b = b, a
    s.stroke([a, b], "bristle", rng.choice(["sill_a", "sill_b", "sill_c", "sill_d"]),
             size=rng.choice([0.014, 0.022, 0.030]), pressure=rng.choice(["even", "taper"]),
             load=rng.uniform(0.42, 0.8), load_falloff=0.18)

# the cast shadow again - broken edges from the brush, no smudging
s.block_in(polygon([(0.46, 0.792), (0.66, 0.802), (0.88, 0.810), (1.06, 0.816),
                    (1.06, 0.874), (0.86, 0.868), (0.62, 0.854), (0.45, 0.840)]).inset(0.011),
           "bristle", "shad_f", direction=(4, -9), density=1.0, size=0.024, load=0.9)
s.block_in(polygon([(0.47, 0.798), (0.62, 0.808), (0.76, 0.818),
                    (0.74, 0.850), (0.60, 0.844), (0.46, 0.832)]).inset(0.008),
           "bristle", "shad", direction=(5, -11), density=1.0, size=0.016, load=1.0)
s.stroke([(0.318, 0.824), (0.398, 0.846), (0.474, 0.826)], "round_hard", "contact",
         size=0.015, pressure=[0.5, 1.0, 0.85], load=1.0)
s.stroke([(0.462, 0.814), (0.522, 0.820)], "round_hard", "contact",
         size=0.010, pressure=[0.9, 0.15], load=1.0)
print("strokes:", s.stroke_count)
print(s.look())
