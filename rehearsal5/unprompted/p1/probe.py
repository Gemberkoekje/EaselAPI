r1 = ribbon([(0.0, 0.30), (1.0, 0.30)], 0.15)
r2 = ribbon([(0.0, 0.30), (1.0, 0.30)], 0.30)
r3 = ribbon([(0.2, 0.2), (0.8, 0.8)], 0.20)
b1 = blob(cell("D5"), 0.20, wobble=0.3, seed=2)
e1 = ellipse(span("C3", "E5"))
for name, sh in (("ribbon w=.15", r1), ("ribbon w=.30", r2), ("ribbon diag", r3),
                 ("blob r=.20 D5", b1), ("ellipse C3:E5", e1)):
    print(f"{name:16s} box={sh.box}  axis={round(sh.axis, 1)}  area={sh.area:.3f}  center={sh.center}")
print("cell D5     ", cell("D5"))
print("span C3:E5  ", span("C3", "E5"))
print("upper-band  ", region("upper-band"))
print("middle-band ", region("middle-band"))
print("lower-band  ", region("lower-band"))
print("horizon(.42)", horizon(0.42))
print("contains .5,.30", r1.contains(0.5, 0.30), " .5,.20", r1.contains(0.5, 0.20),
      " .5,.24", r1.contains(0.5, 0.24), " .5,.17", r1.contains(0.5, 0.17))
