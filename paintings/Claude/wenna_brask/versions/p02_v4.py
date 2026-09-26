"""Pass 2: the setting, back to front -- the dusk sky, the mill's gable wall, the lantern's
light on the wall."""

upper_sky = polygon([(-0.06, -0.06), (1.06, -0.06), (1.06, 0.40), (-0.06, 0.45)], name="upper sky")
lower_sky = polygon([(-0.06, 0.33), (1.06, 0.29), (1.06, 0.76), (-0.06, 0.76)], name="lower sky")
glow = blob(P(598, 296), 0.19, 0.135, wobble=0.2, points=13, seed=5, name="glow")


def lay_sky():
    # A graded field that is most of the picture: two ramps a few degrees off the frame,
    # dark at the top, palest low behind her shoulder, then two starved crossers.
    s.scumble(upper_sky, "sky_high", "sky_mid", 7, direction=4, opacity=0.95)
    s.scumble(lower_sky, "sky_mid", "sky_low", 8, direction=3, opacity=0.95)
    s.stroke([(-0.06, 0.13), (0.28, 0.10), (0.66, 0.03)], "bristle", "sky_high",
             size=0.06, load=0.40, opacity=0.45, pressure="swell")
    s.stroke([(-0.06, 0.47), (0.14, 0.43), (0.36, 0.42)], "bristle", "sky_mid",
             size=0.05, load=0.35, opacity=0.40, pressure="swell")


def lay_mill():
    # The gable wall: one dark mass, its rake crisp against the sky.
    s.block_in(mill, "flat", "mill", size=0.12, density=1.0, solid=True, direction=92,
               edge="hard")


def lay_wall_glow():
    # The lantern's light on the wall behind it. An inward scumble left rings and a rim like a
    # knot in wood, so it is three soft films instead, each smaller and warmer, mixed close to
    # the wall and aimed at a value rather than an opacity.
    field = s.sample(glow)
    v = p.value_of(field)
    p["wall_glow1"] = p.at_value(p.mix(field, "glow_wall", 0.6), v + 0.08)
    p["wall_glow2"] = p.at_value(p.mix("glow_wall", field, 0.3), v + 0.14)
    p["wall_glow3"] = p.at_value(p.mix("glow_wall", field, 0.15), v + 0.20)
    s.dry()
    s.glaze([P(556, 300), P(598, 296), P(640, 300)], "wall_glow1", opacity=0.30,
            size=0.34, pressure="swell", clip=mill)
    s.glaze([P(570, 298), P(598, 294), P(626, 298)], "wall_glow2", opacity=0.30,
            size=0.21, pressure="swell", clip=mill)
    s.glaze([P(584, 296), P(598, 294), P(612, 296)], "wall_glow3", opacity=0.30,
            size=0.12, pressure="swell", clip=mill)
    s.dry()


lay_sky()
lay_mill()
lay_wall_glow()
print(s.look(values=True, path="looks/02-setting-values.png"))
print(s.look(path="looks/02-setting.png"))
