from easel import Session

s = Session(900, 500, ground="toned_grey", seed=2, out_dir="out_ex2")
for i, pr in enumerate(["taper", "press_in", "lift_off", "even", "swell", "dab"]):
    y = 0.12 + i * 0.15
    s.stroke([(0.10, y), (0.50, y)], "round_soft", "titanium_white", pressure=pr,
             size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=pr)
    s.stroke([(0.55, y), (0.92, y)], "bristle", "titanium_white", pressure=pr,
             size=0.05, opacity=0.35, load=1.0, load_falloff=0.0, note=pr)
print("ex2", s.look())

s3 = Session(900, 400, texture="rough", ground="toned_grey", seed=3, out_dir="out_ex3")
for i, load in enumerate([1.0, 0.6, 0.35, 0.2]):
    y = 0.15 + i * 0.22
    s3.stroke([(0.06, y), (0.94, y)], "bristle", "titanium_white",
              size=0.07, load=load, load_falloff=0.0, pressure="even")
print("ex3", s3.look())

s4 = Session(800, 400, ground="white", seed=4, out_dir="out_ex4")
s4.stroke([(0.10, 0.27), (0.90, 0.27)], "flat", "ultramarine", size=0.22, pressure="even")
s4.stroke([(0.15, 0.27), (0.85, 0.27)], "flat", "cadmium_yellow", size=0.10, pressure="even")
s4.stroke([(0.10, 0.73), (0.90, 0.73)], "flat", "ultramarine", size=0.22, pressure="even")
s4.dry()
s4.stroke([(0.15, 0.73), (0.85, 0.73)], "flat", "cadmium_yellow", size=0.10, pressure="even")
print("ex4", s4.look())
