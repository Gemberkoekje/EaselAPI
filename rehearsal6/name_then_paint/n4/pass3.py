exec(open("_pal.py").read())
exec(open("_geom.py").read())
s.dry()

# one even luminous field for the pane, one for the wall
s.block_in(GLASS, "flat", "glass", direction=(98, 14), density=1.0,
           size=0.15, pressure="even", load=1.0, load_falloff=0.2)
s.block_in(WALL, "flat", "wall", direction=(104, 20), density=1.0,
           size=0.135, pressure="even", load=1.0, load_falloff=0.2)
s.dry()

# broad, soft value shifts: glazes, not scumbles
for y in [0.03, 0.10, 0.17, 0.24, 0.31]:
    s.glaze([(0.995, y - 0.05), (0.845, y + 0.09)], "wall_dk", opacity=0.13)
for y in [0.52, 0.60]:
    s.glaze([(0.575, y), (1.0, y + 0.035)], "wall_dk", opacity=0.10)
for i, y in enumerate([0.05, 0.13, 0.21]):
    s.glaze([(0.20, y + 0.10), (0.56, y)], "glass_hot", opacity=0.14)
for i, y in enumerate([0.40, 0.48, 0.555]):
    s.glaze([(0.03, y), (0.45, y + 0.045)], "glass_far", opacity=0.11)
print(s.stroke_count)
print(s.look())
