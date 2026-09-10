def paint_pot(seed=727):
    rng = random.Random(seed)
    _t2 = p.mix(p.mix("burnt_sienna", "cadmium_red", 0.18), "yellow_ochre", 0.22)
    VK = [(-1.00,0.335),(-0.88,0.262),(-0.72,0.228),(-0.56,0.248),(-0.40,0.278),
          (-0.24,0.318),(-0.10,0.368),( 0.05,0.415),( 0.25,0.478),( 0.50,0.548),
          ( 0.72,0.596),( 0.88,0.558),( 1.00,0.468)]
    def vof(u):
        u = max(-1.0, min(1.0, u))
        for i in range(len(VK)-1):
            if VK[i][0] <= u <= VK[i+1][0]:
                (a,va),(b,vb) = VK[i], VK[i+1]
                return va + (vb-va)*(u-a)/(b-a)
        return VK[-1][1]
    CC = {}
    def pc(u, dv=0.0):
        k = (round(u,3), round(dv,3))
        if k not in CC:
            base = (p.mix(_t2, "ultramarine", 0.08+0.18*min(1.0,-u)) if u < -0.06
                    else p.mix(_t2, "cadmium_yellow", 0.05+0.16*u))
            CC[k] = at(p.desaturate(base, 0.19), max(0.145, vof(u)+dv))
        return CC[k]
    def bstroke(u, ya, yb, n=8):
        return [(CX + u*hw(max(0.5545, ya+(yb-ya)*i/(n-1.0))), ya+(yb-ya)*i/(n-1.0))
                for i in range(n)]

    s.dry()
    s.block_in(SIL.inset(0.015), "flat", pc(0.0), direction=(94,), density=1.0,
               size=0.030, pressure="even", load=1.0)
    for i in range(27):
        u = -1.01 + 2.02*i/26.0 + rng.uniform(-0.016, 0.016)
        k = (1.0 - min(0.999, u*u)) ** 0.5
        ya = max(0.5555, 0.5460 + 0.0325*k + 0.003) + rng.uniform(0.0, 0.009)
        yb = 0.7455 + 0.0140*k - rng.uniform(0.0, 0.017)
        s.stroke(bstroke(u, ya, yb), "flat", pc(u, rng.uniform(-0.016, 0.016)),
                 size=rng.uniform(0.014, 0.020), pressure="even", load=1.0)
    for y, ry, a, b, col, sz, pr, ld in [
            (0.5760,0.011,-0.96, 0.96,pc(-0.30,-0.075),0.011,[0.95,1.0,0.85,0.5],0.95),
            (0.6050,0.013,-0.94,-0.16,pc(-0.62,-0.028),0.011,"taper",0.80),
            (0.6350,0.015, 0.82, 0.12,pc( 0.50, 0.028),0.012,"lift_off",0.70),
            (0.6820,0.017,-0.20,-0.90,pc(-0.50, 0.030),0.010,"lift_off",0.60),
            (0.7020,0.018, 0.86,-0.10,pc( 0.30, 0.026),0.011,"taper",0.70),
            (0.7300,0.020,-0.86, 0.86,pc(-0.12,-0.085),0.013,[0.5,1.0,0.8,0.4],0.90)]:
        s.stroke(ring(y, ry, a, b), "bristle", col, size=sz, pressure=pr, load=ld)

    # the collar
    def cstroke(x):
        u = max(-0.999, min(0.999, (x - CX)/0.115))
        k = (1.0 - u*u) ** 0.5
        return [(x, 0.5075 + 0.024*k), (x - 0.001, 0.546 + 0.0325*k)]
    for i in range(19):
        x = 0.5145 + 0.2165*i/18.0
        u = (x - CX)/0.115
        s.stroke(cstroke(x), "flat", pc(max(-1.0,min(1.0,u)), 0.055 + rng.uniform(-0.02,0.02)),
                 size=0.0135, pressure="even", load=1.0)
    # far lip, the dark, what is in it, near lip
    s.stroke(arc(CX, 0.4985, 0.1010, 0.0255, 182, 358, 22), "flat",
             at(p.desaturate(p.mix(_t2,"cadmium_yellow",0.30),0.22), 0.700),
             size=0.010, pressure="even", load=1.0)
    s.block_in(ellipse((CX, 0.5015), 0.0925, 0.0215).inset(0.004), "flat", "pot_dark",
               direction=(3,), density=1.0, size=0.009, pressure="even", load=1.0)
    s.block_in(ellipse((CX, 0.4975), 0.0800, 0.0130).inset(0.003), "flat", "soil",
               direction=(2,), density=1.0, size=0.007, pressure="even", load=1.0)
    for x, y in [(0.556,0.4955),(0.586,0.4920),(0.618,0.4945),(0.650,0.4905),
                 (0.680,0.4960),(0.604,0.4995),(0.666,0.4880),(0.634,0.5010)]:
        s.dab(x, y, "round_hard", "leaf_dk", size=0.012, press=2)
    s.stroke(arc(CX, 0.5085, 0.1055, 0.0270, 168, 12, 22), "flat", pc(0.35, 0.075),
             size=0.009, pressure="even", load=1.0)
    s.stroke(arc(CX, 0.5100, 0.0700, 0.0245, 150, 42, 14), "liner",
             at(p.desaturate(p.mix(_t2,"cadmium_yellow",0.30),0.22), 0.720),
             size=0.005, pressure=[0.3,1.0,0.7,0.9,0.25], load=1.0)
    s.dab(0.5460, 0.5130, "round_hard", "pot_dark", size=0.011, press=2)
    s.dab(0.5440, 0.5075, "round_hard",
          at(p.desaturate(p.mix(_t2,"cadmium_yellow",0.30),0.22), 0.700), size=0.006, press=2)
    # bloom
    for x0,y0,x1,y1,sz,ld in [(0.5540,0.6320,0.5700,0.6200,0.007,0.45),
                              (0.5460,0.6820,0.5610,0.6740,0.006,0.40),
                              (0.6440,0.6920,0.6680,0.6840,0.006,0.45),
                              (0.6980,0.6100,0.7090,0.5990,0.005,0.40)]:
        s.stroke([(x0,y0),(x1,y1)], "bristle", "bloom", size=sz, pressure="taper", load=ld)
    # the crack, last on the pot
    s.stroke([(0.5895,0.5495),(0.5905,0.5620),(0.5865,0.5980),(0.5960,0.6360),
              (0.5880,0.6710),(0.5945,0.7010),(0.5905,0.7250)], "liner", "crackw",
             size=0.0044, pressure=[0.05,0.55,1.0,0.75,1.0,0.5,0.05], load=1.0)
    s.stroke([(0.5952,0.5700),(0.5920,0.5990),(0.6008,0.6320)], "liner",
             at(p.desaturate(p.mix(_t2,"cadmium_yellow",0.20),0.22), 0.680),
             size=0.0030, pressure=[0.1,0.9,0.3], load=1.0)
    s.stroke([(0.5950,0.6420),(0.6135,0.6620),(0.6255,0.6730)], "liner", "crackw",
             size=0.0034, pressure=[0.85,0.5,0.05], load=1.0)
    s.stroke([(0.5860,0.6050),(0.5745,0.6180)], "liner", "crackw",
             size=0.0028, pressure=[0.7,0.05], load=1.0)
