# Pass 1 - the arrangement in graphite, drawn THROUGH the masses. Free.
s.pencil([(-0.06,0.150),(0.34,0.205),(0.62,0.156),(1.06,0.118)], pressure=0.5, note="far edge")
s.pencil([(-0.06,0.855),(0.28,0.812),(0.60,0.748),(1.06,0.638)], pressure=0.45, note="near edge")
for xb in (0.02, 0.46, 0.92, 1.34):
    s.pencil(lane(xb, 0.12, 1.0, 4), pressure=0.4, note="stall line")
s.pencil([(0.762,0.178),(0.770,0.420),(0.780,0.690)], pressure=0.35, note="lamp path")
# the bird, as gesture
s.pencil(T([(0.254,0.087),(0.300,0.100),(0.332,0.144),(0.396,0.242)]), pressure=0.75, note="head+bill")
s.pencil(NECK, pressure=0.7, note="neck")
s.pencil(BACK, pressure=0.6, note="back")
s.pencil(T([(0.372,0.338),(0.376,0.375),(0.358,0.408),(0.322,0.429)]), pressure=0.6, note="breast")
s.pencil(T([(0.227,0.356),(0.262,0.392),(0.322,0.429)]), pressure=0.5, note="belly")
s.pencil(LEG_F, pressure=0.7, note="leg"); s.pencil(LEG_B, pressure=0.6, note="leg")
s.pencil([(-0.02,0.556),(0.30,0.558),(0.64,0.552),(1.06,0.548)], pressure=0.3, note="waterline")
s.pencil([(0.398,0.566),(0.408,0.700),(0.418,0.840)], pressure=0.4, note="reflection")
print(s.look(grid=True))
