p = s.palette

def show(name, c):
    p[name] = c
    print(f"{name:12s} {p.hex(c)}  v={p.value_of(c):.3f}")

show("dark",     p.mix("ultramarine", "burnt_umber", 0.60))
show("dark_c",   p.mix("ultramarine", "burnt_umber", 0.35))
show("dark_w",   p.mix("ultramarine", "burnt_umber", 0.78))
show("bg_dark",  p.mix(p.mix("ultramarine", "burnt_umber", 0.6), "burnt_sienna", 0.30))
show("coat_up",  p.mix(p.mix("ultramarine", "burnt_umber", 0.5), "titanium_white", 0.10))
show("wall",     p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.40), 0.42))
show("wall_lit", p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.22), 0.66))
show("wall_hi",  p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.18), 0.80))
show("hair",     p.mix("burnt_umber", "yellow_ochre", 0.42))
show("hair_dk",  p.mix("burnt_umber", "burnt_sienna", 0.35))
show("hair_lit", p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.30), 0.50))
show("hair_hi",  p.tint(p.mix("yellow_ochre", "cadmium_yellow", 0.35), 0.62))
show("skin",     p.tint(p.mix("burnt_sienna", "cadmium_red", 0.25), 0.42))
show("skin_lit", p.tint(p.mix("burnt_sienna", "yellow_ochre", 0.45), 0.58))
show("skin_hi",  p.tint(p.mix("yellow_ochre", "cadmium_red", 0.18), 0.72))
show("skin_sh",  p.mix("burnt_sienna", "burnt_umber", 0.55))
show("beard",    p.mix("burnt_umber", "ultramarine", 0.28))
show("carton",   p.mix("cadmium_red", "cadmium_yellow", 0.55))
show("greybg",   p.tint(p.mix("ultramarine", "burnt_sienna", 0.50), 0.55))

print()
print("--- pigments ---")
for n in ("burnt_umber", "ultramarine", "burnt_sienna", "yellow_ochre",
          "cadmium_red", "cadmium_yellow", "titanium_white", "cerulean", "alizarin"):
    print(f"{n:16s} {p.hex(n)} v={p.value_of(n):.3f}")

print()
print("--- can I supply a colour? ---")
for probe in ("#101014", (0.05, 0.05, 0.06)):
    try:
        print(repr(probe), "->", p.hex(probe), p.value_of(probe))
    except Exception as e:
        print(repr(probe), "FAILED:", type(e).__name__, e)
