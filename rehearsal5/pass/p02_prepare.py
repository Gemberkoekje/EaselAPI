REF = "C:/temp/Level1.jpg"
prep = s.prepare(REF)
print(prep)
print()
print("areas overlay:", s.look_areas())
print()
print("crops:")
print(s.look(region=span("C2", "F4"), reference=REF, grid=True))
print(s.look(region=span("C5", "F7"), reference=REF, grid=True))
