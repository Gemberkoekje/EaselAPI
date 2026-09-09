from easel import Session, Region

s = Session(900, 200, ground="toned_grey", seed=1)
for i in range(9):
    v = i / 8.0
    band = Region(i / 9.0, 0.15, (i + 1) / 9.0, 0.85)
    s.block_in(band, "flat", s.palette.mix("burnt_umber", "titanium_white", v),
               density=1.0, size=0.06)
print(s.look(values=True))
