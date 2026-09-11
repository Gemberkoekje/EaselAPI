# The boundary between the arch light and the tunnel runs along row 3 and had started
# to read as a waterline. Three marks cross it; that is what a boundary needs, not a
# softer version of itself.
s.stroke([(0.444, 0.196), (0.430, 0.398)], "bristle", "haze",
         size=0.030, load=0.70, opacity=0.55, pressure="taper")
s.stroke([(0.648, 0.258), (0.692, 0.322)], "bristle", "foam",
         size=0.026, load=0.55, opacity=0.62, pressure="swell")
s.stroke([(0.492, 0.240), (0.476, 0.356), (0.488, 0.428)], "bristle", "cyan_md",
         size=0.019, load=0.55, opacity=0.50, pressure="lift_off")

# The upper left had gone flat. Soap sliding down the inside of the arch.
s.stroke([(0.146, 0.094), (0.216, 0.136)], "bristle", "foam",
         size=0.030, load=0.55, opacity=0.60, pressure="swell")
s.stroke([(0.120, 0.048), (0.104, 0.262)], "bristle", "mag_hi",
         size=0.022, load=0.45, opacity=0.45, pressure="taper")
s.stroke([(0.238, 0.052), (0.296, 0.088)], "bristle", "mag_hi",
         size=0.017, load=0.40, opacity=0.40, pressure="lift_off")

# Highlights. Six marks, and the picture has to be finished before them.
s.stroke([(0.806, 0.104), (0.786, 0.196), (0.796, 0.288)], "round_hard", "foam_hi",
         size=0.011, opacity=0.68, pressure=[0.2, 1.0, 0.25])  # the brush's lit ridge
s.stroke([(0.302, 0.428), (0.354, 0.416)], "round_hard", "foam_hi",
         size=0.008, opacity=0.90, pressure=[1.0, 0.2])        # the bloom's core
# Two bright dabs were tried here and taken out. At this scale a dab is a disc and
# reads as one, whatever it is meant to be.
s.stroke([(0.571, 0.333), (0.586, 0.336)], "round_hard", "hot_core",
         size=0.010, opacity=0.95, pressure=[1.0, 0.4])        # the stop light
print(s.look())
