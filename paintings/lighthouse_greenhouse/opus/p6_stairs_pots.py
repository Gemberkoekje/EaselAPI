# The outside stair wrapping the tower, and the pots coming down it. On the
# tower, so after it; under the pots, so before them.
s.dry()

# Four turns. Not four copies of one turn: the top one is a single mark because
# it is small and far up the taper, the bottom one gets three because it is the
# nearest thing on the tower and the only place a tread could read at all.
for i, (path, width) in enumerate(STAIRS):
    s.stroke(path, "flat", "iron", size=width, opacity=0.95, load=1.0,
             load_falloff=0.1, pressure=[0.45, 1.0, 0.85, 0.5],
             note="subject stair")
    if i:                        # the rail catching what light the fog gives
        lift = 0.010 + 0.002 * i
        s.stroke([(x, y - lift) for x, y in path[1:-1]], "round_hard",
                 p.at_value("tower_lit", 0.52 + 0.03 * i), size=0.005 + 0.001 * i,
                 opacity=0.8, pressure=[0.2, 1.0, 0.35], note="subject stair")
# one broken suggestion of treads, on the nearest turn only: a row of even ticks
# is what a small brush does along an edge when nobody chooses otherwise
s.stroke([(0.228, 0.806), (0.246, 0.812), (0.262, 0.814)], "round_hard",
         p.at_value("iron", 0.30), size=0.004, opacity=0.7,
         pressure=[1.0, 0.15, 0.8], note="subject stair")

s.dry()

# The pots. Two chisel marks each: a body and a wider, lighter rim sitting on
# it. One rectangle alone came back as a brick -- the rim is what makes it a pot,
# and it is the only place in this picture where a tool's own geometry is allowed
# to stand for the thing, because a flat's chisel really is that shape.
for x, y, r, tilt, v, rim, green in POTS:
    dy = r * 0.40 * (tilt / 9.0)
    s.stroke([(x - r * 0.80, y - dy), (x + r * 0.80, y + dy)], "flat",
             p.at_value("pot", v), size=r * 1.55, opacity=1.0, load=1.0,
             load_falloff=0.0, size_jitter=0.20, pressure="even",
             note="subject pot")
    if rim is not None:
        ry = y - r * 0.52
        s.stroke([(x - r, ry - dy), (x + r, ry + dy)], "flat",
                 p.at_value("pot_lit", rim - 0.06), size=r * 0.60,
                 opacity=1.0, load=1.0, load_falloff=0.0, size_jitter=0.20,
                 pressure="even", note="subject pot")
    if green is not None:
        dx, gy, colour, gsize, gload = green
        s.stroke([(x - r * 0.45, y - r * 0.95),
                  (x + dx * 0.5, y - r * 0.95 + gy * 0.55),
                  (x + dx, y - r * 0.95 + gy)], "bristle", colour, size=gsize,
                 load=gload, opacity=0.9, pressure="swell", note="subject pot")

# Two tomatoes, because a tomato vine has them and nothing else in the picture
# is that colour. Small, one of them barely a fleck, and both laid *on* a plant:
# the first rehearsal put one on bare wall and it read as a spot of damage.
s.dab(0.331, 0.735, "round_hard", "tomato", size=0.0085, press=3, tip_wobble=0.7,
      note="subject pot")
s.dab(0.293, 0.648, "round_hard", p.at_value("tomato", 0.30), size=0.006, press=3,
      tip_wobble=0.7, note="subject pot")

# And what has got out of the pots and gone down the tower on its own. Three
# runners, none the same length, one of them crossing a stair.
s.stroke([(0.328, 0.478), (0.336, 0.540), (0.326, 0.592)], "bristle", "leaf_dark",
         size=0.010, load=0.5, opacity=0.8, pressure=[0.9, 0.6, 0.0],
         note="subject pot")
s.stroke([(0.224, 0.490), (0.214, 0.556)], "bristle",
         p.mix("leaf_dark", "tower_mid", 0.35), size=0.008, load=0.35,
         opacity=0.6, pressure="lift_off", note="subject pot")
s.stroke([(0.266, 0.640), (0.276, 0.702), (0.268, 0.746)], "bristle", "leaf_mid",
         size=0.012, load=0.55, opacity=0.75, pressure=[0.8, 1.0, 0.0],
         note="subject pot")

print(s.look(grid=True))
print(s.look(region="B2:D8"))
