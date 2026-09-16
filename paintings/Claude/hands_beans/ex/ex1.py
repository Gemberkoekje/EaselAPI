from easel import Session, Region

s = Session(900, 200, ground="toned_grey", seed=1, out_dir="out_ex1")
p = s.palette
dark = p.mix("ultramarine", "burnt_umber", 0.5)
lo, hi = p.value_of(dark), p.value_of("titanium_white")
print("floor", round(lo,3), "ceiling", round(hi,3), "palette darkest", round(p.darkest_value,3))
for i in range(9):
    target = lo + (hi - lo) * i / 8
    band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
    c = p.at_value(dark, target)
    s.block_in(band, "flat", c, density=1.0, size=0.06)
    print(f"step {i}  asked {target:.2f}  reads {p.value_of(c):.2f}  {p.hex(c)}")
print(s.look(values=True))
