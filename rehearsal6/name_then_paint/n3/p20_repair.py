import math, random
rng = random.Random(257)
p = s.palette
s.dry()
# put the glass back over the white speckle, keeping clear of the cup
s.block_in(polygon([(-0.06,0.516),(0.305,0.506),(0.305,0.566),(-0.06,0.578)]).inset(0.007),
           "flat", "sky_h", direction=(-8, 40), density=1.0, size=0.018, load=1.0)
s.block_in(polygon([(-0.06,0.560),(0.236,0.552),(0.236,0.620),(-0.06,0.634)]).inset(0.007),
           "flat", "sky_h", direction=(-6, 46), density=1.0, size=0.018, load=1.0)
s.block_in(polygon([(0.556,0.520),(1.06,0.508),(1.06,0.604),(0.556,0.616)]).inset(0.008),
           "flat", "sky_w", direction=(-5, 44), density=1.0, size=0.020, load=1.0)

# rebuild the sill's back edge: teeth of board biting up into the light
for x0, x1 in [(-0.05, 0.235), (0.56, 1.06)]:
    n = int((x1 - x0) / 0.055) + 1
    for i in range(n):
        x = x0 + (x1 - x0) * i / max(1, n - 1.0)
        y = 0.652 - 0.020 * (x - 0.0) + rng.uniform(-0.012, 0.010)
        L = rng.uniform(0.035, 0.085); a = rng.uniform(-0.30, 0.22)
        s.stroke([(x - L/2, y - a*L/2), (x + L/2, y + a*L/2)], "bristle",
                 rng.choice(["sill", "sill_b", "sill_a", "sill_d"]),
                 size=rng.choice([0.016, 0.024, 0.032]), pressure=rng.choice(["taper","even"]),
                 load=rng.uniform(0.7, 1.0), load_falloff=0.25)

# quiet the pale scratches on the bottom band
for x, y, sz in [(0.115, 0.884, 0.028), (0.72, 0.880, 0.030), (0.88, 0.876, 0.024),
                 (0.30, 0.894, 0.020)]:
    s.stroke([(x-0.085, y+0.010), (x+0.085, y-0.008)], "flat", "ledge",
             size=sz, pressure="even", load=1.0, load_falloff=0.2)
print("strokes:", s.stroke_count)
print(s.look())
