# Two repairs. The inset pulled the glass off the right frame and left a pale strip
# -- a mass that meets the frame should run off it. And the pressed leaf came back a
# cauliflower, because a round tip filling a hull prints its own outline. Both are
# buried with marks shaped like the pane, not with a rectangle: cover() ran its ends
# outside the area and left a panel.
p["panefix"] = p.at_value(p.desaturate(p.mix(p["neutral"], "viridian", 0.20), 0.30), 0.40)
p["panelit"] = p.at_value(p.desaturate(p.mix(p["neutral"], "cerulean", 0.10), 0.35), 0.50)

# --- the glass runs off the right frame
for x, sz, ld, op in [(0.968, 0.042, 1.0, 0.95), (1.006, 0.046, 1.0, 0.95),
                      (1.040, 0.050, 1.0, 0.95)]:
    s.stroke([(x - 0.004, 0.155), (x + 0.005, 0.52), (x - 0.003, 1.06)],
             "bristle", "panefix", size=sz, load=ld, load_falloff=0.0,
             opacity=op, pressure="even", jitter=0.012, note="glass")
s.stroke([(0.955, 0.22), (1.02, 0.46), (0.985, 0.82)], "bristle", "panelit",
         size=0.030, load=0.55, load_falloff=0.35, opacity=0.45,
         pressure="swell", note="glass")
# the pane laps and the runnel that ran through the strip, put back
for hm, wm, op in [(2.02, 0.018, 0.48), (1.54, 0.020, 0.55)]:
    dm0, dm1 = F * WALL / (1.06 - VX), F * WALL / (0.940 - VX)
    s.stroke([P(WALL, hm, dm1), P(WALL, hm, dm0)], "round_hard", "bar",
             size=F * wm / dm0, pressure="even", opacity=op,
             jitter=0.01, size_jitter=0.03, load=1.0, load_falloff=0.0, note="frame")
s.stroke([(0.977, 0.205), (0.970, 0.44), (0.981, 0.63), (0.973, 0.76)],
         "round_hard", "runnelup", size=0.009, pressure=[0.35, 1.0, 0.5, 0.0],
         load=0.6, load_falloff=0.45, opacity=0.72, jitter=0.012,
         tip_wobble=0.35, note="subject")

# --- bury the cauliflower with pane, not with a panel
s.stroke([(0.908, 0.372), (0.922, 0.432), (0.914, 0.492)], "round_hard", "panefix",
         size=0.030, load=1.0, load_falloff=0.0, opacity=1.0, pressure="even",
         jitter=0.012, note="glass")
s.stroke([(0.952, 0.368), (0.962, 0.428), (0.955, 0.488)], "round_hard", "panefix",
         size=0.032, load=1.0, load_falloff=0.0, opacity=1.0, pressure="even",
         jitter=0.012, note="glass")
s.stroke([(0.930, 0.360), (0.940, 0.500)], "round_hard", p.at_value(p["panefix"], 0.43),
         size=0.028, load=1.0, load_falloff=0.0, opacity=0.95, pressure="even",
         jitter=0.012, note="glass")
s.dry()

# --- the leaf, as marks that have a direction: two tapers that meet, and a midrib
p["press"] = p.at_value(p.desaturate(p.mix(p.mix("viridian", "yellow_ochre", 0.36),
                                           "burnt_umber", 0.12), 0.22), 0.30)
p["rib"]   = p.at_value(p.mix(p.mix("viridian", "yellow_ochre", 0.55),
                              "titanium_white", 0.26), 0.47)
s.stroke([(0.912, 0.452), (0.941, 0.418), (0.977, 0.400)], "round_hard", "press",
         size=0.020, pressure=[0.0, 1.0, 0.15], load=1.0, opacity=0.9,
         jitter=0.012, note="subject")
s.stroke([(0.912, 0.452), (0.947, 0.441), (0.977, 0.400)], "round_hard", "press",
         size=0.014, pressure=[0.0, 0.9, 0.2], load=1.0, opacity=0.85,
         jitter=0.012, note="subject")
s.stroke([(0.916, 0.448), (0.946, 0.424), (0.974, 0.403)], "liner", "rib",
         size=0.0035, pressure=[0.0, 0.8, 0.0], load=1.0, opacity=0.75, note="subject")
