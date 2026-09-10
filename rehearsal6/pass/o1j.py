p = s.palette
s.dry()
# the light is a gap between cloud and sea, not a stripe: bring cloud down over it
s.stroke([(0.56,0.470),(0.60,0.560),(0.585,0.600)], "bristle", "squall2", size=0.055,
         load=1.0, opacity=0.85, pressure="lift_off")
s.stroke([(0.72,0.430),(0.755,0.512),(0.745,0.548)], "bristle", "squall2", size=0.042,
         load=1.0, opacity=0.70, pressure="lift_off")
s.stroke([(0.90,0.380),(0.93,0.452),(0.92,0.500)], "bristle", "squall2", size=0.036,
         load=1.0, opacity=0.60, pressure="lift_off")
s.stroke([(0.62,0.500),(0.86,0.446),(1.02,0.412)], "bristle", "squall2", size=0.030,
         load=1.0, opacity=0.45, pressure="swell")
s.stroke([(0.98,0.470),(1.03,0.530)], "bristle", "rain", size=0.030, load=1.0,
         opacity=0.45, pressure="lift_off")
print("cloud fingers", s.stroke_count)
# cover the confetti the wet paint threw about
s.stroke([(0.46,0.740),(0.66,0.756),(0.86,0.748)], "bristle", "water_m", size=0.060,
         load=1.0, opacity=0.85, pressure="even")
s.stroke([(0.52,0.790),(0.70,0.800)], "bristle", "water_m", size=0.045, load=1.0,
         opacity=0.75, pressure="taper")
s.stroke([(0.54,0.830),(0.72,0.842)], "bristle", "water_d", size=0.035, load=1.0,
         opacity=0.45, pressure="swell")
# the reflection, now that there is clean water to put it on
s.stroke([(0.755,0.722),(0.835,0.726)], "bristle", "glow2", size=0.014, load=1.0,
         opacity=0.85, pressure="swell")
s.stroke([(0.742,0.752),(0.804,0.756)], "bristle", "glow", size=0.012, load=1.0,
         opacity=0.65, pressure="swell")
s.stroke([(0.766,0.788),(0.826,0.792)], "bristle", "water_l", size=0.016, load=1.0,
         opacity=0.55, pressure="taper")
s.stroke([(0.720,0.836),(0.800,0.842)], "bristle", "water_l", size=0.020, load=1.0,
         opacity=0.40, pressure="swell")
print("reflection", s.stroke_count)
# the one small thing that says how big the rest of it is
s.stroke([(0.646,0.694),(0.676,0.695)], "round_hard", "ink", size=0.007, load=1.0,
         pressure="swell")
s.stroke([(0.660,0.694),(0.664,0.672)], "liner", "ink", size=0.005, load=1.0,
         pressure=[1.0,0.2])
s.dab(0.828, 0.692, "round_hard", "blaze", size=0.010, press=3)
print("total", s.stroke_count)
print(s.look())
