# edge="clean" insets the fill by half a brush, so the extreme bottom corners kept a
# sliver of bare ground. One pass with the correction recipe -- solid tip, full load,
# no falloff, both ends off the canvas so no chisel end stops inside the picture.
s.stroke([(-0.06, 0.972), (1.06, 0.984)], "flat", "frame", size=0.075,
         load=1.0, load_falloff=0.0, opacity=1.0, pressure="even")

# Knock back a speckled patch of the reflection that had stranded itself on the pillar.
# A flat here left its chisel end standing in the glass. A round tip declares no
# axis and has no chisel, which is the whole reason to reach for one.
s.stroke([(-0.020, 0.812), (0.084, 0.792)], "round_soft", "frame", size=0.042,
         opacity=0.55, pressure="lift_off")

# Two flecks thrown off the leading edge, worked outward from the silhouette rather
# than dropped into the gap. Kept at foam rather than foam_hi: this is incident, and
# the picture already has as many bright accents as it can carry.
s.stroke([(0.716, 0.238), (0.672, 0.214)], "bristle", "foam",
         size=0.013, load=0.35, opacity=0.65, pressure="lift_off")
s.stroke([(0.729, 0.486), (0.681, 0.524)], "bristle", "foam",
         size=0.010, load=0.30, opacity=0.55, pressure="lift_off")
print(s.look())
