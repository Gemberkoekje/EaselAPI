p = s.palette
s.dry()
# a. the floor is not a row of teeth
s.stroke([(-0.05,0.905),(0.16,0.930),(0.34,0.968)], "flat", "floor", size=0.10,
         load=1.0, pressure="even")
s.stroke([(-0.05,1.02),(0.20,1.03)], "flat", "floor", size=0.08, load=1.0,
         pressure="even")
s.stroke([(1.05,0.905),(0.86,0.935),(0.70,0.972)], "flat", "floor", size=0.10,
         load=1.0, pressure="even")
s.stroke([(1.05,1.02),(0.82,1.03)], "flat", "floor", size=0.08, load=1.0,
         pressure="even")
s.stroke([(-0.05,0.862),(0.22,0.868)], "flat", "wall", size=0.045, load=1.0,
         pressure="even")
s.stroke([(1.05,0.862),(0.80,0.868)], "flat", "wall", size=0.045, load=1.0,
         pressure="even")
print("floor", s.stroke_count)
# b. the slot: a door ajar, so it opens downward
s.stroke([(0.452,-0.05),(0.436,0.30),(0.420,0.60),(0.404,0.875)], "flat", "wall",
         size=0.075, load=1.0, pressure="even")
s.stroke([(0.582,-0.05),(0.594,0.30),(0.604,0.60),(0.616,0.875)], "flat", "wall",
         size=0.075, load=1.0, pressure="even")
print("slot", s.stroke_count)
# c. the door's own edge takes the light, the frame opposite takes less
s.stroke([(0.446,-0.04),(0.430,0.30),(0.414,0.60),(0.398,0.870)], "liner", "spill2",
         size=0.009, load=1.0, pressure=[0.4,1.0,0.8,1.0])
s.stroke([(0.588,-0.04),(0.600,0.34),(0.612,0.72),(0.620,0.870)], "liner", "spill",
         size=0.007, load=1.0, pressure=[0.3,0.7,1.0,0.6])
print("edges", s.stroke_count)
print(s.look())
