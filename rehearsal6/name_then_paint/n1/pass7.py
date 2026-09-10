# Pass 7 - raise the table's far edge clear of the pot rim, then redraw larger.
p = s.palette
p["tbl_far"] = p.mix(p["tbl"], p.mix("ultramarine","burnt_umber",0.5), 0.42)
print("tbl_far", p.hex(p["tbl_far"]), round(p.value_of(p["tbl_far"]),3))
s.dry()

tbl_mass = polygon([(0.0, 0.628), (0.35, 0.636), (0.72, 0.648), (1.0, 0.658),
                    (1.0, 1.0), (0.0, 1.0)])
s.block_in(tbl_mass, "flat", "tbl", direction=(5, 169), density=1.0, size=0.11,
           load=1.0, pressure="even", overhang=0)
# the far strip of the table sits back
s.block_in(polygon([(0.0,0.628),(0.35,0.636),(0.72,0.648),(1.0,0.658),
                    (1.0,0.706),(0.55,0.700),(0.0,0.686)]),
           "flat", "tbl_far", direction=(4, 171), density=1.0, size=0.055,
           load=1.0, pressure="even", overhang=0)
s.block_in(polygon([(0.72, 0.648), (1.0, 0.658), (1.0, 1.0), (0.88, 1.0)]), "flat",
           "tbl_dk", direction=(26, 138), density=1.0, size=0.09, load=1.0,
           pressure="even", overhang=0)
s.block_in(polygon([(0.0,0.845),(0.22,0.812),(0.47,0.845),(0.52,0.95),(0.30,1.0),(0.0,1.0)]),
           "flat", "tbl_lit", direction=(9, 163), density=1.0, size=0.09,
           load=1.0, pressure="even", overhang=0)
s.block_in(polygon([(0.03,0.905),(0.20,0.878),(0.33,0.94),(0.26,1.0),(0.05,1.0)]),
           "flat", "tbl_hi", direction=(14, 158), density=1.0, size=0.07,
           load=1.0, pressure="even", overhang=0)

# --- redraw, bigger ------------------------------------------------------------
s.erase()
s.mark("bl_a", 0.436, 0.430); s.mark("bl_b", 0.646, 0.512)
s.mark("bl_c", 0.398, 0.588); s.mark("bud",  0.556, 0.368)

s.pencil([s.pt("rim_l"), (0.360, 0.652), (0.420, 0.650), (0.478, 0.658), s.pt("rim_r")])
s.pencil([s.pt("rim_l"), (0.360, 0.688), s.pt("rim_f"), (0.478, 0.690), s.pt("rim_r")])
s.pencil([(0.324, 0.694), (0.366, 0.716), s.pt("rim_f"), (0.472, 0.718), (0.512, 0.700)])
s.pencil([(0.324, 0.694), (0.336, 0.780), s.pt("base_l")])
s.pencil([(0.512, 0.700), (0.498, 0.782), s.pt("base_r")])
s.pencil([s.pt("base_l"), (0.400, 0.878), (0.446, 0.877), s.pt("base_r")])
s.pencil([(0.372, 0.708), (0.384, 0.752), (0.374, 0.790), (0.390, 0.834), (0.386, 0.862)],
         pressure=0.75)

s.pencil([(0.336,0.492),(0.356,0.398),(0.440,0.348),(0.522,0.372),(0.552,0.320),
          (0.626,0.342),(0.690,0.404),(0.752,0.458),(0.774,0.534),(0.728,0.606),
          (0.640,0.634),(0.552,0.616),(0.468,0.648),(0.382,0.650),(0.322,0.590),
          (0.316,0.528),(0.336,0.492)])
for c, rx, ry in ((s.pt("bl_a"), 0.094, 0.086), (s.pt("bl_b"), 0.106, 0.094),
                  (s.pt("bl_c"), 0.068, 0.058), (s.pt("bud"), 0.048, 0.041)):
    s.pencil(ellipse(Region(c[0]-rx, c[1]-ry, c[0]+rx, c[1]+ry)).closed)

s.pencil([(0.418, 0.640), (0.428, 0.672), (0.424, 0.700)])
s.pencil([(0.520, 0.612), (0.486, 0.660), (0.452, 0.694)])
s.pencil([(0.300, 0.548), (0.250, 0.584), (0.228, 0.632)])
s.pencil([(0.738, 0.580), (0.792, 0.618), (0.824, 0.668)])
s.pencil([(0.560, 0.640), (0.596, 0.678), (0.588, 0.706)])

s.pencil(ellipse(Region(0.578, 0.820, 0.648, 0.856), rotate=-14).closed)
s.pencil(ellipse(Region(0.664, 0.874, 0.742, 0.910), rotate=8).closed)
s.pencil(ellipse(Region(0.756, 0.788, 0.830, 0.824), rotate=-26).closed)

print("strokes:", s.stroke_count)
print(s.look())
