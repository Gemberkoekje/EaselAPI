# The rock the tower stands in, and the only thing in the picture nearer than the
# tower -- so it goes on over the tower's foot and takes it away. The anchoring
# dark, and it is not one mass: it is the planes it is made of, with the block-in
# left showing between them as the shadow.
s.dry()

# Ragged on purpose. The spill past the outline is half a brush of broken comb
# into the water, which is what rock meeting sea in fog looks like, and clean
# would have drawn a line along the one boundary that should have none. Crossed,
# at the widest brush that still breaks: the same mass at size 0.075 costs 23
# passes and at 0.11 it costs 14, for a dark that has to be dark and does not
# have to be finely made.
s.block_in(rock(), "bristle", "rock", size=0.11, density=0.8,
           direction=("axis", 58), note="rock")

# Three planes, and the whole range across them is 0.135 -- the first attempt ran
# up to 0.33 and the top face then sat within 0.07 of the near sea, which stopped
# it being a dark at all. A mass shaded much past 0.15 across itself buys form by
# spending the separation that made it a mass.
faces = [
    # the light along the top edge, in two pieces rather than one band: run the
    # whole length it draws the ramp it is lying on, and an edge found in some
    # places and lost in others is the only kind worth having
    (polygon([(-0.06, 0.768), (0.09, 0.785), (0.20, 0.811), (0.31, 0.830),
              (0.31, 0.858), (0.18, 0.842), (-0.06, 0.806)]),
     "rock_lit", 0.018, "flat", "axis"),
    (polygon([(0.52, 0.869), (0.67, 0.899), (0.79, 0.929), (0.92, 0.959),
              (1.06, 1.014), (1.06, 1.044), (0.82, 0.968), (0.56, 0.906)]),
     p.at_value("rock", 0.275), 0.018, "flat", "axis"),
    # the bulk below it, turned away from everything
    (polygon([(-0.06, 0.836), (0.26, 0.888), (0.58, 0.952), (0.86, 1.020),
              (0.86, 1.062), (-0.06, 1.062)]),
     p.at_value("rock", 0.155), 0.055, "bristle", "axis"),
]
# Each face along its own axis and no crossing: the top band crossed cost 33
# passes against 3 laid one way, because a pass line crosses a long thin diagonal
# shape twice and the second direction steps across its whole bounding box.
for face, colour, size, brush, direction in faces:
    s.block_in(face, brush, colour, size=size, density=1.0, solid=True,
               opacity=1.0, pressure="even", direction=direction, note="rock")

# One boulder standing proud of the general line. The serrations cut into the
# rock's own outline were about 0.02 deep and the block-in's half-brush spill is
# 0.055, so they came back as a smooth ramp from one corner of the picture to the
# other; what breaks a line at this scale is a mass, not a notch.
boulder = blob((0.468, 0.849), 0.052, wobble=0.5, points=9, seed=11, aspect=0.62)
s.block_in(boulder, "bristle", p.at_value("rock", 0.185), size=0.030,
           density=1.0, solid=True, direction=("axis", 74), note="rock")
s.stroke([(0.436, 0.836), (0.470, 0.828), (0.498, 0.838)], "flat",
         p.at_value("rock", 0.300), size=0.012, opacity=0.9, load=1.0,
         load_falloff=0.0, pressure=[0.4, 1.0, 0.2], note="rock")

# One crevice, tapering out rather than stopping, at the floor of the box: 0.14
# is as dark as these pigments mix, and the deepest crack in the nearest thing
# is the one place to spend it. A third plane on the left was dropped here -- it
# cost 10 passes for a light slab that read as sand.
s.stroke([(0.44, 0.898), (0.56, 0.936), (0.63, 0.992)], "round_hard",
         p.at_value("rock", 0.140), size=0.013, opacity=0.9,
         pressure=[0.3, 1.0, 0.0], note="rock")
# Dry brush, for a surface rather than a silhouette.
s.stroke([(0.21, 0.892), (0.37, 0.914), (0.47, 0.946)], "bristle",
         p.at_value("rock", 0.335), size=0.024, load=0.26, opacity=0.6,
         pressure="swell", note="rock")

s.dry()

# The water's edge, on the water side of the boundary. Laid on the rock it comes
# back as scribbles on a dark mass; on the water it is what the sea is doing.
s.stroke([(0.50, 0.866), (0.66, 0.892), (0.79, 0.924)], "bristle",
         p.at_value("sea_near", 0.61), size=0.013, load=0.45, opacity=0.8,
         pressure=[0.2, 1.0, 0.0], note="rock")
print(s.look(grid=True))
print(s.look(values=True))
