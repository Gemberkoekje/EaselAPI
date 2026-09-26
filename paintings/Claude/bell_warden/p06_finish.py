"""Pass 6: the stone, the lost edges, and one spark in the eye."""

p["spark"] = p.at_value(p.mix("cadmium_yellow", "titanium_white", 0.5), 0.86)


def lay_stone():
    # Weathered carving: starved marks that break, cross and disappear -- no two alike.
    for pts, colour, size, load, opacity in (
            ([(0.305, 0.552), (0.312, 0.590), (0.318, 0.628)], "stone_lit", 0.020, 0.30, 0.55),
            ([(0.358, 0.422), (0.382, 0.430), (0.402, 0.446)], "mid_c", 0.030, 0.28, 0.55),
            ([(0.425, 0.566), (0.462, 0.548), (0.500, 0.532)], "core", 0.034, 0.30, 0.55),
            ([(0.598, 0.566), (0.610, 0.598), (0.622, 0.632)], "mid_c", 0.024, 0.30, 0.50),
            ([(0.468, 0.452), (0.510, 0.461), (0.552, 0.476)], "stone_lit", 0.018, 0.25, 0.50),
            ([(0.520, 0.200), (0.536, 0.240), (0.560, 0.282)], "mid_c", 0.028, 0.25, 0.45),
            ([(0.580, 0.300), (0.598, 0.328), (0.612, 0.352)], "membrane_core", 0.028, 0.30, 0.50),
            ([(0.352, 0.782), (0.388, 0.772), (0.424, 0.766)], "stone_mid", 0.030, 0.28, 0.50),
            ([(0.500, 0.862), (0.518, 0.830), (0.540, 0.800)], "stone_dark", 0.024, 0.30, 0.50)):
        s.stroke(pts, "bristle", colour, size=size, load=load + 0.1, opacity=min(0.8, opacity + 0.2),
                 note="stone")
    # Carving seams: punctuation, not grain -- one at the shoulder, the thigh, the wing's root.
    for pts, size in (([(0.333, 0.452), (0.341, 0.478), (0.350, 0.505)], 0.0045),
                      ([(0.548, 0.566), (0.562, 0.592), (0.566, 0.622)], 0.0040),
                      ([(0.428, 0.392), (0.450, 0.402), (0.472, 0.408)], 0.0035)):
        s.stroke(pts, "round_hard", "core", size=size, opacity=0.8, pressure="taper",
                 tip_wobble=0.35, note="stone")


def lose_far_edges():
    # Where the shadow side meets the dark wall, a broken mark in a value between them, across it.
    between = p.mix("core", "wall", 0.5)
    for pts, size in (([(0.626, 0.580), (0.648, 0.588), (0.672, 0.594)], 0.030),
                      ([(0.632, 0.642), (0.652, 0.634), (0.668, 0.622)], 0.026),
                      ([(0.620, 0.334), (0.640, 0.346), (0.662, 0.352)], 0.028)):
        s.stroke(pts, "bristle", between, size=size, load=0.5, opacity=0.5, pressure="taper",
                 note="edge")


def spark():
    s.dab(0.2813, 0.3706, "round_hard", "spark", size=0.0028, press=1, tip_wobble=0.7,
          note="subject")


s.dry()
lay_stone()
lose_far_edges()
spark()
print(s.look(sketch=False, path="looks/06-finish.png"))
print(s.look(region="B2:F7", sketch=False, path="looks/06-finish-crop.png"))
