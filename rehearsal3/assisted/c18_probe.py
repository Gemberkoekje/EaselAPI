# Pass 18 — what value did the tea actually land at? compare() inside a cell
# reports the canvas's own colour per tenth, which is the cheapest probe I have.
# Run: python -m easel run painting.easel c18_probe.py
REF = r"C:\temp\Level1.jpg"
print(s.compare(REF, region=span("D2", "E3")))
print("strokes:", s.stroke_count)
