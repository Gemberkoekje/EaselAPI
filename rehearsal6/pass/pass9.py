R = "/home/user/refs/Level1.jpg"
lipA = [(0.294,0.272),(0.340,0.306),(0.404,0.325),(0.470,0.331),(0.532,0.316),
        (0.585,0.282),(0.620,0.243)]
# d) the near edge of the rim, over the inside
s.block_in(ribbon(lipA, 0.029), "flat", "mug_hi", direction="axis", density=0.95,
           size=0.015, load=1.0, pressure="even")
print("lip", s.stroke_count)
# e) the front wall in the rim's own shade
band = [(0.302,0.302),(0.350,0.340),(0.412,0.360),(0.476,0.366),(0.540,0.350),
        (0.594,0.314),(0.624,0.278)]
s.block_in(ribbon(band, 0.050), "flat", "mug_dk", direction="axis", density=0.9,
           size=0.026, load=1.0, pressure="even")
s.stroke([(0.300,0.320),(0.336,0.348)], "round_hard", "mug_shd", size=0.030,
         load=1.0, opacity=0.7, pressure="even")
s.stroke([(0.588,0.318),(0.618,0.286)], "round_hard", "mug_shd", size=0.028,
         load=1.0, opacity=0.7, pressure="even")
print("under-lip", s.stroke_count)
# f) the side that turns away
rshade = polygon([(0.516,0.352),(0.598,0.300),(0.612,0.440),(0.596,0.524),
                  (0.574,0.600),(0.544,0.650),(0.512,0.642),(0.522,0.486)])
s.block_in(rshade.inset(0.024), "flat", "mug_shd", direction=81, density=0.9,
           size=0.048, load=1.0, pressure="even")
print("right shade", s.stroke_count)
# the lit edge on the right silhouette, painted as a mark not an outline
s.stroke([(0.622,0.318),(0.612,0.430),(0.600,0.520),(0.582,0.592)], "bristle",
         "mug_hi", size=0.020, load=1.0, pressure="swell")
# g) the left of the vessel takes the light
s.stroke([(0.296,0.286),(0.308,0.400),(0.328,0.520),(0.352,0.634)], "bristle",
         "mug_lit", size=0.026, load=1.0, pressure="swell")
s.stroke([(0.300,0.250),(0.316,0.180),(0.360,0.146)], "bristle", "mug_wt",
         size=0.014, load=1.0, pressure="taper")
print("edges", s.stroke_count)
# h) cut the table back up to the silhouette - the edge is where two masses meet
s.stroke([(0.276,0.268),(0.288,0.400),(0.308,0.530),(0.336,0.650)], "flat",
         "wood_l2", size=0.042, load=1.0, pressure="even")
s.stroke([(0.286,0.212),(0.316,0.160),(0.366,0.128),(0.430,0.106)], "flat",
         "wood_l2", size=0.038, load=1.0, pressure="even")
s.stroke([(0.500,0.098),(0.570,0.110),(0.616,0.140),(0.640,0.190)], "flat",
         "wood_lit", size=0.036, load=1.0, pressure="even")
s.stroke([(0.640,0.230),(0.636,0.300),(0.628,0.400)], "flat", "wood_lit",
         size=0.030, load=1.0, pressure="even")
s.stroke([(0.626,0.470),(0.606,0.560),(0.584,0.628)], "flat", "sh_soft",
         size=0.032, load=1.0, pressure="even")
print("total", s.stroke_count)
print(s.look(reference=R, region=span("C1","G7")))
