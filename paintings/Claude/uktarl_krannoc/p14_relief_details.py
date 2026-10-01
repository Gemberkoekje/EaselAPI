"""The relief's small things: its dwarves, its lit ridges, its age.

The caverns are full of tiny carved dwarves; one or two show in each mouth that shows,
a short upright mark of the gilding's ochre, no two the same height or lean. The crags
nearest Uktarl catch the lantern on their faces turned toward him. And two cracks run
down across the rays: the relief is old, and nothing on this level is kept.
"""

p["dwarf_shade"] = p.at_value("dwarf", 0.38)
DWARVES = [((252, 505), 12, -5), ((271, 509), 7, 3), ((372, 469), 10, 8),
           ((58, 567), 12, 4), ((882, 524), 11, -7), ((962, 570), 8, 0)]
for (x, y), h, lean in DWARVES:
    s.stroke(px_pts([(x, y + h * 0.45), (x + lean * 0.3, y - h * 0.5)]), "round_hard",
             "dwarf_shade", size=0.0075, opacity=0.95, pressure=[1.0, 0.75], tip_wobble=0.4)
# One of them swings a pick: a short haft from the top of the figure.
s.stroke(px_pts([(372 + 3, 469 - 5), (372 + 10, 469 - 11)]), "round_hard", "dwarf_shade",
         size=0.004, opacity=0.9, pressure=[1.0, 0.6])

for path, mix in (([(372, 382), (396, 386), (412, 404), (420, 430)], "mount_lit"),
                  ([(448, 354), (440, 372), (436, 396)], "mount_lit"),
                  ([(712, 364), (722, 380), (726, 404)], "mount_lit"),
                  ([(742, 380), (764, 396), (778, 414), (784, 440)], "mount_mid")):
    s.stroke(px_pts(path), "round_hard", mix, size=0.010, opacity=0.8,
             pressure=[0.9, 1.0, 0.6, 0.1], clip=mountain)

crack = p.at_value(p.mix("wall_far", "black", 0.4), 0.14)
for path in ([(196, -4), (214, 60), (204, 118), (226, 180)],
             [(842, 70), (826, 128), (838, 176), (818, 236)]):
    s.stroke(px_pts(path), "round_hard", crack, size=0.0045, opacity=0.75,
             pressure=[0.3, 1.0, 0.8, 0.1])
