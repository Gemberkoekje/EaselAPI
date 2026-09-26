"""Why the flour landed nothing: the p10 finger stroke (record 258) laid again on throwaway
copies of the finished painting, one load at a time, everything else as painted."""
import re
from easel import Session

# Run from this folder: the painting's session file sits one level up.
s = Session.load("../wenna.easel")
p = s.palette
flour = p.at_value(p.mix_many(["titanium_white", "yellow_ochre"], [8, 1]), 0.80)
W, H = 768, 1024


def P(x, y):
    return (x / W, y / H)


pts = [P(396, 469), P(412, 474), P(428, 471)]
for load in (0.22, 0.35, 0.5, 0.7, 0.9):
    for size in (0.012, 0.03):
        c = s.scratch()
        c.stroke(pts, "bristle", flour, size=size, load=load, opacity=0.6)
        line = c.log(last=1).strip().splitlines()[-1]
        landed = re.search(r"(NO PAINT LANDED|[\d.]+k? paint)", line).group(1)
        print(f"load {load:4.2f}  size {size:5.3f}  -> {landed}")
