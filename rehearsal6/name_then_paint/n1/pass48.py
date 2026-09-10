# Pass 48 - the bud's halo, and the dirt along B's lower edge.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()
rnd = random.Random(48)

for t0 in range(0, 360, 30):
    s.stroke(arc(0.550, 0.360, 0.036, 0.030, 1.30 + rnd.uniform(-0.05, 0.06), t0, t0+34, 5),
             "round_hard", "bg", size=0.014, pressure="even", load=1.0)
for t0, t1, f, v in ((176, 240, 1.00, 0.60), (240, 300, 0.98, 0.54), (300, 356, 1.00, 0.45),
                     (356, 62, 0.99, 0.41), (62, 122, 1.00, 0.39), (122, 178, 1.02, 0.50)):
    s.stroke(arc(0.550, 0.360, 0.036, 0.030, f, t0, t1, 6), "bristle",
             (warm(pc(v), 0.10) if v > 0.50 else cool(pc(v), 0.12)),
             size=rnd.uniform(0.008, 0.012), load=rnd.uniform(0.8, 1.0), pressure=[0.4,1.0,0.4])
s.stroke(arc(0.550, 0.360, 0.036, 0.030, 1.00, 198, 248, 6), "liner", warm(pc(0.70), 0.09),
         size=0.0030, pressure=[0.25, 1.0, 0.3])
s.stroke([(0.548,0.390),(0.542,0.416),(0.537,0.440)], "round_hard", "stem",
         size=0.0050, pressure=[0.9, 0.7, 0.25])

# the speckled dirt under B, back to background and table
for t0, t1 in ((16, 62), (56, 104), (98, 140)):
    s.stroke(arc(0.640, 0.520, 0.112, 0.100, 1.20, t0, t1, 6), "round_hard", "bg",
             size=0.026, pressure="even", load=1.0)
for t0, t1, f, v in ((14, 68, 1.00, 0.44), (58, 116, 0.98, 0.41), (104, 146, 1.00, 0.47)):
    s.stroke(arc(0.640, 0.520, 0.112, 0.100, f, t0, t1, 7), "bristle", cool(pc(v), 0.14),
             size=rnd.uniform(0.016, 0.024), load=rnd.uniform(0.85, 1.0), pressure=[0.45,1.0,0.45])

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
