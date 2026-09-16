s.dry()
# (A glaze to mute the one pale column on the deck was rehearsed and dropped: at
#  0.30 it landed darker than the deck around it and read as a post. The streak
#  stays -- it is a wet mark on a wet deck, which is what it was for.)

# and the last formless patch of water, on the near left
s.glaze([(0.160, 0.762), (0.260, 0.800), (0.340, 0.822)], p.at_value("water", 0.50),
        opacity=0.30, size=0.065, pressure="swell", note="subject")
s.glaze([(0.122, 0.742), (0.182, 0.772)], p.at_value("water", 0.47),
        opacity=0.26, size=0.050, pressure="taper", note="subject")
s.stroke([(0.202, 0.726), (0.282, 0.743)], "bristle", p.at_value("water", 0.70),
         size=0.028, load=0.32, opacity=0.60, load_falloff=0.4, pressure="swell",
         note="subject")
s.stroke([(0.262, 0.784), (0.322, 0.796)], "bristle", p.at_value("water", 0.74),
         size=0.026, load=0.26, opacity=0.50, load_falloff=0.45, pressure="taper",
         note="subject")
print(s.look())
