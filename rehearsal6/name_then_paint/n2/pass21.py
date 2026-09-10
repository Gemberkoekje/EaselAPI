import random, math
p = s.palette; rnd = random.Random(707); dk = p["dk"]
p["glow_w"] = p.mix(p.mix("titanium_white","cerulean",0.11), "yellow_ochre", 0.13)
p["glow_p"] = p.mix("titanium_white", "yellow_ochre", 0.09)
p["glow_g"] = p.mix(p.mix("titanium_white","cerulean",0.16), "yellow_ochre", 0.09)
for n in ("glow_w","glow_p","glow_g"): print(n, p.hex(p[n]), round(p.value_of(p[n]),2))
def leaf(x, y, w, col, tilt, ln=0.55, brush="round_hard"):
    dx = math.cos(math.radians(tilt))*w*ln/2; dy = math.sin(math.radians(tilt))*w*ln/2
    s.stroke([(x-dx,y-dy),(x+dx,y+dy)], brush, col, size=w, pressure="even", load=1.0)

s.dry()
# --- the window is banded and too blue: break it with slanting scumbles ---
cols = ["glow_w","glow_p","glow_g","glow_w","glow_p","glow_g","glow_w"]
for i in range(18):
    x0 = rnd.uniform(0.055, 0.330); y0 = rnd.uniform(0.150, 0.615)
    ln = rnd.uniform(0.09, 0.21); ang = rnd.uniform(-0.80, -0.22)
    s.stroke([(x0,y0),(x0+ln, y0+ln*ang)], "bristle", cols[i % 7],
             size=rnd.uniform(0.035,0.070), load=rnd.uniform(0.35,0.60),
             pressure=rnd.choice(["taper","lift_off","swell"]))
for i in range(7):
    x0 = rnd.uniform(0.310, 0.430); y0 = rnd.uniform(0.180, 0.600)
    ln = rnd.uniform(0.05, 0.12); ang = rnd.uniform(-0.9, -0.3)
    s.stroke([(x0,y0),(x0+ln, y0+ln*ang)], "bristle", cols[(i*3) % 7],
             size=rnd.uniform(0.030,0.055), load=rnd.uniform(0.35,0.55), pressure="taper")
s.stroke([(0.070,0.470),(0.255,0.452)], "round_soft", "glow_w", size=0.034,
         load=0.5, opacity=0.45, pressure="even")
s.stroke([(0.318,0.505),(0.465,0.488)], "round_soft", "glow_g", size=0.030,
         load=0.5, opacity=0.45, pressure="even")

# --- a breath of warmth in the far corner so the dark is not one flat field ---
s.block_in(blob((0.870,0.330), 0.18, 0.16, wobble=0.5, seed=61), "bristle",
           p.mix(dk, "burnt_sienna", 0.34), density=0.28, size=0.06,
           direction=(48,132), load=0.35)
s.block_in(blob((0.590,0.150), 0.14, 0.13, wobble=0.5, seed=67), "bristle",
           p.mix(dk, "titanium_white", 0.10), density=0.24, size=0.05,
           direction=(-24,64), load=0.30)

# --- the backlit edge of the plant: solid leaf shapes, not bristle speckle ---
for x, y, w, c, t in [(0.4260,0.4180,0.032,"lf_dk2",-38),(0.4020,0.4600,0.028,"lf_dk2",30),
                      (0.4400,0.3900,0.026,"lf_dk",  60),(0.4120,0.5020,0.026,"lf_dk2",-58),
                      (0.4560,0.3640,0.024,"lf_dk",  14),(0.3960,0.5320,0.022,"lf_dk2",44),
                      (0.4680,0.4460,0.030,"lf_dk", -22)]:
    leaf(x, y, w, c, t, ln=0.8)
leaf(0.4340,0.4420,0.016,"lf_25", 26, ln=0.7)
leaf(0.4160,0.4900,0.014,"lf_mid",-34, ln=0.7)

# --- lose three edges; not every boundary should be crisp ---
s.smudge([(0.6560,0.2980),(0.7080,0.3080)], size=0.030)
s.smudge([(0.6690,0.6480),(0.6900,0.6520)], size=0.026)
s.smudge([(0.9320,0.6640),(0.9880,0.6700)], size=0.030)
print("strokes:", s.stroke_count)
