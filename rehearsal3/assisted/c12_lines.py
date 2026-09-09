# Pass 12 — the wood block-in buried the whole underdrawing. sketch_lines() still
# has the geometry, so work out which line is which and re-lay the useful ones on
# top of the paint (pencil is free).
# Run: python -m easel run painting.easel c12_lines.py
REF = r"C:\temp\Level1.jpg"

lines = s.sketch_lines()
for i, ln in enumerate(lines):
    xs = [q[0] for q in ln]
    ys = [q[1] for q in ln]
    print(f"{i:2d} n={len(ln):5d}  x {min(xs):.3f}-{max(xs):.3f}  "
          f"y {min(ys):.3f}-{max(ys):.3f}")
print("strokes:", s.stroke_count)
