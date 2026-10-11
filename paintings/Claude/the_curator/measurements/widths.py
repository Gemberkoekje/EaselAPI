"""Each script's stroke sizes in pixels: size is a fraction of the canvas's long side (REFERENCE.md, Units)."""
import re, sys
TOOLS = sys.argv[1] if len(sys.argv) > 1 else "the-curator/tools/easel"
canv = {"beyond_doorway.py": (560, 600), "desk.py": (1920, 720), "counter.py": (1920, 360), "shelves.py": (640, 720),
        "doorway_wall.py": (1920, 720), "locked_shelf.py": (300, 460), "patron_default.py": (400, 620), "candle.py": (120, 300)}
for f, (w, h) in canv.items():
    rows = {}
    for line in open(f"{TOOLS}/{f}").read().splitlines():
        m = re.search(r"s\.stroke\(.*?\"(round_hard|liner|bristle|flat|round_soft)\".*?size=([0-9.]+)", line)
        if m:
            rows.setdefault(float(m.group(2)), set()).add(m.group(1))
    long = max(w, h)
    print(f"{f:18s} long side {long:4d}: " + ", ".join(f"{s:g}={s * long:.1f}px ({'/'.join(sorted(b))})" for s, b in sorted(rows.items())))
