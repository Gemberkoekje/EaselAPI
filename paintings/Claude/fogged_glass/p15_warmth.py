# What the picture is about is warmth you can see and not quite reach, and there is
# almost none in it. Not sunlight -- there is no sun on a day like this -- but the
# earth colours a greenhouse is full of: terracotta, timber, wet soil, brick. Glazes
# mixed close in value to what they land on, so they move the hue and not the value.
p["warmglaze"] = p.at_value(p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.34),
                                  "burnt_umber", 0.22), 0.44)
p["potdk"]     = p.at_value(p.mix(p.mix("burnt_sienna", "burnt_umber", 0.40),
                                  "ultramarine", 0.14), 0.30)

def along(hm, d0, d1, n=6):
    return [P(WALL, hm, d0 + (d1 - d0) * i / (n - 1.0)) for i in range(n)]

# --- warmth pools where the pots and the soil are. Laid the length of the bench it
#     came back as three orange bands: a stripe, not a glow.
for pts, sz, op in [
        ([(0.742, 0.902), (0.800, 0.866), (0.842, 0.902), (0.788, 0.930)], 0.052, 0.20),
        ([(0.670, 0.812), (0.716, 0.780), (0.752, 0.808)], 0.040, 0.17),
        ([(0.866, 0.988), (0.930, 0.950), (0.996, 0.982)], 0.058, 0.16),
        ([(0.626, 0.742), (0.664, 0.724), (0.698, 0.744)], 0.030, 0.13),
        ([(0.900, 0.882), (0.950, 0.856)], 0.034, 0.11)]:
    s.glaze(pts, "warmglaze", opacity=op, size=sz, note="glass")

# --- a second warm note further along, smaller, so the first reads as a rhythm and
#     not a blemish -- and one difference each: this one shows its rim, that one glows
s.dab(0.706, 0.792, "round_soft", "glow", size=0.020, press=2, note="subject")
s.stroke([(0.696, 0.784), (0.716, 0.782)], "round_hard", "potdk", size=0.008,
         pressure=[0.9, 0.3], load=1.0, opacity=0.8, tip_wobble=0.6, note="subject")
s.dab(0.784, 0.880, "round_hard", p.at_value(p["glow"], 0.48), size=0.008,
      press=3, tip_wobble=0.6, note="subject")

# --- and a breath of it on the brick, where the light bounces off the wet base
s.glaze([(0.396, 0.700), (0.462, 0.784), (0.520, 0.856)], "warmglaze",
        opacity=0.13, size=0.022, note="frame")
