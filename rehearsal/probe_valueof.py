from easel import Session
import numpy as np

# Paint flat swatches of known colours, then read what look(values=True) shows,
# and compare with what value_of() claims.
p = Session(100, 100, seed=1).palette
names = ["titanium_white", "cadmium_yellow", "yellow_ochre", "cadmium_red",
         "burnt_sienna", "burnt_umber", "ultramarine"]

print(f"{'colour':<16}{'value_of':>10}{'greyscale view':>16}")
for n in names:
    s = Session(200, 200, ground=p.hex(n), seed=1, timelapse=False)
    grey = np.asarray(s.look_array(values=True), dtype=np.float32) / 255.0 \
        if hasattr(s, "look_array") else None
    if grey is None:
        from easel.look import render_look
        grey = np.asarray(render_look(s, values=True), dtype=np.float32) / 255.0
    shown = float(grey[..., 0].mean()) if grey.ndim == 3 else float(grey.mean())
    print(f"{n:<16}{p.value_of(n):>10.2f}{shown:>16.2f}")
