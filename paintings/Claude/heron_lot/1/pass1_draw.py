# Pass 1 - the arrangement in graphite. Free. Drawn THROUGH the masses.
s.pencil(WATER_TOP, pressure=0.62, note="draw far edge")
s.pencil([p_ for p_ in TREES.points[:12]], pressure=0.45, note="draw treeline")
s.pencil([(1.06, 0.640), (0.93, 0.712), (0.84, 0.792), (0.760, 0.876),
          (0.712, 0.952), (0.690, 1.06)], pressure=0.6, note="draw flood edge")
for ln in (LANE1, LANE2, LANE3):
    s.pencil(ln, pressure=0.42, note="draw stall line")
s.pencil([POLE_TOP, (0.216, 0.30), POLE_FOOT], pressure=0.7, note="draw pole")
s.pencil([(0.206, 0.088), (0.262, 0.104)], pressure=0.7, note="draw lamp arm")
s.pencil([(0.232, 0.60), (0.238, 0.78), (0.244, 0.95)], pressure=0.35, note="draw pole refl")

# the heron, as gesture through the masses - not an outline
s.pencil([(0.470, 0.355), (0.560, 0.340), (0.596, 0.400), (0.600, 0.470),
          (0.640, 0.520), (0.706, 0.532)], pressure=0.75, note="draw heron axis")
s.pencil([(0.580, 0.520), (0.650, 0.492), (0.712, 0.522)], pressure=0.5, note="draw heron back")
s.pencil([(0.584, 0.566), (0.650, 0.588), (0.700, 0.550)], pressure=0.5, note="draw heron belly")
s.pencil(LEG_F, pressure=0.7, note="draw leg")
s.pencil(LEG_B, pressure=0.55, note="draw leg")
s.pencil([(0.606, 0.665), (0.612, 0.74), (0.620, 0.812)], pressure=0.35, note="draw heron refl")
print(s.look(grid=True))
