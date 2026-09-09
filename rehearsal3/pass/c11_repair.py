# c11 - repairs driven by compare (12 cells out, largest 0.19):
#   D3 +0.19  D2 +0.14  E2 +0.18  E3 +0.14 -> the cup's opening is too light:
#       the rim's front lip and the inner-wall band are both far too wide, and
#       the coffee does not reach the rim. look_022 shows it plainly.
#   D4 +0.14 -> the crewmate's head is not as dark as its body.
#   E7 -0.17  F6 -0.15 -> the shadow overreaches to the lower right; the
#       reference has bright table there (0.54, 0.58).
#   H1 +0.13  H8 +0.11 -> corners.
#   D5 +0.17 is the palette floor (ref 0.06, canvas already 0.23). Not fixable.
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


def arc(cx, cy, a, b, shear, t0, t1, n=28):
    out = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        dx = a * math.cos(t)
        out.append((cx + dx, cy + b * math.sin(t) + shear * dx))
    return out


CERAMIC = p.desaturate(p.mix("cerulean", "burnt_sienna", 0.22), 0.62)
p["cof2"] = p.desaturate(p.mix("burnt_umber", "ultramarine", 0.42), 0.30)
p["wall2"] = at_value(p.desaturate(p.mix("ultramarine", "burnt_umber", 0.55), 0.4), 0.300)
p["lip2"] = at_value(CERAMIC, 0.500)
p["lip_hi"] = at_value(p.desaturate(CERAMIC, 0.35), 0.700)
p["brt"] = at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.32), 0.28), 0.575)
p["brt2"] = at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.30), 0.26), 0.545)
p["cnr"] = at_value(p.desaturate(p.mix("ultramarine", "burnt_umber", 0.5), 0.5), 0.240)
print("cof2", p.hex(p["cof2"]), round(p.value_of(p["cof2"]), 3))

n0 = s.stroke_count
s.dry()

# ---- 1. the coffee, right out to the rim, on dry canvas ---------------
CIX, CIY, CIA, CIB, CISH = 0.480, 0.227, 0.137, 0.086, 0.13
x, k = 0.350, 0
while x < 0.612:
    u = max(-1.0, min(1.0, (x - CIX) / CIA))
    h = CIB * math.sqrt(max(0.0, 1 - u * u))
    yc = CIY + CISH * (x - CIX)
    if h > 0.008:
        a, z = ((x, yc - h + 0.004), (x, yc + h)) if k % 2 else ((x, yc + h), (x, yc - h + 0.004))
        s.stroke([a, z], "flat", "cof2", size=0.034, load=1.0, pressure="even",
                 load_falloff=0.06)
    x += 0.024
    k += 1
print("coffee:", s.stroke_count - n0)

# ---- 2. a NARROW dark inner wall across the back only -----------------
s.stroke(arc(0.481, 0.234, 0.126, 0.074, 0.13, math.pi * 1.12, math.pi * 1.88),
         "round_hard", "wall2", size=0.013, load=1.0, pressure="swell")
# ---- 3. a NARROW front lip, sitting where the reference's is ----------
s.stroke(arc(0.476, 0.230, 0.152, 0.100, 0.150, math.pi * 0.14, math.pi * 0.90),
         "round_hard", "lip2", size=0.017, load=1.0, pressure="swell")
s.stroke(arc(0.474, 0.226, 0.163, 0.109, 0.157, math.pi * 0.30, math.pi * 0.74),
         "round_hard", "lip_hi", size=0.007, load=1.0, pressure="swell")
# a bright accent on the back-left of the rim only - the light comes from there
s.stroke(arc(0.476, 0.226, 0.158, 0.104, 0.152, math.pi * 1.02, math.pi * 1.36),
         "round_hard", "lip_hi", size=0.009, load=1.0, pressure="swell")
s.dry()

# ---- 4. the spoon's metal was a white stick; it is dark with a glint ---
s.stroke([(0.497, 0.223), (0.514, 0.256), (0.537, 0.293)], "round_hard",
         "cof2", size=0.017, load=1.0, pressure="even")
s.dab(0.508, 0.243, "round_hard", at_value(p.desaturate("cerulean", 0.5), 0.60),
      size=0.008)
s.dab(0.531, 0.286, "round_hard", at_value(p.desaturate("cerulean", 0.5), 0.55),
      size=0.007)

# ---- 5. the crewmate's head, down to the body's value ------------------
s.dry()
for xx, t, b in [(0.396, 0.412, 0.470), (0.414, 0.402, 0.470), (0.434, 0.398, 0.470),
                 (0.454, 0.397, 0.470), (0.474, 0.398, 0.470), (0.492, 0.410, 0.470)]:
    s.stroke([(xx, t), (xx, b)], "flat", "crew2", size=0.024, load=1.0,
             pressure="even", load_falloff=0.05)

# ---- 6. bright table back over E7 and F6 ------------------------------
for a, b_, sz, col in [((0.500, 0.812), (0.660, 0.760), 0.075, "brt"),
                       ((0.520, 0.870), (0.700, 0.800), 0.070, "brt"),
                       ((0.612, 0.700), (0.760, 0.652), 0.070, "brt"),
                       ((0.640, 0.640), (0.770, 0.612), 0.055, "brt2"),
                       ((0.560, 0.760), (0.700, 0.712), 0.055, "brt")]:
    s.stroke([a, b_], "flat", col, size=sz, load=1.0, pressure="swell",
             load_falloff=0.15)
s.smudge([(0.540, 0.790), (0.600, 0.756)], size=0.06)

# ---- 7. corners --------------------------------------------------------
s.stroke([(0.895, 0.002), (1.02, 0.036)], "flat", "cnr", size=0.042,
         load=1.0, pressure="even")
s.stroke([(0.900, 0.988), (1.02, 0.960)], "flat",
         at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.6), 0.3), 0.360),
         size=0.075, load=1.0, pressure="swell", opacity=0.7)

print("strokes:", s.stroke_count)
print(s.look(reference=REF))
