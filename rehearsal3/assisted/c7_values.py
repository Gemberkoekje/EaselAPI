# Pass 7 — plan the values as numbers before mixing anything (PAINTER.md step 2).
# Throwaway session; touches no canvas.  Run: python c7_values.py
from easel import Session

p = Session(200, 200, seed=1).palette

cand = {
    # the table
    "wood":       p.tint(p.mix("yellow_ochre", "burnt_umber", 0.40), 0.35),
    "wood_lit":   p.tint(p.mix("yellow_ochre", "burnt_umber", 0.25), 0.55),
    "wood_dim":   p.tint(p.mix("yellow_ochre", "burnt_umber", 0.62), 0.22),
    # the cast shadow
    "shadow":     p.tint(p.mix("ultramarine", "burnt_umber", 0.62), 0.28),
    "shadow_out": p.tint(p.mix("ultramarine", "burnt_sienna", 0.55), 0.40),
    # the mug
    "mug_lit":    p.tint(p.mix("cerulean", "titanium_white", 0.90), 0.55),
    "mug_mid":    p.tint(p.mix("ultramarine", "burnt_umber", 0.45), 0.72),
    "mug_dim":    p.tint(p.mix("ultramarine", "burnt_umber", 0.50), 0.58),
    # the dark things
    "tea":        p.shade(p.mix("burnt_umber", "ultramarine", 0.30), 0.6),
    "figure":     p.mix("burnt_umber", "burnt_sienna", 0.30),
    "figure_lit": p.tint(p.mix("burnt_umber", "burnt_sienna", 0.45), 0.18),
    "tag":        p.shade(p.mix("ultramarine", "burnt_umber", 0.40), 0.45),
    "steel":      p.tint(p.desaturate("cerulean", 0.7), 0.55),
    "hi":         p.tint("titanium_white", 0.0),
}
for k, c in cand.items():
    print(f"{k:12s} {p.hex(c)}  {p.value_of(c):.3f}")
print()
print("darkest reachable :", p.hex(p.shade(p.mix("ultramarine", "burnt_umber", 0.5), 1.0)),
      round(p.value_of(p.shade(p.mix("ultramarine", "burnt_umber", 0.5), 1.0)), 3))
print("white             :", p.hex("titanium_white"), round(p.value_of("titanium_white"), 3))
print("ground toned_warm_grey #94897A")
