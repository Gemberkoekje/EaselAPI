# The subject's incident: what makes the tower a made thing with a scale -- the
# lamp's hot centre, the lamplight caught along the gallery, a door, two windows
# at different heights, the glow warmer low on the lit side, a touch of warm on the cap.
S = dict(note="subject")
s.stroke([(TX - 0.016, 0.1987), (TX - 0.004, 0.1983), (TX + 0.013, 0.1988)], "round_hard",
         "lantern2", size=0.0032, opacity=0.8, pressure=[0.2, 1.0, 0.6, 0.1], **S)   # gallery lit
s.stroke([(TX - 0.003, 0.5385), (TX - 0.003, 0.5215)], "flat", "land", size=0.0075,
         opacity=0.9, load=1.0, load_falloff=0.0, pressure="even", clip=tower, **S)   # door
s.stroke([(TX + 0.0015, 0.311), (TX + 0.0015, 0.324)], "round_hard", "land", size=0.0036,
         opacity=0.75, tip_wobble=0.3, pressure=[0.6, 1.0, 0.7], **S)                 # window
s.stroke([(TX - 0.001, 0.424), (TX - 0.001, 0.433)], "round_hard", "land", size=0.0031,
         opacity=0.65, tip_wobble=0.3, pressure=[0.7, 1.0, 0.6], **S)                 # window
s.dry()
p["tower_warm"] = p.at_value(p.mix("tower_lit", "glow", 0.25), 0.43)
s.glaze([(TX - 0.0105, 0.537), (TX - 0.0095, 0.470), (TX - 0.0085, 0.400)], "tower_warm",
        opacity=0.22, size=0.013, pressure=[1.0, 0.7, 0.2], clip=tower, **S)          # glow, low
s.dab(TX - 0.0068, 0.1512, "round_hard", "rim", size=0.0035, press=2, tip_wobble=0.4, **S)
s.dry()
p["lamp_core"] = p.mix("titanium_white", "lemon_yellow", 0.04)          # 0.954, the top of the box
s.dab(TX + 0.0005, 0.1778, "round_hard", "lamp_core", size=0.0065, press=3, tip_wobble=0.3, **S)
s.dry()
