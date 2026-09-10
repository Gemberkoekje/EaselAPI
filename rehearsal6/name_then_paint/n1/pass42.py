# Pass 42 - ruffle the silhouettes: small lobes out, small notches between.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()
rnd = random.Random(1212)

def lobe(cx, cy, rx, ry, th, v, w, f0=0.92, f1=1.10, lit=225.0, bow=0.0):
    r = math.radians(th)
    dx, dy = math.cos(r), math.sin(r)
    nx, ny = -math.sin(r), math.cos(r)
    x0, y0 = cx + f0*rx*dx, cy + f0*ry*dy
    x1, y1 = cx + f1*rx*dx, cy + f1*ry*dy
    xm, ym = (x0+x1)/2 + nx*bow, (y0+y1)/2 + ny*bow
    d = math.cos(math.radians(th - lit))
    c = warm(pc(v), 0.12) if d > 0 else cool(pc(v), 0.09)
    s.stroke([(x0, y0), (xm, ym), (x1, y1)], "round_hard", c, size=w,
             pressure=[0.30, 1.0, 0.22])
    s.stroke([(x0 + nx*w*0.22, y0 + ny*w*0.22), (xm + nx*w*0.30, ym + ny*w*0.30)],
             "liner", warm(pc(min(0.94, v + 0.11)), 0.08), size=0.0030,
             pressure=[0.3, 0.9, 0.2])

A = (0.442, 0.436, 0.100, 0.092); B = (0.640, 0.520, 0.112, 0.100); C = (0.398, 0.586, 0.078, 0.066)
for box, lit, specs in (
    (A, 228, [(186, 0.86, 0.020, 1.12, 0.004), (212, 0.90, 0.024, 1.14, -0.005),
              (240, 0.88, 0.018, 1.10, 0.003), (268, 0.82, 0.021, 1.13, -0.004),
              (296, 0.74, 0.017, 1.09, 0.003), (150, 0.70, 0.016, 1.08, -0.003)]),
    (B, 218, [(176, 0.80, 0.022, 1.12, 0.005), (200, 0.87, 0.026, 1.15, -0.005),
              (226, 0.85, 0.020, 1.11, 0.004), (252, 0.79, 0.023, 1.13, -0.004),
              (284, 0.72, 0.018, 1.09, 0.003), (322, 0.60, 0.016, 1.08, 0.003),
              (12,  0.52, 0.015, 1.07, -0.003)]),
    (C, 236, [(200, 0.78, 0.017, 1.12, 0.003), (228, 0.84, 0.020, 1.14, -0.004),
              (258, 0.75, 0.016, 1.10, 0.003), (296, 0.62, 0.014, 1.08, 0.002)])):
    for th, v, w, f1, bow in specs:
        lobe(*box, th, v, w, f0=0.90, f1=f1, lit=lit, bow=bow)

# small notches between lobes, short enough not to gouge
for box, ths in ((A, (199, 226, 254, 282)), (B, (188, 213, 239, 268, 303)), (C, (214, 243, 277))):
    cx, cy, rx, ry = box
    for th in ths:
        s.stroke([at(cx, cy, rx, ry, 1.06, th), at(cx, cy, rx, ry, 0.93, th + 3)],
                 "round_hard", "bg", size=0.0045, pressure=[1.0, 0.25])

print("strokes:", s.stroke_count)
print(s.look(region=span("C3","G6"), sketch=False))
