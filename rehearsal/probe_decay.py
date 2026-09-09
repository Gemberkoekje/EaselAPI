from easel import Session

s = Session(600, 600, ground="white", seed=31)
s.stroke([(0.1, 0.5), (0.9, 0.5)], "flat", "ultramarine", size=0.3, pressure="even")
print("after laying it      :", round(float(s.canvas.wetness.max()), 3))
for i in range(1, 13):
    s.dab(0.02, 0.02, "round_hard", "titanium_white", size=0.01)   # elsewhere
    if i in (1, 2, 3, 5, 8, 12):
        print(f"after {i:>2} more strokes :", round(float(s.canvas.wetness[250:350,200:400].max()), 3))
