# own, pass 4 - finishing. Three things o3 got wrong and I can see:
#  * the headland is a bar of even thickness all the way across; it has to
#    thin and lift as it goes away.
#  * the horizon "spark" is a dead-straight ruled white line - the outline
#    mistake, in a landscape. Break it so the light is intermittent.
#  * the channel in the lower right reads as a road.
# Then a handful of glints, and stop.
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
p["hz_sky"] = at_value(WARM, 0.885)
p["hz_wat"] = at_value(p.mix(WARM, COOL, 0.20), 0.845)
p["glint"] = at_value(p.desaturate(WARM, 0.05), 0.960)
p["warm_rib"] = at_value(p.mix(WARM, GREY, 0.25), 0.700)
p["sand_l"] = at_value(p.mix(WARM, GREY, 0.60), 0.560)
p["sand_d"] = at_value(p.mix(WARM, GREY, 0.75), 0.440)
p["postlit"] = at_value(p.mix(GREY, WARM, 0.45), 0.470)

s.dry()
n0 = s.stroke_count

# ---- 1. thin the headland away to the right ---------------------------
s.stroke([(0.62, 0.428), (0.50, 0.426), (0.40, 0.422)], "flat", "hz_wat",
         size=0.020, load=1.0, pressure="press_in")
s.stroke([(0.60, 0.412), (0.48, 0.410), (0.39, 0.408)], "flat", "hz_sky",
         size=0.014, load=1.0, pressure="press_in", opacity=0.9)
s.stroke([(0.36, 0.4245), (0.24, 0.4265), (0.13, 0.4285)], "flat", "hz_wat",
         size=0.011, load=1.0, pressure="swell", opacity=0.7)
s.smudge([(0.40, 0.416), (0.56, 0.420), (0.64, 0.424)], size=0.026)

# ---- 2. break the ruled horizon light into three pieces ---------------
s.stroke([(0.672, 0.4205), (0.746, 0.4195)], "flat", "hz_wat", size=0.010,
         load=1.0, pressure="swell")
s.stroke([(0.856, 0.4175), (0.912, 0.4170)], "flat", "hz_wat", size=0.009,
         load=1.0, pressure="swell")
s.stroke([(0.618, 0.4222), (0.664, 0.4215)], "round_hard", "glint",
         size=0.005, load=1.0, pressure="swell")
s.stroke([(0.760, 0.4192), (0.846, 0.4180)], "round_hard", "glint",
         size=0.004, load=1.0, pressure="swell")

# ---- 3. break the channel; it is water, not tarmac --------------------
for a, b, sz, col, op in [((0.02, 0.930), (0.34, 0.862), 0.026, "sand_l", 0.6),
                          ((0.40, 0.848), (0.72, 0.798), 0.022, "warm_rib", 0.55),
                          ((0.74, 0.792), (0.99, 0.762), 0.018, "sand_l", 0.5),
                          ((0.96, 0.786), (0.62, 0.826), 0.014, "sand_d", 0.55),
                          ((0.30, 0.902), (0.02, 0.958), 0.016, "sand_d", 0.5)]:
    s.stroke([a, b], "bristle", col, size=sz, load=0.5, pressure="taper",
             opacity=op, load_falloff=0.22)
s.smudge([(0.10, 0.916), (0.44, 0.848), (0.78, 0.788)], size=0.040)
s.smudge([(0.56, 0.836), (0.86, 0.790)], size=0.032)

# ---- 4. warm ribbons through the middle distance ----------------------
for a, b, sz, ld in [((-0.02, 0.556), (0.52, 0.542), 0.014, 0.5),
                     ((1.02, 0.548), (0.58, 0.560), 0.012, 0.45),
                     ((0.10, 0.648), (0.66, 0.634), 0.016, 0.45),
                     ((1.02, 0.720), (0.52, 0.700), 0.018, 0.4)]:
    s.stroke([a, b], "bristle", "warm_rib", size=sz, load=ld,
             pressure="swell", opacity=0.6, load_falloff=0.2)

# ---- 5. a little warm light down the sunward side of the near posts ----
s.stroke([(0.2245, 0.320), (0.2265, 0.470)], "liner", "postlit", size=0.003,
         load=1.0, pressure="swell", opacity=0.8)
s.stroke([(0.3095, 0.380), (0.3105, 0.500)], "liner", "postlit", size=0.0025,
         load=1.0, pressure="swell", opacity=0.7)

# ---- 6. the glints. Few, deliberate, and that is the end. --------------
s.dab(0.204, 0.500, "round_hard", "glint", size=0.007)
s.dab(0.206, 0.500, "round_hard", "glint", size=0.006)
s.dab(0.446, 0.487, "round_hard", "glint", size=0.006)
s.dab(0.868, 0.507, "round_hard", "glint", size=0.005)
s.dab(0.322, 0.612, "round_hard", at_value(p.desaturate(WARM, 0.05), 0.90),
      size=0.006)
s.smudge([(0.226, 0.618), (0.230, 0.646)], size=0.020)   # lose one post's foot

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
