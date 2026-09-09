p = s.palette
# the headland's base, lost into the water
s.smudge([(0.0, 0.595), (0.3, 0.595), (0.6, 0.60)], size=0.04)
# the shine, broken from a stripe into passages
s.stroke([(0.0, 0.745), (0.14, 0.745)], "bristle", "water2", size=0.03, load=0.6, pressure="taper", opacity=0.8)
s.stroke([(0.47, 0.745), (0.58, 0.748)], "bristle", "water2", size=0.03, load=0.6, pressure="taper", opacity=0.8)
s.stroke([(0.86, 0.745), (1.02, 0.75)], "bristle", "mud", size=0.035, load=0.6, pressure="taper")
s.stroke([(0.22, 0.76), (0.42, 0.762)], "bristle", "mud", size=0.03, load=0.5, pressure="taper")
# the channel: shorter, softer, lit from inside rather than beside
s.stroke([(0.78, 0.91), (0.90, 0.96), (1.02, 1.0)], "bristle", "mud_dk", size=0.08, load=0.9, load_falloff=0.3, pressure="even")
s.stroke([(0.74, 0.895), (0.86, 0.94)], "bristle", "mud", size=0.05, load=0.8, pressure="even")
s.smudge([(0.53, 0.77), (0.62, 0.83), (0.74, 0.89)], size=0.035)
s.smudge([(0.56, 0.78), (0.66, 0.85)], size=0.025)
s.stroke([(0.60, 0.815), (0.67, 0.855)], "round_hard", "shine", size=0.006, load=0.5, pressure="taper")
# glaze the loudest speckle down without hiding it
for y in (0.82, 0.89, 0.96):
    try:
        s.glaze([(0.5, y), (1.02, y)], "mud_dk", opacity=0.35, size=0.09)
    except TypeError as e:
        print("glaze has no size:", e)
        s.glaze([(0.5, y), (1.02, y)], "mud_dk", opacity=0.35)
print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
s.export("own_final.png")
s.timelapse_gif("own_timelapse.gif")
print("exported")
