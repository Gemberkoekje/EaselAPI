p = s.palette
dk   = p["dk"]
pale = p.mix("titanium_white", "yellow_ochre", 0.28)
def U(r): return p.mix(pale, "burnt_umber", r)
def D(r): return p.mix(pale, dk, r)

p["sillA"]=D(0.30); p["sillB"]=U(0.07); p["sillC"]=U(0.115)
p["sillD"]=U(0.26); p["sillE"]=D(0.52); p["sillF"]=D(0.66)
p["faceA"]=U(0.36); p["faceB"]=U(0.30); p["faceC"]=D(0.42); p["faceD"]=D(0.60)
p["potshadow"]=D(0.58); p["under"]=p.mix(dk,"burnt_sienna",0.18)
for n in ("sillA","sillB","sillC","sillD","sillE","sillF","faceA","faceB","faceC","faceD"):
    print(n, p.hex(p[n]), round(p.value_of(p[n]),2))

s.mark("pot_rl", 0.497, 0.543); s.mark("pot_rr", 0.673, 0.537)
s.mark("pot_base", 0.585, 0.726)

s.dry()
# --- the dark under the sill goes first: it is furthest ---
s.block_in(polygon([(-0.08,0.898),(1.10,0.870),(1.10,1.09),(-0.08,1.09)]), "flat",
           "under", density=1.0, size=0.075, direction=(-4, 84), load=1.0)
s.block_in(blob((0.72,0.965), 0.30, 0.06, wobble=0.5, seed=17), "bristle", "wall_warm",
           density=0.5, size=0.05, direction=(6,92), load=0.55)

# --- the sill top, five steps of light falling away to the right ---
def strip(x0, x1, yb0, yb1, yf0, yf1):
    return polygon([(x0,yb0),(x1,yb1),(x1,yf1),(x0,yf0)])
def yb(x): return 0.6480 + 0.020 * x
def yf(x): return 0.8010 - 0.038 * x
steps = [(-0.10, 0.125, "sillA", 0.042, -5),
         ( 0.085, 0.315, "sillB", 0.048,  3),
         ( 0.290, 0.530, "sillC", 0.045, -3),
         ( 0.505, 0.720, "sillD", 0.046,  6),
         ( 0.695, 0.905, "sillE", 0.044, -2),
         ( 0.880, 1.10,  "sillF", 0.048,  4)]
for x0, x1, col, sz, ang in steps:
    sh = strip(x0, x1, yb(x0), yb(x1), yf(x0), yf(x1))
    s.block_in(sh, "flat", col, density=1.0, size=sz, direction=ang, load=1.0)
# lose the joins between the steps
for x in (0.105, 0.302, 0.517, 0.707, 0.892):
    s.smudge([(x, yb(x)+0.022), (x+0.012, yf(x)-0.020)], size=0.036)

# --- the front face, darker: it faces away from the light ---
def fb(x): return 0.8010 - 0.038 * x
def ff(x): return 0.9060 - 0.030 * x
faces = [(-0.10, 0.175, "faceA", 0.038, 4), (0.150, 0.470, "faceB", 0.042, -3),
         (0.445, 0.735, "faceC", 0.040, 5), (0.710, 1.10, "faceD", 0.044, -4)]
for x0, x1, col, sz, ang in faces:
    sh = polygon([(x0,fb(x0)),(x1,fb(x1)),(x1,ff(x1)),(x0,ff(x0))])
    s.block_in(sh, "flat", col, density=1.0, size=sz, direction=ang, load=1.0)
for x in (0.163, 0.458, 0.723):
    s.smudge([(x, fb(x)+0.018), (x+0.010, ff(x)-0.016)], size=0.034)

# --- the pot's cast shadow lies on the sill, so it goes on before the pot ---
cast = polygon([(0.580,0.700),(0.760,0.712),(0.905,0.760),(0.870,0.790),
                (0.700,0.772),(0.585,0.742)])
s.block_in(cast, "flat", "potshadow", density=0.85, size=0.035, direction=8, load=0.9)
s.smudge([(0.800,0.742),(0.895,0.768)], size=0.036)
s.smudge([(0.665,0.706),(0.760,0.716)], size=0.030)
print("strokes:", s.stroke_count)
