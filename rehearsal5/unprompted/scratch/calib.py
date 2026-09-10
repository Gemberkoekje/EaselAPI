from easel import Session, Region

s = Session(900, 320, ground="toned_grey", seed=1)
p = s.palette
dark = p.mix("ultramarine", "burnt_umber", 0.5)
lo, hi = p.value_of(dark), p.value_of("titanium_white")
print("floor", round(lo, 3), "ceiling", round(hi, 3))


def at_value(target):
    a, b = 0.0, 1.0
    for _ in range(20):
        mid = (a + b) / 2
        a, b = (mid, b) if p.value_of(p.mix(dark, "titanium_white", mid)) < target else (a, mid)
    return (a + b) / 2


for i in range(9):
    r = at_value(lo + (hi - lo) * i / 8)
    band = Region(i / 9.0, 0.12, (i + 1) / 9.0, 0.88)
    s.block_in(band, "flat", p.mix(dark, "titanium_white", r), density=1.0, size=0.06)
    print(f"value {lo + (hi - lo) * i / 8:.2f}  white {r:.2f}")

# mixtures I expect to want
tests = {
    "sea_dark": p.mix("ultramarine", "burnt_umber", 0.35),
    "mud_mid": p.tint(p.mix("burnt_umber", "yellow_ochre", 0.45), 0.35),
    "sky_pale": p.tint(p.mix("cerulean", "cadmium_red", 0.18), 0.72),
    "warm_grey": p.tint(p.mix("ultramarine", "burnt_sienna", 0.5), 0.7),
    "weed": p.mix("viridian", "burnt_umber", 0.4),
    "hull_lit": p.tint(p.mix("yellow_ochre", "burnt_sienna", 0.3), 0.55),
}
for k, v in tests.items():
    print(k, p.hex(v), round(p.value_of(v), 3))

print(s.look(values=True))
print("strokes", s.stroke_count)
