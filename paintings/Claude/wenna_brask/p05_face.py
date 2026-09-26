"""Pass 5: the face -- what makes the lit mask a woman who has not slept. The sockets and the
eyes, brows lifted at the inner ends, the nose's own shadow and the one it throws, the mouth
turned down at its near corner, the jaw's underside, the hollow of the cheek, the dark under
the eyes, the kerchief's hem, two loose strands, and the terminator lost where it crosses the
cheek."""

p["skin_hi"] = p.at_value(p.mix("skin_lit", "titanium_white", 0.3), 0.74)
p["under_eye"] = p.at_value(p.mix_many(["skin_mid", "burnt_umber", "ultramarine"], [8, 1, 0.5]), 0.42)
p["cast"] = p.at_value(p.mix("skin_shade", "skin_mid", 0.4), 0.34)
p["socket"] = p.at_value(p.mix("skin_mid", "skin_shade", 0.4), 0.38)
p["brow"] = p.at_value(p.mix("hair", "skin_shade", 0.3), 0.20)
p["lip"] = p.at_value(p.mix("skin_mid", "cadmium_red", 0.12), 0.47)
p["turn"] = p.mix("skin_lit", "skin_mid", 0.5)
F = dict(clip=face, note="subject")


def lay_sockets():
    # Each eye sits in a hollow, laid before the eye itself.
    s.stroke([P(338, 286), P(356, 280), P(376, 284)], "round_soft", "socket", size=0.026,
             opacity=0.55, pressure=[0.5, 1.0, 0.6], **F)
    s.stroke([P(410, 282), P(420, 278), P(430, 282)], "round_soft", "socket", size=0.018,
             opacity=0.55, pressure=[0.5, 1.0, 0.5], **F)
    s.stroke([P(346, 300), P(360, 303), P(374, 300)], "round_soft", "under_eye", size=0.010,
             opacity=0.32, pressure=[0.3, 1.0, 0.4], **F)


def lay_eyes():
    # The upper lids, the irises looking right past the lamp, and one catchlight.
    s.stroke([P(341, 290), P(356, 285), P(372, 287)], "round_hard", "skin_core", size=0.005,
             opacity=0.9, pressure=[0.4, 1.0, 0.7], tip_wobble=0.35, **F)
    s.dab(*P(364, 289), "round_hard", "skin_core", size=0.009, press=3, tip_wobble=0.35, **F)
    s.stroke([P(413, 283), P(420, 280), P(427, 282)], "round_hard", "skin_core", size=0.004,
             opacity=0.9, pressure=[0.5, 1.0, 0.6], tip_wobble=0.35, **F)
    s.dab(*P(423, 283), "round_hard", "skin_core", size=0.006, press=2, tip_wobble=0.5, **F)


def lay_brows():
    # Lifted at the inner ends: worry, not surprise.
    s.stroke([P(338, 273), P(356, 268), P(376, 262)], "round_hard", "brow", size=0.006,
             opacity=0.85, pressure=[0.3, 0.8, 1.0], tip_wobble=0.35, **F)
    s.stroke([P(414, 264), P(424, 260), P(432, 259)], "round_hard", "brow", size=0.005,
             opacity=0.8, pressure=[1.0, 0.7, 0.3], tip_wobble=0.35, **F)


def lay_nose():
    # Its near side in half-tone, the shadow it throws on the cheek, the wing and nostril.
    s.stroke([P(428, 274), P(438, 296), P(448, 318), P(450, 336)], "flat", "skin_mid",
             size=0.010, opacity=0.8, load=1.0, load_falloff=0.0,
             pressure=[0.3, 0.8, 1.0, 0.6], **F)
    s.stroke([P(426, 310), P(428, 328), P(430, 344)], "round_soft", "cast", size=0.020,
             opacity=0.22, pressure=[0.3, 1.0, 0.6], **F)
    s.stroke([P(438, 336), P(438, 346), P(446, 351)], "round_hard", "skin_shade", size=0.005,
             opacity=0.8, pressure=[0.4, 1.0, 0.5], tip_wobble=0.35, **F)
    s.dab(*P(447, 348), "round_hard", "skin_core", size=0.006, press=2, tip_wobble=0.5, **F)


def lay_mouth():
    s.stroke([P(442, 367), P(424, 372), P(404, 379)], "round_soft", "lip", size=0.009,
             opacity=0.6, pressure=[0.6, 1.0, 0.4], **F)
    s.stroke([P(439, 376), P(420, 380), P(402, 384), P(393, 389)], "round_hard", "skin_core",
             size=0.0045, opacity=0.9, pressure=[0.9, 1.0, 0.8, 0.2], tip_wobble=0.35, **F)
    s.stroke([P(438, 387), P(424, 389), P(410, 391)], "round_soft", "skin_hi", size=0.006,
             opacity=0.55, pressure=[0.5, 1.0, 0.2], **F)
    s.stroke([P(433, 401), P(424, 402), P(414, 401)], "round_soft", "skin_mid", size=0.008,
             opacity=0.6, pressure=[0.8, 1.0, 0.3], **F)


def lay_modelling():
    # The hollow under the cheekbone and the fold from the nose: she is tired.
    s.stroke([P(360, 330), P(376, 350), P(392, 368)], "round_soft", "skin_mid", size=0.035,
             opacity=0.22, pressure=[0.4, 1.0, 0.5], **F)
    s.stroke([P(436, 353), P(426, 364), P(416, 376)], "round_soft", "skin_mid", size=0.007,
             opacity=0.5, pressure=[0.9, 0.7, 0.2], **F)
    # The jaw's underside turns away from everything.
    s.stroke([P(433, 428), P(416, 440), P(392, 439), P(366, 432)], "round_soft", "skin_core",
             size=0.008, opacity=0.7, pressure=[0.3, 1.0, 1.0, 0.3], **F)
    # The kerchief's hem throws a thin shadow on the forehead.
    s.stroke([P(393, 190), P(381, 203), P(369, 222), P(357, 246)], "round_soft", "skin_shade",
             size=0.007, opacity=0.7, pressure=[0.6, 1.0, 1.0, 0.5], **F)


def lose_terminator():
    # A broken mark across the join, between the two values, where the cheek turns.
    s.stroke([P(338, 336), P(350, 340), P(364, 338)], "bristle", "turn", size=0.03,
             load=0.5, opacity=0.5, pressure="swell", **F)
    s.stroke([P(348, 392), P(360, 396), P(372, 393)], "bristle", "turn", size=0.026,
             load=0.45, opacity=0.45, pressure="swell", **F)


def lay_strands():
    # Two strands loose from the hem at the temple, one catching the lamp.
    s.stroke([P(372, 212), P(365, 238), P(369, 262), P(362, 290)], "round_hard", "hair_lit",
             size=0.0028, opacity=0.8, pressure=[0.8, 1.0, 0.7, 0.1], note="subject")
    s.stroke([P(380, 205), P(383, 228), P(377, 252)], "round_hard", "hair", size=0.003,
             opacity=0.8, pressure=[0.9, 0.8, 0.1], note="subject")


lay_sockets()
lay_eyes()
lay_brows()
lay_nose()
lay_mouth()
lay_modelling()
lose_terminator()
lay_strands()
print(s.look(region="C2:E4", path="looks/05-face-crop.png"))
print(s.look(region="C2:E4", values=True, path="looks/05-face-values.png"))
