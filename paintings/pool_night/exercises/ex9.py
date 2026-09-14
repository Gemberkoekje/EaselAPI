from easel import Session, Region

s = Session(1000, 220, ground="toned_grey", seed=9, out_dir="out9", timelapse=False)
p = s.palette
plan = {
    "night":  p.at_value(p.mix("cerulean", "burnt_umber", 0.55), 0.16),
    "truss":  p.at_value(p.mix("burnt_umber", "ultramarine", 0.40), 0.21),
    "wall":   p.at_value(p.mix(p.mix("cerulean", "burnt_umber", 0.45), "viridian", 0.25), 0.34),
    "deckfar":p.at_value(p.desaturate(p.mix("cerulean", "yellow_ochre", 0.40), 0.45), 0.39),
    "deck":   p.at_value(p.desaturate(p.mix("cerulean", "yellow_ochre", 0.35), 0.35), 0.48),
    "water":  p.at_value(p.mix("cerulean", "viridian", 0.45), 0.64),
    "watlit": p.at_value(p.mix(p.mix("cerulean", "viridian", 0.35), "titanium_white", 0.5), 0.82),
    "core":   p.at_value(p.mix("cerulean", "titanium_white", 0.82), 0.93),
    "warm":   p.at_value(p.mix("cadmium_red", "yellow_ochre", 0.40), 0.50),
}
n = len(plan)
for i, (name, colour) in enumerate(plan.items()):
    band = Region(i / n + 0.004, 0.10, (i + 1) / n - 0.004, 0.90)
    s.block_in(band, "flat", colour, size=0.07, solid=True)
    print(f"{name:8s} {p.hex(colour)}  value {p.value_of(colour):.2f}  chroma {p.chroma_of(colour):.2f}")
print(s.look())
print(s.look(values=True))
