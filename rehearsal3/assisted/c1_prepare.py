# Pass 1 — read the reference: prepare() the machine cut-up, look at it.
# Run: python -m easel run painting.easel c1_prepare.py

REF = r"C:\temp\Level1.jpg"

prep = s.prepare(REF)
print(prep)
print("---- look_areas ----")
print(s.look_areas())
print("---- ref beside blank canvas, grid ----")
print(s.look(reference=REF, grid=True))
print("strokes:", s.stroke_count)
