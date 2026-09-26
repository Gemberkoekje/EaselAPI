"""Pass 3: Wenna's masses, back to front -- the neck, the shawl, the knot, the kerchief, the
face, the fist. Each goes down in its shadow colour and its lit planes are shapes laid on it,
drawn with the silhouette. (Copies of the silhouette moved away from the lamp, which lit the
Bell-Warden, turned this face into three stacked profiles and the kerchief into a striped
helmet in rehearsal.)"""


def lay_neck():
    # In the jaw's shadow and the shawl's: darker than the face's own shadow side, so the
    # jaw stands off it.
    s.block_in(neck, "flat", "neck", size=0.04, density=1.0, solid=True, direction=95,
               edge="hard", note="subject")


def lay_shawl():
    s.block_in(shawl, "flat", "shawl", size=0.12, density=0.9, solid=True, direction=100,
               edge="hard")
    # The right shoulder faces up into the lamp's light: dry wool catching it.
    s.stroke([P(488, 506), P(560, 540), P(622, 598), P(646, 650)], "round_soft", "shawl_lit",
             size=0.05, opacity=0.55, pressure=[0.3, 1.0, 0.8, 0.2], clip=shawl)


def lay_knot():
    s.block_in(knot, "flat", "kerchief_shade", size=0.02, density=1.0, solid=True,
               direction="axis", edge="hard")
    for tail, size in zip(tails, (0.016, 0.013)):
        s.stroke(tail, "round_hard", "kerchief_shade", size=size, opacity=0.95,
                 pressure=[1.0, 0.8, 0.3])


def lay_kerchief():
    s.block_in(kerchief, "flat", "kerchief_shade", size=0.06, density=1.0, solid=True,
               direction=100, edge="hard", note="subject")
    s.block_in(kerchief_crown, "flat", "kerchief", size=0.03, density=1.0, solid=True,
               direction=[(0.30, 0.16), (0.47, 0.12)], edge="hard", clip=kerchief,
               opacity=1.0, pressure="even", note="subject")
    s.block_in(kerchief_lit, "flat", "kerchief_lit", size=0.02, density=1.0, solid=True,
               direction=[(0.46, 0.25), (0.51, 0.18)], edge="hard", clip=kerchief,
               opacity=1.0, pressure="even", note="subject")


def lay_face():
    s.block_in(face, "flat", "skin_shade", size=0.05, density=1.0, solid=True, direction=95,
               edge="hard", note="subject")
    s.block_in(face_mid, "flat", "skin_mid", size=0.02, density=1.0, solid=True,
               direction=[(0.474, 0.217), (0.482, 0.422)], edge="hard", clip=face,
               opacity=1.0, pressure="even", note="subject")
    s.block_in(face_lit, "flat", "skin_lit", size=0.03, density=1.0, solid=True,
               direction=[(0.50, 0.19), (0.54, 0.43)], edge="hard", clip=face, opacity=1.0,
               pressure="even", note="subject")
    # The join, at half strength, is what turns the form rather than striping it.
    s.stroke([P(x, y) for x, y in terminator], "flat",
             p.mix("skin_lit", "skin_mid", 0.5), size=0.010, opacity=0.6, load=1.0,
             load_falloff=0.0, pressure="even", clip=face, note="subject")


def lay_fist():
    s.block_in(fist, "flat", "skin_shade", size=0.03, density=1.0, solid=True,
               direction=-15, edge="hard", note="subject")
    s.block_in(fist_front, "flat", "skin_mid", size=0.018, density=1.0, solid=True,
               direction=-12, edge="hard", clip=fist, opacity=1.0, pressure="even",
               note="subject")
    s.block_in(fist_top, "flat", "skin_lit", size=0.014, density=1.0, solid=True,
               direction=-8, edge="hard", clip=fist, opacity=1.0, pressure="even",
               note="subject")
    s.block_in(thumb, "flat", "skin_shade", size=0.016, density=1.0, solid=True,
               direction=5, edge="hard", note="subject")


lay_neck()
lay_shawl()
lay_knot()
lay_kerchief()
lay_face()
lay_fist()
print(s.look(values=True, path="looks/03-figure-values.png"))
print(s.look(path="looks/03-figure.png"))
print(s.look(region="C1:F5", path="looks/03-figure-crop.png"))
