"""Repaint sunset_landscape deterministically, save the session and make the timelapse."""
from easel import Session

# Run the original painting script in its own namespace so `s` is bound after.
ns = {"__name__": "__main__"}
with open("sunset_paint.py", encoding="utf-8") as fh:
    code = compile(fh.read(), "sunset_paint.py", "exec")
exec(code, ns)
s = ns["s"]

# Now save the session (which stores the timelapse frames) and write the GIF.
s.save("sunset.easel")
s.timelapse_gif("sunset_landscape.gif", fps=8.0)
print(f"Saved sunset.easel with {s.stroke_count} strokes, seed {s.seed}")