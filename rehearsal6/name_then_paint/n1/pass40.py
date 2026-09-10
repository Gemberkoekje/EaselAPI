# Pass 40 - the bud again, the smear under A, and highlights as marks not dots.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()
rnd = random.Random(404)

# --- clear and repaint the bud ------------------------------------------------
s.block_in(polygon([(0.486,0.288),(0.640,0.284),(0.652,0.402),(0.560,0.438),(0.494,0.404)]),
           "flat", "bg", direction=(43, 133), density=1.0, size=0.018, load=1.0, pressure="even")
head(0.552, 0.358, 0.043, 0.037, 63, 0.545, 0.155, 0.009, lit=240.0, heart=False)
for t0, t1, f, v in ((178, 240, 1.00, 0.66), (240, 300, 0.98, 0.60), (140, 182, 1.02, 0.54),
                     (300, 356, 1.00, 0.50), (356, 60, 0.98, 0.44), (60, 130, 1.00, 0.41)):
    s.stroke(arc(0.552, 0.358, 0.043, 0.037, f*rnd.uniform(0.97, 1.05), t0, t1, 6), "bristle",
             (warm(pc(v), 0.10) if v > 0.55 else cool(pc(v), 0.12)),
             size=rnd.uniform(0.008, 0.013), load=rnd.uniform(0.6, 0.9),
             pressure=[0.4, 1.0, 0.4])
s.stroke(arc(0.552, 0.358, 0.043, 0.037, 1.00, 196, 246, 6), "liner", warm(pc(0.74), 0.09),
         size=0.0032, pressure=[0.25, 1.0, 0.3])
# the stalk of it, disappearing behind A
s.stroke([(0.548,0.398),(0.536,0.424),(0.520,0.440)], "round_hard", "stem",
         size=0.005, pressure=[0.8, 0.5, 0.15])

# --- the smear where A sits on C ----------------------------------------------
for t0, t1, f, v, sz in ((14, 74, 0.98, 0.54, 0.018), (30, 92, 1.04, 0.48, 0.016),
                         (56, 104, 0.92, 0.58, 0.014)):
    s.stroke(arc(0.442, 0.436, 0.100, 0.092, f, t0, t1, 7), "bristle", cool(pc(v), 0.13),
             size=sz, load=0.9, pressure=[0.45, 1.0, 0.45])
for t0, t1, f, v, sz in ((208, 262, 1.00, 0.80, 0.014), (262, 306, 0.98, 0.72, 0.012),
                         (176, 212, 1.02, 0.70, 0.011)):
    s.stroke(arc(0.398, 0.586, 0.078, 0.066, f, t0, t1, 7), "bristle", warm(pc(v), 0.10),
             size=sz, load=0.85, pressure=[0.45, 1.0, 0.45])
s.stroke(arc(0.398, 0.586, 0.078, 0.066, 1.00, 214, 258, 6), "liner", warm(pc(0.88), 0.08),
         size=0.0038, pressure=[0.25, 1.0, 0.3])

# --- highlights as marks ------------------------------------------------------
for x0, y0, x1, y1, col, w in (
        (0.386,0.400, 0.404,0.386, "titanium_white", 0.0085),
        (0.412,0.380, 0.430,0.370, p.mix("titanium_white","yellow_ochre",0.10), 0.0065),
        (0.578,0.480, 0.598,0.466, "titanium_white", 0.0080),
        (0.358,0.562, 0.374,0.552, p.mix("titanium_white","yellow_ochre",0.08), 0.0055),
        (0.772,0.803, 0.786,0.797, p.mix("titanium_white","yellow_ochre",0.14), 0.0042)):
    s.stroke([(x0, y0), ((x0+x1)/2, (y0+y1)/2 - 0.002), (x1, y1)], "round_hard", col,
             size=w, pressure=[0.3, 1.0, 0.3])

print("strokes:", s.stroke_count)
print(s.look(sketch=False))
