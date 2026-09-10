import random, math
p = s.palette; rnd = random.Random(202)
def leaf(x, y, w, col, tilt, ln=0.55, brush="round_hard", pr="even", ld=1.0):
    dx = math.cos(math.radians(tilt))*w*ln/2; dy = math.sin(math.radians(tilt))*w*ln/2
    s.stroke([(x-dx,y-dy),(x+dx,y+dy)], brush, col, size=w, pressure=pr, load=ld)

s.dry()
# --- the pale discs were never gaps: bury them ---
for x, y, w, t in [(0.4255,0.4720,0.048,-28),(0.4430,0.4180,0.040,44),
                   (0.4680,0.5620,0.036,-52),(0.4400,0.5180,0.034,18)]:
    leaf(x, y, w, "lf_dk", t, ln=0.6)
# --- a gap is a sliver of background glimpsed, not a disc: broken strokes at the edge ---
for a, b, w, col, ld in [((0.4030,0.4380),(0.4560,0.4560),0.020,"glow_c",0.55),
                         ((0.4180,0.5020),(0.4720,0.4920),0.017,"glow_c",0.5),
                         ((0.4090,0.5480),(0.4640,0.5380),0.015,"haze",0.5),
                         ((0.4560,0.3980),(0.5020,0.3820),0.016,"glow_b",0.5),
                         ((0.4420,0.5820),(0.4900,0.5760),0.014,"glow_c",0.45),
                         ((0.5240,0.3200),(0.5720,0.3120),0.017,"wall",0.55),
                         ((0.6260,0.3020),(0.6740,0.3140),0.019,"wall",0.55),
                         ((0.7660,0.3720),(0.8080,0.4060),0.020,"wall",0.55),
                         ((0.8060,0.4880),(0.8320,0.5320),0.018,"wall",0.5),
                         ((0.7180,0.5720),(0.7640,0.5620),0.016,"wall",0.5)]:
    s.stroke([a,b], "bristle", col, size=w, load=ld, pressure="taper")
# a couple of leaves reaching out into the light
leaf(0.4180,0.4620,0.026,"lf_dk", 34, ln=0.8)
leaf(0.4300,0.5340,0.022,"lf_dk",-24, ln=0.8)
leaf(0.6140,0.3060,0.028,"lf_sh", 12, ln=0.8)
leaf(0.7860,0.4360,0.026,"lf_sh",-44, ln=0.8)

# --- the drooping: leaves and a stalk hanging over the rim, in front of the pot ---
leaf(0.5040,0.5680,0.042,"lf_sh", 26, ln=0.7)
leaf(0.5380,0.5860,0.034,"lf_dk",-18, ln=0.7)
leaf(0.6480,0.5800,0.032,"lf_sh", 40, ln=0.7)
leaf(0.6860,0.5580,0.040,"lf_mid",-32, ln=0.7)
leaf(0.6660,0.5960,0.026,"lf_dk", 14, ln=0.7)
s.stroke([(0.5100,0.5560),(0.4960,0.5900),(0.4880,0.6280)], "bristle", "lf_dk",
         size=0.005, pressure=[1.0,0.7,0.3], load=0.9)
leaf(0.4880,0.6360,0.030,"lf_dk", 52, ln=0.7)
s.stroke([(0.6760,0.5540),(0.7040,0.5860),(0.7120,0.6180)], "bristle", "lf_sh",
         size=0.005, pressure=[1.0,0.7,0.3], load=0.9)
leaf(0.7140,0.6260,0.026,"lf_sh",-38, ln=0.7)

# --- give some leaves an edge: a lighter rim on the side facing the window ---
for x, y, w, c, t in [(0.6940,0.3880,0.030,"lf_lit",-28),(0.7100,0.4640,0.028,"lf_lit",62),
                      (0.5960,0.3780,0.026,"lf_lit", 48),(0.6560,0.4880,0.026,"lf_lit",24),
                      (0.7380,0.4260,0.024,"lf_hot", 36),(0.6320,0.4260,0.024,"lf_lit",-44)]:
    leaf(x-w*0.16, y-w*0.16, w, c, t, ln=0.5)
print("strokes:", s.stroke_count)
