"""Exercise 9 for this painting: every mixture side by side, on a throwaway session."""
from easel import Region

names = ["sky_high", "sky_mid", "sky_low", "mill", "glow_wall", "shawl", "shawl_lit", "dress",
         "kerchief", "kerchief_lit", "kerchief_shade", "skin_lit", "skin_mid", "skin_shade",
         "skin_core", "hair", "hair_lit", "iron", "horn", "flame", "flour"]
cols = 7
for i, name in enumerate(names):
    r, c = divmod(i, cols)
    band = Region(0.02 + c * 0.14, 0.05 + r * 0.32, 0.14 + c * 0.14, 0.30 + r * 0.32)
    s.block_in(band, "flat", name, size=0.03, solid=True)
    print(f"{name:15s} value {p.value_of(name):.2f}  chroma {p.chroma_of(name):.2f}")
print(s.look(path="looks/00-swatches.png"))
