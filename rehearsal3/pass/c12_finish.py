# c12 - finishing. c11's E7/F6 correction was value-correct and picture-wrong:
# a flat pale wedge with hard ends stuck on the shadow. Broken up here rather
# than removed (the reference really is 0.54-0.58 there).
# Then the marks that make the object identifiable: the visor, the tea tag and
# its string, the lit edge of the mug's foot. Highlights last, fewest strokes.
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


wood = p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.42), 0.30)
p["t55"] = at_value(wood, 0.550)
p["t50"] = at_value(wood, 0.500)
p["t44"] = at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.55), 0.3), 0.440)
p["visor"] = at_value(p.desaturate(p.mix("cerulean", "burnt_umber", 0.30), 0.45), 0.560)
p["glint"] = at_value(p.desaturate("cerulean", 0.25), 0.860)
p["tag"] = p.desaturate(p.mix("ultramarine", "burnt_umber", 0.30), 0.15)
p["string"] = at_value(p.desaturate("cerulean", 0.4), 0.660)
p["foot"] = at_value(p.desaturate(p.mix("cerulean", "burnt_sienna", 0.2), 0.5), 0.720)
p["cer_md"] = at_value(p.desaturate(p.mix("cerulean", "burnt_sienna", 0.22), 0.62), 0.545)

n0 = s.stroke_count
s.dry()

# ---- 1. break the pale wedge: overlapping passes, varied, soft ends ----
for a, b_, sz, col, op in [((0.470, 0.845), (0.700, 0.762), 0.085, "t50", 0.85),
                           ((0.560, 0.905), (0.790, 0.815), 0.075, "t55", 0.7),
                           ((0.600, 0.700), (0.800, 0.640), 0.060, "t50", 0.8),
                           ((0.520, 0.780), (0.660, 0.735), 0.050, "t44", 0.6),
                           ((0.640, 0.880), (0.840, 0.800), 0.060, "t55", 0.55)]:
    s.stroke([a, b_], "flat", col, size=sz, load=1.0, pressure="swell",
             opacity=op, load_falloff=0.18)
for a, b_, sz in [((0.470, 0.900), (0.820, 0.770), 0.010),
                  ((0.560, 0.985), (0.900, 0.850), 0.008),
                  ((0.630, 0.755), (0.880, 0.672), 0.009)]:
    s.stroke([a, b_], "bristle", "t44", size=sz, load=0.45, pressure="taper",
             opacity=0.5, load_falloff=0.2)
s.smudge([(0.500, 0.800), (0.590, 0.762), (0.680, 0.720)], size=0.07)
s.smudge([(0.660, 0.640), (0.740, 0.624)], size=0.05)

# ---- 2. the shelf band c11 left across the mug's upper body -----------
s.dry()
s.stroke([(0.345, 0.372), (0.440, 0.392), (0.545, 0.386), (0.600, 0.366)],
         "flat", "cer_md", size=0.040, load=1.0, pressure="swell", opacity=0.85)
s.smudge([(0.352, 0.352), (0.470, 0.372), (0.596, 0.352)], size=0.035)

# ---- 3. the visor: the one mark that names the figure ------------------
s.dry()
s.stroke([(0.372, 0.462), (0.400, 0.470), (0.428, 0.474)], "round_hard",
         "visor", size=0.028, load=1.0, pressure="swell")
s.stroke([(0.376, 0.457), (0.398, 0.463)], "round_hard", "glint", size=0.011,
         load=1.0, pressure="lift_off")
s.dab(0.382, 0.459, "round_hard", "glint", size=0.009)

# ---- 4. the tea tag and its string -------------------------------------
for a, b_, sz in [((0.812, 0.560), (0.876, 0.588), 0.040),
                  ((0.822, 0.600), (0.878, 0.626), 0.032),
                  ((0.830, 0.548), (0.874, 0.570), 0.020)]:
    s.stroke([a, b_], "flat", "tag", size=sz, load=1.0, pressure="even")
s.dab(0.836, 0.586, "round_hard", at_value(p.desaturate("cerulean", 0.3), 0.82),
      size=0.010)
s.stroke([(0.646, 0.216), (0.700, 0.292), (0.731, 0.400), (0.766, 0.492),
          (0.806, 0.556)], "liner", "string", size=0.004, load=1.0,
         pressure="even", load_falloff=0.0)

# ---- 5. the lit edge of the foot, and two accents. Then stop. ---------
s.stroke([(0.362, 0.648), (0.430, 0.666), (0.500, 0.668), (0.566, 0.640)],
         "round_hard", "foot", size=0.009, load=1.0, pressure="swell")
s.dab(0.336, 0.300, "round_hard", "foot", size=0.010)
s.smudge([(0.318, 0.430), (0.322, 0.560)], size=0.03)   # lose the left edge low down

print("strokes:", s.stroke_count)
print(s.look(reference=REF))
print(s.look(reference=REF, values=True))
