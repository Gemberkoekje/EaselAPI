"""Read the reference's values inside a few cells, at tenths."""
for c in ("E4", "E5", "C6", "E2", "G5", "F4"):
    print("=== cell", c)
    print(s.compare("ref.jpg", region=cell(c)))
    print()
prep = s.prepare("ref.jpg", level="fine")
print(prep)
