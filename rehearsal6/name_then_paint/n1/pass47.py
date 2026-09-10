# Pass 47 - repaint bloom A's lit shoulder, solidly, over the speckle crust.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()
rnd = random.Random(47)
A = (0.442, 0.436, 0.100, 0.092)

for f, t0, t1, v in ((0.98, 176, 232, 0.86), (0.98, 228, 284, 0.83), (0.99, 280, 322, 0.74),
                     (0.86, 172, 230, 0.89), (0.86, 226, 286, 0.86), (0.86, 282, 326, 0.77),
                     (0.72, 178, 238, 0.90), (0.72, 234, 294, 0.86), (0.72, 290, 330, 0.78),
                     (0.58, 184, 246, 0.87), (0.58, 242, 300, 0.83),
                     (1.03, 186, 240, 0.80), (1.03, 236, 292, 0.76)):
    s.stroke(arc(*A, f*rnd.uniform(0.98, 1.03), t0, t1, 8), "flat", warm(pc(v), 0.12),
             size=rnd.uniform(0.018, 0.028), load=1.0,
             pressure=("even" if rnd.random() < 0.5 else [0.7, 1.0, 0.6]))
# some surface back into it
for i in range(14):
    th = rnd.uniform(165, 335); f = rnd.uniform(0.45, 1.00)
    v = 0.845 + rnd.uniform(-0.06, 0.055)
    px, py = at(*A, f, th)
    ang = math.radians(rnd.uniform(0, 360)); L = rnd.uniform(0.028, 0.060)
    bx, by = math.cos(ang)*L, math.sin(ang)*L*0.92
    s.stroke([(px - bx/2, py - by/2), (px + bx*0.06, py - bx*0.06), (px + bx/2, py + by/2)],
             "bristle", warm(pc(v), 0.12), size=rnd.uniform(0.012, 0.022),
             load=rnd.uniform(0.45, 0.75), pressure=[0.4, 1.0, 0.5])
s.stroke(arc(*A, 1.00, 194, 246, 6), "liner", warm(pc(0.93), 0.07), size=0.0038,
         pressure=[0.25, 1.0, 0.3])
s.stroke(arc(*A, 0.70, 200, 240, 5), "liner", warm(pc(0.91), 0.07), size=0.0032,
         pressure=[0.25, 1.0, 0.3])
s.stroke([(0.386,0.400),(0.395,0.393),(0.404,0.386)], "round_hard", "titanium_white",
         size=0.0085, pressure=[0.3, 1.0, 0.3])
s.stroke([(0.412,0.380),(0.421,0.375),(0.430,0.370)], "round_hard",
         p.mix("titanium_white","yellow_ochre",0.10), size=0.0065, pressure=[0.3,1.0,0.3])

print("strokes:", s.stroke_count)
print(s.look())
