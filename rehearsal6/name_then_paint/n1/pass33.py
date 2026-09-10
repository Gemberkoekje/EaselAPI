# Pass 33 - a few big described petals laid across the rings.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()
rnd = random.Random(909)

def bigpetal(cx, cy, rx, ry, th, f0, f1, w, v, lit=225.0, bow=0.0):
    r = math.radians(th)
    dx, dy = math.cos(r), math.sin(r)
    nx, ny = -math.sin(r), math.cos(r)
    x0, y0 = cx + f0*rx*dx, cy + f0*ry*dy
    x1, y1 = cx + f1*rx*dx, cy + f1*ry*dy
    xm, ym = (x0+x1)/2 + nx*bow, (y0+y1)/2 + ny*bow
    d = math.cos(math.radians(th - lit))
    c = warm(pc(v), 0.13) if d > 0 else cool(pc(v), 0.09)
    s.stroke([(x0, y0), (xm, ym), (x1, y1)], "round_hard", c, size=w,
             pressure=[0.24, 1.0, 0.30])
    # the lit lip along one side of it
    s.stroke([(x0 + nx*w*0.28, y0 + ny*w*0.28),
              (xm + nx*w*0.40, ym + ny*w*0.40),
              (x1 + nx*w*0.24, y1 + ny*w*0.24)], "liner",
             warm(pc(min(0.95, v + 0.13)), 0.08), size=0.0042,
             pressure=[0.25, 1.0, 0.30])
    # and the shadow where it folds away on the other
    s.stroke([(x0 - nx*w*0.30, y0 - ny*w*0.30),
              (xm - nx*w*0.42, ym - ny*w*0.42)], "round_hard",
             cool(pc(max(0.33, v - 0.17)), 0.13), size=0.0055, pressure=[0.9, 0.2])

A = (0.442, 0.436, 0.100, 0.092)
for th, f0, f1, w, v, bow in ((212, 0.30, 1.03, 0.040, 0.86, 0.008),
                              (258, 0.26, 0.98, 0.034, 0.80, -0.006),
                              (168, 0.30, 1.05, 0.036, 0.74, 0.007),
                              (134, 0.28, 0.96, 0.030, 0.63, -0.005),
                              (28,  0.30, 1.00, 0.032, 0.49, 0.006)):
    bigpetal(*A, th, f0, f1, w, v, lit=228.0, bow=bow)

B = (0.640, 0.520, 0.112, 0.100)
for th, f0, f1, w, v, bow in ((204, 0.28, 1.02, 0.042, 0.83, 0.009),
                              (250, 0.26, 0.97, 0.036, 0.77, -0.007),
                              (160, 0.30, 1.04, 0.038, 0.70, 0.006),
                              (300, 0.28, 0.94, 0.030, 0.66, 0.005),
                              (46,  0.30, 1.02, 0.034, 0.45, -0.006),
                              (96,  0.28, 0.96, 0.028, 0.42, 0.005)):
    bigpetal(*B, th, f0, f1, w, v, lit=218.0, bow=bow)

C = (0.398, 0.586, 0.078, 0.066)
for th, f0, f1, w, v, bow in ((220, 0.28, 1.02, 0.030, 0.76, 0.006),
                              (266, 0.26, 0.96, 0.026, 0.68, -0.005),
                              (176, 0.30, 1.04, 0.026, 0.62, 0.005),
                              (60,  0.30, 0.98, 0.024, 0.42, 0.004)):
    bigpetal(*C, th, f0, f1, w, v, lit=236.0, bow=bow)

print("strokes:", s.stroke_count)
print(s.look(region=span("C3","G6"), sketch=False))
