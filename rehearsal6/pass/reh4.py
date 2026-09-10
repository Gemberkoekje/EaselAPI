R = "/home/user/refs/Level1.jpg"
V1 = [dict(points=[(0.376,0.452),(0.412,0.466),(0.444,0.484)], brush="round_hard",
           color="visor", size=0.030, pressure="swell", load=1.0, label="visor fat")]
V2 = [dict(points=[(0.378,0.450),(0.410,0.463),(0.438,0.480)], brush="flat",
           color="visor", size=0.022, pressure="even", load=1.0, label="visor flat")]
V3 = [dict(points=[(0.377,0.451),(0.409,0.464),(0.440,0.481)], brush="round_hard",
           color="visor", size=0.022, pressure="swell", load=1.0),
      dict(points=[(0.384,0.455),(0.412,0.467)], brush="round_hard",
           color="mug_hi", size=0.011, pressure="taper", load=1.0)]
s.preview(V1+[dict(points=[(0.296,0.238),(0.320,0.184),(0.366,0.148),(0.420,0.126)],
                   brush="liner", color="mug_wt", size=0.008, label="rimlight")],
          reference=R, region=span("C2","F5"))
print(s.rehearse(V1, region=span("C4","E5")))
print(s.rehearse(V2, region=span("C4","E5")))
print(s.rehearse(V3, region=span("C4","E5")))
