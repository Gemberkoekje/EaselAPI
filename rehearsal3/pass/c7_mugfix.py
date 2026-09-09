# c7 - repaint the mug body. c6 gave a saturated cornflower staircase:
#   * #637b98 is far too blue - prepare() says the mug's cool mass is #70707A
#   * flat at size 0.030 with pressure="even" left hard square stroke-ends,
#     so the rim's front curve came out as a stair.
# Fix: desaturate hard, wider brush, "swell" so the ends soften, value graded
# smoothly in x AND y instead of three bands. Then cut the silhouette by laying
# the TABLE colour along the outside of the edge (guide's rule: no outlines).
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


CERAMIC = p.desaturate(p.mix("cerulean", "burnt_sienna", 0.22), 0.62)
print("ceramic base", p.hex(CERAMIC), round(p.value_of(CERAMIC), 3))
cache = {}


def ceramic(v):
    k = round(v, 3)
    if k not in cache:
        name = f"cer{int(k*1000)}"
        p[name] = at_value(CERAMIC, k)
        cache[k] = name
    return cache[k]


CX, CY, A, B, SH = 0.474, 0.223, 0.164, 0.110, 0.159
BX, BY, BA, BB, BSH = 0.4665, 0.641, 0.112, 0.024, -0.125
lwall = [(0.310, 0.200), (0.316, 0.330), (0.332, 0.500), (0.355, 0.651)]
rwall = [(0.638, 0.226), (0.632, 0.350), (0.612, 0.500), (0.578, 0.622)]
fx = edge([(0.310, 0.435), (0.345, 0.465), (0.420, 0.480), (0.500, 0.500),
           (0.565, 0.555), (0.600, 0.590), (0.638, 0.620)])


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


s.dry()
n0 = s.stroke_count

# --- body, graded, wider brush, soft ends ------------------------------
x, k = 0.316, 0
while x < 0.640:
    t = rim_front(x) - 0.006
    b = body_bottom(x) + 0.006
    if b - t > 0.03:
        mid = (t + b) / 2
        v = fx(x) - 0.030 * max(0.0, (0.46 - mid) / 0.14) + 0.025 * max(0.0, (mid - 0.50) / 0.14)
        if x < 0.40 and b > 0.58:
            v -= 0.055                    # lower-left corner sits in the shadow
        col = ceramic(max(0.30, min(0.70, v)))
        a, z = ((x, t), (x, b)) if k % 2 else ((x, b), (x, t))
        s.stroke([a, z], "flat", col, size=0.055, load=1.0, pressure="swell",
                 load_falloff=0.12)
    x += 0.021
    k += 1
print("body:", s.stroke_count - n0)

# a crossed horizontal pass so it stops reading as columns
for yy in (0.395, 0.455, 0.520, 0.585):
    x0 = max(0.318, min(0.352, 0.310 + (yy - 0.20) * 0.10))
    x1 = 0.636 - (yy - 0.226) * 0.14
    v = fx((x0 + x1) / 2)
    s.stroke([(x0 + 0.01, yy), (x1 - 0.01, yy + 0.004)], "flat", ceramic(v),
             size=0.045, load=0.75, pressure="swell", opacity=0.55,
             load_falloff=0.2)

# --- cut the silhouette with the ground, not with a line ---------------
p["tbl_edge"] = at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.5), 0.3), 0.455)
p["tbl_dark2"] = at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.6), 0.3), 0.375)
# left of the mug: brush centre outside the shape, walking down the wall
for y0, y1, xx, col in [(0.190, 0.320, 0.297, "tbl_edge"), (0.310, 0.450, 0.302, "tbl_edge"),
                        (0.440, 0.560, 0.313, "tbl_dark2"), (0.545, 0.640, 0.331, "sh_c")]:
    s.stroke([(xx, y0), (xx + (0.028 if col != "sh_c" else 0.016), y1)], "flat",
             col, size=0.034, load=1.0, pressure="even")
# right of the mug
for y0, y1, xx in [(0.200, 0.330, 0.657), (0.320, 0.470, 0.650), (0.460, 0.560, 0.634),
                   (0.550, 0.640, 0.606)]:
    s.stroke([(xx, y0), (xx - 0.012, y1)], "flat", "tbl_lt", size=0.032,
             load=1.0, pressure="even")
print("strokes:", s.stroke_count)
print(s.look(reference=REF, region=span("C2", "F7")))
