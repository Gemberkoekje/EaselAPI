# Pass 8 — compare() against the bare ground: the left column of the table is the
# reference's own value per cell, which is the value map I have to hit.
# Run: python -m easel run painting.easel c8_refvalues.py
REF = r"C:\temp\Level1.jpg"
print(s.compare(REF))
print("strokes:", s.stroke_count)
