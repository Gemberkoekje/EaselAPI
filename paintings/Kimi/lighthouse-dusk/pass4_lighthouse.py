# Pass 4: the point first, then the tower standing on it, then the lamp.
s.dry()
s.block_in(rock_point(), "flat", "rock", size=0.055, density=1.0,
           solid=True, direction="axis", edge="hard", opacity=1.0,
           pressure="even")

# The rock is planes, not marks on a hull.
for face, colour, size in [
    (polygon([(0.470, 0.745), (0.560, 0.690), (0.650, 0.648), (0.610, 0.760),
              (0.500, 0.820)]), "rock_face", 0.020),
    (polygon([(0.640, 0.655), (0.760, 0.665), (0.895, 0.725), (0.730, 0.805),
              (0.615, 0.755)]), "rock_warm", 0.018),
    (polygon([(0.520, 0.835), (0.700, 0.790), (0.980, 0.850), (1.06, 0.940),
              (0.620, 1.040)]), "sea_deep", 0.024),
]:
    s.block_in(face, "flat", colour, size=size, density=1.0, solid=True,
               direction="axis", opacity=1.0, pressure="even")

s.stroke([(0.585, 0.720), (0.630, 0.760), (0.705, 0.775)], "round_hard", "night",
         size=0.012, opacity=0.85, pressure="taper")
s.stroke([(0.780, 0.720), (0.870, 0.770), (0.945, 0.825)], "bristle", "rock_warm",
         size=0.026, load=0.35, opacity=0.45, pressure="swell")

# Tower: a dark tapered mass with one warm plane on the lamp side.
s.block_in(tower(), "flat", "tower_dark", size=0.018, density=1.0,
           solid=True, direction="axis", edge="hard", opacity=1.0,
           pressure="even", note="subject")
s.block_in(tower_lit_plane(), "flat", "tower_rim", size=0.010, density=1.0,
           solid=True, direction="axis", edge="hard", opacity=0.85,
           pressure="even", note="subject")

# Gallery, lamp room, cap: back edge, warm inside, near edge.
s.block_in(gallery(), "flat", "night", size=0.010, density=1.0, solid=True,
           direction="axis", edge="hard", opacity=1.0, pressure="even",
           note="subject")
s.block_in(lantern(), "flat", "lamp_glass", size=0.010, density=1.0,
           solid=True, direction="axis", edge="hard", opacity=1.0,
           pressure="even", note="subject")
s.block_in(cap(), "flat", "night", size=0.010, density=1.0, solid=True,
           direction="axis", edge="hard", opacity=1.0, pressure="even",
           note="subject")

# A few rails and the one bright core. Few, small, deliberate.
for x0, x1 in [(0.618, 0.642), (0.654, 0.676), (0.690, 0.708)]:
    s.stroke([(x0, 0.333), (x1, 0.306)], "liner", "tower_rim", size=0.0035,
             opacity=0.72, load=0.8, pressure="taper", note="subject")
s.dab(*s.pt("lamp"), "round_hard", "gold_core", size=0.018, press=3,
      tip_wobble=0.25, note="subject")
s.stroke([(0.640, 0.575), (0.648, 0.635), (0.642, 0.682)], "round_hard",
         "tower_rim", size=0.006, opacity=0.45, load=0.7,
         pressure=[0.2, 0.7, 0.2], note="subject")

s.look(values=True, path="pass4_values.png")
s.look(path="pass4_colour.png")
