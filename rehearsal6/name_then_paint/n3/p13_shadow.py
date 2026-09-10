import math, random
rng = random.Random(109)
p = s.palette
s.dry()

# repaint the band of sill to the right of the cup, killing the old blue ribbon
band = polygon([(0.548, 0.650), (1.06, 0.630), (1.06, 0.910), (0.492, 0.910),
                (0.492, 0.850), (0.500, 0.796), (0.524, 0.748), (0.540, 0.698)])
s.block_in(band.inset(0.012), "flat", "sill", direction=(-2, 26), density=1.0,
           size=0.055, load=1.0)
for i in range(9):                      # give it back its grain
    y = 0.672 + rng.uniform(0, 0.20)
    x0 = 0.52 + rng.uniform(0.0, 0.30)
    L = rng.uniform(0.09, 0.30)
    a, b = (x0, y), (min(x0 + L, 1.08), y - rng.uniform(0.004, 0.020))
    if i % 2: a, b = b, a
    s.stroke([a, b], "bristle", rng.choice(["sill_a", "sill_b", "sill_c", "sill_d"]),
             size=rng.choice([0.016, 0.024, 0.032]), pressure="even",
             load=rng.uniform(0.45, 0.8), load_falloff=0.15)

# the cast shadow: soft, warm-grey, hardest where it meets the cup
s.block_in(polygon([(0.44, 0.790), (0.64, 0.802), (0.86, 0.812), (1.06, 0.818),
                    (1.06, 0.878), (0.84, 0.870), (0.60, 0.854), (0.43, 0.838)]).inset(0.012),
           "bristle", "shad_f", direction=(4, -10), density=1.0, size=0.026, load=0.95)
s.block_in(polygon([(0.45, 0.796), (0.60, 0.808), (0.74, 0.818),
                    (0.72, 0.852), (0.58, 0.844), (0.44, 0.830)]).inset(0.009),
           "bristle", "shad", direction=(5, -12), density=1.0, size=0.018, load=1.0)

# where the cup meets the board
s.stroke([(0.322, 0.822), (0.398, 0.844), (0.470, 0.826)], "round_hard", "contact",
         size=0.016, pressure=[0.5, 1.0, 0.8], load=1.0)
s.stroke([(0.452, 0.812), (0.508, 0.816)], "round_hard", "contact",
         size=0.011, pressure=[0.9, 0.2], load=1.0)

for a, b in [((0.92, 0.822), (0.98, 0.836)), ((0.78, 0.868), (0.84, 0.860)),
             ((0.66, 0.800), (0.72, 0.810)), ((0.56, 0.858), (0.62, 0.850))]:
    s.smudge([a, b], size=0.036)

print("strokes:", s.stroke_count)
print(s.look())
