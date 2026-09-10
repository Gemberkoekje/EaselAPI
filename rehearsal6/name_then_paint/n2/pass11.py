import random
p = s.palette; dk = p["dk"]; rnd = random.Random(41)
pale = p.mix("titanium_white", "yellow_ochre", 0.28)
def SV(target, b="burnt_umber"):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(pale, b, m)) > target: lo=m
        else: hi=m
    return p.mix(pale, b, (lo+hi)/2)

s.dry()
# --- the mullion's shadow: narrower, graded, and softened at both edges ---
s.block_in(polygon([(0.2670,0.646),(0.2830,0.647),(0.3960,0.800),(0.3770,0.801)]), "flat",
           SV(0.700), density=1.0, size=0.014, direction="axis", load=1.0)   # sill back
s.block_in(polygon([(0.2990,0.649),(0.3110,0.650),(0.4310,0.799),(0.4180,0.800)]), "flat",
           SV(0.655), density=1.0, size=0.013, direction="axis", load=1.0)
for y0, y1, v in [(0.648,0.700,0.520),(0.698,0.750,0.460),(0.748,0.800,0.400)]:
    t0 = (y0-0.648)/0.152; t1 = (y1-0.648)/0.152
    xa = lambda t: 0.2790 + 0.098*t
    sh = polygon([(xa(t0),y0),(xa(t0)+0.023,y0),(xa(t1)+0.023,y1),(xa(t1),y1)])
    s.block_in(sh, "flat", SV(v), density=1.0, size=0.012, direction="axis", load=1.0)
s.smudge([(0.2900,0.664),(0.3300,0.716)], size=0.026)
s.smudge([(0.3450,0.736),(0.3820,0.784)], size=0.024)
s.smudge([(0.3200,0.688),(0.3560,0.740)], size=0.022)

# --- the plant: the whole drooping mass, dark, in one statement ---
p["lf_dk"]  = p.mix(p.mix("viridian","burnt_umber",0.50), "ultramarine", 0.25)
p["lf_sh"]  = p.mix("viridian","burnt_umber",0.34)
p["lf_mid"] = p.mix("viridian","yellow_ochre",0.42)
p["lf_lit"] = p.tint(p.mix("viridian","cadmium_yellow",0.50), 0.22)
p["lf_hot"] = p.tint(p.mix("viridian","cadmium_yellow",0.62), 0.35)
for n in ("lf_dk","lf_sh","lf_mid","lf_lit","lf_hot"):
    print(n, p.hex(p[n]), round(p.value_of(p[n]),2))

clumps = [(0.585,0.400,0.076,0.062,3,"lf_sh",  38),
          (0.672,0.442,0.081,0.067,5,"lf_sh", 118),
          (0.520,0.470,0.068,0.058,7,"lf_dk",  67),
          (0.735,0.506,0.058,0.050,11,"lf_sh",152),
          (0.462,0.548,0.056,0.045,13,"lf_dk", 22),
          (0.626,0.512,0.073,0.050,17,"lf_sh", 95),
          (0.612,0.348,0.049,0.041,19,"lf_sh",130),
          (0.702,0.372,0.051,0.043,23,"lf_dk", 48)]
for cx, cy, rx, ry, sd, col, ang in clumps:
    sh = blob((cx,cy), rx, ry, wobble=0.48, seed=sd)
    s.block_in(sh, "bristle", col, density=0.8, size=0.029, direction=(ang, ang+96), load=0.9)
# stalks reaching up out of the pot, drawn through the mass
for a, b, w in [((0.578,0.552),(0.600,0.376),0.006),((0.566,0.554),(0.538,0.436),0.005),
                ((0.596,0.550),(0.664,0.432),0.006),((0.604,0.554),(0.712,0.498),0.005),
                ((0.570,0.558),(0.486,0.524),0.005),((0.590,0.551),(0.744,0.424),0.004),
                ((0.582,0.553),(0.470,0.556),0.005)]:
    mid = ((a[0]+b[0])/2 + rnd.uniform(0.004,0.016), (a[1]+b[1])/2 + rnd.uniform(0.010,0.026))
    s.stroke([a, mid, b], "bristle", "lf_dk", size=w, pressure=[1.0,0.8,0.35], load=0.9)
print("strokes:", s.stroke_count)
