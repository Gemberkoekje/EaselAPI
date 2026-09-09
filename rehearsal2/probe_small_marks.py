"""What the engine can do at the scale of an eye: on a 1200-wide canvas the
reference's eye is about 15 px across, i.e. size 0.012."""
from easel import Session, Region

s = Session(1200, 800, texture="linen", ground="toned_grey", seed=3, out_dir="out/small")
p = s.palette
p["dk"] = p.mix("ultramarine", "burnt_umber", 0.55)
p["flesh"] = p.tint(p.mix("burnt_sienna", "yellow_ochre", 0.5), 0.55)
p["lt"] = p.tint(p["flesh"], 0.5)
s.block_in(Region(0.05, 0.05, 0.95, 0.55), "flat", "flesh", density=1.0, size=0.12)
s.dry()
# row 1: round_hard dots at shrinking sizes
for i, sz in enumerate((0.03, 0.02, 0.015, 0.012, 0.01, 0.008, 0.006, 0.004, 0.003)):
    s.dab(0.10 + i * 0.09, 0.15, "round_hard", "dk", size=sz)
# row 2: short curved lines (an eyelid's curve) at shrinking sizes, taper
for i, sz in enumerate((0.02, 0.015, 0.012, 0.01, 0.008, 0.006, 0.005, 0.004, 0.003)):
    x = 0.10 + i * 0.09
    s.stroke([(x - 0.03, 0.27), (x, 0.255), (x + 0.03, 0.27)], "round_hard", "dk", size=sz, pressure="taper")
# row 3: the same line with bristle, round_soft and flat at 0.012, and pressures at 0.006
s.stroke([(0.07, 0.38), (0.10, 0.365), (0.13, 0.38)], "bristle", "dk", size=0.012)
s.stroke([(0.16, 0.38), (0.19, 0.365), (0.22, 0.38)], "round_soft", "dk", size=0.012)
s.stroke([(0.25, 0.38), (0.28, 0.365), (0.31, 0.38)], "flat", "dk", size=0.012)
for i, pr in enumerate(("even", "taper", "lift_off", 0.3)):
    x = 0.40 + i * 0.09
    s.stroke([(x - 0.03, 0.38), (x, 0.365), (x + 0.03, 0.38)], "round_hard", "dk", size=0.006, pressure=pr)
# row 4: an eye at the reference's scale, four marks, then a catchlight
ex, ey = 0.20, 0.47
s.dab(ex, ey, "round_soft", "dk", size=0.03, opacity=0.35)                          # socket
s.stroke([(ex - 0.012, ey + 0.002), (ex, ey - 0.005), (ex + 0.012, ey + 0.001)], "round_hard", "dk", size=0.004, pressure="taper")  # lid line
s.dab(ex + 0.001, ey + 0.001, "round_hard", "dk", size=0.007)                       # iris
s.stroke([(ex - 0.010, ey + 0.006), (ex + 0.010, ey + 0.006)], "round_hard", "lt", size=0.003, pressure="taper")   # lower lid
s.dab(ex - 0.002, ey - 0.001, "round_hard", "titanium_white", size=0.002)           # catchlight
# a bigger one beside it, twice the scale, same marks
ex, ey = 0.45, 0.47
s.dab(ex, ey, "round_soft", "dk", size=0.06, opacity=0.35)
s.stroke([(ex - 0.024, ey + 0.004), (ex, ey - 0.01), (ex + 0.024, ey + 0.002)], "round_hard", "dk", size=0.008, pressure="taper")
s.dab(ex + 0.002, ey + 0.002, "round_hard", "dk", size=0.014)
s.stroke([(ex - 0.020, ey + 0.012), (ex + 0.020, ey + 0.012)], "round_hard", "lt", size=0.006, pressure="taper")
s.dab(ex - 0.004, ey - 0.002, "round_hard", "titanium_white", size=0.004)
print(s.look(region=Region(0.03, 0.08, 0.97, 0.53)))
print(s.look(region=Region(0.14, 0.42, 0.26, 0.52)))
print(s.look(region=Region(0.36, 0.40, 0.54, 0.54)))
for rec in s.log().splitlines()[-12:]:
    print(rec)
