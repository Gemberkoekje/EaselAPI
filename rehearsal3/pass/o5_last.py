# own, pass 5 - the banding. Long horizontal strokes on a horizontal subject
# stack into stripes; that is this engine's characteristic failure and it needs
# marks that run ACROSS the bands to cure it. Ripples in the sand do that
# honestly. Two birds for scale, and stop.
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
p["rip_l"] = at_value(p.mix(WARM, GREY, 0.45), 0.615)
p["rip_d"] = at_value(p.mix(WARM, GREY, 0.80), 0.415)
p["fg_l"] = at_value(p.mix(WARM, GREY, 0.62), 0.545)
p["sk_b"] = at_value(p.mix(COOL, WARM, 0.22), 0.645)
p["bird"] = at_value(p.desaturate(p.mix("ultramarine", "burnt_umber", 0.5), 0.3), 0.310)
p["gleam"] = at_value(p.desaturate(WARM, 0.08), 0.905)

s.dry()
n0 = s.stroke_count

# ---- the step where the sky changes hue -------------------------------
for a, b, sz, op in [((-0.02, 0.132), (0.48, 0.150), 0.055, 0.45),
                     ((1.02, 0.146), (0.52, 0.128), 0.050, 0.4),
                     ((0.18, 0.108), (0.72, 0.120), 0.038, 0.35)]:
    s.stroke([a, b], "flat", "sk_b", size=sz, load=1.0, pressure="swell",
             opacity=op, load_falloff=0.25)
s.smudge([(0.06, 0.140), (0.44, 0.150)], size=0.05)
s.smudge([(0.60, 0.136), (0.96, 0.126)], size=0.045)

# ---- the smear left where the headland was rubbed out ------------------
s.stroke([(0.330, 0.4225), (0.420, 0.4205)], "flat",
         at_value(p.mix(WARM, COOL, 0.18), 0.850), size=0.013, load=1.0,
         pressure="swell", opacity=0.9)

# ---- the hard step at the top of the foreground band -------------------
for a, b, sz, col, op in [((-0.02, 0.712), (0.46, 0.694), 0.062, "fg_l", 0.5),
                          ((1.02, 0.700), (0.50, 0.716), 0.058, "fg_l", 0.45),
                          ((0.12, 0.744), (0.68, 0.726), 0.044, "rip_l", 0.4)]:
    s.stroke([a, b], "flat", col, size=sz, load=1.0, pressure="swell",
             opacity=op, load_falloff=0.25)
s.smudge([(0.05, 0.706), (0.42, 0.700), (0.80, 0.710)], size=0.055)

# ---- ripples: short marks running ACROSS the bands ---------------------
rip = [(0.06, 0.775, 0.14, 0.760), (0.19, 0.805, 0.27, 0.788),
       (0.33, 0.782, 0.41, 0.800), (0.47, 0.822, 0.56, 0.804),
       (0.62, 0.792, 0.70, 0.812), (0.76, 0.830, 0.85, 0.812),
       (0.10, 0.888, 0.20, 0.906), (0.30, 0.930, 0.41, 0.912),
       (0.52, 0.902, 0.62, 0.922), (0.70, 0.944, 0.82, 0.924),
       (0.86, 0.882, 0.96, 0.900), (0.40, 0.966, 0.52, 0.948)]
for i, (x0, y0, x1, y1) in enumerate(rip):
    col = "rip_l" if i % 2 else "rip_d"
    s.stroke([(x0, y0), (x1, y1)], "bristle", col, size=0.011 + 0.004 * (i % 3),
             load=0.5, pressure="taper", opacity=0.55, load_falloff=0.2)
for x0, y0, x1, y1 in [(0.14, 0.640, 0.21, 0.632), (0.44, 0.664, 0.52, 0.656),
                       (0.74, 0.636, 0.82, 0.646), (0.60, 0.598, 0.67, 0.592)]:
    s.stroke([(x0, y0), (x1, y1)], "bristle", "rip_l", size=0.008, load=0.45,
             pressure="taper", opacity=0.45)

# ---- the sky's brightest patch mirrored under it -----------------------
s.stroke([(0.38, 0.452), (0.62, 0.448), (0.82, 0.454)], "flat", "gleam",
         size=0.020, load=1.0, pressure="swell", opacity=0.55,
         load_falloff=0.25)
s.smudge([(0.42, 0.456), (0.72, 0.452)], size=0.030)

# ---- two birds, far off. Scale, and then stop. -------------------------
s.stroke([(0.742, 0.228), (0.750, 0.2235), (0.759, 0.229)], "liner", "bird",
         size=0.0028, load=1.0, pressure="even", load_falloff=0.0)
s.stroke([(0.776, 0.244), (0.782, 0.2405), (0.789, 0.245)], "liner", "bird",
         size=0.0024, load=1.0, pressure="even", load_falloff=0.0)

print("strokes:", s.stroke_count)
print(s.look())
