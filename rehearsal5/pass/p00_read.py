REF = "C:/temp/Level1.jpg"

print("=== compare on the empty canvas ===")
print(s.compare(REF))
print()
print("look with grid + reference:", s.look(reference=REF, grid=True))
print("values:", s.look(reference=REF, values=True))
print("stroke_count", s.stroke_count)
