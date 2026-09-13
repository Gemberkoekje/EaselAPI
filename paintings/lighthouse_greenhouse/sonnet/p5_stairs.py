# Pass 5: the exterior stair, bolted to the tower, and the pots that spiral
# down it. The switchback drawn in prelude.py as six points priced out at 141
# strokes as one bent ribbon -- a bend prices on the box it sweeps, cut into
# pieces by the outline -- so it is five straight flights, each a stroke
# rather than a mass (PAINTER.md/PAINTING.md, "a mass much longer than it is
# wide is a stroke"), thickest low and thinning going up. A short cross-mark
# at each interior landing reads as a small platform. The pots go on last,
# largest and warmest low down, smallest and coolest near the top where the
# beam's green tint would actually reach them -- vary one thing per pot
# rather than repeating the same recipe nine times.
FLIGHT_SIZES = [0.020, 0.017, 0.014, 0.0115, 0.0095]
for (a, b), size in zip(FLIGHTS, FLIGHT_SIZES):
    s.stroke([a, b], "flat", "iron", size=size, opacity=0.9, load=1.0,
              load_falloff=0.0, pressure="even", note="stair flight")
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = (dx * dx + dy * dy) ** 0.5
    ox, oy = -dy / length * size * 0.55, dx / length * size * 0.55
    s.stroke([(mx - ox, my - oy), (mx + ox, my + oy)], "round_hard", "rock_deep",
              size=size * 0.5, opacity=0.5, pressure="swell", note="under the tread, shadow")

for lx, ly in LANDINGS:
    ang = 0.018
    s.stroke([(lx - ang, ly), (lx + ang, ly - 0.004)], "flat", "iron", size=0.014,
              opacity=0.85, load=1.0, load_falloff=0.0, pressure="even", note="landing")

POT_STYLES = [
    ("terracotta", "leaf_mid", False), ("terra_lit", "leaf_lit", True),
    ("terracotta", "leaf_lit", False), ("terra_lit", "leaf_mid", True),
    ("terracotta", "leaf_beam", False), ("terra_lit", "leaf_beam", False),
    ("terracotta", "leaf_lit", True), ("terra_lit", "leaf_mid", False),
    ("terracotta", "leaf_beam", False),
]
for (x, y, r), (potcol, leafcol, tomato) in zip(POTS, POT_STYLES):
    # sit the pot just past the rail, not centred on it -- a pot balanced
    # exactly on the line read as threaded onto it rather than standing on a
    # step beside it.
    x, y = x + r * 0.7, y + r * 0.55
    # round_hard, not flat: pressure tapers a round tip's *width*, which is
    # what a pot wants (wide rim, narrow foot) -- a flat brush only varies
    # how much paint lands, so the first attempt at this came back a row of
    # rectangular barrels, chisel ends and all.
    s.stroke([(x, y - r * 0.5), (x + r * 0.1, y + r * 0.6)], "round_hard", potcol,
              size=r * 1.8, opacity=0.95, load=1.0, load_falloff=0.0,
              pressure=[1.0, 0.32], note="pot")
    # bristle disappears below about size 0.02 -- these tufts are smaller
    # than that, so round_hard (which holds up at any size) carries them.
    s.stroke([(x - r * 0.55, y - r * 0.5), (x - r * 0.1, y - r * 1.5)], "round_hard",
              leafcol, size=r * 0.85, opacity=0.85, load=0.7, pressure="lift_off",
              note="trailing plant, one side")
    s.stroke([(x + r * 0.1, y - r * 0.6), (x + r * 0.5, y - r * 1.2)], "round_hard",
              leafcol, size=r * 0.7, opacity=0.8, load=0.7, pressure="lift_off",
              note="trailing plant, other side")
    if tomato:
        s.dab(x + r * 0.1, y - r * 0.85, "round_hard", "tomato", size=r * 0.4, press=2,
              note="tomato")
print(s.look(values=True))
print(s.look())
print(s.look(region="C1:F7"))
