import math, random

CROWN = (0.626, 0.486)

def stem(ang, length, origin=None, bow=0.22, sag=None, rng=None):
    """A curved sprig: three points from `origin` at `ang` degrees (0 = right, 90 = up)."""
    ox, oy = origin if origin else CROWN
    a = math.radians(ang)
    ex, ey = ox + math.cos(a) * length, oy - math.sin(a) * length
    mx, my = (ox + ex) / 2.0, (oy + ey) / 2.0
    px, py = -(ey - oy), (ex - ox)
    L = math.hypot(px, py) or 1.0
    mx += px / L * bow * length
    my += py / L * bow * length
    if sag is None:
        sag = 0.30 * length * abs(math.cos(a))          # sideways stems droop most
    my += sag * 0.55
    ey += sag
    if rng:
        j = 0.010
        mx += rng.uniform(-j, j); my += rng.uniform(-j, j)
        ex += rng.uniform(-j, j); ey += rng.uniform(-j, j)
    return [(ox, oy), (mx, my), (ex, ey)]
