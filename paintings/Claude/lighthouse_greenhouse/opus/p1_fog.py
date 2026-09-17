# The furthest thing, and most of the canvas: fog. An underlayer with the warm
# ground breathing through it, then the whole field thickened toward the horizon,
# then three drifts so it is weather rather than a gradient.
s.block_in(fog_field(), "bristle", "fog_high", size=0.22, density=0.65,
           direction=(8, 98), note="fog under")

# Starved a little so the passes break and the ground keeps flecking through: a
# passage with no incident at all in it is the flatter-looking mistake.
s.scumble(fog_lower(), "fog_high", "fog_low", 9, load=0.6, note="fog thickening")

s.dry()          # the scumble is nine marks and still wet; drifts laid into it
                 # mix away to nothing, which is what the first rehearsal showed

# Three marks that say the air is moving, rather than thirty that say it is
# striped. No two the same length, value, angle or brush -- and one of them is
# vertical, because a field of horizontals is a stack of bands with a name.
# The bright one sits on the horizon on purpose: it is what loses it.
s.stroke([(0.40, 0.078), (0.72, 0.062), (1.06, 0.052)], "bristle",
         p.at_value("fog_high", 0.48), size=0.062, load=0.55, opacity=0.8,
         pressure="swell", note="drift")
s.stroke([(0.40, 0.566), (0.74, 0.575), (1.06, 0.570)], "bristle",
         p.at_value("fog_warm", 0.77), size=0.048, load=0.70, opacity=0.85,
         pressure=[0.0, 0.95, 0.45], note="drift")
s.stroke([(0.058, 0.212), (0.082, 0.372), (0.094, 0.520), (0.088, 0.596)],
         "bristle", p.at_value("fog_high", 0.50), size=0.034, load=0.50,
         opacity=0.62, pressure="lift_off", note="drift")

print(s.look())
print(s.look(values=True))
