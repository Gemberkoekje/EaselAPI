"""own2, pass 3 - the seed disc over the petals' inner ends, ridges down the
petals so they stop being soft lozenges, and repairs to two bad marks."""
import math
import random

p = s.palette
p["disc_dk"] = p.mix(p.mix("burnt_umber", "ultramarine", 0.28), "viridian", 0.15)
p["disc_md"] = p.mix("burnt_umber", "burnt_sienna", 0.45)
p["disc_lt"] = p.mix(p.mix("yellow_ochre", "burnt_sienna", 0.4),
                     "titanium_white", 0.22)
p["floret"] = p.mix(p.mix("cadmium_yellow", "viridian", 0.22),
                    "titanium_white", 0.12)
for n in ("disc_dk", "disc_md", "disc_lt", "floret"):
    print(f"{n:8s} {p.hex(p[n])} v={p.value_of(p[n]):.2f}")

CX, CY = 0.470, 0.450
rng = random.Random(17)
s.dry()

# repairs first: the scratchy dark combs, and the leaf veins that overshot
for a, b, col, sz in [((0.310, 0.290), (0.365, 0.330), "pet_lit", 0.032),
                      ((0.400, 0.180), (0.425, 0.255), "pet_lit", 0.030),
                      ((0.250, 0.320), (0.330, 0.370), "pet_lit", 0.028),
                      ((0.600, 0.520), (0.660, 0.545), "pet_sh", 0.026)]:
    s.stroke([a, b], "flat", col, size=sz, pressure="even", load=1.0,
             note="cover the scratchy comb")
for a, b in [((0.010, 0.075), (0.135, 0.098)), ((0.760, 0.585), (0.900, 0.640)),
             ((0.000, 0.795), (0.060, 0.775)), ((0.800, 0.845), (0.905, 0.880))]:
    s.stroke([a, b], "flat", "bg_dk", size=0.020, pressure="even", load=1.0,
             note="kill the overshooting vein")
print("repairs:", s.stroke_count)

# the disc
disc = ellipse(Region(CX - 0.158, CY - 0.152, CX + 0.158, CY + 0.152))
s.block_in(disc.inset(0.026), "flat", "disc_dk", direction=(28, 118),
           density=1.0, size=0.050, load=1.0)
print("disc:", s.stroke_count)

# the lit side of the disc, upper left, worked wet into the dark
s.block_in(ellipse(Region(CX - 0.150, CY - 0.145, CX + 0.010, CY + 0.010)
                   ).inset(0.020), "flat", p.mix(p["disc_dk"], p["disc_md"], 0.6),
           direction=(38,), density=0.9, size=0.038, load=1.0)

# seed rows: short arcs on the golden angle, two values, never the same length
GOLD = math.pi * (3 - 5 ** 0.5)
for i in range(22):
    r = 0.030 + 0.115 * (i / 21) ** 0.55
    a = i * GOLD * 3.2 + rng.uniform(-0.12, 0.12)
    span = rng.uniform(0.30, 0.72)
    pts = [(CX + r * math.cos(a + t * span), CY + r * math.sin(a + t * span))
           for t in (0.0, 0.5, 1.0)]
    lit = math.cos(a) * -0.707 + math.sin(a) * -0.707
    col = p.mix(p["disc_dk"], p["disc_lt"], 0.20 + 0.42 * (0.5 + 0.5 * lit))
    s.stroke(pts, "bristle", col, size=rng.uniform(0.010, 0.020),
             opacity=rng.uniform(0.45, 0.85), load=0.9, note="seed row")
print("seeds:", s.stroke_count)

# the ring of florets round the disc's rim
for i in range(16):
    a = 2 * math.pi * i / 16 + rng.uniform(-0.10, 0.10)
    r0, r1 = 0.132, 0.132 + rng.uniform(0.018, 0.036)
    s.stroke([(CX + r0 * math.cos(a), CY + r0 * math.sin(a)),
              (CX + r1 * math.cos(a), CY + r1 * math.sin(a))], "liner",
             "floret", size=rng.uniform(0.005, 0.009),
             pressure=[0.9, 0.15], note="floret")
print("florets:", s.stroke_count)

# a ridge down ten petals so they read as folded, not inflated
rng2 = random.Random(3)
for i in range(11):
    a = 2 * math.pi * i / 11 + rng2.uniform(-0.15, 0.15)
    r0, r1 = 0.175, rng2.uniform(0.255, 0.345)
    lit = math.cos(a) * -0.707 + math.sin(a) * -0.707
    col = "pet_lit" if lit > 0.15 else ("pet_mid" if lit > -0.4 else "pet_sh")
    s.stroke([(CX + r0 * math.cos(a), CY + r0 * math.sin(a)),
              (CX + r1 * math.cos(a), CY + r1 * math.sin(a))], "flat", col,
             size=rng2.uniform(0.008, 0.016), pressure=[1.0, 0.25], load=1.0,
             note="petal ridge")
print("strokes:", s.stroke_count)
print(s.look())
