p = s.palette
s.dry()
# the three hanging bars are not cloud - break them back into the sky
s.stroke([(0.52,0.290),(0.66,0.318),(0.78,0.300)], "bristle", "squall", size=0.075,
         load=1.0, opacity=0.65, pressure="swell")
s.stroke([(0.80,0.268),(0.94,0.286),(1.03,0.272)], "bristle", "squall", size=0.065,
         load=1.0, opacity=0.60, pressure="taper")
s.stroke([(0.56,0.372),(0.72,0.352),(0.88,0.330)], "bristle", "rain", size=0.038,
         load=1.0, opacity=0.40, pressure="swell")
s.stroke([(0.90,0.330),(1.03,0.310)], "bristle", "rain", size=0.030, load=1.0,
         opacity=0.35, pressure="taper")
# the last of the confetti
s.stroke([(0.56,0.752),(0.70,0.762)], "bristle", "water_m", size=0.040, load=1.0,
         opacity=0.95, pressure="even")
s.stroke([(0.58,0.792),(0.70,0.800)], "bristle", "water_m", size=0.030, load=1.0,
         opacity=0.90, pressure="even")
s.stroke([(0.48,0.716),(0.60,0.722)], "bristle", "water_m", size=0.026, load=1.0,
         opacity=0.85, pressure="taper")
print("total", s.stroke_count)
s.stroke([(0.036,0.938),(0.050,0.964),(0.078,0.922)], "liner", "rain", size=0.006,
         load=1.0, pressure=[0.9,1.0,0.4], note="signature")
print(s.look())
print(s.look(values=True))
