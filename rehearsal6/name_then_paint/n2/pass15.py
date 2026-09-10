import random, math
p = s.palette; rnd = random.Random(505)
p["bl_dk"]  = p.mix("alizarin", "burnt_umber", 0.38)
p["bl_mid"] = p.mix("cadmium_red", "alizarin", 0.40)
p["bl"]     = "cadmium_red"
p["bl_lit"] = p.tint(p.mix("cadmium_red", "cadmium_yellow", 0.16), 0.20)
p["bl_hot"] = p.tint(p.mix("cadmium_red", "cadmium_yellow", 0.28), 0.42)
p["stalk"]  = p.mix(p["lf_sh"], "burnt_sienna", 0.30)
for n in ("bl_dk","bl_mid","bl","bl_lit","bl_hot","stalk"):
    print(n, p.hex(p[n]), round(p.value_of(p[n]),2))
def mark(x, y, w, col, tilt, ln=0.55, brush="round_hard"):
    dx = math.cos(math.radians(tilt))*w*ln/2; dy = math.sin(math.radians(tilt))*w*ln/2
    s.stroke([(x-dx,y-dy),(x+dx,y+dy)], brush, col, size=w, pressure="even", load=1.0)

s.dry()
# --- the stalks stand above the leaves: they go on first ---
for a, b, w in [((0.6800,0.4560),(0.7020,0.3820),0.0055),
                ((0.7280,0.4980),(0.7460,0.4560),0.0050),
                ((0.6060,0.4020),(0.6130,0.3400),0.0050),
                ((0.5620,0.4560),(0.5580,0.4180),0.0042)]:
    s.stroke([a, ((a[0]+b[0])/2 - 0.004, (a[1]+b[1])/2), b], "bristle", "stalk",
             size=w, pressure=[1.0,0.85,0.5], load=0.9)

def umbel(cx, cy, r, n, cols, lits, seed, squash=0.86):
    g = random.Random(seed)
    s.block_in(blob((cx,cy), r*1.02, r*squash*1.02, wobble=0.45, seed=seed), "flat",
               "bl_dk", density=1.0, size=r*0.42, direction="axis", load=1.0)
    pts = []
    for i in range(n):
        a = g.uniform(0, 2*math.pi); rr = r * math.sqrt(g.uniform(0.02, 0.86))
        pts.append((cx + rr*math.cos(a), cy + rr*squash*math.sin(a)))
    for i, (x, y) in enumerate(pts):
        mark(x, y, r*g.uniform(0.36, 0.52), cols[i % len(cols)],
             g.uniform(0, 180), ln=g.uniform(0.4, 0.9))
    for (dx, dy, w, c) in lits:
        mark(cx+dx*r, cy+dy*r, r*w, c, g.uniform(0,180), ln=0.6)

umbel(0.7010, 0.3540, 0.0420, 9, ["bl","bl_mid","bl","bl_lit","bl_mid"],
      [(-0.32,-0.34,0.40,"bl_lit"), (0.10,-0.46,0.34,"bl_lit"),
       (-0.50,0.06,0.30,"bl_mid"), (-0.26,-0.30,0.20,"bl_hot")], 11)
umbel(0.7470, 0.4400, 0.0325, 7, ["bl_mid","bl","bl_mid","bl"],
      [(-0.36,-0.36,0.36,"bl_lit"), (0.22,-0.20,0.26,"bl_lit")], 13)
umbel(0.6130, 0.3320, 0.0305, 6, ["bl","bl_mid","bl_lit","bl_mid"],
      [(-0.40,-0.28,0.34,"bl_lit"), (0.16,0.26,0.24,"bl_dk")], 17)
umbel(0.5580, 0.4050, 0.0215, 5, ["bl_mid","bl_dk","bl_mid"],
      [(-0.34,-0.30,0.30,"bl")], 19)
umbel(0.5150, 0.5020, 0.0185, 4, ["bl_dk","bl_mid","bl_dk"],
      [(-0.30,-0.26,0.28,"bl_mid")], 23)

# petals that have already dropped, down on the lit sill
mark(0.4180, 0.7420, 0.0125, "bl_mid", 28, ln=0.9)
mark(0.3660, 0.7660, 0.0105, "bl", -52, ln=0.9)
mark(0.4880, 0.7080, 0.0090, "bl_dk", 14, ln=0.9)
print("strokes:", s.stroke_count)
