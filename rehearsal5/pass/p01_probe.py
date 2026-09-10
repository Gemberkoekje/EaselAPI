REF = "C:/temp/Level1.jpg"

# The canvas is a uniform 0.54 everywhere, so  reference = 0.54 - delta.
for c in ["C4", "E4", "D3", "C6", "D7", "A5", "F5", "G2", "D5", "F3"]:
    print("=" * 8, c, "=" * 8)
    print(s.compare(REF, region=cell(c)))
    print()
