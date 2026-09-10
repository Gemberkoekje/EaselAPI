# Pass 12 - turn the pot: eight overlapping steps across the form, then cross them.
p = s.palette
s.dry()
vmid = p.value_of(p["terra_mid"])
def terra_at(v):
    a, b, lo, hi = 0.0, 1.0, p["terra_mid"], (p["terra_hi"] if v >= vmid else p["terra_sh"])
    up = v >= vmid
    for _ in range(22):
        m = (a + b) / 2
        got = p.value_of(p.mix(lo, hi, m))
        if (got < v) == up: a = m
        else: b = m
    return p.mix(lo, hi, (a + b) / 2)

steps = [(0.334,0.395),(0.352,0.470),(0.372,0.492),(0.394,0.445),(0.416,0.380),
         (0.438,0.315),(0.458,0.255),(0.478,0.200),(0.496,0.185),(0.508,0.215)]
for i, (xt, v) in enumerate(steps):
    f = (xt - 0.3265) / 0.1855
    xb = 0.3525 + f * 0.1295
    yt = 0.690 + f * 0.002
    yb = 0.8595 + f * 0.008
    s.stroke([(xt, yt + 0.008), ((xt + xb) / 2 + (0.003 if i % 2 else -0.002), (yt + yb) / 2),
              (xb, yb - 0.008)], "bristle", terra_at(v),
             size=(0.030 if i % 3 == 0 else 0.024), load=0.95,
             pressure=("even" if i % 2 else [0.9, 1.0, 0.75]))

# marks that run round the form, breaking the vertical joins
s.stroke([(0.340,0.716),(0.402,0.732),(0.464,0.726)], "bristle", terra_at(0.40),
         size=0.013, pressure="taper", load=0.55)
s.stroke([(0.346,0.768),(0.410,0.784),(0.472,0.776)], "bristle", terra_at(0.335),
         size=0.011, pressure="taper", load=0.45)
s.stroke([(0.352,0.822),(0.414,0.842),(0.474,0.834)], "bristle", terra_at(0.375),
         size=0.015, pressure="taper", load=0.6)
s.stroke([(0.404,0.700),(0.462,0.712)], "bristle", terra_at(0.29),
         size=0.010, pressure="taper", load=0.45)
s.stroke([(0.358,0.854),(0.428,0.868)], "bristle", terra_at(0.30),
         size=0.012, pressure="taper", load=0.5)

# --- the rim again, lighter in touch ------------------------------------------
s.stroke([(0.322,0.666),(0.364,0.647),(0.418,0.641),(0.472,0.647),(0.514,0.666)],
         "flat", terra_at(0.45), size=0.015, pressure="even", load=1.0)
s.block_in(ellipse(Region(0.334, 0.650, 0.500, 0.688)).inset(0.007), "flat", "pot_in",
           direction=(6, 174), density=1.0, size=0.015, load=1.0, pressure="even")
s.stroke([(0.346,0.658),(0.402,0.652),(0.458,0.657)], "round_hard",
         p.mix(p["pot_in"], "burnt_sienna", 0.35), size=0.007, pressure=[0.35,0.85,0.35])
s.stroke([(0.322,0.670),(0.366,0.692),(0.418,0.698),(0.470,0.692),(0.512,0.672)],
         "flat", terra_at(0.44), size=0.016, pressure="even", load=1.0)
s.stroke([(0.330,0.668),(0.374,0.688),(0.420,0.694)], "round_hard", "terra_hi",
         size=0.006, pressure=[0.45,1.0,0.25])
s.stroke([(0.340,0.686),(0.390,0.708),(0.444,0.712),(0.494,0.702)], "round_hard",
         "terra_sh", size=0.006, pressure=[0.3,0.9,0.9,0.35])

# --- the crack, over the new paint --------------------------------------------
s.stroke([(0.366,0.702),(0.379,0.744),(0.370,0.788),(0.383,0.828),(0.380,0.858)],
         "round_hard", "crack", size=0.0050, pressure=[1.0,0.85,1.0,0.65,0.3])
s.stroke([(0.362,0.712),(0.374,0.748)], "round_hard", "terra_hi",
         size=0.0032, pressure=[0.6,0.25])
s.stroke([(0.373,0.762),(0.392,0.790)], "round_hard", "crack",
         size=0.0038, pressure=[0.75,0.15])

# --- silhouette ----------------------------------------------------------------
s.stroke([(0.312,0.692),(0.320,0.772),(0.336,0.856)], "flat", "bg", size=0.024,
         pressure="even", load=1.0)
s.stroke([(0.524,0.688),(0.514,0.762),(0.498,0.842)], "flat", "cast", size=0.024,
         pressure="even", load=1.0)
s.stroke([(0.352,0.888),(0.420,0.898),(0.488,0.884)], "flat", "cast", size=0.022,
         pressure="even", load=1.0)
s.stroke([(0.356,0.872),(0.418,0.882),(0.478,0.872)], "round_hard",
         p.mix(p["cast"], "burnt_umber", 0.5), size=0.011, pressure=[0.6,1.0,0.5])

print("strokes:", s.stroke_count)
print(s.look(region=span("C5","F8"), sketch=False))
