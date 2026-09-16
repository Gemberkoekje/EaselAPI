# Pass 6: the moon. One stroke: a tapered arc on the round tip, its horns thinning
# to nothing, the lit limb toward where the sun went down. (A disc with a second
# disc in the sky's colour bitten out of it was rehearsed first; the bite showed
# as a ghost.) A beam from the lantern was planned and rehearsed twice: as a gold
# glaze it was a mustard stripe across the sky, and faint enough not to be one it
# was not there at all. The halo carries the light; there is no beam.
import math
cx, cy, r = MOON[0], MOON[1], 0.015
arc = [(cx + r * math.cos(math.radians(a)), cy + r * s.aspect * math.sin(math.radians(a)))
       for a in (-62, -20, 30, 80, 122)]
s.stroke(arc, "round_hard", "moon", size=0.011, opacity=0.95, load=1.0, load_falloff=0.0,
         pressure=[0.05, 0.6, 1.0, 0.6, 0.05], note="moon")
print(s.look())
print(s.look(region="F1:H2"))
