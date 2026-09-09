from easel import Session

# Same as guide exercise 2 but with load run-out removed, to see pressure alone.
s = Session(900, 500, ground="toned_grey", seed=2)
for i, p in enumerate(["taper", "press_in", "lift_off", "even", "swell", "dab"]):
    y = 0.1 + i * 0.15
    s.stroke([(0.08, y), (0.5, y - 0.03), (0.92, y)], "bristle",
             "titanium_white", pressure=p, size=0.06, note=p,
             load=1.0, load_falloff=0.0)
print(s.look())
