"""This painting's mixtures side by side, before the first mass (exercise 9)."""
from easel import Session, Region
import runpy
names = ["wall_far", "wall", "ray", "mount", "mount_lit", "cavern", "dwarf", "glow", "floor",
         "rim", "bedroll", "black", "rim_light", "lining", "lining_lit", "face_lit",
         "face_mid", "face_shade", "d_skin", "wood", "wood_lit", "wax", "gold", "copper",
         "silver", "card"]
sw = Session(1300, 200, ground="#54443a", seed=9, out_dir="out")
src = open("prelude.py", encoding="utf-8").read()
mix_part = src[src.index("# ---- Mixtures"):src.index("# ---- Places the plan")]
g = {"s": sw}
exec("from easel import *\n" + mix_part, g)
p = sw.palette
w = 1.0 / len(names)
for i, n in enumerate(names):
    sw.block_in(Region(i * w + 0.002, 0.10, (i + 1) * w - 0.002, 0.80), "flat", n,
                size=0.012, solid=True)
    print(f"{n:11s} value {p.value_of(n):.2f}  chroma {p.chroma_of(n):.3f}  {p.hex(n)}")
sw.look(path="out/swatches.png")
