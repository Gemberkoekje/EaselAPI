import math, random
rng = random.Random(151)
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

# variation as short marks at their own angles, clustered, never spanning the board
def clump(cx, cy, n, spread, cols):
    for _ in range(n):
        x = cx + rng.gauss(0, spread); y = cy + rng.gauss(0, spread * 0.32)
        if 0.25 < x < 0.56 and y < 0.855:  continue          # keep off the cup
        L = rng.uniform(0.022, 0.072); a = rng.uniform(-1.0, 1.0)
        s.stroke([(x - L/2*math.cos(a), y - L/2*math.sin(a)*0.5),
                  (x + L/2*math.cos(a), y + L/2*math.sin(a)*0.5)],
                 "bristle", rng.choice(cols), size=rng.choice([0.009, 0.013, 0.019]),
                 pressure=rng.choice(["taper", "even", "lift_off"]),
                 load=rng.uniform(0.5, 0.95), load_falloff=0.3)
clump(0.10, 0.712, 6, 0.070, ["sill_a", "sill_c"])
clump(0.19, 0.822, 5, 0.060, ["sill_a", "sill_b"])
clump(0.045, 0.868, 4, 0.050, ["sill_c", "sill_a"])
clump(0.66, 0.700, 5, 0.075, ["sill_b", "sill_d"])
clump(0.90, 0.760, 5, 0.060, ["sill_b", "sill_a"])
clump(0.78, 0.882, 4, 0.055, ["sill_d", "sill_b"])
clump(0.40, 0.884, 4, 0.060, ["sill_a", "sill_b"])

# the shadow, as a shadow shape: pooled at the cup, tapering away right
pen = polygon([(0.40, 0.786), (0.54, 0.781), (0.68, 0.787), (0.80, 0.798), (0.892, 0.812),
               (0.936, 0.830), (0.876, 0.846), (0.755, 0.856), (0.62, 0.858),
               (0.50, 0.850), (0.412, 0.838)])
umb = polygon([(0.41, 0.792), (0.525, 0.789), (0.635, 0.796), (0.702, 0.807),
               (0.660, 0.840), (0.552, 0.845), (0.442, 0.836)])
s.block_in(pen.inset(0.010), "bristle", "shad_f", direction=(3, -14), density=1.0,
           size=0.020, load=0.9)
s.block_in(umb.inset(0.008), "bristle", "shad", direction=(4, -12), density=1.0,
           size=0.015, load=1.0)
s.stroke([(0.318, 0.824), (0.398, 0.846), (0.476, 0.826)], "round_hard", "contact",
         size=0.015, pressure=[0.5, 1.0, 0.85], load=1.0)
s.stroke([(0.464, 0.812), (0.520, 0.818)], "round_hard", "contact",
         size=0.009, pressure=[0.9, 0.15], load=1.0)

# sharpen the cup's right edge by laying the board up to it
for dx, sz in [(0.011, 0.018), (0.020, 0.014)]:
    s.stroke([(0.535+dx, 0.640), (0.520+dx, 0.702), (0.500+dx, 0.760), (0.486+dx, 0.800)],
             "bristle", "sill", size=sz, pressure="even", load=1.0, load_falloff=0.2)
print("strokes:", s.stroke_count)
print(s.look())
