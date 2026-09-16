exec(open("helpers.py").read())
p = s.palette
# the curtain keeps the sun off the right end of the sill
s.stroke([(0.78, 0.63), (1.03, 0.64)], "round_soft", "cast", size=0.06, opacity=0.45,
         pressure=[0.3, 1.0], load=1.0, note="curtain shadow on the sill")
s.stroke([(0.84, 0.72), (1.03, 0.73)], "round_soft", "cast", size=0.05, opacity=0.35,
         pressure=[0.3, 1.0], load=1.0, note="curtain shadow on the sill, lower")
print("strokes before signing:", s.stroke_count)
print(s.look())
# the signature: a small lift-off chevron and a dot, close in value to the wall it sits on
p["sig"] = to_value(p["wall_low"], 0.40)
s.stroke([(0.925, 0.957), (0.94, 0.937), (0.955, 0.957)], "liner", "sig", size=0.005,
         pressure=[0.6, 1.0, 0.2], note="signature")
s.dab(0.966, 0.955, "round_hard", "sig", size=0.006, press=2, note="signature")
print("strokes after signing:", s.stroke_count)
print(s.export("painting.png"))
print(s.timelapse_gif("painting.gif"))
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    s.log()
open("log.txt", "w").write(buf.getvalue())
print("log lines:", len(buf.getvalue().splitlines()))
