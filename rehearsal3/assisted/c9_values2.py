# Pass 9 — re-plan values now that compare() has told me the reference's real map.
# The table is 0.36-0.58, not 0.65; the mug's left half is 0.06-0.20, below my floor.
# Run: python c9_values2.py
from easel import Session

p = Session(200, 200, seed=1).palette
M, T, D, S = p.mix, p.tint, p.desaturate, p.shade

cand = {
    "wood_dim":  D(M("yellow_ochre", "burnt_umber", 0.55), 0.30),
    "wood_mid":  T(D(M("yellow_ochre", "burnt_umber", 0.45), 0.30), 0.10),
    "wood_lit":  T(D(M("yellow_ochre", "burnt_umber", 0.32), 0.28), 0.28),
    "wood_warm": T(M("yellow_ochre", "burnt_sienna", 0.30), 0.22),
    "shadow":    D(M("ultramarine", "burnt_umber", 0.62), 0.25),
    "shad_core": S(M("ultramarine", "burnt_umber", 0.55), 0.55),
    "shad_edge": T(D(M("ultramarine", "burnt_umber", 0.60), 0.35), 0.16),
    "mug_lit":   T(M("cerulean", "titanium_white", 0.93), 0.35),
    "mug_mid":   T(M("ultramarine", "burnt_umber", 0.42), 0.66),
    "mug_dim":   T(M("ultramarine", "burnt_umber", 0.48), 0.45),
    "tea":       S(M("burnt_umber", "ultramarine", 0.35), 0.8),
    "figure":    M("burnt_umber", "burnt_sienna", 0.22),
    "fig_lit":   T(M("burnt_umber", "burnt_sienna", 0.50), 0.14),
    "steel":     T(D("cerulean", 0.72), 0.48),
    "dark_bg":   S(M("ultramarine", "burnt_umber", 0.60), 0.9),
}
for k, c in cand.items():
    print(f"{k:10s} {p.hex(c)}  {p.value_of(c):.3f}")
print("\nref targets: woodA .36  woodB/C .42  woodF .55  woodG .48  woodH .43")
print("             shadow .32   tea/figure .06-.22 (floor is .23)   ground .54")
