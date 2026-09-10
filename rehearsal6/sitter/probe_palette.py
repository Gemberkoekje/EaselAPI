p = s.palette
def at_value(base, target, other="titanium_white"):
    a, b = 0.0, 1.0
    for _ in range(24):
        m = (a+b)/2
        if p.value_of(p.mix(base, other, m)) < target: a = m
        else: b = m
    return (a+b)/2
def show(label, c):
    print(f"{label:14s} {p.hex(c):8s} v={p.value_of(c):.3f}")

dark = p.mix("ultramarine","burnt_umber",0.5)
show("darkest mix", dark)
for r in (0.25,0.35,0.5,0.65,0.8):
    show(f"ultra/umb {r}", p.mix("ultramarine","burnt_umber",r))
print()
# candidate bases for the warm room
bases = {
 "ochre":"yellow_ochre",
 "och+sie.3": p.mix("yellow_ochre","burnt_sienna",0.3),
 "och+sie.5": p.mix("yellow_ochre","burnt_sienna",0.5),
 "sie":"burnt_sienna",
 "sie+red.3": p.mix("burnt_sienna","cadmium_red",0.3),
 "umb+och.5": p.mix("burnt_umber","yellow_ochre",0.5),
 "sie+umb.4": p.mix("burnt_sienna","burnt_umber",0.4),
}
for name, b in bases.items():
    show(name, b if isinstance(b,str) else b)
print()
for tgt in (0.73,0.64,0.55,0.47,0.37,0.29,0.22):
    row=[]
    for name,b in bases.items():
        r = at_value(b, tgt)
        c = p.mix(b,"titanium_white",r)
        row.append(f"{name}:{p.hex(c)}({r:.2f})")
    print(f"v={tgt:.2f}  " + "  ".join(row))
print()
# supplied darks
for h in ("#0d0b0c","#100d0b","#131010","#161311","#0a0908"):
    p["t"]=h; show(h, p["t"])
