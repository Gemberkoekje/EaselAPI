import math, random
rng = random.Random(313)
p = s.palette
s.dry()

# ---- glass: veils that run right off the canvas, above the cup -------------
for i in range(6):
    y = 0.430 + i * 0.024 + rng.uniform(-0.008, 0.008)
    col = rng.choice(["sky_w", "sky_h", "sky_w", "sky"])
    a, b = (-0.20, y), (1.20, y - rng.uniform(0.004, 0.020))
    if i % 2: a, b = b, a
    s.stroke([a, b], "flat", col, size=rng.choice([0.055, 0.075, 0.040]),
             pressure="even", load=1.0, load_falloff=0.10)
# ---- glass beside the cup: marks that taper out before they reach it -------
for i in range(9):
    y = 0.552 + i * 0.011 + rng.uniform(-0.006, 0.006)
    s.stroke([(-0.16, y), (0.10, y + 0.004), (0.253, y - 0.004)], "round_hard",
             rng.choice(["sky_h", "sky_w", "sky_h"]),
             size=rng.choice([0.030, 0.044, 0.022]), pressure=[1.0, 0.95, 0.10], load=1.0)
for i in range(9):
    y = 0.545 + i * 0.011 + rng.uniform(-0.006, 0.006)
    s.stroke([(1.18, y - 0.012), (0.80, y - 0.004), (0.556, y)], "round_hard",
             rng.choice(["sky_w", "sky", "sky_w"]),
             size=rng.choice([0.030, 0.044, 0.022]), pressure=[1.0, 0.95, 0.10], load=1.0)

# ---- board: one clean surface again ---------------------------------------
left  = polygon([(-0.06, 0.668), (0.238, 0.660), (0.246, 0.720), (0.286, 0.790),
                 (0.316, 0.846), (0.330, 0.912), (-0.06, 0.912)])
right = polygon([(0.552, 0.656), (1.06, 0.642), (1.06, 0.912), (0.486, 0.912),
                 (0.490, 0.848), (0.506, 0.790), (0.526, 0.738), (0.542, 0.694)])
under = polygon([(0.24, 0.852), (0.56, 0.846), (0.56, 0.912), (0.24, 0.912)])
for shp in (left, right, under):
    s.block_in(shp.inset(0.016), "flat", "sill", direction=(-2, 25), density=1.0,
               size=0.040, load=1.0)

def bristly(x, y, cols, sizes, lo=0.028, hi=0.085, spread=0.9):
    L = rng.uniform(lo, hi); a = rng.uniform(-spread, spread)
    s.stroke([(x-L/2*math.cos(a), y-L/2*math.sin(a)*0.5),
              (x, y),
              (x+L/2*math.cos(a), y+L/2*math.sin(a)*0.5)], "round_hard",
             rng.choice(cols), size=rng.choice(sizes),
             pressure=[rng.uniform(0.1,0.3), 1.0, rng.uniform(0.1,0.35)], load=1.0)

# the board's back edge biting up into the light
for x0, x1 in [(-0.05, 0.235), (0.56, 1.05)]:
    n = int((x1-x0)/0.048) + 1
    for i in range(n):
        x = x0 + (x1-x0)*i/max(1, n-1.0)
        y = 0.654 - 0.018*x + rng.uniform(-0.011, 0.009)
        bristly(x, y, ["sill", "sill_b", "sill_a", "sill_d"], [0.016, 0.024, 0.032],
                0.030, 0.075, 0.35)
# worn board, low contrast, clustered
for cx, cy, n, sp in [(0.10, 0.730, 6, 0.075), (0.17, 0.836, 5, 0.062),
                      (0.05, 0.878, 4, 0.050), (0.70, 0.700, 6, 0.085),
                      (0.92, 0.762, 5, 0.060), (0.80, 0.884, 4, 0.055),
                      (0.40, 0.888, 4, 0.055), (0.62, 0.876, 4, 0.050)]:
    for _ in range(n):
        x = cx + rng.gauss(0, sp); y = cy + rng.gauss(0, sp*0.30)
        if 0.24 < x < 0.56 and y < 0.856: continue
        bristly(x, y, ["sill_a", "sill_b", "sill_c", "sill_d"], [0.010, 0.015, 0.021])

# ---- the shadow again ------------------------------------------------------
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
