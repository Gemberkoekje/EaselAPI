# Last marks. The pot is reading as if it were on the near side of the glass -- one
# thin film to seat it behind. And the building is not standing on anything: a
# shadow where the base meets the ground, and the weeds that grow in that corner.
p["foot"] = p.at_value(p.mix(p["neutral"], "burnt_umber", 0.34), 0.31)
p["weed"] = p.at_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.44), 0.62), 0.44)

s.glaze([(0.680, 0.852), (0.712, 0.872), (0.732, 0.898)], "fogthin",
        opacity=0.13, size=0.040, note="subject")

# the dark where the base meets the ground: a step or two below, and it loses its
# far end rather than running out to a point
s.stroke([(0.288, 0.572), (0.372, 0.724), (0.462, 0.888), (0.524, 1.010)],
         "round_hard", "foot", size=0.016, pressure=[0.0, 0.32, 0.72, 1.0],
         load=1.0, opacity=0.72, jitter=0.014, note="ground")

# weeds in the angle, each sized off how far away it is
for x, y, h, w, leans, op in [(0.352, 0.700, 0.036, 0.0034, (-0.35, 0.20), 0.62),
                              (0.441, 0.864, 0.058, 0.0046, (0.26, -0.18, 0.52), 0.72),
                              (0.494, 0.958, 0.074, 0.0056, (-0.30, 0.12), 0.78),
                              (0.402, 0.798, 0.046, 0.0040, (0.40,), 0.66)]:
    for k, lean in enumerate(leans):
        hk = h * (1.0 - 0.15 * k)
        s.stroke([(x + k * w * 0.8, y), (x + k * w * 0.8 + lean * hk * 0.45, y - hk * 0.6),
                  (x + k * w * 0.8 + lean * hk, y - hk)], "liner", "weed",
                 size=w * (1.0 - 0.16 * k), pressure=[0.95, 0.45, 0.0], load=1.0,
                 opacity=op * (1.0 - 0.13 * k), note="ground")
