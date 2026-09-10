import math, random
def build(s):
    p = s.palette
    grey = p.mix("ultramarine", "burnt_sienna", 0.50)
    LO = p.tint(grey, 0.34)
    HI = p.mix("titanium_white", "yellow_ochre", 0.06)
    def pc(v):
        a, b = 0.0, 1.0
        for _ in range(20):
            m = (a + b) / 2
            a, b = (m, b) if p.value_of(p.mix(LO, HI, m)) < v else (a, m)
        return p.mix(LO, HI, (a + b) / 2)
    def warm(c, k=0.10): return p.mix(c, p.mix("yellow_ochre", "cadmium_red", 0.30), k)
    def cool(c, k=0.10): return p.mix(c, "ultramarine", k)
    def arc(cx, cy, rx, ry, f, t0, t1, n=7):
        return [(cx + f*rx*math.cos(math.radians(t0+(t1-t0)*i/(n-1))),
                 cy + f*ry*math.sin(math.radians(t0+(t1-t0)*i/(n-1)))) for i in range(n)]
    def at(cx, cy, rx, ry, f, th):
        r = math.radians(th); return (cx + f*rx*math.cos(r), cy + f*ry*math.sin(r))

    def clean(cx, cy, rx, ry, segs, sz=0.020, rr=1.15):
        """paint the neighbour's colour in a ring safely outside the silhouette"""
        for t0, t1, col in segs:
            rnd = random.Random(int(t0) + 7)
            th = t0
            while th < t1:
                b = min(t1, th + 22 + rnd.uniform(-4, 6))
                s.stroke(arc(cx, cy, rx, ry, rr + rnd.uniform(-0.02, 0.03), th, b, 6),
                         "round_hard", col, size=sz*rnd.uniform(0.9, 1.25),
                         pressure="even", load=1.0)
                th = b

    def head(cx, cy, rx, ry, seed, vbase, vamp, sz, lit=225.0, heart=True):
        rnd = random.Random(seed)
        e = ellipse(Region(cx-rx, cy-ry, cx+rx, cy+ry))
        s.block_in(e.inset(sz*0.6), "flat", pc(vbase - 0.02), direction=("axis", 74),
                   density=1.0, size=sz, load=1.0, pressure="even")
        for f, dv in [(0.30,-0.10),(0.50,-0.02),(0.68,0.04),(0.84,0.06),(0.96,-0.01)]:
            segs = 5 if f > 0.6 else 4
            for k in range(segs):
                t0 = lit - 180 + (360.0/segs)*k + rnd.uniform(-14, 14)
                t1 = t0 + 360.0/segs + rnd.uniform(6, 26)
                d = math.cos(math.radians((t0+t1)/2 - lit))
                v = max(0.32, min(0.92, vbase + vamp*d + dv + rnd.uniform(-0.03, 0.03)))
                c = warm(pc(v), 0.13) if d > 0 else cool(pc(v), 0.10)
                s.stroke(arc(cx, cy, rx, ry, f*rnd.uniform(0.95, 1.04), t0, t1), "flat", c,
                         size=sz*rnd.uniform(0.8, 1.3),
                         pressure=("even" if k % 2 else [0.7, 1.0, 0.6]), load=1.0)
        for k, (t0, sp, f, dv) in enumerate([(-16, 74, 0.66, -0.86), (2, 82, 0.86, -0.94),
                                             (24, 66, 0.98, -1.02), (44, 54, 0.50, -0.76)]):
            v = max(0.32, vbase + vamp*dv)
            s.stroke(arc(cx, cy, rx, ry, f, lit + 180 + t0, lit + 180 + t0 + sp, 8), "flat",
                     cool(pc(v), 0.16), size=sz*(0.9 + 0.2*(k % 2)), pressure="even", load=1.0)
        if heart:
            s.stroke(arc(cx+rx*0.03, cy+ry*0.04, rx, ry, 0.17, 30, 320, 6), "round_hard",
                     cool(pc(max(0.34, vbase - vamp*0.85)), 0.14), size=sz*0.6, pressure="even")
            s.stroke([at(cx, cy, rx, ry, 0.10, 190), at(cx, cy, rx, ry, 0.06, 270),
                      at(cx, cy, rx, ry, 0.12, 350)], "round_hard",
                     p.mix(pc(vbase - 0.06), p["pet_heart"], 0.40), size=sz*0.36,
                     pressure=[0.4, 1.0, 0.35])

    def edges(cx, cy, rx, ry, seed, vbase, vamp, sz, specs, lit=225.0):
        rnd = random.Random(seed)
        for th, w, dv, f in specs:
            d = math.cos(math.radians(th - lit))
            v = min(0.94, vbase + vamp*d + dv)
            s.stroke(arc(cx, cy, rx, ry, f, th-w/2, th+w/2, 6), "round_hard",
                     warm(pc(v), 0.10), size=sz*rnd.uniform(0.20, 0.36),
                     pressure=[0.3, 1.0, 0.35])

    def ruffle(cx, cy, rx, ry, seed, vbase, vamp, n, sz, lit=225.0):
        """petals added OUTWARD, never cut inward"""
        rnd = random.Random(seed)
        for i in range(n):
            th = rnd.uniform(0, 360)
            d = math.cos(math.radians(th - lit))
            v = max(0.34, min(0.90, vbase + vamp*d + rnd.uniform(-0.05, 0.08)))
            f = rnd.uniform(0.98, 1.08)
            cxo, cyo = at(cx, cy, rx, ry, f, th)
            a = rx * rnd.uniform(0.16, 0.26); b = ry * rnd.uniform(0.11, 0.18)
            el = ellipse(Region(cxo-a, cyo-b, cxo+a, cyo+b), rotate=th+90)
            s.block_in(el.inset(sz*0.55), "flat", (warm(pc(v), 0.12) if d > 0 else cool(pc(v), 0.08)),
                       direction="axis", density=1.0, size=sz, load=1.0, pressure="even")
    return pc, warm, cool, arc, at, clean, head, edges, ruffle
