A = [dict(points=[(0.03,0.44),(0.09,0.98)], color="rain", opacity=0.13, size=0.16),
     dict(points=[(0.17,0.47),(0.24,0.94)], color="rain", opacity=0.11, size=0.13),
     dict(points=[(0.30,0.50),(0.36,0.88)], color="squall2", opacity=0.10, size=0.10),
     dict(points=[(0.42,0.49),(0.46,0.80)], color="rain", opacity=0.08, size=0.075)]
B = [dict(points=p["points"], brush="bristle", color=p["color"], size=p["size"],
          load=1.0, opacity=0.22, pressure="lift_off") for p in A]
print(s.rehearse([dict(a, _glaze=True) for a in A]) if False else "")
print("A", s.rehearse(A, region=span("A3","E8")))
print("B", s.rehearse(B, region=span("A3","E8")))
