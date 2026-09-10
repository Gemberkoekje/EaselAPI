# Pass 34 - dissolve the propeller: irregular scumble, no radial structure.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()

def scumble(cx, cy, rx, ry, seed, vbase, vamp, n, lit, szlo, szhi):
    rnd = random.Random(seed)
    for i in range(n):
        # a point inside the head, biased away from the exact centre
        while True:
            u, v_ = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
            if 0.04 < u*u + v_*v_ <= 1.02: break
        px, py = cx + u*rx, cy + v_*ry
        th = math.degrees(math.atan2(v_, u))
        d = math.cos(math.radians(th - lit)) * min(1.0, math.hypot(u, v_) * 1.25)
        local = vbase + vamp * d
        val = max(0.32, min(0.93, local + rnd.uniform(-0.065, 0.065)))
        ang = math.radians(rnd.uniform(0, 360))
        L = rnd.uniform(0.020, 0.055) * (rx / 0.10)
        bx, by = math.cos(ang) * L, math.sin(ang) * L * (ry / rx)
        cbow = rnd.uniform(-0.28, 0.28)
        pts = [(px - bx/2, py - by/2),
               (px - by*cbow, py + bx*cbow),
               (px + bx/2, py + by/2)]
        c = warm(pc(val), 0.12) if d > 0 else cool(pc(val), 0.09)
        s.stroke(pts, "bristle", c, size=rnd.uniform(szlo, szhi),
                 load=rnd.uniform(0.5, 0.9), pressure=[0.35, 1.0, rnd.uniform(0.3, 0.7)])

scumble(0.442, 0.436, 0.100, 0.092, 401, 0.700, 0.205, 30, 228, 0.010, 0.024)
scumble(0.640, 0.520, 0.112, 0.100, 411, 0.645, 0.220, 32, 218, 0.011, 0.026)
scumble(0.398, 0.586, 0.078, 0.066, 421, 0.575, 0.195, 22, 236, 0.008, 0.019)
scumble(0.556, 0.370, 0.045, 0.039, 431, 0.505, 0.150, 12, 242, 0.006, 0.013)

print("strokes:", s.stroke_count)
print(s.look(region=span("C3","G6"), sketch=False))
