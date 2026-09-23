"""Check claims before making them: (1) the vertical seam in scumbles, (2) whether hard-clip
edges are anti-aliased in the export, (3) pressure lists on a scumble vs opacity,
(4) the width of a round-tip glaze under pressure [1.0 -> 0.1]."""
import os, numpy as np
from PIL import Image
from easel import Session, Region, polygon
V = os.path.dirname(os.path.abspath(__file__)); os.chdir(V)

def lum(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(float) / 255.0
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]

# (1) seam: same scumble on a plain ground, three ways; find columns with a jump
print("(1) vertical seams: top column jumps (x as a fraction of width, mean |dL| over the band)")
for name, place, d in (("region_dir-2", Region(-0.06, 0.05, 1.06, 0.60), -2),
                       ("polygon_dir-2", polygon([(-0.06, 0.05), (1.06, 0.03), (1.06, 0.58), (-0.06, 0.60)]), -2),
                       ("region_dir0", Region(-0.06, 0.05, 1.06, 0.60), 0)):
    s = Session(1024, 768, ground="toned_grey", seed=1, out_dir=V)
    s.scumble(place, "ultramarine", "titanium_white", 8, direction=d, opacity=0.95,
              jitter=0.01, size_jitter=0.03)
    s.export(f"{V}/seam_{name}.png", sketch=False)
    L = lum(f"{V}/seam_{name}.png")[int(0.08 * 768):int(0.55 * 768)]
    jump = np.abs(np.diff(L, axis=1)).mean(axis=0)
    top = np.argsort(jump)[::-1][:3]
    print(f"   {name:14s}", ", ".join(f"x={t/1024:.3f} ({jump[t]:.4f})" for t in top),
          f"| median {np.median(jump):.4f}")

# (2) edges in the finished export: pixel values across the tower's left side and the waterline
L = lum(f"{V}/../painting.png")   # filed as painting.png; the painter had it beside the scripts as lighthouse_at_dusk.png
y = int(0.40 * 768); x0 = int(0.683 * 1024)
print("(2) tower left edge, row y=0.40, x px", x0 - 4, "..", x0 + 4, ":",
      " ".join(f"{v:.2f}" for v in L[y, x0 - 4:x0 + 5]))
y = int(0.70 * 768); row = L[y, int(0.50 * 1024):int(0.70 * 1024)]
k = int(np.argmax(np.abs(np.diff(row)))) + int(0.50 * 1024)
print("(2) waterline, row y=0.70, around x px", k, ":", " ".join(f"{v:.2f}" for v in L[y, k - 4:k + 5]))

# (3) a pressure list on a scumble, at two opacities: does the right end fade?
print("(3) scumble pressure=[1.0,0.75,0.25,0.0] on a dark field: mean value left / middle / right third")
for op in (0.9, 0.5):
    s = Session(1024, 768, ground="toned_grey", seed=2, out_dir=V)
    s.block_in(Region(0, 0, 1, 1), "flat", s.palette.mix("ultramarine", "burnt_umber", 0.5),
               size=0.1, solid=True, edge="hard")
    s.dry()
    s.scumble(Region(-0.06, 0.30, 1.06, 0.70), "cadmium_yellow", "titanium_white", 6,
              opacity=op, pressure=[1.0, 0.75, 0.25, 0.0])
    s.export(f"{V}/pressure_op{op}.png", sketch=False)
    L = lum(f"{V}/pressure_op{op}.png")[int(0.35 * 768):int(0.65 * 768)]
    print(f"   opacity {op}: " + " / ".join(f"{L[:, int(a*1024):int(b*1024)].mean():.3f}"
          for a, b in ((0.02, 0.33), (0.33, 0.66), (0.66, 0.98))))

# (4) a round_soft glaze with pressure [1.0 -> 0.1]: which end is wide?
s = Session(1024, 768, ground="toned_grey", seed=3, out_dir=V)
s.block_in(Region(0, 0, 1, 1), "flat", s.palette.mix("ultramarine", "burnt_umber", 0.5),
           size=0.1, solid=True, edge="hard")
s.dry()
base = lum_before = None
s.export(f"{V}/glaze_before.png", sketch=False)
s.glaze([(0.10, 0.5), (0.50, 0.5), (0.90, 0.5)], "titanium_white", opacity=0.3, size=0.10,
        pressure=[1.0, 0.55, 0.1])
s.export(f"{V}/glaze_after.png", sketch=False)
D = np.abs(lum(f"{V}/glaze_after.png") - lum(f"{V}/glaze_before.png"))
for fx in (0.2, 0.5, 0.8):
    col = D[:, int(fx * 1024)]
    rows = np.where(col > 0.01)[0]
    print(f"(4) glaze pressure [1.0 -> 0.1], x={fx}: painted height {len(rows)} px, peak change {col.max():.3f}")
