# mixtures, landmarks, masses -- shared by every pass
# Why this subject: the only light in the picture is inside it -- a screen in a dark
# room -- so every form is lit by the subject itself, and the painting is about the
# fall of that light, not about a monitor.

p = s.palette
p["room"]    = p.at_value(p.mix("ultramarine", "burnt_umber", 0.45), 0.16)
p["room_c"]  = p.at_value(p.mix("ultramarine", "burnt_umber", 0.55), 0.19)
p["halo_a"]  = p.at_value(p.mix("viridian", "burnt_umber", 0.40), 0.20)
p["halo_b"]  = p.at_value(p.mix("viridian", "burnt_umber", 0.40), 0.26)
p["desk"]    = p.at_value(p.mix("burnt_umber", "ultramarine", 0.35), 0.21)
p["fore"]    = p.at_value(p.mix("ultramarine", "burnt_umber", 0.50), 0.14)
p["pool_a"]  = p.at_value(p.mix("cerulean", "lemon_yellow", 0.55), 0.24)
p["pool_b"]  = p.at_value(p.mix("cerulean", "lemon_yellow", 0.55), 0.37)
p["glass"]   = p.at_value(p.mix("viridian", "burnt_umber", 0.45), 0.28)
p["glass_lit"] = p.at_value(p.mix("viridian", "burnt_umber", 0.42), 0.33)
p["phos"]    = p.at_value(p.mix("lemon_yellow", "cerulean", 0.30), 0.72)
p["phos_dim"] = p.at_value(p.mix("lemon_yellow", "cerulean", 0.34), 0.56)
p["cursor"]  = p.at_value(p.mix("lemon_yellow", "cerulean", 0.20), 0.85)
p["bezel"]   = p.at_value(p.mix("ultramarine", "burnt_umber", 0.50), 0.14)
p["key"]     = p.at_value(p.mix("burnt_umber", "ultramarine", 0.40), 0.17)
p["key_rim"] = p.at_value(p.mix("cerulean", "lemon_yellow", 0.45), 0.42)
p["mug"]     = p.at_value(p.mix("burnt_umber", "ultramarine", 0.30), 0.20)
p["mug_rim"] = p.at_value(p.mix("cerulean", "lemon_yellow", 0.40), 0.50)
p["shadow"]  = p.at_value(p.mix("ultramarine", "burnt_umber", 0.50), 0.18)

# landmarks -- the drawing hangs on these
s.mark("scr_tl", 0.320, 0.215)
s.mark("scr_tr", 0.688, 0.205)
s.mark("scr_br", 0.694, 0.565)
s.mark("scr_bl", 0.316, 0.545)
s.mark("bz_tl", 0.303, 0.199)
s.mark("bz_tr", 0.705, 0.189)
s.mark("bz_br", 0.712, 0.583)
s.mark("bz_bl", 0.299, 0.561)
s.mark("kb_tl", 0.372, 0.665)
s.mark("kb_tr", 0.640, 0.665)
s.mark("kb_bl", 0.358, 0.735)
s.mark("kb_br", 0.655, 0.735)
s.mark("mug_c", 0.795, 0.700)

# named masses -- keep every mass in a named function so repairs re-run the stack
scr   = polygon([s.pt("scr_tl"), s.pt("scr_tr"), s.pt("scr_br"), s.pt("scr_bl")])
bezel = polygon([s.pt("bz_tl"), s.pt("bz_tr"), s.pt("bz_br"), s.pt("bz_bl")])
kb    = polygon([s.pt("kb_tl"), s.pt("kb_tr"), s.pt("kb_br"), s.pt("kb_bl")])
halo  = blob(span("C1", "G6"), wobble=0.22, seed=4)
pool  = polygon([(0.30, 0.655), (0.73, 0.655), (0.88, 0.865), (0.16, 0.865)])
desk_band = polygon([(0.0, 0.645), (1.0, 0.645), (1.0, 0.865), (0.0, 0.865)])
fore  = polygon([(0.0, 0.865), (1.0, 0.865), (1.0, 1.05), (0.0, 1.05)])
