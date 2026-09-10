base = [[(0.545,0.88),(0.79,0.735),(1.0,0.62)],
        [(0.50,0.655),(0.755,0.515),(1.0,0.415)],
        [(0.545,0.40),(0.80,0.26),(1.0,0.175)],
        [(0.60,0.135),(0.84,0.045)]]
D = [dict(points=q, brush="flat", color="wood_lit", size=0.14, load=1.0,
          opacity=0.16, pressure="even") for q in base]
E = [dict(points=q, brush="flat", color="wood_mid", size=0.15, load=1.0,
          opacity=0.20, pressure="even") for q in base]
print("D", s.rehearse(D, region=span("E4","H8")))
print("E", s.rehearse(E, region=span("E4","H8")))
