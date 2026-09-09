# Pass 4 — read the machine's drawing at the size of the object, before touching it.
# Run: python -m easel run painting.easel c4_inspect.py

REF = r"C:\temp\Level1.jpg"
print(s.look(region=span("C1", "G7"), reference=REF))
print("strokes:", s.stroke_count)
