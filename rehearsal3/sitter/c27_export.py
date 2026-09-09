# Pass 27: one last stroke on the worst cell (H5 was +0.32 — I had lit the table
# where the reference has his shoulder), then measure and export.
REF = "C:/temp/Level3.jpg"
p = s.palette
p["coat"] = p.shade(p.mix("ultramarine", "burnt_umber", 0.62), 0.55)
s.dry()

n0 = s.stroke_count
s.stroke([(0.880, 0.520), (0.940, 0.548), (1.000, 0.576)], "flat", "coat",
         size=0.088, load=1.0, load_falloff=0.0, pressure="even")
print("last:", s.stroke_count - n0)

print(s.compare(REF))
print("side :", s.look(reference=REF))
print("vals :", s.look(reference=REF, values=True))
print("alone:", s.look(sketch=False))
print("head :", s.look(region=span("D2", "F5"), reference=REF))
s.export("copy_final.png")
s.timelapse_gif("copy_timelapse.gif")
print("TOTAL strokes:", s.stroke_count)
