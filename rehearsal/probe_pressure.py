from easel import Session
import numpy as np

# Does `pressure` change the mark at all?  Same stroke, scalar pressures.
for p in [0.1, 0.3, 0.6, 1.0]:
    s = Session(600, 200, ground="toned_grey", seed=11)
    before = s.canvas.rgb.copy()
    s.stroke([(0.1, 0.5), (0.9, 0.5)], "bristle", "titanium_white",
             pressure=p, size=0.08, load=1.0, load_falloff=0.0)
    d = np.abs(s.canvas.rgb - before)
    changed = (d.max(axis=2) > 1e-4)
    print(f"pressure={p:<4}  px changed={changed.sum():>6}  "
          f"mean delta={d.mean():.5f}  bbox_h={np.any(changed,axis=1).sum()}")
