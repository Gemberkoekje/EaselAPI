"""Pass 2: the room, back to front -- the wall, its glow, the air, the pillar, the floor."""


def lay_wall():
    # A graded field that is most of the picture: dark on the right, warmer toward the light,
    # the passes a few degrees off the frame, run off every edge.
    s.scumble(wall, "night", "wall", 7, direction=117, opacity=0.95)


def lay_glow():
    # The light on the wall behind the head: dark at every edge, its first ring the wall's value.
    s.scumble(glow, "wall", "glow", 16, direction="inward")


def lay_beam():
    # A volume of lit air falling from the upper left, mixed close to what it sits in.
    field = s.sample(span("A1", "C4"))
    v = p.value_of(field)
    p["air_far"] = p.at_value(p.mix(field, "stone_hi", 0.5), v + 0.05)
    p["air_body"] = p.at_value(p.mix("stone_hi", field, 0.35), v + 0.09)
    p["air_core"] = p.at_value(p.mix("stone_hi", field, 0.25), v + 0.13)
    source, far = (0.02, -0.02), (0.33, 0.66)
    s.dry()
    s.glaze([source, (0.16, 0.30), far], "air_far", opacity=0.09, size=0.22,
            pressure=[0.4, 0.8, 1.0])
    s.glaze([source, (0.16, 0.30), (0.32, 0.64)], "air_body", opacity=0.14, size=0.12,
            pressure=[1.0, 0.8, 0.4])
    s.glaze([source, (0.11, 0.20), (0.24, 0.47)], "air_core", opacity=0.16, size=0.06,
            pressure=[1.0, 0.7, 0.12])
    s.dry()


def lay_pillar():
    # A stone column turning from the light: solid dark, then the light laid on its lit side
    # as soft films, widest and faintest first.
    side = [(0.765, -0.06), (0.76, 0.875)]
    s.block_in(pillar, "flat", "pillar_dark", size=0.04, solid=True, direction=side, edge="hard")
    s.dry()
    s.glaze([(0.790, -0.03), (0.788, 0.45), (0.786, 0.87)], "pillar_lit", opacity=0.40,
            size=0.055, pressure="even", clip=pillar)
    s.glaze([(0.778, -0.03), (0.776, 0.45), (0.774, 0.87)], "pillar_lit", opacity=0.45,
            size=0.022, pressure="even", clip=pillar)
    s.dry()


def lay_floor():
    s.block_in(floor, "flat", "floor", size=0.07, solid=True, direction=2)
    # The light on the floor: two soft tapered strokes, the wide one faint, the core shorter.
    s.stroke([(0.02, 0.935), (0.22, 0.925), (0.44, 0.932)], "round_soft", "floor_lit",
             size=0.075, opacity=0.45, pressure=[0.2, 1.0, 0.15])
    s.stroke([(0.07, 0.93), (0.20, 0.924), (0.33, 0.929)], "round_soft", "floor_lit",
             size=0.04, opacity=0.55, pressure=[0.15, 1.0, 0.1])


lay_wall()
lay_glow()
lay_beam()
lay_floor()
lay_pillar()
print(s.look(values=True, path="looks/02-room-values.png"))
print(s.look(path="looks/02-room.png"))
