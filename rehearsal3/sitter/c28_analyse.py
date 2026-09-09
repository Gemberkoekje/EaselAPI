"""Which of the cells compare() reports as 'out' are actually reachable?

The palette bottoms out around 0.23. Any cell whose *reference* value is below
0.13 can never come within compare()'s 0.10 threshold. This reads the reference
photograph only (not the engine), and uses the same Rec.709 luma that compare()
uses -- verified against compare()'s own printout: C2 #18110D -> 0.07, H7
#21140E -> 0.09, D5 #271B12 -> 0.12.

Run with plain python:  python c28_analyse.py
"""
from PIL import Image

REF = r"C:/temp/Level3.jpg"
COLS = "ABCDEFGH"
DELTA = {  # copied from the final compare() table
    "A1": -0.02, "B1": -0.02, "C1": -0.03, "D1": +0.01, "E1": -0.02, "F1": -0.03, "G1": +0.04, "H1": +0.04,
    "A2": +0.13, "B2": -0.05, "C2": +0.23, "D2": +0.18, "E2": +0.08, "F2": -0.05, "G2": -0.05, "H2": -0.01,
    "A3": +0.02, "B3": -0.02, "C3": +0.19, "D3": +0.15, "E3": +0.02, "F3": -0.00, "G3": -0.01, "H3": -0.01,
    "A4": +0.05, "B4": -0.00, "C4": +0.10, "D4": +0.05, "E4": -0.02, "F4": +0.12, "G4": -0.02, "H4": -0.06,
    "A5": +0.08, "B5": +0.05, "C5": +0.10, "D5": +0.21, "E5": +0.10, "F5": +0.19, "G5": +0.02, "H5": +0.07,
    "A6": +0.07, "B6": +0.13, "C6": +0.10, "D6": +0.17, "E6": +0.17, "F6": +0.19, "G6": +0.08, "H6": +0.11,
    "A7": +0.11, "B7": +0.11, "C7": +0.06, "D7": +0.18, "E7": +0.19, "F7": +0.19, "G7": +0.14, "H7": +0.22,
    "A8": -0.03, "B8": +0.15, "C8": +0.09, "D8": +0.17, "E8": +0.17, "F8": -0.05, "G8": +0.11, "H8": +0.12,
}
FLOOR = 0.23

im = Image.open(REF).convert("RGB")
W, H = im.size
ref = {}
for ci, c in enumerate(COLS):
    for r in range(1, 9):
        box = (int(ci * W / 8), int((r - 1) * H / 8), int((ci + 1) * W / 8), int(r * H / 8))
        px = list(im.crop(box).getdata())
        n = len(px)
        rr = sum(q[0] for q in px) / n
        gg = sum(q[1] for q in px) / n
        bb = sum(q[2] for q in px) / n
        ref["%s%d" % (c, r)] = (0.2126 * rr + 0.7152 * gg + 0.0722 * bb) / 255.0

out = {k: v for k, v in DELTA.items() if abs(v) > 0.10}
impossible, fixable = [], []
for k, v in sorted(out.items(), key=lambda kv: -abs(kv[1])):
    best = FLOOR - ref[k]          # smallest delta achievable if painted at the floor
    (impossible if best > 0.10 else fixable).append((k, v, ref[k], best))

print("cells more than 0.10 out: %d of 64" % len(out))
print()
print("UNREACHABLE (reference darker than the palette's floor of %.2f):" % FLOOR)
for k, v, rv, best in impossible:
    print("  %-3s delta %+0.2f   ref %.2f   best possible %+0.2f" % (k, v, rv, best))
print()
print("REACHABLE (my error, could still be painted out):")
for k, v, rv, best in fixable:
    print("  %-3s delta %+0.2f   ref %.2f" % (k, v, rv))
print()
print("%d unreachable, %d reachable" % (len(impossible), len(fixable)))
