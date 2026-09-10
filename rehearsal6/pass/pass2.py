R = "/home/user/refs/Level1.jpg"
p = s.palette
p["wood_lo"] = p.mix(p["wood_dk"], p["wood_mid"], 0.35)
print("wood_lo", p.hex(p["wood_lo"]), round(p.value_of(p["wood_lo"]),3))

# 1. knock the swathe back and cross the ribbing  (rehearsal E)
for q in ([(0.545,0.88),(0.79,0.735),(1.0,0.62)],
          [(0.50,0.655),(0.755,0.515),(1.0,0.415)],
          [(0.545,0.40),(0.80,0.26),(1.0,0.175)],
          [(0.60,0.135),(0.84,0.045)]):
    s.stroke(q, "flat", "wood_mid", size=0.15, load=1.0, opacity=0.20, pressure="even")

# 2. the far corner of the table falls away into shade
s.stroke([(0.72,1.02),(0.90,0.94),(1.02,0.86)], "flat", "wood_lo", size=0.17,
         load=1.0, opacity=0.55, pressure="even")
s.stroke([(0.80,0.98),(1.02,0.80)], "flat", "wood_lo", size=0.14, load=1.0,
         opacity=0.45, pressure="even")
s.stroke([(0.93,0.70),(1.02,0.60)], "bristle", "wood_lo", size=0.11, load=0.8,
         opacity=0.35, pressure="taper")

# 3. lose the swathe's straight left boundary
s.smudge([(0.60,0.10),(0.615,0.22)], size=0.042)
s.smudge([(0.615,0.44),(0.60,0.55)], size=0.042)
s.smudge([(0.565,0.80),(0.53,0.90)], size=0.038)

# 4. grain: a few marks that describe it, not thirty that repeat it
s.stroke([(0.02,0.30),(0.20,0.245),(0.31,0.235)], "liner", "wood_lo",
         size=0.007, load=0.7, pressure=[0.9,0.3,0.7])
s.stroke([(0.0,0.61),(0.17,0.55)], "liner", "wood_dk", size=0.005, load=0.6,
         pressure=[0.2,1.0])
s.stroke([(0.05,0.93),(0.34,0.845),(0.46,0.83)], "bristle", "wood_lo",
         size=0.022, load=0.55, opacity=0.30, pressure="swell")
s.stroke([(0.60,0.955),(0.86,0.90)], "liner", "wood_lo", size=0.006, load=0.8,
         pressure=[0.7,1.0,0.2])
s.stroke([(0.14,0.13),(0.36,0.085)], "bristle", "wood_hi", size=0.030, load=0.6,
         opacity=0.30, pressure="lift_off")
print("total", s.stroke_count)
print(s.look())
