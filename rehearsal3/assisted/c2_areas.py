# Pass 2 — identify which numbered mass is which thing, before merging.
# Run: python -m easel run painting.easel c2_areas.py

REF = r"C:\temp\Level1.jpg"

prep = s.prepare(REF)
for i in range(1, 8):
    try:
        r = prep.region(i)
        print("area", i, "->", r)
    except Exception as exc:
        print("area", i, "region failed:", type(exc).__name__, exc)
print("strokes:", s.stroke_count)
