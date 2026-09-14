s.dry()
# In greyscale the far deck was still a light band running behind the pool and
# competing with it. Taken down toward the room's value, above the coping rim so
# the rim itself is untouched: the water now has dark behind it on every side.
for pts, size, op, val in [([(0.100, 0.522), (0.280, 0.410), (0.462, 0.336)], 0.110, 0.48, 0.275),
                           ([(0.455, 0.336), (0.700, 0.390), (1.035, 0.448)], 0.100, 0.42, 0.290),
                           ([(0.925, 0.500), (1.030, 0.566)],                 0.080, 0.36, 0.300)]:
    s.glaze(pts, p.at_value("deck", val), opacity=op, size=size, pressure="swell")
print(s.look())
print(s.look(values=True))
