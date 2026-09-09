from easel import Session, Region
import numpy as np

R = Region(0.40, 0.42, 0.70, 0.62)          # a small box in the middle
print("asked for  x 0.40-0.70   y 0.42-0.62")
for direction in ["horizontal", "vertical", "diagonal", "cross"]:
    for size in [0.20, 0.08]:
        s = Session(1000, 600, ground="toned_grey", seed=5)
        before = s.canvas.rgb.copy()
        s.block_in(R, "bristle", "titanium_white", density=0.9,
                   size=size, direction=direction)
        d = (np.abs(s.canvas.rgb - before).max(axis=2) > 1e-3)
        ys, xs = np.where(d)
        print(f"  {direction:<11} size={size}  ->  x {xs.min()/1000:.2f}-{xs.max()/1000:.2f}"
              f"   y {ys.min()/600:.2f}-{ys.max()/600:.2f}   ({s.stroke_count} strokes)")
