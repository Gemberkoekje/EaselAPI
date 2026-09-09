# c9 - the inside of the cup, the rim, the crewmate. Every dark passage is
# preceded by s.dry(); c9_probe2 proved a dark laid into wet ceramic comes out
# mid-brown instead of near-black.
# Rehearsal verdicts acted on here:
#   R1a (rim as a liner line, rehearse_011) REJECTED - reads as a drawn outline.
#   R1b at size 0.028 (rehearse_012) too thick and one flat value -> 0.022, graded.
#   R2a (crewmate as a box, rehearse_013) REJECTED - a brick rectangle.
#   R2b (bristle at 0.036 stepped 0.020, rehearse_014) gapped -> crossed pass added.
#   R3b (coffee as bristle arcs, rehearse_016) REJECTED - streaky, did not fill.
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


def arc(cx, cy, a, b, shear, t0, t1, n=32):
    out = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        dx = a * math.cos(t)
        out.append((cx + dx, cy + b * math.sin(t) + shear * dx))
    return out


CERAMIC = p.desaturate(p.mix("cerulean", "burnt_sienna", 0.22), 0.62)
p["coffee"] = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.35), 0.35)
p["inwall"] = at_value(p.desaturate(p.mix("ultramarine", "burnt_umber", 0.5), 0.5), 0.335)
p["crew"] = at_value(p.desaturate(p.mix("alizarin", "burnt_umber", 0.5), 0.30), 0.235)
p["rim_hi"] = at_value(p.desaturate(p.mix("cerulean", "yellow_ochre", 0.30), 0.55), 0.760)
p["rim_md"] = at_value(p.desaturate(p.mix("cerulean", "yellow_ochre", 0.20), 0.55), 0.600)
p["rim_lo"] = at_value(CERAMIC, 0.505)
p["cer_l"] = at_value(CERAMIC, 0.470)
p["cer_r"] = at_value(CERAMIC, 0.590)
p["tbl_cut"] = at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.5), 0.3), 0.450)
p["tbl_cut2"] = at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.35), 0.3), 0.530)
for n in ("coffee", "inwall", "crew", "rim_hi", "rim_md", "rim_lo"):
    print(f"{n:8s} {p.hex(p[n])} {p.value_of(p[n]):.3f}")

n0 = s.stroke_count
s.dry()

# ---- 1. repaint the two tan stripes c7 cut into the mug's sides -------
lwall = [(0.310, 0.200), (0.316, 0.330), (0.332, 0.500), (0.355, 0.651)]
rwall = [(0.638, 0.226), (0.632, 0.350), (0.612, 0.500), (0.578, 0.622)]
for xs, ys, xe, ye, col in [(0.325, 0.290, 0.348, 0.630, "cer_l"),
                            (0.338, 0.300, 0.356, 0.615, "cer_l"),
                            (0.606, 0.300, 0.585, 0.610, "cer_r"),
                            (0.622, 0.290, 0.596, 0.600, "cer_r"),
                            (0.632, 0.280, 0.606, 0.560, "cer_r")]:
    s.stroke([(xs, ys), (xe, ye)], "flat", col, size=0.032, load=1.0,
             pressure="swell", load_falloff=0.12)
s.dry()

# ---- 2. inside of the cup: coffee first, wall crescent over it --------
CIX, CIY, CIA, CIB, CISH = 0.480, 0.227, 0.135, 0.084, 0.13
x, k = 0.352, 0
while x < 0.610:
    u = max(-1.0, min(1.0, (x - CIX) / CIA))
    h = CIB * math.sqrt(max(0.0, 1 - u * u))
    yc = CIY + CISH * (x - CIX)
    if h > 0.010:
        a, z = ((x, yc - h), (x, yc + h)) if k % 2 else ((x, yc + h), (x, yc - h))
        s.stroke([a, z], "flat", "coffee", size=0.040, load=1.0,
                 pressure="even", load_falloff=0.08)
    x += 0.028
    k += 1
# crossed pass, so it is a mass and not a set of columns
for yy in (0.180, 0.215, 0.252, 0.288):
    u = max(0.02, 1 - ((yy - 0.238) / 0.082) ** 2)
    half = CIA * math.sqrt(u)
    s.stroke([(CIX + half - 0.012, yy + 0.004), (CIX - half + 0.012, yy)],
             "flat", "coffee", size=0.036, load=1.0, pressure="swell")
# lit far wall inside the cup, a crescent above the liquid
s.stroke(arc(0.481, 0.236, 0.128, 0.077, 0.13, math.pi * 1.06, math.tau * 0.985),
         "flat", "inwall", size=0.026, load=1.0, pressure="swell")
print("cup interior:", s.stroke_count - n0)
s.dry()

# ---- 3. the rim, as a mass, graded round the ellipse -------------------
RX, RY, RA, RB, RSH = 0.477, 0.225, 0.150, 0.097, 0.145
s.stroke(arc(RX, RY, RA, RB, RSH, math.pi * 1.00, math.pi * 1.42), "round_hard",
         "rim_hi", size=0.024, load=1.0, pressure="swell")
s.stroke(arc(RX, RY, RA, RB, RSH, math.pi * 1.38, math.pi * 1.80), "round_hard",
         "rim_md", size=0.023, load=1.0, pressure="swell")
s.stroke(arc(RX, RY, RA, RB, RSH, math.pi * 1.76, math.tau * 1.07), "round_hard",
         "rim_lo", size=0.022, load=1.0, pressure="swell")
s.stroke(arc(RX, RY, RA, RB, RSH, math.pi * 0.10, math.pi * 0.94), "round_hard",
         "rim_lo", size=0.024, load=1.0, pressure="swell")
# the front lip catches a little light on its outer edge only
s.stroke(arc(0.474, 0.228, 0.158, 0.104, 0.155, math.pi * 0.30, math.pi * 0.76),
         "round_hard", "rim_md", size=0.012, load=1.0, pressure="swell",
         opacity=0.75)
print("rim:", s.stroke_count - n0)
s.dry()

# ---- 4. the crewmate, driven along its own silhouette ------------------
ctop = edge([(0.377, 0.492), (0.383, 0.430), (0.402, 0.404), (0.470, 0.396),
             (0.500, 0.416), (0.511, 0.468), (0.519, 0.474), (0.560, 0.478)])
cbot = edge([(0.377, 0.653), (0.4275, 0.656), (0.4285, 0.610), (0.4710, 0.610),
             (0.4720, 0.654), (0.5215, 0.651), (0.5225, 0.556), (0.560, 0.552)])
x, k = 0.384, 0
while x < 0.556:
    t, b = ctop(x), cbot(x)
    if b - t > 0.02:
        a, z = ((x, t), (x, b)) if k % 2 else ((x, b), (x, t))
        s.stroke([a, z], "bristle", "crew", size=0.030, load=1.0,
                 pressure="swell", load_falloff=0.10)
    x += 0.0155
    k += 1
# crossed pass closes the comb R2b showed
for yy, x0, x1 in [(0.430, 0.392, 0.500), (0.480, 0.382, 0.552),
                   (0.530, 0.382, 0.552), (0.580, 0.382, 0.516),
                   (0.630, 0.386, 0.516)]:
    s.stroke([(x1, yy), (x0, yy + 0.003)], "bristle", "crew", size=0.030,
             load=1.0, pressure="swell", opacity=0.85)
print("crewmate:", s.stroke_count - n0)

print("strokes:", s.stroke_count)
print(s.look(reference=REF, region=span("C2", "F7")))
