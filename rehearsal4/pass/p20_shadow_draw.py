"""Pass B - the cast shadow (still a far mass, the mug stands in front of it),
then the pencil drawing on top of it, before any near paint."""
p = s.palette
p["shad_soft"] = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.5), 0.5)
p["shad_core"] = p.desaturate(p.mix("burnt_umber", "viridian", 0.1), 0.25)
p["shad_hand"] = p.mix(p["shad_soft"], p["table_lit"], 0.45)
for n in ("shad_soft", "shad_core", "shad_hand"):
    print(f"{n:10s} {p.hex(p[n])} v={p.value_of(p[n]):.2f}")

s.dry()
# penumbra first, wide and soft-shaped
s.block_in(ellipse(Region(0.275, 0.560, 0.665, 0.875), rotate=-6), "bristle",
           "shad_soft", direction=(-20, 62), density=0.85, size=0.13, load=1.0)
print("penumbra:", s.stroke_count)

# the core of the shadow, hugging the base of the mug
core = polygon([(0.325, 0.655), (0.335, 0.720), (0.372, 0.782), (0.430, 0.812),
                (0.500, 0.808), (0.560, 0.775), (0.598, 0.718), (0.610, 0.658),
                (0.580, 0.610), (0.480, 0.590), (0.390, 0.598), (0.345, 0.622)])
s.block_in(core, "bristle", "shad_core", direction=(-14, 70), density=0.9,
           size=0.11, load=1.0)
print("core:", s.stroke_count)

# the handle throws a smaller, much lighter one to the right
s.block_in(ellipse(Region(0.600, 0.482, 0.712, 0.588), rotate=-14), "bristle",
           "shad_hand", direction=(-22,), density=0.8, size=0.05, load=0.8)
print("handle shadow:", s.stroke_count)

# ---- the drawing -------------------------------------------------------
mug = [(0.304, 0.247), (0.322, 0.180), (0.358, 0.138), (0.412, 0.114),
       (0.470, 0.107), (0.528, 0.120), (0.578, 0.148), (0.612, 0.196),
       (0.628, 0.268), (0.622, 0.372), (0.608, 0.498), (0.591, 0.624),
       (0.5625, 0.670), (0.500, 0.706), (0.430, 0.712), (0.372, 0.666),
       (0.352, 0.625), (0.334, 0.500), (0.3206, 0.375), (0.304, 0.247)]
s.pencil(mug, pressure=0.7)

inside = [(0.336, 0.258), (0.352, 0.200), (0.395, 0.160), (0.450, 0.140),
          (0.515, 0.145), (0.565, 0.175), (0.594, 0.225), (0.590, 0.268),
          (0.545, 0.297), (0.470, 0.313), (0.400, 0.300), (0.355, 0.280),
          (0.336, 0.258)]
s.pencil(inside, pressure=0.6)

handle = [(0.628, 0.290), (0.672, 0.300), (0.706, 0.336), (0.716, 0.388),
          (0.702, 0.446), (0.664, 0.484), (0.612, 0.497)]
s.pencil(handle, pressure=0.6)
handle_in = [(0.626, 0.322), (0.660, 0.334), (0.682, 0.372), (0.676, 0.418),
             (0.648, 0.452), (0.614, 0.464)]
s.pencil(handle_in, pressure=0.5)

crew = [(0.372, 0.428), (0.398, 0.407), (0.462, 0.400), (0.500, 0.412),
        (0.511, 0.448), (0.511, 0.487), (0.556, 0.490), (0.556, 0.588),
        (0.512, 0.592), (0.510, 0.640), (0.500, 0.670), (0.470, 0.672),
        (0.462, 0.628), (0.440, 0.628), (0.434, 0.674), (0.398, 0.674),
        (0.378, 0.648), (0.366, 0.560), (0.362, 0.482), (0.372, 0.428)]
s.pencil(crew, pressure=0.65)
s.pencil([(0.372, 0.462), (0.392, 0.450), (0.428, 0.452), (0.442, 0.470),
          (0.436, 0.492), (0.400, 0.497), (0.376, 0.486), (0.372, 0.462)],
         pressure=0.5)

spoon = [(0.508, 0.000), (0.512, 0.090), (0.518, 0.175), (0.530, 0.232),
         (0.548, 0.278), (0.566, 0.308)]
s.pencil(spoon, pressure=0.7)

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(region=span("C2", "F6"), reference="ref.jpg"))
