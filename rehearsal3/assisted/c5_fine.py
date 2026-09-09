# Pass 5 — read the tenths where the machine's drawing is missing or wrong:
#   (a) the mug's base, which the sketch seems to have swallowed into the shadow
#   (b) the spoon, which the sketch missed completely
# Run: python -m easel run painting.easel c5_fine.py

REF = r"C:\temp\Level1.jpg"
print(s.look(region=span("C5", "F7"), reference=REF, grid="fine"))
print(s.look(region=span("D1", "F3"), reference=REF, grid="fine"))
print("strokes:", s.stroke_count)
