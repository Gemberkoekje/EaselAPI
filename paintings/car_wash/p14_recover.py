# compare() put the brush at -0.12 against its written value after the form went on, and
# that is not bookkeeping: the shadow side had come down to 0.41 against a tunnel at
# 0.32, nine hundredths apart, so the mass was starting to merge with the glass behind
# it. The form was right and too deep. A ramp only has to clear 0.10 to read as form;
# past that it spends the mass's separation from what is behind it, which is the more
# expensive thing. So the range is compressed, not removed -- two bristle passes lifting
# the shadow side back toward 0.51 and leaving the lit edge where it is.
import numpy as np
def prof(tag):
    v = s.canvas.rgb @ np.array([0.2126, 0.7152, 0.0722])
    v = np.where(v <= 0.0031308, v*12.92, 1.055*np.power(np.maximum(v,1e-9),1/2.4)-0.055)
    h, w = v.shape
    print(f"  {tag:6s} " + " ".join(
        f"{x:.2f}:{v[int(0.05*h):int(0.50*h), int(x*w)-12:int(x*w)+12].mean():.2f}"
        for x in (0.74, 0.78, 0.82, 0.86, 0.90, 0.94)))
prof("before")
s.stroke([(0.906, -0.04), (0.884, 0.34), (0.910, 0.70)], "bristle", "brush_lt",
         size=0.050, opacity=0.46, load=0.80, pressure="lift_off")
s.stroke([(0.962, 0.00), (0.944, 0.36), (0.966, 0.68)], "bristle", "brush_lt",
         size=0.044, opacity=0.42, load=0.75, pressure="lift_off")
prof("after")
s.paint({"shape": pillar_r(), "brush": "flat", "color": "frame", "size": 0.024,
         "direction": "axis", "density": 1.0, "load": 1.0, "load_falloff": 0.0,
         "edge": "clean"})
print(s.compare(PLAN))
