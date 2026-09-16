# Pass 1: graphite. Free. Arrangement before any paint.
s.erase()
s.unguide("horizon")

print("values:")
for name in ("dusk_high", "dusk_mid", "glow", "glow_core", "water", "sheet",
             "water_near", "ink", "pier", "land", "warm_dark", "mast"):
    print(f"  {name:12s} {p.value_of(name):.2f}  chroma {p.chroma_of(name):.2f}")

print(s.compare({
    sky_upper(): 0.28,
    sky_low(): 0.50,
    water_far(): 0.40,
    sheet_shape(): 0.48,
    water_near_shape(): 0.34,
    headland(): 0.22,
    pier_deck(): 0.20,
    mid_boat(): 0.16,
}))

s.guide([(-0.02, 0.40), (0.18, 0.385), (0.28, 0.38), (0.70, 0.392), (1.02, 0.40)],
        note="horizon")
s.pencil(pier_deck().closed, pressure=0.55, smooth=False)
s.pencil(pier_face().closed, pressure=0.45, smooth=False)
s.pencil(sky_whole().closed, pressure=0.25, smooth=False)
s.pencil(headland().closed, pressure=0.5, smooth=False)
s.pencil(far_boat().closed, pressure=0.6, smooth=False)
s.pencil(mid_boat().closed, pressure=0.65, smooth=False)
s.pencil(dinghy_far_rim().closed, pressure=0.55, smooth=False)
s.pencil(dinghy_near_rim().closed, pressure=0.7, smooth=False)
s.pencil(dinghy_inside().closed, pressure=0.4, smooth=False)
s.pencil([s.pt("mid_mast_foot"), s.pt("mid_mast_top")], pressure=0.7)
s.pencil([s.pt("far_mast_foot"), s.pt("far_mast_top")], pressure=0.5)
s.pencil([P(2.15, 0.0, 5.2), P(2.15, 1.55, 5.2)], pressure=0.5)
s.pencil([P(2.15, 0.0, 7.4), P(2.15, 1.35, 7.4)], pressure=0.45)
s.pencil([P(2.15, 0.0, 10.5), P(2.15, 1.15, 10.5)], pressure=0.4)
s.look(grid=True, path="pass1_draw.png")
