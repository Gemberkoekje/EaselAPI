# own, pass 2 - sky, then the wet sand. Big quiet masses, so `flat`, long
# strokes, direction alternating so the dry ends do not line up down one side.
HZ = 0.425
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


COOL = p.desaturate(p.mix("ultramarine", "cerulean", 0.55), 0.30)
WARM = p.desaturate(p.mix("yellow_ochre", "alizarin", 0.20), 0.18)
GREY = p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.48), 0.30)
p["sky1"] = at_value(COOL, 0.585)
p["sky2"] = at_value(p.mix(COOL, WARM, 0.35), 0.690)
p["sky3"] = at_value(p.mix(COOL, WARM, 0.65), 0.790)
p["sky4"] = at_value(WARM, 0.880)
p["glow"] = at_value(p.desaturate(WARM, 0.10), 0.930)
p["cld"] = at_value(GREY, 0.545)
p["cld2"] = at_value(GREY, 0.640)
p["cldlit"] = at_value(p.mix(GREY, WARM, 0.6), 0.815)
p["w1"] = at_value(p.mix(WARM, COOL, 0.20), 0.830)
p["w2"] = at_value(p.mix(WARM, COOL, 0.40), 0.710)
p["w3"] = at_value(p.mix(WARM, COOL, 0.45), 0.615)
p["w4"] = at_value(p.mix(WARM, GREY, 0.55), 0.520)
p["w5"] = at_value(p.mix(WARM, GREY, 0.70), 0.455)
p["rib"] = at_value(p.desaturate(WARM, 0.12), 0.790)
p["chan"] = at_value(p.mix(GREY, COOL, 0.35), 0.395)
for n in ("sky1", "sky4", "glow", "cld", "w1", "w3", "w5", "chan"):
    print(f"{n:6s} {p.hex(p[n])} {p.value_of(p[n]):.3f}")

n0 = s.stroke_count

# ---- sky: five graded bands, each laid the opposite way to the last ----
bands = [(0.585, 0.020, "sky1", 0.115), (0.585, 0.115, "sky1", 0.105),
         (0.690, 0.205, "sky2", 0.100), (0.690, 0.278, "sky2", 0.090),
         (0.790, 0.335, "sky3", 0.080), (0.880, 0.388, "sky4", 0.062),
         (0.930, 0.418, "glow", 0.038)]
for i, (_, y, col, sz) in enumerate(bands):
    a, b = ((-0.03, y - 0.004), (1.03, y + 0.006)) if i % 2 else ((1.03, y + 0.006), (-0.03, y - 0.004))
    s.stroke([a, b], "flat", col, size=sz, load=1.0, pressure="even",
             load_falloff=0.22)
# break the banding: shorter overlapping passes, places left alone
for a, b, sz, col, op in [((0.05, 0.150), (0.62, 0.128), 0.085, "sky1", 0.55),
                          ((0.44, 0.250), (1.02, 0.232), 0.080, "sky2", 0.5),
                          ((-0.02, 0.320), (0.55, 0.330), 0.070, "sky3", 0.5),
                          ((0.40, 0.372), (1.02, 0.360), 0.062, "sky3", 0.45),
                          ((0.08, 0.402), (0.78, 0.408), 0.048, "sky4", 0.5)]:
    s.stroke([a, b], "flat", col, size=sz, load=1.0, pressure="swell",
             opacity=op, load_falloff=0.25)
# two bars of cloud, soft ends, and light under the lower one
s.stroke([(0.04, 0.198), (0.36, 0.178), (0.66, 0.204), (0.90, 0.186)], "flat",
         "cld", size=0.036, load=1.0, pressure="swell", load_falloff=0.2)
s.stroke([(0.86, 0.290), (0.58, 0.276), (0.30, 0.288)], "flat", "cld2",
         size=0.026, load=1.0, pressure="swell", opacity=0.85)
s.stroke([(0.10, 0.216), (0.40, 0.198), (0.68, 0.222)], "flat", "cldlit",
         size=0.012, load=1.0, pressure="swell", opacity=0.8)
s.stroke([(0.72, 0.310), (0.44, 0.298)], "flat", "cldlit", size=0.009,
         load=1.0, pressure="lift_off", opacity=0.7)
s.smudge([(0.04, 0.200), (0.16, 0.192)], size=0.05)
s.smudge([(0.84, 0.196), (0.94, 0.190)], size=0.045)
print("sky:", s.stroke_count - n0)
print(s.look())

# ---- the wet sand: same idea, warmer and darker as it comes forward ---
n1 = s.stroke_count
wat = [(0.448, "w1", 0.048), (0.484, "w1", 0.048), (0.524, "w2", 0.060),
       (0.572, "w2", 0.062), (0.624, "w3", 0.072), (0.686, "w3", 0.075),
       (0.752, "w4", 0.085), (0.826, "w4", 0.090), (0.910, "w5", 0.095),
       (0.982, "w5", 0.090)]
for i, (y, col, sz) in enumerate(wat):
    a, b = ((-0.03, y + 0.006), (1.03, y - 0.005)) if i % 2 else ((1.03, y - 0.005), (-0.03, y + 0.006))
    s.stroke([a, b], "flat", col, size=sz, load=1.0, pressure="even",
             load_falloff=0.2)
# ribbons of sky caught in the wet sand - bristle, part loaded, so they break
for a, b, sz, ld, col in [((-0.02, 0.520), (0.62, 0.506), 0.020, 0.55, "rib"),
                          ((0.44, 0.512), (1.02, 0.498), 0.017, 0.5, "rib"),
                          ((1.02, 0.602), (0.34, 0.610), 0.024, 0.5, "w2"),
                          ((-0.02, 0.598), (0.42, 0.612), 0.020, 0.45, "rib"),
                          ((-0.02, 0.700), (0.50, 0.678), 0.028, 0.5, "w2"),
                          ((0.46, 0.680), (1.02, 0.706), 0.024, 0.45, "rib"),
                          ((1.02, 0.840), (0.40, 0.866), 0.032, 0.5, "w3"),
                          ((-0.02, 0.828), (0.44, 0.864), 0.026, 0.42, "rib")]:
    s.stroke([a, b], "bristle", col, size=sz, load=ld, pressure="swell",
             opacity=0.75, load_falloff=0.18)
# the channel curving in from the bottom left
s.stroke([(-0.03, 0.968), (0.20, 0.900), (0.48, 0.836), (0.72, 0.790),
          (0.95, 0.758)], "flat", "chan", size=0.030, load=1.0,
         pressure="swell", load_falloff=0.2)
s.stroke([(0.90, 0.776), (0.60, 0.808), (0.28, 0.878), (-0.02, 0.946)],
         "bristle", "chan", size=0.014, load=0.5, pressure="taper",
         opacity=0.7)
s.smudge([(0.30, 0.884), (0.58, 0.820), (0.86, 0.776)], size=0.045)
s.smudge([(0.20, 0.520), (0.60, 0.510)], size=0.035)
print("water:", s.stroke_count - n1)
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
