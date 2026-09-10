s.dry()
# I ran a repair straight across the light. Put the column back.
s.block_in(polygon([(0.498,0.170),(0.556,0.170),(0.558,0.300),(0.496,0.300)]),
           "flat", "blaze", direction=90, density=0.95, size=0.028, load=1.0,
           pressure="even")
s.stroke([(0.492,0.165),(0.490,0.305)], "liner", "lit", size=0.011, load=1.0,
         pressure="even")
s.stroke([(0.562,0.165),(0.564,0.305)], "liner", "lit", size=0.010, load=1.0,
         pressure="even")
s.stroke([(0.470,0.230),(0.486,0.234)], "round_hard", "spill", size=0.022, load=1.0,
         opacity=0.6, pressure="even")
s.stroke([(0.570,0.228),(0.588,0.232)], "round_hard", "spill", size=0.020, load=1.0,
         opacity=0.5, pressure="even")
# take the orange tick off the light and put the mark somewhere quiet
s.stroke([(0.030,0.950),(0.095,0.992)], "round_hard", "spill2", size=0.040,
         load=1.0, opacity=0.9, pressure="even")
print("total", s.stroke_count)
s.stroke([(0.885,0.822),(0.899,0.840),(0.929,0.808)], "liner", "wall_l", size=0.006,
         load=1.0, pressure=[0.9,1.0,0.4], note="signature")
print(s.look())
