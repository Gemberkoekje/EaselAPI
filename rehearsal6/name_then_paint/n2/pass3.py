import random
p = s.palette
rnd = random.Random(21)
p["glow_a"] = p.mix("titanium_white", "yellow_ochre", 0.05)
p["glow_b"] = p.mix("titanium_white", "cerulean", 0.09)
p["glow_c"] = p.mix(p.mix("titanium_white","cerulean",0.15), "yellow_ochre", 0.05)
p["case"]   = p.mix(p.mix("ultramarine","burnt_umber",0.6), "burnt_sienna", 0.34)
p["case_lit"]= p.mix(p.mix("titanium_white","yellow_ochre",0.30), "burnt_umber", 0.20)
p["reveal"] = p.mix(p.mix("titanium_white","yellow_ochre",0.28), "burnt_umber", 0.26)
p["reveal_d"]= p.mix(p.mix("titanium_white","yellow_ochre",0.28), "burnt_umber", 0.42)
p["wall_warm"]= p.mix(p.mix("ultramarine","burnt_umber",0.55), "burnt_sienna", 0.42)
for n in ("case","case_lit","reveal","reveal_d","wall_warm"):
    print(n, p.hex(p[n]), round(p.value_of(p[n]),2))

s.dry()
# --- break the horizontal banding in the window with slanting brushwork ---
cols = ["glow_a","glow_b","glow_a","glow_c","glow_b","glow_a","glow_b","glow_c"]
for i in range(16):
    x0 = rnd.uniform(0.02, 0.34); y0 = rnd.uniform(0.10, 0.62)
    ln = rnd.uniform(0.10, 0.26); ang = rnd.uniform(-0.85, -0.30)
    x1 = x0 + ln; y1 = y0 + ln * ang
    s.stroke([(x0,y0),(x1,y1)], "bristle", cols[i % 8],
             size=rnd.uniform(0.045,0.085), load=rnd.uniform(0.45,0.8),
             pressure=rnd.choice(["taper","lift_off","swell"]))
for a, b in [((0.06,0.272),(0.24,0.245)), ((0.28,0.290),(0.46,0.262)),
             ((0.10,0.470),(0.30,0.452)), ((0.33,0.500),(0.49,0.470)),
             ((0.14,0.388),(0.36,0.372))]:
    s.smudge([a,b], size=0.038)

# --- consolidate the wall: crossed flat, then out to the canvas edge ---
s.dry()
right_wall = polygon([(0.484,-0.09), (1.12,-0.09), (1.12,0.80), (0.468,0.74)])
s.block_in(right_wall.inset(0.048), "flat", "wall", density=1.0, size=0.095,
           direction=(58, 142), load=1.0)
s.block_in(polygon([(0.86,-0.09),(1.14,-0.09),(1.14,0.82),(0.86,0.80)]), "flat", "wall",
           density=1.0, size=0.075, direction=(101, 12), load=1.0)
s.block_in(polygon([(-0.10,-0.09),(1.14,-0.09),(1.14,0.10),(-0.10,0.06)]), "flat", "wall",
           density=1.0, size=0.06, direction=(-5, 86), load=1.0)
# light spilling onto the wall beside the window, and the sill's bounce low right
s.block_in(blob((0.565,0.300), 0.075, 0.24, wobble=0.4, seed=11), "bristle", "wall_hi",
           density=0.5, size=0.05, direction=(77,150), load=0.6)
s.block_in(blob((0.80,0.640), 0.26, 0.075, wobble=0.5, seed=13), "bristle", "wall_warm",
           density=0.55, size=0.055, direction=(9,88), load=0.6)

# --- the open casement on the left: nearer than the light, so it goes on top ---
case = polygon([(-0.07,0.030), (0.118,0.070), (0.107,0.706), (-0.07,0.694)])
s.block_in(case, "flat", "case", density=1.0, size=0.048, direction=88, load=1.0)
s.block_in(case.inset(0.012), "flat", "case", density=0.9, size=0.040, direction=79, load=1.0)
# its inner face catching the light - broken, not one line
s.stroke([(0.110,0.086),(0.106,0.255)], "flat", "case_lit", size=0.013, pressure="lift_off")
s.stroke([(0.107,0.300),(0.104,0.470)], "flat", "case_lit", size=0.011, pressure="taper")
s.stroke([(0.105,0.520),(0.102,0.660)], "flat", "reveal_d", size=0.010, pressure="press_in")

# --- the right reveal: the window has a thickness ---
rev = polygon([(0.488,0.108),(0.507,0.112),(0.519,0.652),(0.485,0.650)])
s.block_in(rev, "flat", "reveal", density=1.0, size=0.020, direction=89, load=1.0)
s.block_in(polygon([(0.489,0.420),(0.512,0.424),(0.519,0.652),(0.486,0.650)]), "flat",
           "reveal_d", density=1.0, size=0.017, direction=87, load=1.0)
print("strokes:", s.stroke_count)
