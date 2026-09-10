p = s.palette
s.dry()
edge = [(-0.05,0.648),(0.15,0.566),(0.33,0.502),(0.50,0.430),(0.68,0.350),
        (0.86,0.292),(1.05,0.250)]
s.preview([{"points":edge,"brush":"bristle","size":0.13,"color":"squall2",
            "label":"cloud base"}])
n0=s.stroke_count
s.sweep(edge, "bristle", "squall2", into="up", depth=0.30, size=0.13, cross=24,
        density=0.85, load=1.0)
print("sweep", s.stroke_count - n0)
s.block_in(span("A1","H2"), "bristle", "squall", direction=(-13,9), density=0.8,
           size=0.15, load=1.0)
print("cloud top", s.stroke_count)
# the base of it is torn, not ruled
s.stroke([(0.06,0.600),(0.22,0.548),(0.34,0.520)], "bristle", "sky", size=0.030,
         load=0.55, opacity=0.55, pressure="swell")
s.stroke([(0.52,0.446),(0.66,0.398),(0.78,0.360)], "bristle", "mid1", size=0.026,
         load=0.5, opacity=0.45, pressure="taper")
s.stroke([(0.30,0.470),(0.46,0.418)], "bristle", "squall", size=0.045, load=1.0,
         opacity=0.7, pressure="swell")
s.stroke([(0.84,0.300),(1.02,0.268)], "bristle", "mid2", size=0.018, load=0.6,
         opacity=0.4, pressure="lift_off")
print("total", s.stroke_count)
print(s.look())
