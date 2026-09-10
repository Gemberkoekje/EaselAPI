REF = "C:/temp/Level1.jpg"
s.stroke([(0.500, 0.362), (0.532, 0.358), (0.558, 0.346)], "round_hard",
         "tea_lit", size=0.024, pressure="swell", load=1.0,
         note="carry the lip shadow round")
print(s.compare(REF))
print("strokes", s.stroke_count)
print(s.export("copy_final.png"))
print(s.timelapse_gif("copy_timelapse.gif"))
print(s.look())
