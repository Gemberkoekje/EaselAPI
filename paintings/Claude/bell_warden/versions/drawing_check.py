from easel import *
import easel
t = Session(1024, 768, ground="warm_white", seed=1, out_dir="looks")
ns = {k: getattr(easel, k) for k in dir(easel) if not k.startswith("_")}
ns["s"] = t
exec(open("prelude.py", encoding="utf-8").read().split("s.plan(")[0], ns)
for shp in ("plinth_top", "plinth_front", "plinth_side", "wing", "body", "tail"):
    t.pencil(ns[shp].closed, pressure=0.9, smooth=False)
for shp in ("head_top", "cheek", "chest_lit", "shoulder_lit", "back_lit", "haunch_lit", "wing_lit"):
    t.pencil(ns[shp].closed, pressure=0.35, smooth=False)
for tip in ns["finger_tips"]:
    t.pencil([ns["wrist"], tip], pressure=0.7, smooth=False)
print(t.look(grid=True, path="looks/01e-drawing-clean.png"))
