# Signed with two marks: a thing standing, and the shorter broken thing the
# water gives back. It is the whole painting reduced to the least I could
# make it out of, and it is what I would put in the corner of this one.
here = s.sample((0.92, 0.930, 0.99, 0.990))
sig = p.at_value(p.mix(here, "ultramarine", 0.25), p.value_of(here) - 0.085)
s.stroke([(0.9520, 0.9385), (0.9508, 0.9585)], "liner", sig, size=0.0038,
         opacity=0.85, load=1.0, load_falloff=0.0, pressure=[1.0, 0.7],
         note="signature")
s.stroke([(0.9512, 0.9700), (0.9505, 0.9790)], "liner", sig, size=0.0030,
         opacity=0.5, load=0.8, load_falloff=0.5, pressure=[0.8, 0.15],
         note="signature")
print(s.look())
print(s.budget_line())
