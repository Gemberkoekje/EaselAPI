# 2. the near plane: the wall and the door, cutting the light down to a slot
s.block_in(polygon([(-0.05,-0.04),(0.435,-0.04),(0.415,0.855),(-0.05,0.88)]),
           "flat", "wall", direction=84, density=0.85, size=0.105, load=1.0,
           pressure="even")
print("left wall", s.stroke_count)
s.block_in(polygon([(0.605,-0.04),(1.05,-0.04),(1.05,0.88),(0.585,0.855)]),
           "flat", "wall", direction=96, density=0.85, size=0.105, load=1.0,
           pressure="even")
print("right wall", s.stroke_count)
# the floor either side of the wedge of light
s.block_in(polygon([(-0.05,0.855),(0.30,0.855),(0.02,1.04),(-0.05,1.04)]),
           "flat", "floor", direction=30, density=0.9, size=0.055, load=1.0,
           pressure="even")
s.block_in(polygon([(0.72,0.855),(1.05,0.855),(1.05,1.04),(1.00,1.04)]),
           "flat", "floor", direction=-30, density=0.9, size=0.055, load=1.0,
           pressure="even")
print("floor", s.stroke_count)
print(s.look())
