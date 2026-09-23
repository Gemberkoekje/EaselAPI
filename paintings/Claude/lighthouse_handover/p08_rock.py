# The headland's inside, at dusk: ledges catching the last skylight (cool, a step above
# the face, each its own angle, length and width -- not a comb), a fissure, crevices
# under two of the ledges, and the warm west ribbon broken by two dark rocks.
p["ledge"] = p.at_value(p.mix("cliff", "pale", 0.3), 0.245)
p["ledge_warm"] = p.at_value(p.mix("lit_dim", "glow", 0.2), 0.27)
H = dict(clip=headland)
s.stroke([(0.515, 0.641), (0.585, 0.628), (0.650, 0.622)], "flat", "ledge_warm",
         size=0.010, opacity=0.6, load=0.8, pressure=[0.3, 1.0, 0.2], **H)
s.stroke([(0.715, 0.603), (0.790, 0.591), (0.895, 0.588)], "flat", "ledge",
         size=0.013, opacity=0.55, load=0.8, pressure=[0.2, 1.0, 0.5, 0.1], **H)
s.stroke([(0.628, 0.703), (0.672, 0.689), (0.738, 0.687)], "flat", "ledge",
         size=0.009, opacity=0.6, load=0.7, pressure=[0.4, 1.0, 0.1], **H)
s.stroke([(0.855, 0.676), (0.925, 0.672), (1.03, 0.649)], "flat", "ledge",
         size=0.016, opacity=0.5, load=0.8, pressure=[0.1, 0.9, 1.0], **H)
s.stroke([(0.790, 0.806), (0.842, 0.790), (0.905, 0.793)], "flat", "ledge",
         size=0.011, opacity=0.5, load=0.7, pressure=[0.2, 1.0, 0.3], **H)
s.stroke([(0.72, 0.614), (0.79, 0.603), (0.87, 0.600)], "round_hard", "land",
         size=0.006, opacity=0.8, pressure=[0.1, 1.0, 0.6, 0.1], **H)          # crevice
s.stroke([(0.64, 0.713), (0.69, 0.700), (0.74, 0.699)], "round_hard", "land",
         size=0.005, opacity=0.8, pressure=[0.2, 1.0, 0.2], **H)               # crevice
s.stroke([(0.772, 0.612), (0.764, 0.660), (0.781, 0.724), (0.776, 0.770)], "round_hard",
         "land", size=0.007, opacity=0.8, pressure=[0.2, 1.0, 0.7, 0.1], **H)  # fissure
s.stroke([(0.503, 0.592), (0.512, 0.611), (0.516, 0.628)], "round_hard", "land",
         size=0.011, opacity=0.85, tip_wobble=0.5, pressure=[0.4, 1.0, 0.3], **H)   # breaks the
s.stroke([(0.598, 0.556), (0.604, 0.572), (0.603, 0.584)], "round_hard", "land",
         size=0.009, opacity=0.8, tip_wobble=0.5, pressure=[0.5, 1.0, 0.2], **H)    # west ribbon
s.dry()
