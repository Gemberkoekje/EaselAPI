from easel import Session
p = Session(100, 100, seed=1).palette

print("-- my stage-1 mixes --")
mixes = {
    "wall":     p.mix(p.tint("yellow_ochre", 0.45), "burnt_sienna", 0.25),
    "wall_dim": p.mix("yellow_ochre", "burnt_umber", 0.55),
    "dark":     p.mix("ultramarine", "burnt_umber", 0.55),
}
mixes["coat"] = p.shade(mixes["dark"], 0.45)
mixes["hair"] = p.mix("burnt_umber", "yellow_ochre", 0.35)
for k, v in mixes.items():
    print(f"  {k:<9} {p.hex(v)}  value {p.value_of(v):.2f}")

print("-- range of the raw pigments --")
for name in ["titanium_white", "cadmium_yellow", "yellow_ochre", "burnt_sienna",
             "cadmium_red", "burnt_umber", "ultramarine", "viridian"]:
    print(f"  {name:<15} value {p.value_of(name):.2f}")

print("-- how dark can a mixed dark actually go? --")
for r in [0.3, 0.5, 0.7]:
    d = p.mix("ultramarine", "burnt_umber", r)
    for sh in [0.0, 0.5, 0.9]:
        c = p.shade(d, sh) if sh else d
        print(f"  umber-ratio {r} shade {sh} -> {p.hex(c)} value {p.value_of(c):.2f}")
print("-- how light can flesh go? --")
for t in [0.5, 0.7, 0.85]:
    c = p.tint(p.mix("burnt_sienna", "cadmium_red", 0.2), t)
    print(f"  tint {t} -> {p.hex(c)} value {p.value_of(c):.2f}")
