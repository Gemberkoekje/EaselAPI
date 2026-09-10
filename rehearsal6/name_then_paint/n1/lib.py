import math, random
def make(s):
    p = s.palette
    grey = p.mix("ultramarine", "burnt_sienna", 0.50)
    LO = p.tint(grey, 0.36)
    HI = p.mix("titanium_white", "yellow_ochre", 0.07)
    def pc(v):
        a, b = 0.0, 1.0
        for _ in range(20):
            m = (a + b) / 2
            a, b = (m, b) if p.value_of(p.mix(LO, HI, m)) < v else (a, m)
        return p.mix(LO, HI, (a + b) / 2)
    def warm(c, k=0.10): return p.mix(c, p.mix("yellow_ochre", "cadmium_red", 0.30), k)
    def cool(c, k=0.10): return p.mix(c, "ultramarine", k)
    def arc(cx, cy, rx, ry, f, t0, t1, steps=7):
        return [(cx + f*rx*math.cos(math.radians(t0+(t1-t0)*i/(steps-1))),
                 cy + f*ry*math.sin(math.radians(t0+(t1-t0)*i/(steps-1)))) for i in range(steps)]
    def at(cx, cy, rx, ry, f, th):
        r = math.radians(th)
        return (cx + f*rx*math.cos(r), cy + f*ry*math.sin(r))

    def dome(cx, cy, rx, ry, seed, vbase, vamp, sz, lit=225.0):
        rnd = random.Random(seed)
        for f, dv in [(0.30,-0.10),(0.50,-0.02),(0.68,0.04),(0.84,0.06),(0.98,-0.02)]:
            segs = 5 if f > 0.6 else 4
            for k in range(segs):
                t0 = lit - 180 + (360.0/segs)*k + rnd.uniform(-14, 14)
                t1 = t0 + 360.0/segs + rnd.uniform(6, 26)
                d = math.cos(math.radians((t0+t1)/2 - lit))
                v = max(0.34, min(0.90, vbase + vamp*d + dv + rnd.uniform(-0.03, 0.03)))
                c = warm(pc(v), 0.13) if d > 0 else cool(pc(v), 0.10)
                s.stroke(arc(cx, cy, rx, ry, f*rnd.uniform(0.94, 1.06), t0, t1), "flat", c,
                         size=sz*rnd.uniform(0.8, 1.35),
                         pressure=("even" if k % 2 else [0.7, 1.0, 0.6]), load=1.0)

    def finish(cx, cy, rx, ry, seed, vbase, vamp, sz, lit=225.0, bg="bg",
               notches=8, edges=7, out_petals=4, bites=4, droop=()):
        rnd = random.Random(seed + 100)
        # shadow flank
        for k in range(3):
            t0 = lit + 105 + k*38 + rnd.uniform(-10, 10)
            v = vbase - vamp*0.92 + rnd.uniform(-0.02, 0.03)
            s.stroke(arc(cx, cy, rx, ry, (0.62 + 0.17*k)*rnd.uniform(0.96, 1.04), t0, t0+62),
                     "flat", cool(pc(max(0.34, v)), 0.16), size=sz*rnd.uniform(0.9, 1.3),
                     pressure="even", load=1.0)
        # petals hanging off the mass
        for cxo, cyo, rxo, ryo, v in droop:
            e = ellipse(Region(cxo-rxo, cyo-ryo, cxo+rxo, cyo+ryo))
            s.block_in(e.inset(0.006), "flat", pc(v), direction="axis", density=1.0,
                       size=0.012, load=1.0, pressure="even")
            s.stroke([(cxo-rxo*0.8, cyo-ryo*0.5), (cxo, cyo-ryo*0.95), (cxo+rxo*0.7, cyo-ryo*0.4)],
                     "round_hard", pc(min(0.93, v+0.16)), size=0.005, pressure=[0.4, 1.0, 0.3])
        # separations between petals
        for i in range(notches):
            th = rnd.uniform(0, 360)
            d = math.cos(math.radians(th - lit))
            v = max(0.32, vbase + vamp*d - 0.15)
            f1 = rnd.uniform(0.94, 1.04); f0 = f1 - rnd.uniform(0.30, 0.55)
            s.stroke([at(cx, cy, rx, ry, f0, th+rnd.uniform(-6, 6)),
                      at(cx, cy, rx, ry, (f0+f1)/2, th+rnd.uniform(-4, 4)),
                      at(cx, cy, rx, ry, f1, th)],
                     "round_hard", cool(pc(v), 0.12), size=sz*rnd.uniform(0.24, 0.42),
                     pressure=[0.25, 1.0, 0.45])
        # lit petal edges
        for i in range(edges):
            th = lit + rnd.uniform(-95, 95)
            d = math.cos(math.radians(th - lit))
            v = min(0.94, vbase + vamp*d + rnd.uniform(0.10, 0.20))
            f = rnd.uniform(0.62, 1.00)
            w = rnd.uniform(24, 52)
            s.stroke(arc(cx, cy, rx, ry, f, th-w/2, th+w/2, 5), "round_hard",
                     warm(pc(v), 0.10), size=sz*rnd.uniform(0.22, 0.40),
                     pressure=[0.3, 1.0, rnd.uniform(0.25, 0.6)])
        # petals breaking the silhouette outward
        for i in range(out_petals):
            th = lit + rnd.uniform(-110, 110)
            d = math.cos(math.radians(th - lit))
            v = max(0.36, min(0.90, vbase + vamp*d + rnd.uniform(-0.04, 0.10)))
            f = rnd.uniform(1.02, 1.12)
            cxo, cyo = at(cx, cy, rx, ry, f, th)
            e = ellipse(Region(cxo-rx*0.20, cyo-ry*0.15, cxo+rx*0.20, cyo+ry*0.15),
                        rotate=th+90)
            s.block_in(e.inset(0.005), "flat", pc(v), direction="axis", density=1.0,
                       size=0.011, load=1.0, pressure="even")
        # bites of background taken out of the rim
        for i in range(bites):
            th = rnd.uniform(0, 360)
            a0 = at(cx, cy, rx, ry, rnd.uniform(1.02, 1.14), th - rnd.uniform(4, 12))
            a1 = at(cx, cy, rx, ry, rnd.uniform(0.80, 0.92), th + rnd.uniform(4, 12))
            s.stroke([a0, a1], "round_hard", bg, size=sz*rnd.uniform(0.30, 0.52),
                     pressure=[1.0, 0.35])
    return pc, warm, cool, arc, at, dome, finish
