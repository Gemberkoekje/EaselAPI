import random, math
p = s.palette; rnd = random.Random(303)
def leaf(x, y, w, col, tilt, ln=0.55, brush="round_hard", pr="even", ld=1.0):
    dx = math.cos(math.radians(tilt))*w*ln/2; dy = math.sin(math.radians(tilt))*w*ln/2
    s.stroke([(x-dx,y-dy),(x+dx,y+dy)], brush, col, size=w, pressure=pr, load=ld)
p["lf_dk2"] = p.mix(p["lf_dk"], p["dk"], 0.35)
p["lf_25"]  = p.mix(p["lf_sh"], p["lf_mid"], 0.45)
p["lf_38"]  = p.mix(p["lf_mid"], p["lf_lit"], 0.35)
for n in ("lf_dk2","lf_25","lf_38"): print(n, p.hex(p[n]), round(p.value_of(p[n]),2))

s.dry()
# --- bury the scattered brights: the light is not everywhere at once ---
for x, y, w, t, c in [(0.5960,0.3780,0.034,48,"lf_sh"),(0.6320,0.4260,0.032,-44,"lf_sh"),
                      (0.5340,0.4640,0.038,-36,"lf_dk"),(0.4930,0.5220,0.034,24,"lf_dk"),
                      (0.6560,0.4880,0.032,24,"lf_25"),(0.5560,0.4880,0.030,-62,"lf_dk"),
                      (0.6400,0.4340,0.036,-40,"lf_25"),(0.5480,0.4180,0.036,-56,"lf_dk")]:
    leaf(x, y, w, c, t, ln=0.6)
# --- the left third is backlit: push it down to a silhouette ---
s.block_in(blob((0.4780,0.4880), 0.085, 0.098, wobble=0.5, seed=31), "bristle", "lf_dk2",
           density=0.55, size=0.026, direction=(34,126), load=0.7)
s.block_in(blob((0.5320,0.4400), 0.062, 0.070, wobble=0.5, seed=37), "bristle", "lf_dk",
           density=0.45, size=0.024, direction=(-22,72), load=0.6)
# --- the underside of the mass falls away into the pot's own shadow ---
s.block_in(blob((0.6300,0.5320), 0.140, 0.048, wobble=0.5, seed=43), "bristle", "lf_dk",
           density=0.5, size=0.024, direction=(12,100), load=0.65)
# --- trim the right edge back: the plant leans toward the window, not away ---
for a, b, w in [((0.8180,0.4200),(0.8340,0.4880),0.030),((0.7980,0.5220),(0.8180,0.4620),0.026),
                ((0.7820,0.5560),(0.8060,0.5180),0.022)]:
    s.stroke([a,b], "bristle", "wall", size=w, load=0.85, pressure="even")
leaf(0.7140,0.6260,0.032,"wall", 40, ln=0.6)

# --- the light rakes across the tops, upper right, and only there ---
for x, y, w, c, t in [(0.6980,0.3760,0.038,"lf_38",-26),(0.7280,0.4120,0.034,"lf_lit", 30),
                      (0.6720,0.4020,0.030,"lf_mid", 56),(0.7480,0.4560,0.030,"lf_38",-18),
                      (0.7080,0.4720,0.028,"lf_mid", 44),(0.6420,0.3660,0.028,"lf_25",-52),
                      (0.7620,0.4860,0.024,"lf_25", 20)]:
    leaf(x, y, w, c, t, ln=0.55)
leaf(0.7300,0.4020,0.020,"lf_hot", 34, ln=0.5)
leaf(0.6900,0.3600,0.018,"lf_lit",-40, ln=0.5)
# two backlit leaves with the sun through them, on the window side only
leaf(0.4460,0.4560,0.020,"lf_mid", 30, ln=0.6)
leaf(0.4700,0.5300,0.017,"lf_25", -22, ln=0.6)
print("strokes:", s.stroke_count)
