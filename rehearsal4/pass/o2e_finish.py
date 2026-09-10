"""own2, pass 5 - finishing. The eight 'gaps' landed two values below the
petals and read as black slugs lying on top; replay the same RNG to find them
and paint them out with the petal's own colour, then re-cut them much softer."""
import math
import random

p = s.palette
CX, CY = 0.470, 0.450
LX, LY = -0.707, -0.707
s.dry()

# replay o2d's RNG to recover exactly where the slugs are
rng = random.Random(31)
for _ in range(19):
    rng.uniform(-0.10, 0.10); rng.uniform(0.268, 0.330)
    rng.uniform(-0.022, 0.022); rng.uniform(0.030, 0.050)
gaps = []
for i in range(8):
    a = 2 * math.pi * (i + 0.5) / 8 + rng.uniform(-0.14, 0.14)
    r1 = rng.uniform(0.230, 0.300)
    rng.uniform(0.012, 0.022)
    gaps.append((a, r1))

for a, r1 in gaps:
    dx, dy = math.cos(a), math.sin(a)
    lit = dx * LX + dy * LY
    col = p.mix(p["pet_sh"], p["pet_lit"], 0.26 + 0.62 * (0.5 + 0.5 * lit))
    s.stroke([(CX + dx * 0.150, CY + dy * 0.150),
              (CX + dx * (r1 + 0.012), CY + dy * (r1 + 0.012))], "round_hard",
             col, size=0.046, pressure=[0.85, 1.0, 0.30], load=1.0,
             note="paint the slug out")
print("slugs out:", s.stroke_count)

# the same separations, but a shadow instead of a hole - two values, not four
for a, r1 in gaps[::2]:
    dx, dy = math.cos(a), math.sin(a)
    lit = dx * LX + dy * LY
    col = p.mix(p["pet_sh"], p["pet_dk"], 0.35 - 0.2 * lit)
    s.stroke([(CX + dx * 0.168, CY + dy * 0.168),
              (CX + dx * (r1 - 0.03), CY + dy * (r1 - 0.03))], "round_hard",
             col, size=0.016, opacity=0.55, pressure=[0.8, 0.15], load=1.0,
             note="separation, softer")
print("gaps:", s.stroke_count)

# the pale ladder residue still showing on the upper-left petals
for a_deg, r0, r1, sz in [(207, 0.150, 0.315, 0.044), (196, 0.150, 0.300, 0.040),
                          (218, 0.150, 0.290, 0.038), (185, 0.150, 0.305, 0.036)]:
    a = math.radians(a_deg)
    dx, dy = math.cos(a), math.sin(a)
    s.stroke([(CX + dx * r0, CY + dy * r0),
              (CX + dx * (r0 + r1) * 0.5 - dy * 0.014,
               CY + dy * (r0 + r1) * 0.5 + dx * 0.014),
              (CX + dx * r1, CY + dy * r1)], "round_hard",
             p.mix(p["pet_mid"], p["pet_lit"], 0.6), size=sz,
             pressure=[0.8, 1.0, 0.12], load=1.0, note="cover the ladder")
print("ladders:", s.stroke_count)

# the leaves are pasted-on slabs: cut their edges and put some form in them
p["leaf_dk"] = p.mix(p["leaf"], "burnt_umber", 0.45)
for pts, sz in ([[(0.03, 0.905), (0.19, 0.792), (0.35, 0.752)], 0.030],
                [[(1.00, 0.742), (0.84, 0.664), (0.70, 0.660)], 0.026],
                [[(0.10, 0.075), (0.235, 0.192), (0.325, 0.276)], 0.024],
                [[(0.955, 0.995), (0.762, 0.912), (0.630, 0.848)], 0.026]):
    s.stroke(pts, "bristle", "bg_dk", size=sz, opacity=0.8, load=0.9,
             note="cut the leaf edge")
for pts, sz in ([[(0.06, 0.820), (0.20, 0.722), (0.34, 0.690)], 0.020],
                [[(0.96, 0.678), (0.83, 0.606), (0.70, 0.606)], 0.017]):
    s.stroke(pts, "bristle", "leaf_dk", size=sz, opacity=0.6, load=0.9,
             note="shadow in the leaf")
print("leaves:", s.stroke_count)

# last three marks
s.dab(CX - 0.055, CY - 0.070, "round_hard",
      p.mix(p["disc_lt"], "titanium_white", 0.45), size=0.014, press=3)
s.stroke([(CX - 0.170, CY - 0.210), (CX - 0.215, CY - 0.290)], "round_hard",
         p.mix("cadmium_yellow", "titanium_white", 0.62), size=0.013,
         pressure=[1.0, 0.10], load=1.0, note="the brightest tip")
s.smudge([(0.300, 0.640), (0.345, 0.685)], size=0.036)
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
print(s.export("own2_final.png"))
print(s.timelapse_gif("own2_timelapse.gif"))
