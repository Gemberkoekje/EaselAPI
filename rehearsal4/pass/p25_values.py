"""Pass J - the seven cells compare() says are out. Fix the masses, not the cells."""
p = s.palette
s.dry()

# E7, F6: my shadow spread too far right and down. Table back over it.
s.block_in(ellipse(Region(0.596, 0.580, 0.845, 0.800)), "flat", "table_lit",
           direction=(-70,), density=1.0, size=0.080, load=1.0)
s.block_in(ellipse(Region(0.482, 0.725, 0.820, 0.940)), "flat", "table_lit",
           direction=(-8,), density=1.0, size=0.080, load=1.0)
print("shadow back:", s.stroke_count)

# E6: lighten the shadow just off the mug's lower right - and that stroke,
# run outside the silhouette, is also what sharpens the mug's edge there
s.stroke([(0.600, 0.618), (0.588, 0.672), (0.556, 0.706)], "flat",
         p.mix(p["shad_pen"], p["table_lit"], 0.55), size=0.042,
         pressure="even", load=1.0, note="cut the base edge")
s.stroke([(0.612, 0.660), (0.598, 0.720), (0.560, 0.762)], "flat",
         p.mix(p["shad_pen"], p["table_lit"], 0.40), size=0.050,
         pressure="even", load=1.0, note="shadow off the base")

# E2, E3: the dark inside has to reach the rim; the rim band was far too fat
tea2 = ellipse(Region(0.330, 0.128, 0.602, 0.324), rotate=-3)
s.block_in(tea2.inset(0.022), "flat", "tea", direction=(-3,), density=1.0,
           size=0.045, load=1.0)
print("tea:", s.stroke_count)

# D4 and the whole figure: he was left milk-chocolate. Darker, and shaped.
crew = polygon([(0.372, 0.428), (0.398, 0.407), (0.462, 0.400), (0.500, 0.412),
                (0.511, 0.448), (0.511, 0.487), (0.556, 0.490), (0.556, 0.588),
                (0.512, 0.592), (0.510, 0.640), (0.500, 0.670), (0.470, 0.672),
                (0.462, 0.628), (0.440, 0.628), (0.434, 0.674), (0.398, 0.674),
                (0.378, 0.648), (0.366, 0.560), (0.362, 0.482)])
s.block_in(crew.inset(0.017), "flat", "crew", direction="axis", density=1.0,
           size=0.036, load=1.0)
print("crew:", s.stroke_count)
s.stroke([(0.451, 0.632), (0.4525, 0.676)], "flat", "mug_face", size=0.013,
         pressure="even", load=1.0, note="leg gap")
s.stroke([(0.379, 0.480), (0.427, 0.468)], "round_hard", "visor", size=0.028,
         pressure="even", load=1.0, note="visor")
s.stroke([(0.393, 0.556), (0.402, 0.618)], "bristle", "crew_warm", size=0.028,
         opacity=0.28, load=1.0, note="warmth in the figure")
print("strokes:", s.stroke_count)
print(s.look())
