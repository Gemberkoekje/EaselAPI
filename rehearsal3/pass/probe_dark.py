"""Probe: how dark can this palette actually go, and does stacking glazes beat it?
The reference has cells at 0.04-0.12. PAINTER.md says the floor is "about 0.23".
Scratch session - nothing here touches the painting."""
from easel import Session, region

s = Session(400, 300, ground="umber_wash", seed=99)
p = s.palette

best = []
pigments = ["ultramarine", "burnt_umber", "alizarin", "viridian", "cerulean",
            "burnt_sienna", "cadmium_red", "yellow_ochre"]
for a in pigments:
    for b in pigments:
        for r in (0.0, 0.25, 0.5, 0.75, 1.0):
            c = p.mix(a, b, r)
            for sh in (0.0, 0.5, 1.0):
                c2 = p.shade(c, sh) if sh else c
                for ds in (0.0, 0.5, 1.0):
                    c3 = p.desaturate(c2, ds) if ds else c2
                    best.append((p.value_of(c3), a, b, r, sh, ds, p.hex(c3)))
best.sort()
print("--- 6 darkest mixtures reachable ---")
for v, a, b, r, sh, ds, hx in best[:6]:
    print(f"  {v:.4f} {hx}  mix({a},{b},{r}) shade={sh} desat={ds}")

# does painting the same dark twice go darker?  does glazing?
dark = p.mix("ultramarine", "burnt_umber", 0.5)
p["dk"] = dark
print("\npigment value_of(dk) =", round(p.value_of(dark), 4))

s.block_in(region("left-half"), "flat", "dk", density=1.0, size=0.12)
s.block_in(region("right-half"), "flat", "dk", density=1.0, size=0.12)
s.dry()
print("after one coat:", s.compare(r"C:\temp\Level1.jpg").splitlines()[2][:40])

# glaze the right half four times with the same dark
for i in range(4):
    s.glaze([(0.55, 0.2), (0.95, 0.2), (0.95, 0.8), (0.55, 0.8)], "dk", opacity=0.35)
    s.dry()
print("look:", s.look())
print("log tail:")
print("\n".join(s.log().splitlines()[-6:]))
