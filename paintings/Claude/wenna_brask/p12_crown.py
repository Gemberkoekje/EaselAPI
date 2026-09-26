"""Pass 12: the kerchief's crown read as the band of a knitted cap -- a warm stripe across the
top of the head. It is the part of her the sky lights, so it is cooled with one film of the
sky mixed into its own colour."""

p["crown_cool"] = p.at_value(p.mix("kerchief", "sky_mid", 0.5), 0.27)
s.dry()
s.glaze([P(236, 150), P(290, 122), P(350, 128), P(372, 148)], "crown_cool", opacity=0.45,
        size=0.05, pressure=[0.4, 1.0, 1.0, 0.3], clip=kerchief, note="subject")
s.dry()
print(s.look(region="C1:E3", sketch=False, path="looks/12-crown-crop.png"))
print(s.look(sketch=False, path="looks/12-final.png"))
