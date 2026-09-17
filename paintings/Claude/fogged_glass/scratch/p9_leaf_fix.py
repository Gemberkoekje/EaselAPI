# The pressed leaf came back a cauliflower: a round tip filling a hull prints its
# own outline. Bury it and lay it as marks that have a direction -- two tapering
# strokes that meet, and a midrib.
from easel import Region

around = s.sample(Region(0.900, 0.330, 0.995, 0.380))     # the pane beside it
s.cover(Region(0.905, 0.380, 0.985, 0.478), around)
s.dry()

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
