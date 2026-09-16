# Pass 4: the rock the tower stands on, in front of the sea and behind the
# tower. A solid dark mass with a clean silhouette, then the planes it is made
# of, each a shape at one value, few and broad: the top surfaces taking the
# fog's cool light, the near face on the right a shade warmer, and the spur
# running out to the left lighter and cooler because it is further into the
# fog. The block-in's dark is what is left between them. Then one crevice, the
# undercut below the hump, two dry-brush marks, and the spur's edge against
# the sea lost with one smudge along it and one starved stroke across.
# The first version had a thin top plane laid in eight passes that came back
# as terraces, a warm face at 0.27 that sat on the rock like a slab, and two
# crevices that read as drawn lines.
p["rock_top"]  = p.at_value(p.mix("rock", "fog", 0.35), 0.26)
p["rock_warm"] = p.at_value(p.mix("rock", "burnt_sienna", 0.35), 0.22)
p["rock_spur"] = p.at_value(p.mix("rock", "sea_far", 0.45), 0.31)
p["rock_deep"] = p.at_value("rock", 0.14)

def top_plane():
    return polygon([(0.50, 0.912), (0.56, 0.886), (0.63, 0.878), (0.70, 0.858),
                    (0.77, 0.866), (0.81, 0.842), (0.86, 0.806), (0.93, 0.796),
                    (0.99, 0.818), (1.06, 0.806), (1.06, 0.852), (0.97, 0.862),
                    (0.90, 0.85), (0.85, 0.872), (0.80, 0.905), (0.73, 0.922),
                    (0.65, 0.93), (0.57, 0.944), (0.515, 0.955)])
def spur():
    return polygon([(0.38, 1.06), (0.44, 0.965), (0.50, 0.912), (0.53, 0.925),
                    (0.50, 0.98), (0.47, 1.06)])
def near_face():
    return polygon([(0.86, 0.90), (0.93, 0.865), (1.06, 0.875), (1.06, 1.06), (0.90, 1.06)])

s.block_in(rocks(), "flat", "rock", size=0.045, density=1.0, solid=True, direction="axis",
           edge="clean", note="rock mass")
s.block_in(top_plane(), "flat", "rock_top", size=0.03, density=1.0, solid=True,
           direction="axis", opacity=1.0, pressure="even", note="rock top, cool")
s.block_in(near_face(), "flat", "rock_warm", size=0.035, density=1.0, solid=True,
           direction=20, opacity=1.0, pressure="even", note="near face, warm")
s.block_in(spur(), "flat", "rock_spur", size=0.02, density=1.0, solid=True,
           direction="axis", opacity=1.0, pressure="even", note="the spur, into the fog")
s.stroke([(0.79, 0.87), (0.81, 0.915), (0.815, 0.96)], "round_hard", "rock_deep", size=0.009,
         opacity=0.75, pressure="taper", note="crevice")
s.stroke([(0.87, 0.868), (0.95, 0.862), (1.02, 0.87)], "round_hard", "rock_deep", size=0.008,
         opacity=0.7, pressure="swell", note="undercut below the hump")
s.stroke([(0.89, 0.93), (0.99, 0.965)], "bristle", "rock_lit", size=0.025, load=0.35,
         opacity=0.5, pressure="taper", note="dry brush, warm")
s.stroke([(0.64, 0.905), (0.75, 0.895)], "bristle", "rock_top", size=0.022, load=0.3,
         opacity=0.5, pressure="taper", note="dry brush, top")
s.smudge([(0.38, 1.04), (0.42, 0.985), (0.46, 0.94), (0.50, 0.912)], note="lose the spur's edge")
s.stroke([(0.40, 0.99), (0.45, 0.95), (0.49, 0.925)], "bristle", p.mix("rock_spur", "sea_near", 0.5),
         size=0.025, load=0.5, opacity=0.5, pressure="taper", note="across the spur's edge")
print(s.look(values=True))
print(s.look())
