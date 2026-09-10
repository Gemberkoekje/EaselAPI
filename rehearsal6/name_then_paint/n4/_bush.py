def grow_bush(seed=31):
    rng = random.Random(seed)

    def lit_at(x, y):
        return max(0.0, min(1.0, 0.62 * (x - 0.44) / 0.46 + 0.38 * (0.54 - y) / 0.44))

    def pick(x, y, bias=0.0):
        f = lit_at(x, y) + bias + rng.uniform(-0.13, 0.13)
        if f < 0.36:  return "leaf_dk"
        if f < 0.64:  return "leaf_mid"
        if f < 0.92:  return "leaf_lit"
        return "leaf_hot"

    def along(path, t):
        a, b, c = path
        if t < 0.5:
            u = t * 2.0
            return (a[0] + (b[0]-a[0])*u, a[1] + (b[1]-a[1])*u)
        u = (t - 0.5) * 2.0
        return (b[0] + (c[0]-b[0])*u, b[1] + (c[1]-b[1])*u)

    def branch(origin, ang, length, depth, dark_only=False):
        path = stem(ang + rng.uniform(-7, 7), length, origin=origin,
                    bow=rng.uniform(-0.32, 0.32), rng=rng)
        mid = along(path, 0.6)
        col = "leaf_dk" if dark_only else pick(*mid, bias=-0.12 + 0.11 * (2 - depth))
        sz = max(0.008, 0.019 * (0.55 + 0.45 * depth) * rng.uniform(0.75, 1.3))
        s.stroke(path, "bristle", col, size=sz,
                 pressure=rng.choice(["taper", "lift_off", [1.0, 0.85, 0.2]]),
                 load=rng.uniform(0.65, 1.0))
        if depth <= 0:
            return
        for t in (0.42, 0.66, 0.86):
            if rng.random() < 0.32:
                continue
            o = along(path, t)
            for side in (1, -1):
                if rng.random() < 0.38:
                    continue
                branch(o, ang + side * rng.uniform(16, 46) + rng.uniform(-9, 9),
                       length * rng.uniform(0.36, 0.60), depth - 1, dark_only)

    CORE = hull([(0.452,0.512),(0.482,0.318),(0.578,0.222),(0.740,0.244),
                 (0.818,0.360),(0.772,0.482),(0.628,0.524)])
    for _ in range(66):
        for _t in range(24):
            x = rng.uniform(0.44, 0.83); y = rng.uniform(0.21, 0.53)
            if CORE.contains(x, y):
                break
        a = math.degrees(math.atan2(CROWN[1] - y, x - CROWN[0])) + rng.uniform(-32, 32)
        s.stroke(stem(a, rng.uniform(0.030, 0.080), origin=(x, y),
                      bow=rng.uniform(-0.4, 0.4), sag=0.0, rng=rng),
                 "bristle", "leaf_dk" if rng.random() < 0.74 else "leaf_mid",
                 size=rng.uniform(0.015, 0.038), pressure="taper",
                 load=rng.uniform(0.55, 0.95))

    MAIN = [(168,0.190),(157,0.235),(146,0.200),(134,0.265),(122,0.225),(111,0.285),
            (100,0.240),( 89,0.295),( 78,0.245),( 67,0.290),( 56,0.235),( 45,0.275),
            ( 34,0.230),( 23,0.260),( 12,0.215),(  1,0.235),(-10,0.180),
            (183,0.165),(193,0.145),(203,0.125),(212,0.100),(174,0.205)]
    ORIG = [(0.556,0.504),(0.594,0.496),(0.626,0.490),(0.662,0.494),(0.698,0.502),
            (0.574,0.448),(0.678,0.444),(0.626,0.416),(0.538,0.474),(0.716,0.472)]
    for i, (ang, ln) in enumerate(MAIN):
        branch(ORIG[i % len(ORIG)], ang, ln * rng.uniform(0.88, 1.14), 2,
               dark_only=(ang > 128 and rng.random() < 0.62))
