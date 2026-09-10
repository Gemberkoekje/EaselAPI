import math
import random

p = s.palette
rng = random.Random(113)
WHITE = "titanium_white"


def to_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(base, WHITE, m)) < target else (a, m)
    return p.mix(base, WHITE, (a + b) / 2)


COOL = p.mix("cerulean", "burnt_sienna", 0.18)
WARM = p.mix("yellow_ochre", "cadmium_red", 0.24)
GREY = p.mix("ultramarine", "burnt_sienna", 0.45)


def wash(v, kind="cool"):
    base = {"cool": COOL, "warm": WARM, "grey": GREY}[kind]
    return p.desaturate(to_value(base, v), 0.30)


p["edge_dk"] = p.desaturate(to_value(p.mix("viridian", "burnt_umber", 0.50), 0.165), 0.45)

s.dry()

#      cx     cy     rx     ry    base
POOLS = [(0.688, 0.120, 0.075, 0.070, 0.82),
         (0.576, 0.264, 0.070, 0.052, 0.82),
         (0.650, 0.352, 0.090, 0.045, 0.70),
         (0.452, 0.400, 0.058, 0.050, 0.70),
         (0.500, 0.198, 0.078, 0.038, 0.70),
         (0.322, 0.524, 0.048, 0.036, 0.70),
         (0.238, 0.646, 0.032, 0.024, 0.55)]

for cx, cy, rx, ry, base in POOLS:
    # three passes crossing the comb, at angles the canvas did not choose
    for k in range(3):
        ang = math.radians(rng.uniform(46, 104) * (1 if k % 2 == 0 else -1) * 0.9 + 62)
        dv = [0.05, -0.13, -0.27][k]
        kind = ["cool", "grey", "cool"][k] if base > 0.6 else ["grey", "cool", "grey"][k]
        col = wash(max(0.16, min(0.92, base + dv)), kind)
        ln = min(rx, ry) * rng.uniform(1.5, 2.4)
        ox = rng.uniform(-rx * 0.55, rx * 0.55)
        oy = rng.uniform(-ry * 0.45, ry * 0.45)
        s.stroke([(cx + ox - ln / 2 * math.cos(ang), cy + oy - ln / 2 * math.sin(ang)),
                  (cx + ox + ln / 2 * math.cos(ang), cy + oy + ln / 2 * math.sin(ang))],
                 "bristle", col, size=max(0.007, min(rx, ry) * rng.uniform(0.35, 0.55)),
                 load=rng.uniform(0.8, 1.0), pressure="swell")
    # two round accents - the tip that declares no axis
    for k in range(2):
        ang = math.radians(rng.uniform(0, 360))
        dv = [0.07, -0.20][k]
        col = wash(max(0.16, min(0.93, base + dv)), "warm" if k == 0 and base > 0.7 else "cool")
        ln = min(rx, ry) * rng.uniform(0.8, 1.5)
        ox, oy = rng.uniform(-rx * 0.4, rx * 0.4), rng.uniform(-ry * 0.4, ry * 0.4)
        s.stroke([(cx + ox - ln / 2 * math.cos(ang), cy + oy - ln / 2 * math.sin(ang)),
                  (cx + ox + ln / 2 * math.cos(ang), cy + oy + ln / 2 * math.sin(ang))],
                 "round_hard", col, size=max(0.005, min(rx, ry) * rng.uniform(0.18, 0.32)),
                 pressure="swell")
    # weed pushing in from the field, so the boundary is not a cut edge
    for k in range(2):
        th = rng.uniform(0, 2 * math.pi)
        ex, ey = cx + rx * math.cos(th) * 1.05, cy + ry * math.sin(th) * 1.05
        ln = min(rx, ry) * rng.uniform(0.9, 1.6)
        s.stroke([(ex, ey), (ex - ln * math.cos(th) * 0.9, ey - ln * math.sin(th) * 0.9)],
                 "bristle", "edge_dk", size=max(0.006, min(rx, ry) * rng.uniform(0.25, 0.45)),
                 load=rng.uniform(0.7, 1.0), pressure="press_in")

print("strokes", s.stroke_count)
print(s.look())
print(s.look(region=span("D1", "H4")))
