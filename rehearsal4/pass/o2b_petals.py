"""own2, pass 2 - the corona. One stroke per petal, tapered to a point by the
pressure profile, each one aimed out from the centre. Back row first, then the
front row over it - the same back-to-front rule, but in radius instead of depth."""
import math
import random

p = s.palette
p["pet_lit"] = p.mix("cadmium_yellow", "titanium_white", 0.34)
p["pet_mid"] = p.mix("cadmium_yellow", "yellow_ochre", 0.30)
p["pet_sh"] = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.35),
                    "burnt_umber", 0.22)
p["pet_dk"] = p.mix("burnt_sienna", "burnt_umber", 0.55)
for n in ("pet_dk", "pet_sh", "pet_mid", "pet_lit"):
    print(f"{n:8s} {p.hex(p[n])} v={p.value_of(p[n]):.2f}")

CX, CY = 0.470, 0.450
LX, LY = -0.707, -0.707          # the light comes from the upper left
rng = random.Random(9)


def petal(a, r0, r1, col, size, brush="round_hard", press=None):
    dx, dy = math.cos(a), math.sin(a)
    bend = rng.uniform(-0.035, 0.035)
    px, py = -dy * bend, dx * bend
    pts = [(CX + dx * r0, CY + dy * r0),
           (CX + dx * (r0 + r1) * 0.5 + px, CY + dy * (r0 + r1) * 0.5 + py),
           (CX + dx * r1, CY + dy * r1)]
    s.stroke(pts, brush, col, size=size,
             pressure=press or [0.7, 1.0, 0.12], load=1.0, note="petal")


# back row: shorter, duller, slightly off the front row's angles
n_back = 15
for i in range(n_back):
    a = 2 * math.pi * i / n_back + rng.uniform(-0.09, 0.09)
    lit = math.cos(a) * LX + math.sin(a) * LY
    col = p.mix(p["pet_dk"], p["pet_sh"], 0.35 + 0.5 * (0.5 + 0.5 * lit))
    petal(a, 0.130, rng.uniform(0.245, 0.315), col, rng.uniform(0.050, 0.072))
print("back row:", s.stroke_count)

# front row
n_front = 17
for i in range(n_front):
    a = 2 * math.pi * (i + 0.5) / n_front + rng.uniform(-0.07, 0.07)
    lit = math.cos(a) * LX + math.sin(a) * LY
    t = 0.5 + 0.5 * lit
    col = p.mix(p["pet_sh"], p["pet_lit"], 0.30 + 0.62 * t)
    petal(a, 0.140, rng.uniform(0.285, 0.395), col, rng.uniform(0.042, 0.068))
print("front row:", s.stroke_count)

# a few darks driven back between petals, so the corona has holes in it
for i in range(7):
    a = 2 * math.pi * rng.random()
    petal(a, 0.165, rng.uniform(0.240, 0.310), p["pet_dk"],
          rng.uniform(0.016, 0.028), brush="bristle", press=[0.9, 0.7, 0.1])
print("strokes:", s.stroke_count)
print(s.look())
