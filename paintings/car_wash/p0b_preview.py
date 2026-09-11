# The whole composition as silhouettes, painting nothing. The wheel is previewed as
# the stroke it is rather than as a ribbon: costed as a swept ribbon it came to 23,
# because a curved mass pays for the box its bend sweeps out.
s.preview([
    {"shape": archband(),  "label": "arch"},
    {"shape": glow(),      "label": "bloom"},
    {"shape": brushmass(), "label": "brush"},
    {"shape": dash(),      "label": "dash"},
    {"shape": binnacle(),  "label": "hood"},
    {"shape": pillar_l(),  "label": "pillar L"},
    {"shape": pillar_r(),  "label": "pillar R"},
    {"shape": mirror(),    "label": "mirror"},
    {"points": wheel(), "size": 0.026, "brush": "flat", "label": "wheel"},
], grid=True)
