# Pass 10 — the table. Biggest brush, quiet masses, flat (not bristle) so the
# weave does not print corduroy across the whole picture.
# Run: python -m easel run painting.easel c10_wood.py
REF = r"C:\temp\Level1.jpg"
p = s.palette
M, T, D, S = p.mix, p.tint, p.desaturate, p.shade

p["wood_dim"] = T(D(M("yellow_ochre", "burnt_umber", 0.55), 0.30), 0.06)
p["wood_mid"] = T(D(M("yellow_ochre", "burnt_umber", 0.45), 0.30), 0.18)
p["wood_lit"] = T(D(M("yellow_ochre", "burnt_umber", 0.32), 0.28), 0.40)
p["wood_warm"] = T(D(M("yellow_ochre", "burnt_sienna", 0.28), 0.22), 0.30)
p["dark_bg"] = S(M("ultramarine", "burnt_umber", 0.60), 0.9)
for k in ("wood_dim", "wood_mid", "wood_lit", "wood_warm", "dark_bg"):
    print(f"{k:10s} {p.hex(p[k])} {p.value_of(p[k]):.3f}")

n0 = s.stroke_count
s.block_in(region("all"), "flat", "wood_mid", density=0.9, size=0.17,
           direction="diagonal")
print("base pass:", s.stroke_count - n0)

n0 = s.stroke_count
s.block_in(span("A1", "B8"), "flat", "wood_dim", density=0.85, size=0.15,
           direction="vertical")
s.block_in(span("A1", "H1"), "flat", "wood_dim", density=0.55, size=0.12,
           direction="horizontal")
print("darks:", s.stroke_count - n0)

n0 = s.stroke_count
s.block_in(span("F1", "G8"), "flat", "wood_lit", density=0.85, size=0.15,
           direction="diagonal")
s.block_in(span("D8", "F8"), "flat", "wood_lit", density=0.7, size=0.13,
           direction="horizontal")
print("lights:", s.stroke_count - n0)

print(s.look(reference=REF, values=True))
print("total strokes:", s.stroke_count)
