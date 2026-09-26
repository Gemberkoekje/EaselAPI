"""Pass 3: Wenna's masses, back to front -- the neck, the shawl, the knot, the kerchief, the
face, the fist. The lantern is to her right at eye level, so each mass goes down in its light
first and copies moved away from the lantern lay the half-tone and the shade over it, held to
the mass: the lit band then follows every edge that faces the lamp."""

shoulder_lit = poly([(482, 548), (520, 552), (580, 565), (625, 600), (652, 650), (636, 668),
                     (598, 630), (540, 596), (494, 580)], "shoulder lit")


def lay_neck():
    s.block_in(neck, "flat", "skin_mid", size=0.04, density=1.0, solid=True, direction=95,
               edge="hard", note="subject")
    s.block_in(neck.shifted(-0.045, 0.0), "flat", "skin_shade", size=0.04, density=1.0,
               solid=True, direction=95, edge="hard", clip=neck, opacity=1.0,
               pressure="even", note="subject")
    # Under the jaw the neck turns away from the lamp and down: its core shadow.
    s.stroke([P(292, 400), P(330, 424), P(372, 440), P(414, 448)], "round_soft", "skin_core",
             size=0.035, opacity=0.8, pressure=[0.6, 1.0, 1.0, 0.4], clip=neck, note="subject")


def lay_shawl():
    s.block_in(shawl, "flat", "shawl", size=0.12, density=0.9, solid=True, direction=100,
               edge="hard")
    # The right shoulder faces up into the lamp's light: dry wool catching it.
    s.block_in(shoulder_lit, "bristle", "shawl_lit", size=0.04, density=0.9,
               direction=[(0.63, 0.55), (0.84, 0.64)], edge="hard", load=0.7)


def lay_knot():
    s.block_in(knot, "flat", "kerchief_shade", size=0.02, density=1.0, solid=True,
               direction="axis", edge="hard")
    for tail, size in zip(tails, (0.016, 0.013)):
        s.stroke(tail, "round_hard", "kerchief_shade", size=size, opacity=0.95,
                 pressure=[1.0, 0.8, 0.3])


def lay_kerchief():
    s.block_in(kerchief, "flat", "kerchief_lit", size=0.05, density=1.0, solid=True,
               direction="axis", edge="hard", note="subject")
    s.block_in(kerchief.shifted(-0.035, 0.0), "flat", "kerchief", size=0.05, density=1.0,
               solid=True, direction=100, edge="hard", clip=kerchief, opacity=1.0,
               pressure="even", note="subject")
    s.block_in(kerchief.shifted(-0.085, 0.0), "flat", "kerchief_shade", size=0.05,
               density=1.0, solid=True, direction=100, edge="hard", clip=kerchief,
               opacity=1.0, pressure="even", note="subject")


def lay_face():
    s.block_in(face, "flat", "skin_lit", size=0.035, density=1.0, solid=True,
               direction="axis", edge="hard", note="subject")
    s.block_in(face.shifted(-0.044, 0.0), "flat", "skin_mid", size=0.035, density=1.0,
               solid=True, direction=95, edge="hard", clip=face, opacity=1.0,
               pressure="even", note="subject")
    s.block_in(face.shifted(-0.083, 0.0), "flat", "skin_shade", size=0.035, density=1.0,
               solid=True, direction=95, edge="hard", clip=face, opacity=1.0,
               pressure="even", note="subject")


def lay_fist():
    for mass, dx, dy in ((fist, 0.0, 0.0), (fist.shifted(-0.028, 0.022), None, None),
                         (fist.shifted(-0.060, 0.045), None, None)):
        pass
    s.block_in(fist, "flat", "skin_lit", size=0.025, density=1.0, solid=True,
               direction="axis", edge="hard", note="subject")
    s.block_in(fist.shifted(-0.026, 0.020), "flat", "skin_mid", size=0.025, density=1.0,
               solid=True, direction=-20, edge="hard", clip=fist, opacity=1.0,
               pressure="even", note="subject")
    s.block_in(fist.shifted(-0.058, 0.044), "flat", "skin_shade", size=0.025, density=1.0,
               solid=True, direction=-20, edge="hard", clip=fist, opacity=1.0,
               pressure="even", note="subject")
    s.block_in(thumb, "flat", "skin_mid", size=0.018, density=1.0, solid=True,
               direction="axis", edge="hard", note="subject")
    s.block_in(thumb.shifted(-0.02, 0.016), "flat", "skin_shade", size=0.018, density=1.0,
               solid=True, direction="axis", edge="hard", clip=thumb, opacity=1.0,
               pressure="even", note="subject")


lay_neck()
lay_shawl()
lay_knot()
lay_kerchief()
lay_face()
lay_fist()
print(s.look(values=True, path="looks/03-figure-values.png"))
print(s.look(path="looks/03-figure.png"))
print(s.look(region="C2:F5", path="looks/03-figure-crop.png"))
