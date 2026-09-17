# The warm glazes came back as four soft orange ovals -- flares, not things. One of
# them becomes a pot, with the form a pot has and no drawn outline; the others are
# glazed back until they are just warmth in the mist.
from easel import polygon

p["pot"]     = p.at_value(p.mix(p.mix("burnt_sienna", "yellow_ochre", 0.26),
                                "burnt_umber", 0.24), 0.41)
p["potfoot"] = p.at_value(p.mix(p.mix("burnt_sienna", "burnt_umber", 0.52),
                                "ultramarine", 0.16), 0.29)
p["back"]    = p.at_value(p.desaturate(p.mix(p["neutral"], "viridian", 0.16), 0.36), 0.44)

# --- the pot: a mass with a top wider than its foot, then the dark it stands in
pot = polygon([(0.6845, 0.8430), (0.7275, 0.8415), (0.7205, 0.9015), (0.6915, 0.9025)])
s.block_in(pot, "round_hard", "pot", direction=84, density=1.0, size=0.011,
           pressure="even", opacity=0.82, note="subject")
s.stroke([(0.6870, 0.8985), (0.7185, 0.8975)], "round_hard", "potfoot", size=0.009,
         pressure=[0.4, 1.0], load=1.0, opacity=0.70, tip_wobble=0.5, note="subject")
s.stroke([(0.6865, 0.8455), (0.7250, 0.8440)], "round_hard",
         p.at_value(p["pot"], 0.50), size=0.006, pressure=[0.3, 0.9],
         load=1.0, opacity=0.55, tip_wobble=0.5, note="subject")

# --- the film is still in front of it, so it does not get to be sharp
s.glaze([(0.678, 0.860), (0.712, 0.838), (0.734, 0.876)], "fogthin",
        opacity=0.20, size=0.034, note="subject")

# --- the other three ovals back into the mist
for pts, sz, op in [([(0.742, 0.906), (0.800, 0.868), (0.846, 0.904)], 0.050, 0.26),
                    ([(0.868, 0.986), (0.932, 0.950), (0.996, 0.980)], 0.056, 0.24),
                    ([(0.898, 0.884), (0.952, 0.858)], 0.032, 0.22)]:
    s.glaze(pts, "back", opacity=op, size=sz, note="glass")
