p = s.palette
s.dry()
n = s.stroke_count

# the "scarf" across the shoulder: too light by two stops. Paint it out.
s.stroke([(0.628, 0.476), (0.710, 0.456), (0.792, 0.474)], "flat", "coat",
         size=0.052, pressure="even", load=1.0)
s.stroke([(0.640, 0.504), (0.722, 0.486), (0.790, 0.500)], "flat", "coat",
         size=0.040, pressure="even", load=1.0)
s.stroke([(0.652, 0.446), (0.716, 0.436), (0.772, 0.452)], "flat", "coat",
         size=0.026, pressure="even", load=1.0)
# the pale seam down the chest
s.stroke([(0.556, 0.640), (0.596, 0.722), (0.614, 0.824)], "flat", "coat",
         size=0.030, pressure="even", load=1.0)
s.stroke([(0.518, 0.590), (0.542, 0.634), (0.560, 0.688)], "flat", "coat",
         size=0.016, opacity=0.65, pressure="even")
s.stroke([(0.5445, 0.6470), (0.5590, 0.6535)], "round_hard", "coat",
         size=0.009, load=1.0)
s.stroke([(0.856, 0.498), (0.876, 0.544)], "flat", "coat", size=0.034,
         pressure="even", load=1.0)
print("coat repairs", s.stroke_count - n); n = s.stroke_count

# the hair is dark where it falls over the forehead
s.stroke([(0.486, 0.152), (0.462, 0.196), (0.442, 0.234)], "bristle", "hair_d",
         size=0.026, load=0.85)
s.stroke([(0.508, 0.132), (0.478, 0.172)], "bristle", "hair_d", size=0.018,
         load=0.8)
print("forehead hair", s.stroke_count - n)
print("total:", s.stroke_count)
print(s.look(reference="ref.jpg"))
print(s.compare("ref.jpg"))
