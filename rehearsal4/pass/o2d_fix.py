"""own2, pass 4 - the flat-brush ridges read as sticky-note bars: a flat tip is
held square to its travel and its width does not follow pressure, so a short
one is a rectangle. Repaint the corona's inner half with a round tip, which
declares no axis and does taper in width."""
import math
import random

p = s.palette
CX, CY = 0.470, 0.450
LX, LY = -0.707, -0.707
rng = random.Random(31)
s.dry()

# the leaf veins, out properly this time - along their whole path
for pts in ([(0.02, 0.86), (0.20, 0.74), (0.36, 0.70)],
            [(0.98, 0.70), (0.82, 0.62), (0.68, 0.62)],
            [(0.14, 0.10), (0.26, 0.22), (0.34, 0.30)],
            [(0.92, 0.96), (0.74, 0.88), (0.62, 0.82)]):
    s.stroke(pts, "round_hard", p.mix(p["leaf"], p["bg_dk"], 0.35), size=0.016,
             pressure="even", load=1.0, note="vein out")
print("veins:", s.stroke_count)

# repaint the corona's inner half, one round stroke per ray
for i in range(19):
    a = 2 * math.pi * i / 19 + rng.uniform(-0.10, 0.10)
    lit = math.cos(a) * LX + math.sin(a) * LY
    t = 0.5 + 0.5 * lit
    col = p.mix(p["pet_sh"], p["pet_lit"], 0.26 + 0.66 * t)
    r0, r1 = 0.150, rng.uniform(0.268, 0.330)
    bend = rng.uniform(-0.022, 0.022)
    dx, dy = math.cos(a), math.sin(a)
    s.stroke([(CX + dx * r0, CY + dy * r0),
              (CX + dx * (r0 + r1) * 0.5 - dy * bend,
               CY + dy * (r0 + r1) * 0.5 + dx * bend),
              (CX + dx * r1, CY + dy * r1)], "round_hard", col,
             size=rng.uniform(0.030, 0.050), pressure=[0.75, 1.0, 0.10],
             load=1.0, note="petal, round tip")
print("corona:", s.stroke_count)

# cut dark gaps back in so it is a corona and not a disc
for i in range(8):
    a = 2 * math.pi * (i + 0.5) / 8 + rng.uniform(-0.14, 0.14)
    dx, dy = math.cos(a), math.sin(a)
    r0, r1 = 0.162, rng.uniform(0.230, 0.300)
    s.stroke([(CX + dx * r0, CY + dy * r0), (CX + dx * r1, CY + dy * r1)],
             "round_hard", p.mix(p["pet_dk"], p["bg_dk"], 0.4),
             size=rng.uniform(0.012, 0.022), pressure=[0.9, 0.12], load=1.0,
             note="gap between petals")
print("gaps:", s.stroke_count)

# highlights: the lit tips only, and few of them
for a_deg, r, sz in [(198, 0.335, 0.016), (222, 0.318, 0.014), (246, 0.300, 0.012),
                     (174, 0.312, 0.013), (270, 0.288, 0.011)]:
    a = math.radians(a_deg)
    dx, dy = math.cos(a), math.sin(a)
    s.stroke([(CX + dx * (r - 0.075), CY + dy * (r - 0.075)),
              (CX + dx * r, CY + dy * r)], "round_hard",
             p.mix("cadmium_yellow", "titanium_white", 0.55), size=sz,
             pressure=[1.0, 0.10], load=1.0, note="lit tip")
s.dab(CX - 0.075, CY - 0.088, "round_hard",
      p.mix(p["disc_lt"], "titanium_white", 0.35), size=0.020, press=3)

# two edges lost where the shadowed petals meet the ground
for a, b in [((0.640, 0.560), (0.690, 0.600)), ((0.520, 0.680), (0.560, 0.720))]:
    s.smudge([a, b], size=0.038)
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
