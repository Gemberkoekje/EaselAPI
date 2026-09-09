from easel import Region, Session

s = Session(800, 400, ground="white", seed=4)
top, bottom = Region(0, 0, 1, 0.5), Region(0, 0.5, 1, 1)
s.block_in(top, "flat", "ultramarine", density=1.0, size=0.12)
s.block_in(bottom, "flat", "ultramarine", density=1.0, size=0.12)
s.dry(1.0, region=bottom)
s.stroke([(0.15, 0.25), (0.85, 0.25)], "flat", "cadmium_yellow", size=0.1)  # wet
s.stroke([(0.15, 0.75), (0.85, 0.75)], "flat", "cadmium_yellow", size=0.1)  # dry
print(s.look())
