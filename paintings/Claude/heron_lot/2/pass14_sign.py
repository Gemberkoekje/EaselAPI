# Two marks in the bottom-right, where the sheet is thinnest: a short vertical
# and the shorter broken one the water gives back. The same mark as painting 1,
# because it is the same hand and this picture is the same thought, carried out
# a second time.
here = s.sample((0.93, 0.935, 0.99, 0.995))
sig = p.at_value(p.mix(here, "ultramarine", 0.28), p.value_of(here) - 0.095)
s.stroke([(0.9545, 0.9410), (0.9532, 0.9605)], "liner", sig, size=0.0038,
         opacity=0.85, load=1.0, load_falloff=0.0, pressure=[1.0, 0.7],
         note="signature")
s.stroke([(0.9536, 0.9718), (0.9528, 0.9806)], "liner", sig, size=0.0030,
         opacity=0.5, load=0.8, load_falloff=0.5, pressure=[0.8, 0.15],
         note="signature")
print(s.look()); print(s.look(values=True)); print(s.budget_line())
