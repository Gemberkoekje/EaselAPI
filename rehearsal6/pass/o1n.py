s.dry()
# three evenly-spaced hanging bars is a machine's idea of virga. Keep one.
s.stroke([(0.655,0.422),(0.775,0.462),(0.865,0.450)], "round_hard", "squall2",
         size=0.078, load=1.0, opacity=0.92, pressure="even")
s.stroke([(0.845,0.396),(0.965,0.430),(1.03,0.420)], "round_hard", "squall2",
         size=0.072, load=1.0, opacity=0.92, pressure="even")
s.stroke([(0.715,0.496),(0.800,0.505)], "round_hard", "rain", size=0.042, load=1.0,
         opacity=0.8, pressure="swell")
s.stroke([(0.895,0.474),(0.975,0.482)], "round_hard", "rain", size=0.036, load=1.0,
         opacity=0.75, pressure="swell")
s.stroke([(0.568,0.548),(0.596,0.582)], "round_hard", "mid1", size=0.030, load=1.0,
         opacity=0.50, pressure="taper")
print("total", s.stroke_count)
print(s.look())
