# Pass 13 — re-lay the drawing on top of the wood. Lines 3, 5, 6 are the machine's
# useful ones (mug silhouette / handle+right shadow / dark mass); 0,1,2,4 are the
# wood-grain junk and stay buried. 7-12 are mine. Pencil costs nothing.
# Run: python -m easel run painting.easel c13_redraw.py
REF = r"C:\temp\Level1.jpg"

lines = s.sketch_lines()
KEEP = [3, 5, 6, 7, 8, 9, 10, 11, 12]
WIN = (0.275, 0.78, 0.0, 0.86)          # x0, x1, y0, y1 -- the mug's neighbourhood


def runs(pts):
    out, cur = [], []
    for x, y in pts:
        if WIN[0] <= x <= WIN[1] and WIN[2] <= y <= WIN[3]:
            cur.append((x, y))
        else:
            if len(cur) >= 4:
                out.append(cur)
            cur = []
    if len(cur) >= 4:
        out.append(cur)
    return out


laid = 0
for i in KEEP:
    for run in runs(lines[i]):
        s.pencil(run, pressure=0.75)
        laid += 1
print("re-laid", laid, "runs")
print(s.look(region=span("C1", "G7"), reference=REF))
print("strokes:", s.stroke_count)
