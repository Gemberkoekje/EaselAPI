from easel import Session, Region

s = Session(900, 200, ground="toned_grey", seed=1)
p = s.palette
dark = p.mix("ultramarine", "burnt_umber", 0.5)
lo, hi = p.value_of(dark), p.value_of("titanium_white")
for i in range(9):
    target = lo + (hi - lo) * i / 8
    band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
    s.block_in(band, "flat", p.at_value(dark, target), density=1.0, size=0.06)
    print(f"value {target:.2f}  reads {p.value_of(p.at_value(dark, target)):.2f}")
print(s.look(values=True))
