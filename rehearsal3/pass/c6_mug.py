# c6 - repair the shadow (c5 left a hard-edged bar) and put the mug in.
# prepare() masses used as targets: lit ceramic 0.56, mug's cool planes 0.44
# (#70707A), darks 0.14 (floor 0.22), table light 0.56 / mid 0.48 / dark 0.36.
import math

REF = r"C:\temp\Level1.jpg"
p = s.palette


def at_value(base, target):
    lo, hi = 0.0, 1.0
    if p.value_of(base) > target:
        for _ in range(26):
            mid = (lo + hi) / 2
            if p.value_of(p.shade(base, mid)) > target:
                lo = mid
            else:
                hi = mid
        return p.shade(base, (lo + hi) / 2)
    for _ in range(26):
        mid = (lo + hi) / 2
        if p.value_of(p.tint(base, mid)) < target:
            lo = mid
        else:
            hi = mid
    return p.tint(base, (lo + hi) / 2)


def edge(knots):
    def at(x):
        if x <= knots[0][0]:
            return knots[0][1]
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1]
    return at


warm_dk = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.18), 0.25)
p["sh_a"] = at_value(warm_dk, 0.235)
p["sh_b"] = at_value(warm_dk, 0.300)
p["sh_c"] = at_value(warm_dk, 0.385)
cool = p.desaturate("cerulean", 0.55)
p["mug_md"] = at_value(cool, 0.475)
p["mug_dk"] = at_value(cool, 0.395)
p["mug_lt"] = at_value(p.desaturate(cool, 0.3), 0.575)
p["mug_hi"] = at_value(p.desaturate(cool, 0.2), 0.660)
for n in ("sh_a", "sh_b", "sh_c", "mug_dk", "mug_md", "mug_lt", "mug_hi"):
    print(f"{n:7s} {p.hex(p[n])} {p.value_of(p[n]):.3f}")

s.dry()
n0 = s.stroke_count

# ---------- shadow, repainted opaquely over the bar --------------------
top = edge([(0.302, 0.664), (0.322, 0.596), (0.344, 0.572), (0.358, 0.640),
            (0.430, 0.660), (0.510, 0.664), (0.580, 0.644), (0.624, 0.624),
            (0.668, 0.612), (0.702, 0.612)])
bot = edge([(0.302, 0.716), (0.316, 0.764), (0.338, 0.795), (0.402, 0.829),
            (0.456, 0.845), (0.546, 0.831), (0.618, 0.764), (0.670, 0.690),
            (0.702, 0.616)])
x, k = 0.306, 0
while x < 0.706:
    t, b = top(x), bot(x)
    if b - t > 0.010:
        f = min(1.0, abs(x - 0.43) / 0.27)          # 0 at the core, 1 at the ends
        col = "sh_a" if f < 0.30 else ("sh_b" if f < 0.68 else "sh_c")
        a, z = ((x, t - 0.012), (x, b + 0.014)) if k % 2 else ((x, b + 0.014), (x, t - 0.012))
        s.stroke([a, z], "flat", col, size=0.105 - 0.02 * f, load=1.0,
                 pressure="swell", load_falloff=0.15)
    x += 0.038
    k += 1
# crossed pass along the blob so it stops looking combed
for yy, x0, x1, c in [(0.700, 0.318, 0.660, "sh_a"), (0.742, 0.310, 0.628, "sh_a"),
                      (0.782, 0.330, 0.588, "sh_b"), (0.818, 0.372, 0.540, "sh_c")]:
    s.stroke([(x1, yy - 0.004), (x0, yy + 0.006)], "flat", c, size=0.055,
             load=1.0, pressure="swell", opacity=0.8)
s.smudge([(0.330, 0.800), (0.430, 0.842), (0.540, 0.836)], size=0.07)
s.smudge([(0.610, 0.780), (0.680, 0.688)], size=0.06)
s.smudge([(0.300, 0.700), (0.318, 0.610)], size=0.06)
print("shadow repaint:", s.stroke_count - n0)
print(s.look(region=span("B5", "G8")))

# ---------- the mug ----------------------------------------------------
CX, CY, A, B, SH = 0.474, 0.223, 0.164, 0.110, 0.159
BX, BY, BA, BB, BSH = 0.4665, 0.641, 0.112, 0.024, -0.125
lwall = [(0.310, 0.200), (0.316, 0.330), (0.332, 0.500), (0.355, 0.651)]
rwall = [(0.638, 0.226), (0.632, 0.350), (0.612, 0.500), (0.578, 0.622)]


def rim_front(x):
    u = max(-1.0, min(1.0, (x - CX) / A))
    return CY + B * math.sqrt(1 - u * u) + SH * (x - CX)


def base_front(x):
    v = max(-1.0, min(1.0, (x - BX) / BA))
    return BY + BB * math.sqrt(1 - v * v) + BSH * (x - BX)


def wall_y(knots, x):
    for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
        if min(x0, x1) <= x <= max(x0, x1):
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return knots[-1][1]


def body_bottom(x):
    if x < 0.355:
        return wall_y(lwall, x)
    if x > 0.578:
        return wall_y(rwall, x)
    return base_front(x)


n1 = s.stroke_count
x, k = 0.313, 0
while x < 0.637:
    t = rim_front(x) - 0.010
    b = body_bottom(x) + 0.004
    if b - t > 0.02:
        if x < 0.350:
            col = "mug_md"
        elif x < 0.560:
            col = "mug_md"
        elif x < 0.618:
            col = "mug_lt"
        else:
            col = "mug_hi"
        a, z = ((x, t), (x, b)) if k % 2 else ((x, b), (x, t))
        s.stroke([a, z], "flat", col, size=0.030, load=1.0, pressure="even",
                 load_falloff=0.1)
    x += 0.0125
    k += 1
print("mug body:", s.stroke_count - n1)
print("strokes:", s.stroke_count)
print(s.look(reference=REF))
