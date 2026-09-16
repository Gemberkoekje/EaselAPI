# pass 2, take two -- monitor, back to front; glow inside the glass as crossing-free glazes
neck = polygon([(0.478, 0.583), (0.532, 0.583), (0.528, 0.648), (0.482, 0.648)])
base = polygon([(0.428, 0.645), (0.590, 0.645), (0.596, 0.658), (0.422, 0.658)])

s.block_in(neck, "flat", p["shadow"], size=0.018, solid=True, pressure="even",
           direction=90)
s.block_in(base, "flat", p["shadow"], size=0.016, solid=True, pressure="even",
           direction=0)
s.dry()                                   # bezel must cover, not mix with the halo
s.block_in(bezel, "flat", p["bezel"], size=0.035, solid=True, opacity=1.0,
           pressure="even", direction=(s.pt("bz_tl"), s.pt("bz_tr")), edge="clean")
s.block_in(scr, "round_hard", p["glass"], size=0.045, solid=True, opacity=1.0,
           pressure="even", direction=(s.pt("scr_tl"), s.pt("scr_tr")), edge="clean")

# glow pooling behind the text: three horizontal glazes, no crossings
glass_field = s.sample(scr)
gv = p.value_of(glass_field)
p["glow_mid"] = p.at_value(p.mix(glass_field, p["glass_lit"], 0.8), gv + 0.045)
s.glaze([(0.38, 0.36), (0.50, 0.345), (0.63, 0.355)], p["glow_mid"], opacity=0.20,
        size=0.13, pressure=[0.3, 1.0, 0.3], brush="round_soft")
s.glaze([(0.42, 0.30), (0.51, 0.295), (0.60, 0.30)], p["glow_mid"], opacity=0.14,
        size=0.10, pressure=[0.3, 1.0, 0.3], brush="round_soft")
s.glaze([(0.44, 0.42), (0.52, 0.415), (0.60, 0.425)], p["glow_mid"], opacity=0.14,
        size=0.09, pressure=[0.3, 1.0, 0.3], brush="round_soft")

s.block_in(kb, "flat", p["key"], size=0.035, solid=True, opacity=1.0,
           pressure="even", direction=(s.pt("kb_tl"), s.pt("kb_tr")), edge="hard")
s.look()
s.look(region=span("E2", "H5"), values=True, impasto=False)
