# Pass 3 — the machine underdrawing. Merge the four wood masses into one, then
# lay the outlines as pencil.  Run: python -m easel run painting.easel c3_sketch.py

REF = r"C:\temp\Level1.jpg"

prep = s.prepare(REF)
# 1, 3, 5 are all "the table, at four different brightnesses". So is most of 2.
prep.merge(2, 1)
print("after merge(2,1):", prep.numbers)
prep.merge(1, 3)
prep.merge(1, 5)
print("after wood merges:", prep.numbers)
print(prep)

try:
    n = s.sketch(REF)
except TypeError as exc:
    print("sketch(REF) rejected:", exc)
    n = s.sketch()
print("sketch returned:", n)

print(s.look(reference=REF, grid=True))
print("sketch_lines:", len(s.sketch_lines()))
print("strokes:", s.stroke_count)
