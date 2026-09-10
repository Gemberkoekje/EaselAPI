"""own1, pass 5 - finishing. Break the last two straight edges, put the sun
back (the haze had swallowed it), and stop."""
p = s.palette
s.dry()

for x, y, w, col, sz in [(0.44, 0.660, 0.20, "wat_near", 0.017),
                         (0.66, 0.905, 0.22, "wat_near", 0.019),
                         (0.70, 0.822, 0.17, "wat_near", 0.015),
                         (0.46, 0.742, 0.14, "wat_far", 0.013)]:
    s.stroke([(x, y), (x + w, y + 0.004)], "bristle", col, size=sz,
             opacity=0.85, load=0.95, note="last of the straight edge")

s.dab(0.632, 0.398, "round_hard", "sun", size=0.042, press=3)
s.dab(0.632, 0.396, "round_hard", "titanium_white", size=0.018, press=3)

# the sun catches the top of the far bank right under it
s.stroke([(0.560, 0.452), (0.640, 0.446), (0.712, 0.452)], "liner",
         p.mix(p["glow"], "titanium_white", 0.3), size=0.004,
         pressure=[0.3, 1.0, 0.3], note="sun on the bank")
s.stroke([(0.596, 0.490), (0.668, 0.487)], "bristle", "wat_lit", size=0.010,
         opacity=0.9, load=1.0, note="first glint")

# two dark passages so the water is not one value all the way across
s.stroke([(0.03, 0.560), (0.26, 0.556)], "bristle", "bank", size=0.014,
         opacity=0.35, load=0.9, note="dark in the far water")
s.stroke([(0.84, 0.612), (1.00, 0.608)], "bristle", "bank", size=0.016,
         opacity=0.35, load=0.9, note="dark in the far water")

# light on the tips of two reeds and one on the near bank
s.stroke([(0.208, 0.800), (0.222, 0.782)], "liner", "wat_lit", size=0.004,
         pressure=[0.9, 0.2], note="lit reed")
s.stroke([(0.312, 0.762), (0.322, 0.744)], "liner", "wat_lit", size=0.003,
         pressure=[0.9, 0.2], note="lit reed")
s.stroke([(0.06, 0.938), (0.20, 0.926), (0.33, 0.934)], "bristle",
         p.mix(p["mud"], p["wat_lit"], 0.35), size=0.008, opacity=0.5,
         load=0.8, note="light on the near bank")

print("strokes:", s.stroke_count)
print(s.look())
print(s.export("own1_final.png"))
print(s.timelapse_gif("own1_timelapse.gif"))
