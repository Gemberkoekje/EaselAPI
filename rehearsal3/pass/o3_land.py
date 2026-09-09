# own, pass 3 - the headland, the posts and their reflections. The dark mass
# and the only hard edges in the picture, so they go on last and stay few.
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
p["land"] = at_value(p.desaturate(p.mix("ultramarine", "burnt_umber", 0.55), 0.35), 0.275)
p["land2"] = at_value(p.desaturate(p.mix("ultramarine", "burnt_umber", 0.45), 0.40), 0.345)
p["post"] = at_value(p.desaturate(p.mix("ultramarine", "burnt_umber", 0.60), 0.25), 0.230)
p["refl"] = at_value(p.mix(COOL, WARM, 0.30), 0.410)
p["refl2"] = at_value(p.mix(COOL, WARM, 0.40), 0.500)
p["spark"] = at_value(p.desaturate(WARM, 0.06), 0.955)
p["bank"] = at_value(p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.5), 0.3), 0.520)
print("land", p.hex(p["land"]), "| post", p.hex(p["post"]),
      "| spark", p.hex(p["spark"]))

n0 = s.stroke_count
s.dry()

# ---- the headland: one band, ragged on top, dying to nothing on the right
s.stroke([(-0.03, 0.401), (0.09, 0.394), (0.18, 0.406), (0.27, 0.399),
          (0.36, 0.410)], "flat", "land", size=0.030, load=1.0,
         pressure="even", load_falloff=0.1)
s.stroke([(0.34, 0.412), (0.45, 0.415), (0.53, 0.421), (0.60, 0.425)],
         "flat", "land2", size=0.022, load=1.0, pressure="lift_off")
# a few ticks so the skyline is not a ruled line
for x, y in [(0.055, 0.380), (0.145, 0.386), (0.212, 0.383), (0.298, 0.390),
             (0.392, 0.399)]:
    s.stroke([(x, y), (x + 0.006, 0.418)], "round_hard", "land", size=0.008,
             load=1.0, pressure="lift_off")
# a far mudbank on the right, barely there
s.stroke([(1.02, 0.470), (0.80, 0.465), (0.63, 0.472)], "bristle", "bank",
         size=0.010, load=0.5, pressure="taper", opacity=0.6)

# ---- the horizon's last light, right of the headland -------------------
s.stroke([(0.615, 0.4215), (1.03, 0.4155)], "liner", "spark", size=0.004,
         load=1.0, pressure="even", load_falloff=0.0)
s.dry()

# ---- the posts: silhouettes, no lit edge, uneven tops ------------------
s.stroke([(0.213, 0.296), (0.219, 0.452), (0.223, 0.620)], "flat", "post",
         size=0.012, load=1.0, pressure="even", load_falloff=0.05)
s.stroke([(0.2295, 0.302), (0.2325, 0.620)], "flat", "post", size=0.0095,
         load=1.0, pressure="even", load_falloff=0.05)
s.stroke([(0.302, 0.362), (0.3065, 0.592)], "flat", "post", size=0.0105,
         load=1.0, pressure="even", load_falloff=0.05)
s.stroke([(0.6555, 0.437), (0.6585, 0.547)], "flat", "post", size=0.008,
         load=1.0, pressure="even", load_falloff=0.05)
s.dab(0.2155, 0.2985, "round_hard", "post", size=0.011)
s.dab(0.3025, 0.3645, "round_hard", "post", size=0.010)

# ---- reflections: broken, wandering, never as dark as the post ---------
for pts, sz, ld, col in [([(0.2225, 0.624), (0.2265, 0.690), (0.2185, 0.760)], 0.014, 0.5, "refl"),
                         ([(0.2205, 0.780), (0.2285, 0.860), (0.2245, 0.930)], 0.016, 0.4, "refl2"),
                         ([(0.2330, 0.624), (0.2360, 0.686), (0.2300, 0.742)], 0.011, 0.45, "refl"),
                         ([(0.3065, 0.596), (0.3005, 0.658), (0.3085, 0.726)], 0.012, 0.5, "refl"),
                         ([(0.3040, 0.750), (0.3100, 0.804)], 0.012, 0.35, "refl2"),
                         ([(0.6585, 0.551), (0.6545, 0.598), (0.6605, 0.640)], 0.009, 0.5, "refl")]:
    s.stroke(pts, "bristle", col, size=sz, load=ld, pressure="swell",
             opacity=0.8, load_falloff=0.25)
s.smudge([(0.222, 0.700), (0.226, 0.780)], size=0.030)
s.smudge([(0.306, 0.700), (0.304, 0.760)], size=0.026)

print("strokes:", s.stroke_count)
print(s.look())
