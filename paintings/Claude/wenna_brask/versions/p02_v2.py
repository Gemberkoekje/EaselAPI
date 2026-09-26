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
    # The lantern's light on the wall: dark at every edge, its first ring the wall's value.
    s.scumble(glow, "mill", "glow_wall", 18, direction="inward", clip=mill)


lay_sky()
lay_mill()
lay_wall_glow()
print(s.look(values=True, path="looks/02-setting-values.png"))
print(s.look(path="looks/02-setting.png"))
