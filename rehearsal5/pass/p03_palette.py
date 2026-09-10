p = s.palette

def to_value(base, target, other="titanium_white"):
    """Ratio of `other` in mix(base, other, r) that reads `target`."""
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        v = p.value_of(p.mix(base, other, mid))
        if v < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def show(label, c):
    print(f"  {label:<14} {p.hex(c)}  v={p.value_of(c):.3f}")

darkest = p.mix("ultramarine", "burnt_umber", 0.5)
show("darkest mix", darkest)
show("umber/blue .75", p.mix("ultramarine", "burnt_umber", 0.75))
show("umber/blue .30", p.mix("ultramarine", "burnt_umber", 0.30))
print()

print("wood bases:")
for r in (0.25, 0.35, 0.45, 0.6):
    show(f"ochre+sienna {r}", p.mix("yellow_ochre", "burnt_sienna", r))
print()

wood = p.mix("yellow_ochre", "burnt_sienna", 0.35)
print("wood tinted to value:")
for t in (0.35, 0.46, 0.52, 0.58, 0.63):
    r = to_value(wood, t)
    show(f"target {t}", p.mix(wood, "titanium_white", r))
    print("      white ratio", round(r, 3))
print()

print("wood shaded toward the dark mix:")
for t in (0.35, 0.28, 0.20):
    r = to_value(wood, t, darkest)
    show(f"target {t}", p.mix(wood, darkest, r))
    print("      dark ratio", round(r, 3))
print()

print("cool greys for the mug:")
for base, name in [(p.mix("ultramarine", "burnt_sienna", 0.5), "ultra+sienna"),
                   (p.mix("ultramarine", "burnt_umber", 0.45), "ultra+umber"),
                   (p.desaturate("cerulean", 0.45), "cerulean desat")]:
    show(name + " raw", base)
    for t in (0.40, 0.50, 0.58, 0.66, 0.74):
        r = to_value(base, t)
        show(f"  {name} -> {t}", p.mix(base, "titanium_white", r))
    print()
