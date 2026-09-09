# Coverage test — why does a colour at value 0.23 laid repeatedly over a light
# ground still read about 0.42?  Six patches, all the same pigment.
# Run: python t1_coverage.py
from easel import Session, Region

s = Session(900, 600, texture="linen", ground="white", seed=3)
p = s.palette
dark = p.shade(p.mix("ultramarine", "burnt_umber", 0.55), 1.0)
print("dark", p.hex(dark), round(p.value_of(dark), 3))

cols = [Region(i / 6, 0.05, (i + 1) / 6 - 0.005, 0.95) for i in range(6)]

# 1: one flat stroke
s.stroke([(0.08, 0.10), (0.08, 0.90)], "flat", dark, size=0.16, load=1.0,
         load_falloff=0.0, pressure="even")
# 2: three passes of the same stroke
for _ in range(3):
    s.stroke([(0.245, 0.10), (0.245, 0.90)], "flat", dark, size=0.16, load=1.0,
             load_falloff=0.0, pressure="even")
# 3: block_in density 1.0
s.block_in(cols[2], "flat", dark, density=1.0, size=0.08)
# 4: block_in density 1.0, three times
for _ in range(3):
    s.block_in(cols[3], "flat", dark, density=1.0, size=0.08)
# 5: one flat stroke, opacity forced to 1.0
s.stroke([(0.745, 0.10), (0.745, 0.90)], "flat", dark, size=0.16, load=1.0,
         load_falloff=0.0, pressure="even", opacity=1.0, hardness=1.0)
# 6: three passes, drying between each
for _ in range(3):
    s.stroke([(0.912, 0.10), (0.912, 0.90)], "flat", dark, size=0.16, load=1.0,
             load_falloff=0.0, pressure="even", opacity=1.0)
    s.dry()

print(s.look())
print(s.look(values=True))
print("strokes:", s.stroke_count)
