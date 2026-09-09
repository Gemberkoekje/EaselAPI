# c8 - three decisions tried on the scrap of canvas before any of them is paid for.
# Nothing here touches the painting and nothing here appears in s.log().
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


def arc(cx, cy, a, b, shear, t0, t1, n=40):
    out = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        dx = a * math.cos(t)
        out.append((cx + dx, cy + b * math.sin(t) + shear * dx))
    return out


p["rimwhite"] = at_value(p.desaturate(p.mix("cerulean", "yellow_ochre", 0.25), 0.55), 0.80)
p["crewdk"] = at_value(p.desaturate(p.mix("alizarin", "burnt_umber", 0.45), 0.35), 0.235)
p["coffee"] = at_value(p.desaturate(p.mix("burnt_umber", "ultramarine", 0.35), 0.35), 0.225)

# ---- R1: the rim. A liner line, or a wide mark that is a MASS? --------
outer_back = arc(0.474, 0.223, 0.164, 0.110, 0.159, math.pi, math.tau)
mid_back = arc(0.477, 0.225, 0.150, 0.097, 0.145, math.pi, math.tau)
r1a = [{"points": outer_back, "brush": "liner", "size": 0.005,
        "color": "rimwhite", "label": "rim-as-line"}]
r1b = [{"points": mid_back, "brush": "round_hard", "size": 0.028,
        "color": "rimwhite", "pressure": "swell", "label": "rim-as-mass"}]
print("R1a liner :", s.rehearse(r1a, reference=REF, region=span("C2", "F4")))
print("R1b mass  :", s.rehearse(r1b, reference=REF, region=span("C2", "F4")))

# ---- R2: the crewmate. A box, or strokes that follow the silhouette? --
r2a = []
yy = 0.408
while yy < 0.655:
    r2a.append({"points": [(0.378, yy), (0.560, yy)], "brush": "flat",
                "size": 0.03, "color": "crewdk", "pressure": "even"})
    yy += 0.028
crew_top = [(0.398, 0.404), (0.440, 0.396), (0.478, 0.400), (0.502, 0.420),
            (0.510, 0.452)]
r2b = []
xx = 0.386
while xx < 0.556:
    if xx < 0.505:
        t = 0.404 + 0.10 * max(0.0, (xx - 0.470) / 0.040) ** 2
        b_ = 0.652 if (xx < 0.428 or xx > 0.474) else 0.610
    else:
        t = 0.470
        b_ = 0.558
    r2b.append({"points": [(xx, t), (xx, b_)], "brush": "bristle",
                "size": 0.036, "color": "crewdk", "pressure": "swell",
                "load": 1.0})
    xx += 0.020
print("R2a box   :", s.rehearse(r2a, reference=REF, region=span("C4", "E6")))
print("R2b shape :", s.rehearse(r2b, reference=REF, region=span("C4", "E6")))

# ---- R3: the coffee. One fat flat pass, or bristle following the ellipse?
r3a = [{"points": [(0.355, 0.235), (0.605, 0.250)], "brush": "flat",
        "size": 0.14, "color": "coffee", "pressure": "even"}]
r3b = []
for i, yy in enumerate([0.185, 0.212, 0.240, 0.268, 0.292]):
    half = 0.128 * math.sqrt(max(0.02, 1 - ((yy - 0.243) / 0.075) ** 2))
    r3b.append({"points": [(0.482 - half, yy), (0.482 + half, yy + 0.006)],
                "brush": "bristle", "size": 0.038, "color": "coffee",
                "pressure": "swell", "load": 1.0})
print("R3a flat  :", s.rehearse(r3a, reference=REF, region=span("C2", "F4")))
print("R3b arcs  :", s.rehearse(r3b, reference=REF, region=span("C2", "F4")))
print("strokes (unchanged):", s.stroke_count)
