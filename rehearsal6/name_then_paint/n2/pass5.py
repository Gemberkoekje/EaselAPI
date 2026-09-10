import random
p = s.palette; rnd = random.Random(77)
dk = p["dk"]; pale = p.mix("titanium_white", "yellow_ochre", 0.28)

def at_val(target, b):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if p.value_of(p.mix(pale, b, mid)) > target: lo = mid
        else: hi = mid
    return p.mix(pale, b, (lo + hi) / 2)

warm = "burnt_umber"
def V(t):                       # warm above 0.42, cooling into the shadows
    return at_val(t, warm) if t > 0.44 else at_val(t, dk)

s.dry()
def yb(x): return 0.6480 + 0.020 * x
def yf(x): return 0.8010 - 0.038 * x
def ff(x): return 0.9060 - 0.030 * x

# --- sill top: eight interlocking steps, joins slanted, not vertical ---
top = [(-0.11, 0.105, 0.46, 0.040, -6, 0.010), (0.075, 0.250, 0.745, 0.046, 3, -0.014),
       (0.225, 0.395, 0.710, 0.043, -4, 0.016), (0.370, 0.515, 0.662, 0.041, 5, -0.012),
       (0.492, 0.615, 0.585, 0.038, -3, 0.014), (0.594, 0.712, 0.470, 0.036, 6, -0.010),
       (0.690, 0.835, 0.360, 0.040, -5, 0.012), (0.812, 1.11, 0.270, 0.046, 4, -0.016)]
for x0, x1, val, sz, ang, skew in top:
    sh = polygon([(x0, yb(x0)), (x1, yb(x1) + skew), (x1, yf(x1) + skew), (x0, yf(x0))])
    s.block_in(sh, "flat", V(val), density=1.0, size=sz, direction=ang, load=1.0)
# interlock the joins by scumbling each neighbour a little way across
for i in range(len(top) - 1):
    xj = (top[i][1] + top[i+1][0]) / 2
    for src, dx in ((top[i], 0.030), (top[i+1], -0.030)):
        sh = polygon([(xj-0.026, yb(xj)+0.006), (xj+0.026, yb(xj)+0.006),
                      (xj+0.026+dx*0.4, yf(xj)-0.008), (xj-0.026+dx*0.4, yf(xj)-0.008)])
        s.block_in(sh, "bristle", V(src[2]), density=0.45, size=0.030,
                   direction=rnd.choice([62, 74, 108, 118]), load=0.55)

# --- front face ---
face = [(-0.11, 0.170, 0.40, 0.038, 4), (0.145, 0.350, 0.462, 0.040, -5),
        (0.325, 0.530, 0.420, 0.037, 6), (0.505, 0.710, 0.340, 0.039, -4),
        (0.685, 0.890, 0.272, 0.041, 3), (0.865, 1.11, 0.232, 0.044, -3)]
for x0, x1, val, sz, ang in face:
    sh = polygon([(x0, yf(x0)), (x1, yf(x1)), (x1, ff(x1)), (x0, ff(x0))])
    s.block_in(sh, "flat", V(val), density=1.0, size=sz, direction=ang, load=1.0)
for i in range(len(face) - 1):
    xj = (face[i][1] + face[i+1][0]) / 2
    s.block_in(polygon([(xj-0.030, yf(xj)+0.005), (xj+0.030, yf(xj)+0.005),
                        (xj+0.030, ff(xj)-0.006), (xj-0.030, ff(xj)-0.006)]),
               "bristle", V((face[i][2]+face[i+1][2])/2), density=0.5, size=0.028,
               direction=rnd.choice([58, 71, 112, 124]), load=0.6)

# --- a worked surface: a few marks, varied, not a repeated grain ---
for x0, x1, y, val, sz, ld in [(0.14, 0.44, 0.706, 0.68, 0.020, 0.45),
                               (0.30, 0.50, 0.762, 0.60, 0.014, 0.40),
                               (0.55, 0.78, 0.690, 0.40, 0.016, 0.50),
                               (0.06, 0.19, 0.746, 0.55, 0.012, 0.35),
                               (0.70, 0.95, 0.845, 0.29, 0.018, 0.45)]:
    s.stroke([(x0, y), (x1, y - 0.012 * (x1 - x0))], "bristle", V(val),
             size=sz, load=ld, pressure=rnd.choice(["lift_off", "taper", "swell"]))
s.stroke([(0.235, 0.690), (0.262, 0.775)], "bristle", V(0.62), size=0.012, load=0.4)
s.stroke([(0.905, 0.700), (0.868, 0.766)], "bristle", V(0.33), size=0.013, load=0.4)

# --- the lip catches the light, brightest at the left, lost to the right ---
s.stroke([(-0.02, 0.804), (0.20, 0.795)], "flat", V(0.82), size=0.009, pressure="lift_off")
s.stroke([(0.235, 0.792), (0.44, 0.784)], "flat", V(0.78), size=0.008, pressure="taper")
s.stroke([(0.475, 0.783), (0.60, 0.778)], "flat", V(0.62), size=0.007, pressure="lift_off")
s.stroke([(0.66, 0.776), (0.78, 0.771)], "flat", V(0.40), size=0.006, pressure="taper")

# --- the cast shadow, stated again now the sill is right ---
cast = polygon([(0.582, 0.702), (0.755, 0.714), (0.900, 0.758), (0.862, 0.788),
                (0.700, 0.770), (0.586, 0.740)])
s.block_in(cast, "flat", V(0.245), density=0.9, size=0.030, direction=9, load=0.95)
s.block_in(polygon([(0.585, 0.706), (0.690, 0.716), (0.686, 0.748), (0.588, 0.738)]),
           "flat", V(0.195), density=1.0, size=0.020, direction=7, load=1.0)
print("strokes:", s.stroke_count)
