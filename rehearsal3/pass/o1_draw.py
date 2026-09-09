# own painting, pass 1 - my own pencil. No reference, no sketch().
# Subject: LOW TIDE. A wide estuary at dusk - a big luminous sky, a low dark
# headland on the left horizon, wet sand mirroring the sky in ribbons, and
# three old mooring posts standing in it.
# Chosen for what this engine does well and badly: soft horizontal masses and
# long directional bristle strokes are its strength; hard geometry stair-steps.
# Value plan (three separated masses, no near-black needed):
#   LIGHT  sky glow above the horizon 0.88, its mirror in the sand 0.80
#   MID    foreground sand 0.48-0.62, sky top 0.60
#   DARK   headland 0.26, posts 0.23
p = s.palette

HZ = 0.425

s.mark("hz_l",   0.020, 0.432)
s.mark("hz_r",   0.980, 0.418)
s.mark("land_r", 0.615, 0.421)
s.mark("post_a", 0.216, 0.296)
s.mark("foot_a", 0.223, 0.618)
s.mark("foot_b", 0.306, 0.590)
s.mark("foot_c", 0.658, 0.545)

# horizon, not level and not straight
s.pencil([(0.00, 0.433), (0.25, 0.428), (0.50, 0.424), (0.75, 0.421), (1.00, 0.418)])
# the headland's profile - low, ragged, dying away to the right
s.pencil([(0.00, 0.386), (0.08, 0.379), (0.17, 0.392), (0.26, 0.384),
          (0.35, 0.396), (0.44, 0.400), (0.52, 0.410), (0.585, 0.417),
          (0.615, 0.421)])
# the three posts
s.pencil([(0.213, 0.296), (0.219, 0.450), (0.223, 0.618)])
s.pencil([(0.229, 0.300), (0.233, 0.618)])
s.pencil([(0.302, 0.362), (0.306, 0.590)])
s.pencil([(0.655, 0.437), (0.658, 0.545)])
# their reflections, broken and wandering
s.pencil([(0.222, 0.622), (0.226, 0.700), (0.218, 0.790), (0.228, 0.880)])
s.pencil([(0.306, 0.594), (0.300, 0.660), (0.308, 0.730)])
s.pencil([(0.658, 0.549), (0.654, 0.596), (0.660, 0.640)])
# ribbons of wet sand - the drawing that carries the foreground
s.pencil([(0.00, 0.520), (0.28, 0.505), (0.62, 0.512), (1.00, 0.498)])
s.pencil([(0.00, 0.596), (0.30, 0.612), (0.66, 0.588), (1.00, 0.602)])
s.pencil([(0.00, 0.700), (0.34, 0.672), (0.70, 0.706), (1.00, 0.686)])
s.pencil([(0.00, 0.830), (0.36, 0.868), (0.72, 0.812), (1.00, 0.844)])
# a channel curving in from the bottom left
s.pencil([(0.00, 0.960), (0.20, 0.900), (0.46, 0.836), (0.70, 0.790),
          (0.90, 0.760)])
# a bar of cloud
s.pencil([(0.06, 0.196), (0.34, 0.176), (0.62, 0.202), (0.88, 0.184)])
s.pencil([(0.30, 0.286), (0.58, 0.276), (0.84, 0.294)])

print("strokes:", s.stroke_count)
print(s.look())
