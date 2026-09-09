# Pass 28 — the brief says UNDER 300 and c27 landed exactly on 300, so scrape one
# mark (the handle's highlight dab, the least load-bearing of the last three) and
# finish: final compare, side-by-side looks, export, timelapse.
# Run: python -m easel run painting.easel c28_finish.py
REF = r"C:\temp\Level1.jpg"

s.undo(1)
print("after undo:", s.stroke_count)

print(s.compare(REF))
print(s.look(reference=REF))
print(s.look(reference=REF, values=True))
print(s.look())
print(s.export("copy_final.png"))
print(s.timelapse_gif("copy_timelapse.gif"))
print("final strokes:", s.stroke_count)
