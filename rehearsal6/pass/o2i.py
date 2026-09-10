p = s.palette
s.dry()
# the pool has to spread: the light gets out under the door
for x1, col, sz, op in [(0.01,"spill",0.090,0.60),(0.16,"spill2",0.085,0.72),
                        (0.32,"lit",0.070,0.82),(0.68,"lit",0.070,0.82),
                        (0.84,"spill2",0.085,0.72),(0.99,"spill",0.090,0.60),
                        (0.44,"blaze",0.048,0.85),(0.58,"blaze",0.048,0.85)]:
    s.stroke([(0.512,0.878),(0.512*0.5+x1*0.5,0.948),(x1,1.05)], "bristle", col,
             size=sz, load=1.0, opacity=op, pressure="lift_off")
print("pool", s.stroke_count)
# soften where the pool runs out into the unlit floor
s.stroke([(0.06,0.940),(0.22,0.918),(0.34,0.900)], "bristle", "spill", size=0.045,
         load=1.0, opacity=0.35, pressure="swell")
s.stroke([(0.94,0.940),(0.78,0.918),(0.66,0.900)], "bristle", "spill", size=0.045,
         load=1.0, opacity=0.35, pressure="swell")
s.smudge([(0.28,0.930),(0.20,0.952)], size=0.035)
s.smudge([(0.72,0.930),(0.80,0.952)], size=0.035)
# the hot spot at the threshold, and the blob under it taken off
s.stroke([(0.478,0.882),(0.548,0.882)], "round_hard", "blaze", size=0.020,
         load=1.0, opacity=0.9, pressure="swell")
s.stroke([(0.452,0.900),(0.512,0.894),(0.572,0.900)], "round_hard", "lit",
         size=0.024, load=1.0, opacity=0.6, pressure="swell")
print("threshold", s.stroke_count)
# three marks on the wall so it is a surface and not a fill
s.stroke([(0.12,0.46),(0.30,0.42),(0.38,0.44)], "bristle", "wall_l", size=0.026,
         load=0.8, opacity=0.22, pressure="swell")
s.stroke([(0.66,0.30),(0.84,0.27)], "bristle", "wall_d", size=0.034, load=0.9,
         opacity=0.30, pressure="lift_off")
s.stroke([(0.80,0.70),(0.96,0.74)], "bristle", "wall_l", size=0.022, load=0.7,
         opacity=0.18, pressure="taper")
print("total", s.stroke_count)
print(s.look())
print(s.look(values=True))
