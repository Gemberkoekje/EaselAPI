"""Guide exercises 1, 6, 8 condensed - calibration before the real painting."""
from easel import Session, Region, blob, cell

# --- Exercise 1: a value scale -------------------------------------------
s = Session(900, 200, ground="toned_grey", seed=1)
p = s.palette
dark = p.mix("ultramarine", "burnt_umber", 0.5)
lo, hi = p.value_of(dark), p.value_of("titanium_white")
print("darkest mix", p.hex(dark), round(lo, 3), " white", round(hi, 3))


def at_value(target):
    a, b = 0.0, 1.0
    for _ in range(20):
        mid = (a + b) / 2
        if p.value_of(p.mix(dark, "titanium_white", mid)) < target:
            a = mid
        else:
            b = mid
    return (a + b) / 2


for i in range(9):
    v = lo + (hi - lo) * i / 8
    r = at_value(v)
    band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
    s.block_in(band, "flat", p.mix(dark, "titanium_white", r), density=1.0, size=0.06)
    print(f"value {v:.2f}  white {r:.2f}")
print("scale ->", s.look(values=True))

# --- Exercise 6: mixing --------------------------------------------------
print()
for a, b, r in [("yellow_ochre", "titanium_white", 0.6),
                ("burnt_umber", "titanium_white", 0.6),
                ("yellow_ochre", "burnt_sienna", 0.35),
                ("ultramarine", "burnt_sienna", 0.5),
                ("cerulean", "titanium_white", 0.75),
                ("ultramarine", "titanium_white", 0.85),
                ("yellow_ochre", "cerulean", 0.2)]:
    c = p.mix(a, b, r)
    print(f"{a} + {b} @{r} -> {p.hex(c)}  v={p.value_of(c):.2f}")
