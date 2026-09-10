p = s.palette

def to_value(base, target):
    """Mix `base` toward white (or umber) until it reads `target`."""
    other = "titanium_white" if p.value_of(base) < target else "burnt_umber"
    lo, hi = 0.0, 1.0
    for _ in range(28):
        mid = (lo + hi) / 2.0
        v = p.value_of(p.mix(base, other, mid))
        if (v < target) == (other == "titanium_white"):
            lo = mid
        else:
            hi = mid
    return p.mix(base, other, (lo + hi) / 2.0)

recipes = {
    "coat":     (p.mix("ultramarine", "burnt_umber", 0.62), None),
    "coat_lt":  (p.mix("ultramarine", "burnt_umber", 0.45), 0.22),
    "bg_dark":  (p.mix(p.mix("ultramarine", "burnt_umber", 0.6), "burnt_sienna", 0.35), 0.17),
    "wall_m":   (p.mix("yellow_ochre", "burnt_sienna", 0.45), 0.42),
    "wall_l":   (p.mix("yellow_ochre", "burnt_sienna", 0.22), 0.60),
    "wall_h":   (p.mix("yellow_ochre", "burnt_sienna", 0.15), 0.72),
    "greyblur": (p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.5), 0.35), 0.40),
    "hair_d":   (p.mix("burnt_umber", "burnt_sienna", 0.40), 0.19),
    "hair_m":   (p.mix("burnt_umber", "yellow_ochre", 0.55), 0.32),
    "hair_l":   (p.mix("yellow_ochre", "burnt_sienna", 0.28), 0.52),
    "hair_h":   (p.mix("yellow_ochre", "cadmium_yellow", 0.3), 0.70),
    "skin_d":   (p.mix("burnt_sienna", "burnt_umber", 0.45), 0.22),
    "skin_m":   (p.mix("burnt_sienna", "cadmium_red", 0.30), 0.38),
    "skin_l":   (p.mix("burnt_sienna", "yellow_ochre", 0.50), 0.52),
    "skin_h":   (p.mix("yellow_ochre", "cadmium_red", 0.20), 0.68),
    "beard":    (p.mix("burnt_umber", "ultramarine", 0.30), None),
    "carton":   (p.mix("cadmium_red", "cadmium_yellow", 0.55), 0.50),
    "glove":    (p.mix("ultramarine", "burnt_umber", 0.45), 0.17),
    "red_pat":  (p.mix("cadmium_red", "cadmium_yellow", 0.25), 0.36),
    "shirt_bl": (p.mix("cerulean", "ultramarine", 0.35), 0.30),
}
for name, (base, tgt) in recipes.items():
    c = base if tgt is None else to_value(base, tgt)
    p[name] = c
    print(f"{name:10s} {p.hex(c)}  v={p.value_of(c):.3f}   (asked {tgt})")
