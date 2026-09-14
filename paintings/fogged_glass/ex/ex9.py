from easel import Session, Region
s = Session(900, 200, ground="toned_grey", seed=9)
p = s.palette
plan = {"haze": p.at_value(p.mix("cerulean", "titanium_white", 0.8), 0.64),
        "deep": p.at_value(p.mix("cerulean", "burnt_umber", 0.4), 0.40),
        "dark": p.at_value(p.mix("burnt_umber", "viridian", 0.3), 0.20),
        "lit":  p.at_value(p.mix("yellow_ochre", "titanium_white", 0.6), 0.78)}
for i, (name, colour) in enumerate(plan.items()):
    band = Region(0.05 + i * 0.225, 0.15, 0.25 + i * 0.225, 0.85)
    s.block_in(band, "flat", colour, size=0.08, solid=True)
    print(f"{name:5s} value {p.value_of(colour):.2f}  chroma {p.chroma_of(colour):.2f}")
print(s.look())
