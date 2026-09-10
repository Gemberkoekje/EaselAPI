exec(open("_pal.py").read())
exec(open("_geom.py").read())
import random
rng = random.Random(21)
s.dry()

s.block_in(GLASS, "flat", "glass", direction=(98, 14), density=1.0,
           size=0.15, pressure="even", load=1.0, load_falloff=0.2)
s.block_in(WALL, "flat", "wall", direction=(104, 20), density=1.0,
           size=0.135, pressure="even", load=1.0, load_falloff=0.2)

def walk(a, b, n, size=0.035, reach=0.055):
    """Walk a join: short smudges crossing it, none the same length or angle."""
    import math
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    for i in range(n):
        t = (i + 0.5) / n + rng.uniform(-0.12, 0.12) / n
        px, py = a[0] + dx * t, a[1] + dy * t
        r1 = reach * rng.uniform(0.45, 1.15)
        r2 = reach * rng.uniform(0.45, 1.15)
        j = rng.uniform(-0.25, 0.25)
        s.smudge([(px - nx * r1 + dx / L * j * r1, py - ny * r1 + dy / L * j * r1),
                  (px + nx * r2, py + ny * r2)], size=size * rng.uniform(0.8, 1.2))

# the wall darkens toward the right edge
dark = polygon([(0.845, 0.0), (1.0, 0.0), (1.0, 0.665), (0.900, 0.645), (0.935, 0.30)])
s.block_in(dark.inset(0.03), "flat", "wall_dk", direction=(96, 18), density=1.0,
           size=0.06, pressure="even", load=1.0)
walk((0.848, 0.02), (0.898, 0.64), 11, size=0.038, reach=0.060)

# the pane is hottest at the top
hot = polygon([(0.020, 0.0), (0.566, 0.0), (0.559, 0.245), (0.300, 0.215), (0.028, 0.290)])
s.block_in(hot.inset(0.03), "flat", "glass_hot", direction=(8, 96), density=1.0,
           size=0.06, pressure="even", load=1.0)
walk((0.030, 0.285), (0.560, 0.242), 12, size=0.036, reach=0.055)
print(s.stroke_count)
print(s.look())
