import math, random
rng = random.Random(433)
p = s.palette
s.dry()

# the board's back band, laid in its own colour so the join cannot show
for poly, sz in [(polygon([(-0.06,0.652),(0.238,0.644),(0.240,0.716),(-0.06,0.730)]), 0.016),
                 (polygon([(0.548,0.644),(1.06,0.632),(1.06,0.714),(0.548,0.726)]), 0.016)]:
    s.block_in(poly.inset(0.007), "flat", "sill", direction=(-2, 24), density=1.0,
               size=sz, load=1.0)
# and the clean patch behind the handle, worked to match its surroundings
for _ in range(10):
    x = rng.uniform(0.55, 0.74); y = rng.uniform(0.650, 0.800)
    sz = rng.choice([0.009, 0.013, 0.018]); L = sz * rng.uniform(7, 15)
    a = rng.uniform(-0.6, 0.6)
    s.stroke([(x - L/2*math.cos(a), y - L/2*math.sin(a)*0.55),
              (x + L/2*math.cos(a), y + L/2*math.sin(a)*0.55)], "bristle",
             rng.choice(["sill_a", "sill_b", "sill_c", "sill_d"]), size=sz,
             pressure=rng.choice(["taper","lift_off"]), load=rng.uniform(0.5, 0.85),
             load_falloff=0.3)
# teeth of board biting into the light again
for x0, x1 in [(-0.05, 0.230), (0.556, 1.05)]:
    n = int((x1-x0)/0.050) + 1
    for i in range(n):
        x = x0 + (x1-x0)*i/max(1, n-1.0) + rng.uniform(-0.012, 0.012)
        y = 0.652 - 0.017*x + rng.uniform(-0.010, 0.008)
        sz = rng.choice([0.013, 0.018, 0.024]); L = sz * rng.uniform(3.5, 6.0)
        a = rng.uniform(-0.28, 0.22)
        s.stroke([(x - L/2*math.cos(a), y - L/2*math.sin(a)*0.6),
                  (x + L/2*math.cos(a), y + L/2*math.sin(a)*0.6)], "bristle",
                 rng.choice(["sill", "sill_b", "sill_a", "sill_d"]), size=sz,
                 pressure="taper", load=rng.uniform(0.75, 1.0), load_falloff=0.25)

# cross the glare's banding with veils at a different slope, ends off the canvas
for i in range(5):
    y = 0.155 + i * 0.075 + rng.uniform(-0.02, 0.02)
    col = rng.choice(["sky", "sky_w", "sky_c", "sky_w"])
    a, b = (-0.22, y + 0.055), (1.22, y - 0.048)
    if i % 2: a, b = b, a
    s.stroke([a, b], "flat", col, size=rng.choice([0.075, 0.055, 0.095]),
             pressure="even", load=1.0, load_falloff=0.08)
for i in range(3):
    y = 0.335 + i * 0.062
    a, b = (-0.22, y - 0.030), (1.22, y + 0.036)
    if i % 2: a, b = b, a
    s.stroke([a, b], "flat", rng.choice(["sky_w", "sky_h"]),
             size=rng.choice([0.060, 0.085]), pressure="even", load=1.0, load_falloff=0.08)
print("strokes:", s.stroke_count)
print(s.look(sketch=False))
