REF = "C:/temp/Level1.jpg"
print(s.look())
print(s.look(values=True))
print(s.look(reference=REF, values=True))
print("export:", s.export("copy_final.png"))
print("gif:   ", s.timelapse_gif("copy_timelapse.gif"))
print("strokes:", s.stroke_count)
print(s.log())
