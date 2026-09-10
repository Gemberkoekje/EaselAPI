import math, random
rng = random.Random(347)
p = s.palette
s.dry()
left  = polygon([(-0.06, 0.668), (0.238, 0.660), (0.246, 0.720), (0.286, 0.790),
                 (0.316, 0.846), (0.330, 0.912), (-0.06, 0.912)])
right = polygon([(0.552, 0.656), (1.06, 0.642), (1.06, 0.912), (0.486, 0.912),
                 (0.490, 0.848), (0.506, 0.790), (0.526, 0.738), (0.542, 0.694)])
under = polygon([(0.24, 0.852), (0.56, 0.846), (0.56, 0.912), (0.24, 0.912)])
for shp in (left, right, under):
    s.block_in(shp.inset(0.016), "flat", "sill", direction=(-2, 25), density=1.0,
               size=0.040, load=1.0)

def streak(x, y, cols, ratio=(7, 14), sizes=(0.008, 0.011, 0.015), spread=0.55):
    sz = rng.choice(sizes); L = sz * rng.uniform(*ratio); a = rng.uniform(-spread, spread)
    dx, dy = L/2*math.cos(a), L/2*math.sin(a)*0.55
    s.stroke([(x-dx, y-dy), (x+dx, y+dy)], "bristle", rng.choice(cols), size=sz,
             pressure=rng.choice(["taper", "lift_off", "even"]),
             load=rng.uniform(0.5, 0.85), load_falloff=0.3)

# the board's back edge, biting up into the light
for x0, x1 in [(-0.05, 0.232), (0.562, 1.05)]:
    n = int((x1-x0)/0.052) + 1
    for i in range(n):
        x = x0 + (x1-x0)*i/max(1, n-1.0) + rng.uniform(-0.012, 0.012)
        y = 0.653 - 0.017*x + rng.uniform(-0.010, 0.008)
        streak(x, y, ["sill", "sill_b", "sill_a", "sill_d"],
               ratio=(5, 9), sizes=(0.012, 0.017, 0.023), spread=0.30)
# a dozen quiet marks of wear, well apart, each at its own angle
for x, y in [(0.085, 0.712), (0.155, 0.802), (0.045, 0.866), (0.196, 0.876),
             (0.665, 0.694), (0.742, 0.742), (0.905, 0.706), (0.958, 0.796),
             (0.836, 0.882), (0.628, 0.886), (0.402, 0.890), (0.118, 0.762),
             (0.980, 0.876), (0.700, 0.780)]:
    streak(x + rng.uniform(-0.02, 0.02), y + rng.uniform(-0.012, 0.012),
           ["sill_a", "sill_b", "sill_c", "sill_d"], ratio=(8, 16), spread=0.75)

s.block_in(polygon([(0.46, 0.792), (0.66, 0.802), (0.88, 0.810), (1.06, 0.816),
                    (1.06, 0.874), (0.86, 0.868), (0.62, 0.854), (0.45, 0.840)]).inset(0.011),
           "bristle", "shad_f", direction=(4, -9), density=1.0, size=0.022, load=0.92)
s.block_in(polygon([(0.452, 0.794), (0.560, 0.791), (0.648, 0.799), (0.668, 0.818),
                    (0.622, 0.842), (0.520, 0.844), (0.446, 0.834)]).inset(0.008),
           "bristle", "umbra", direction=(4, -12), density=1.0, size=0.014, load=1.0)
s.stroke([(0.318, 0.824), (0.398, 0.846), (0.476, 0.826)], "round_hard", "contact",
         size=0.015, pressure=[0.5, 1.0, 0.85], load=1.0)
s.stroke([(0.464, 0.812), (0.524, 0.818)], "round_hard", "contact",
         size=0.009, pressure=[0.9, 0.15], load=1.0)
print("strokes:", s.stroke_count)
print(s.look())
