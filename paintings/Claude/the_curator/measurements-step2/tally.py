"""Both candidates over my 176 hand-laid strokes (marks.jsonl, from run_o3.py), split by what each stroke's
comment says it was for (intent.py); signatures by their note. 'Lost': meant to read, its colour 0.15 or more
off the value under it, and it moved its pixels under a quarter of the way there."""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from intent import INTENT
rows = [json.loads(l) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "marks.jsonl"))]
for r in rows:
    r["k"] = "S" if r["note"] == "signature" else INTENT[r["script"]][r["line"]]
    r["piece"] = r["script"].replace(".py", "") + (f"_{r['args'].split()[0]}" if r["script"] == "shelves.py" else "")
seen, first = set(), set()
for i, r in enumerate(rows):
    key = (r["piece"], r["tip"], r["width_px"])
    if r["M2"] and key not in seen:
        seen.add(key); first.add(i)
o3 = lambda d, q: (lambda r: abs(r["distance"]) >= d and r["reach90"] < q)
lost = lambda r: r["k"] == "L" and abs(r["distance"]) >= 0.15 and r["reach90"] < 0.25
print("strokes:", len(rows), dict(collections.Counter(r["k"] for r in rows)), " lost:", sum(map(lost, rows)))
print(f"{'candidate':32s} {'speaks':>6s} {'lost':>5s} {'landed L':>9s} {'gilt':>5s} {'grain':>6s} {'sign.':>6s} {'broad':>6s} {'lines':>6s}")
def row(name, fires):
    h = [r for i, r in enumerate(rows) if fires(i, r)]
    c = collections.Counter(r["k"] for r in h); f = sum(map(lost, h))
    print(f"{name:32s} {len(h):6d} {f:5d} {c['L'] - f:9d} {c['G']:5d} {c['F']:6d} {c['S']:6d} {c['B']:6d} {len({(r['piece'], r['line']) for r in h}):6d}")
row("M2 at the call", lambda i, r: r["M2"])
row("M2 once per brush and width", lambda i, r: i in first)
for d, q in ((0.10, 0.25), (0.15, 0.15), (0.15, 0.25), (0.15, 0.35), (0.25, 0.25)):
    row(f"O3 {d:.2f} / {q:.2f}", lambda i, r, d=d, q=q: o3(d, q)(r))
row("O3 0.15 / 0.25, no signatures", lambda i, r: o3(0.15, 0.25)(r) and r["k"] != "S")
print("lost, by line:")
groups = collections.defaultdict(list)
for r in rows:
    if lost(r): groups[(r["piece"], r["line"])].append(r)
for (p, l), rs in groups.items():
    print(f"  {p:16s}:{l:<3d} x{len(rs)}  {rs[0]['width_px']} px, opacity {rs[0]['opacity']}, reach {min(x['reach90'] for x in rs):.2f}-{max(x['reach90'] for x in rs):.2f}")
big = [r for r in rows if r["script"] in ("desk.py", "counter.py", "doorway_wall.py")]
print("1920-wide pieces: M2", dict(collections.Counter(r["k"] for r in big if r["M2"])), " O3 0.15/0.25", dict(collections.Counter(r["k"] for r in big if o3(0.15, 0.25)(r))))
print("O3 0.15/0.25 firings that are also M2:", sum(1 for r in rows if o3(0.15, 0.25)(r) and r["M2"]), "of", sum(1 for r in rows if o3(0.15, 0.25)(r)))
