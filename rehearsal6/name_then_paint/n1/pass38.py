# Pass 38 - dry brush over the heads for a worked surface; mend the bud's horn.
exec(open("lib2.py").read())
pc, warm, cool, arc, at, clean, head, edges, ruffle = build(s)
import math, random
p = s.palette
s.dry()

# the bud's horn, and the hard band under B
s.block_in(polygon([(0.494,0.300),(0.560,0.296),(0.566,0.336),(0.516,0.348)]), "flat",
           "bg", direction=(44, 134), density=1.0, size=0.016, load=1.0, pressure="even")
for t0, t1, f, v in ((196, 250, 1.00, 0.60), (250, 292, 0.98, 0.55), (160, 200, 1.02, 0.52)):
    s.stroke(arc(0.556, 0.370, 0.045, 0.039, f, t0, t1, 6), "bristle",
             warm(pc(v), 0.10), size=0.010, load=0.85, pressure=[0.4, 1.0, 0.4])
for t0, t1, f, v in ((40, 96, 1.00, 0.47), (74, 126, 0.94, 0.44), (16, 62, 1.04, 0.50)):
    s.stroke(arc(0.640, 0.520, 0.112, 0.100, f, t0, t1, 7), "bristle",
             cool(pc(v), 0.13), size=0.020, load=0.55, pressure=[0.4, 1.0, 0.45])

def drybrush(cx, cy, rx, ry, seed, vbase, vamp, n, lit, szlo, szhi):
    rnd = random.Random(seed)
    for i in range(n):
        while True:
            u, v_ = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
            rr = u*u + v_*v_
            if 0.03 < rr <= 0.96: break
        px, py = cx + u*rx, cy + v_*ry
        th = math.degrees(math.atan2(v_, u))
        d = math.cos(math.radians(th - lit)) * min(1.0, math.sqrt(rr) * 1.3)
        val = max(0.32, min(0.94, vbase + vamp*d + rnd.uniform(-0.055, 0.075)))
        ang = math.radians(rnd.uniform(0, 360))
        L = rnd.uniform(0.030, 0.070) * (rx / 0.10)
        bx, by = math.cos(ang)*L, math.sin(ang)*L*(ry/rx)
        bow = rnd.uniform(-0.25, 0.25)
        pts = [(px - bx/2, py - by/2), (px - by*bow, py + bx*bow), (px + bx/2, py + by/2)]
        c = warm(pc(val), 0.13) if d > 0 else cool(pc(val), 0.10)
        s.stroke(pts, "bristle", c, size=rnd.uniform(szlo, szhi),
                 load=rnd.uniform(0.32, 0.55), pressure=[0.4, 1.0, rnd.uniform(0.35, 0.75)])

drybrush(0.442, 0.436, 0.100, 0.092, 601, 0.700, 0.205, 26, 228, 0.012, 0.026)
drybrush(0.640, 0.520, 0.112, 0.100, 611, 0.645, 0.220, 28, 218, 0.013, 0.028)
drybrush(0.398, 0.586, 0.078, 0.066, 621, 0.575, 0.195, 18, 236, 0.010, 0.020)
drybrush(0.556, 0.370, 0.045, 0.039, 631, 0.505, 0.150, 10, 242, 0.007, 0.014)

print("strokes:", s.stroke_count)
print(s.look(region=span("C3","G6"), sketch=False))
