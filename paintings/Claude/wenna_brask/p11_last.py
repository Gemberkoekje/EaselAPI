"""Pass 11: the why, read back. 'A mother who has not slept' -- her eyes were open and alert, so
the upper lids come down over the irises and the dark under them deepens a little. 'Everything
else is dusk' -- the shawl's lower left, furthest from the lamp, goes down another step. Then
the signature."""

p["under_eye"] = p.at_value(p.mix_many(["skin_mid", "burnt_umber", "ultramarine"], [8, 1, 0.5]), 0.42)
p["socket"] = p.at_value(p.mix("skin_mid", "skin_shade", 0.4), 0.38)
p["dusk"] = p.at_value(p.mix("shawl", "mill", 0.5), 0.145)
p["mark"] = p.at_value(p.mix("mill", "glow_wall", 0.3), 0.18)
F = dict(clip=face, note="subject")

s.dry()
# Heavy lids: the lid line comes down over the top of each iris, a crease above it.
s.stroke([P(348, 286), P(360, 285.5), P(372, 287)], "round_hard", "skin_mid", size=0.005,
         opacity=0.85, pressure=[0.4, 1.0, 0.6], tip_wobble=0.35, **F)
s.stroke([P(346, 281), P(358, 278), P(372, 280)], "round_hard", "socket", size=0.003,
         opacity=0.6, pressure=[0.3, 1.0, 0.4], tip_wobble=0.35, **F)
s.stroke([P(414, 281), P(421, 280), P(427, 281)], "round_hard", "skin_mid", size=0.003,
         opacity=0.8, pressure=[0.4, 1.0, 0.5], tip_wobble=0.35, **F)
s.stroke([P(348, 299), P(360, 302), P(372, 299)], "round_soft", "under_eye", size=0.009,
         opacity=0.25, pressure=[0.3, 1.0, 0.4], **F)

# The half-tone band down the side of her face still shows its passes as stripes: one soft
# film of its own colour over it.
s.dry()
s.glaze([P(354, 252), P(338, 330), P(350, 412)], "skin_mid", opacity=0.3, size=0.03,
        pressure=[0.5, 1.0, 0.6], **F)

# The dusk takes the part of her furthest from the lamp.
s.dry()
s.glaze([P(-40, 760), P(200, 960), P(460, 1070)], "dusk", opacity=0.35, size=0.32,
        pressure=[1.0, 0.8, 0.4], clip=shawl)
s.dry()

# The signature: a bell's outline with no clapper, small, in the wall's own dark.
s.stroke([P(734, 1004), P(738, 993), P(745, 988), P(752, 993), P(756, 1004)], "liner", "mark",
         size=0.003, opacity=0.9, note="signature")
s.stroke([P(731, 1005), P(759, 1005)], "liner", "mark", size=0.003, opacity=0.9,
         note="signature")

print(s.look(region="C2:E3", path="looks/11-eyes-crop.png"))
print(s.look(sketch=False, path="looks/11-final.png"))
print(s.look(values=True, sketch=False, path="looks/11-final-values.png"))
