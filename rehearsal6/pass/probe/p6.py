p = s.palette
def show(name, c):
    print(f"{name:16s} {p.hex(c)}  v={p.value_of(c):.3f}")

def at_value(base, target):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a+b)/2
        a, b = (m, b) if p.value_of(p.mix(base, "titanium_white", m)) < target else (a, m)
    return (a+b)/2

dk  = p.mix("ultramarine","burnt_umber",0.5)
dkw = p.mix("ultramarine","burnt_umber",0.72)
dkc = p.mix("ultramarine","burnt_umber",0.30)
show("dk .50", dk); show("dk warm .72", dkw); show("dk cool .30", dkc)
show("umber", "burnt_umber")
show("um+aliz .2", p.mix("burnt_umber","alizarin",0.2))
show("um+ultra .25", p.mix("burnt_umber","ultramarine",0.25))
print("--- wood family (ochre/sienna/umber + white) ---")
for r in (0.15,0.3,0.45):
    base = p.mix("yellow_ochre","burnt_sienna",r)
    show(f"ochre+sien {r}", base)
    for t in (0.25,0.4,0.55):
        show(f"   +white {t}", p.tint(base,t))
print("--- wood, greyed with a little blue ---")
w = p.mix(p.mix("yellow_ochre","burnt_sienna",0.3), "ultramarine", 0.12)
show("wood greyed", w)
for t in (0.2,0.35,0.5,0.62):
    show(f"   +white {t}", p.tint(w,t))
print("--- mug: cool pale greys ---")
mg = p.mix("ultramarine","burnt_sienna",0.45)
show("ultra+sien .45", mg)
for t in (0.55,0.65,0.72,0.8,0.88):
    show(f"   +white {t}", p.tint(mg,t))
print("--- cerulean greys ---")
cg = p.mix("cerulean","burnt_umber",0.35)
show("cerul+umb .35", cg)
for t in (0.5,0.62,0.72,0.85):
    show(f"   +white {t}", p.tint(cg,t))
print("--- tea ---")
show("umb+ultra .35", p.mix("burnt_umber","ultramarine",0.35))
show("tea tint .12", p.tint(p.mix("burnt_umber","ultramarine",0.35),0.12))
print("--- targets: white ratio for a value, base=greyed wood ---")
for tv in (0.35,0.45,0.50,0.58,0.63):
    r = at_value(w, tv); print(f"  wood v{tv} -> white {r:.3f} {p.hex(p.mix(w,'titanium_white',r))} v={p.value_of(p.mix(w,'titanium_white',r)):.3f}")
for tv in (0.45,0.55,0.70,0.80,0.88):
    r = at_value(mg, tv); print(f"  cool v{tv} -> white {r:.3f} {p.hex(p.mix(mg,'titanium_white',r))} v={p.value_of(p.mix(mg,'titanium_white',r)):.3f}")
