R = r"C:\temp\AntonConspiracy.jpg"
p = s.palette
# the last green, above and beside the fringe
s.stroke([(0.398, 0.10), (0.404, 0.19)], "round_hard", "wall_mid2", size=0.022, pressure="even")
s.stroke([(0.41, 0.11), (0.418, 0.17)], "round_hard", "hair", size=0.02, pressure="even")
# soften the corduroy in the hair mass without losing its value
for pts in ([(0.50, 0.10), (0.62, 0.08), (0.70, 0.18)],
            [(0.52, 0.20), (0.62, 0.18), (0.70, 0.30)],
            [(0.55, 0.30), (0.64, 0.32), (0.68, 0.42)]):
    s.stroke(pts, "round_soft", "hair", size=0.06, opacity=0.45, pressure="even")
s.stroke([(0.49, 0.13), (0.56, 0.08), (0.64, 0.09)], "round_soft", "hair_lt", size=0.03, opacity=0.5, pressure="taper")
# the beard as a mass under the jaw, not a hook
s.stroke([(0.445, 0.49), (0.47, 0.52), (0.50, 0.53)], "round_soft", "beard", size=0.035, opacity=0.8, pressure="even")
s.stroke([(0.455, 0.55), (0.49, 0.565)], "round_soft", "beard", size=0.025, opacity=0.8, pressure="even")
s.smudge([(0.52, 0.53), (0.54, 0.56)], size=0.025)
print("strokes:", s.stroke_count)
print(s.look(reference=R))
s.export("copy_final.png")
s.timelapse_gif("copy_timelapse.gif")
print("exported")
