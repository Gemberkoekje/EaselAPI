"""Bare ground inside each cut, split into the 2 px along the cut's edge and the rest, read with the canvas's
own measure (Canvas.ground_showing, the checklist's ground line). The cut is the places' 4x4 coverage over 0.5."""
import os, runpy, sys
import numpy as np
from easel import Session
T = "/home/user/projects/the-curator/tools/easel/"
al = np.load("/tmp/claude-0/-home-user-projects/effc84d7-d7e9-5d60-848f-887f6f888335/scratchpad/step2/cut/alphas.npz")
caught = {}
orig = Session.export
def grab(self, *a, **kw):
    caught["s"] = self
    return orig(self, *a, **kw)
Session.export = grab
def erode(m, n):
    for _ in range(n):
        m = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
    return m
for name, script in (("candle", "candle.py"), ("patron", "patron_default.py"), ("doorway wall", "doorway_wall.py")):
    os.makedirs(name.replace(" ", "_"), exist_ok=True); os.chdir(name.replace(" ", "_"))
    sys.argv = [T + script, "99"]
    runpy.run_path(T + script, run_name="__main__")
    os.chdir("..")
    c = caught["s"].canvas
    inside = al[f"{name}|c4"] > 0.5
    band = inside & ~erode(inside, 2)
    core = inside & ~band
    g = lambda m: c.ground_showing(where=m)
    print(f"{name:13s} whole canvas {g(np.ones_like(inside)):7.2%}  inside the cut {g(inside):7.2%}  "
          f"(the 2 px along its edge {g(band):7.2%} of the band, {band.sum()} px; the rest {g(core):7.2%})", file=sys.stderr)
    th = c.thickness
    print(f"{'':13s} paint thickness 0 (nothing laid): whole {(th <= 0).mean():7.2%}  inside {(th[inside] <= 0).mean():7.2%}  "
          f"band {(th[band] <= 0).mean():7.2%}  rest {(th[core] <= 0).mean():7.2%}", file=sys.stderr)
