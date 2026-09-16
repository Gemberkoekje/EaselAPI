s.erase()
for shape in (SKY, YARD, GLASS, BASE, LIP, PATH):
    s.pencil(shape.closed, pressure=0.45, smooth=False)
for dm in BAR_DM:
    s.pencil([P(WALL, EAVE, dm), P(WALL, 0.0, dm)], pressure=0.42, smooth=False)
for m in (TALL, BANK, HANG, DIM):
    s.pencil(m.closed, pressure=0.34)
for pts, w in RUNNELS:
    s.pencil(pts, pressure=0.20 + 0.25 * w)
s.pencil(TRUNK, pressure=0.6)
for pts, w in BOUGHS:
    s.pencil(pts, pressure=w * 0.7)
s.pencil(CROWN.closed, pressure=0.15)
s.mark("eave_r", *EAVE_R); s.mark("eave_f", *EAVE_F)
s.mark("sill_b", *SILL_B); s.mark("vp", VX, VY)
