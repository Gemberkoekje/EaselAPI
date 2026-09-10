# Pass 35 - resurface the heads with strokes big enough to bury the blade lines.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()

def resurface(cx, cy, rx, ry, seed, vbase, vamp, n, lit, szlo, szhi):
    rnd = random.Random(seed)
    for i in range(n):
        while True:
            u, v_ = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
            rr = u*u + v_*v_
            if 0.02 < rr <= 1.0: break
        px, py = cx + u*rx, cy + v_*ry
        th = math.degrees(math.atan2(v_, u))
        d = math.cos(math.radians(th - lit)) * min(1.0, math.sqrt(rr) * 1.3)
        val = max(0.32, min(0.92, vbase + vamp*d + rnd.uniform(-0.05, 0.05)))
        ang = math.radians(rnd.uniform(0, 360))
        L = rnd.uniform(0.035, 0.085) * (rx / 0.10)
        bx, by = math.cos(ang)*L, math.sin(ang)*L*(ry/rx)
        bow = rnd.uniform(-0.22, 0.22)
        pts = [(px - bx/2, py - by/2), (px - by*bow, py + bx*bow), (px + bx/2, py + by/2)]
        c = warm(pc(val), 0.12) if d > 0 else cool(pc(val), 0.09)
        s.stroke(pts, "bristle", c, size=rnd.uniform(szlo, szhi),
                 load=rnd.uniform(0.8, 1.0), pressure=[0.4, 1.0, rnd.uniform(0.4, 0.8)])

resurface(0.442, 0.436, 0.100, 0.092, 501, 0.700, 0.205, 34, 228, 0.020, 0.034)
resurface(0.640, 0.520, 0.112, 0.100, 511, 0.645, 0.220, 36, 218, 0.022, 0.036)
resurface(0.398, 0.586, 0.078, 0.066, 521, 0.575, 0.195, 24, 236, 0.016, 0.028)
resurface(0.556, 0.370, 0.045, 0.039, 531, 0.505, 0.150, 14, 242, 0.011, 0.019)

print("strokes:", s.stroke_count)
print(s.look(region=span("C3","G6"), sketch=False))
