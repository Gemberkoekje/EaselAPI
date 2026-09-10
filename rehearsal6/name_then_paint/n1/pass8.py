# Pass 8 - kill the full-width dark band; set the table edge allowing for spill.
p = s.palette
s.dry()

# restore background down over the band
s.block_in(polygon([(0.0,0.40),(1.0,0.40),(1.0,0.655),(0.0,0.635)]), "flat", "bg",
           direction=(37, 127), density=1.0, size=0.09, load=1.0, pressure="even")
s.block_in(polygon([(0.0,0.42),(0.30,0.40),(0.52,0.50),(0.40,0.60),(0.0,0.58)]), "flat",
           "bg_a", direction=(29, 117), density=1.0, size=0.08, load=1.0, pressure="even")

# table: polygon top sits half a brush BELOW the edge I want, spill brings it up
s.block_in(polygon([(0.0,0.658),(0.40,0.672),(1.0,0.692),(1.0,1.0),(0.0,1.0)]),
           "flat", "tbl", direction=(5, 169), density=1.0, size=0.105,
           load=1.0, pressure="even", overhang=0)
# shade only the right half of the far table, running out before it crosses
s.block_in(polygon([(0.46,0.700),(0.78,0.706),(1.0,0.712),(1.0,0.792),(0.62,0.770),(0.44,0.730)]),
           "flat", "tbl_far", direction=(11, 152), density=0.95, size=0.06,
           load=1.0, pressure="even", overhang=0)
s.block_in(polygon([(0.78, 0.700), (1.0, 0.712), (1.0, 1.0), (0.90, 1.0)]), "flat",
           "tbl_dk", direction=(31, 133), density=1.0, size=0.08, load=1.0,
           pressure="even", overhang=0)
s.block_in(polygon([(0.0,0.845),(0.22,0.812),(0.47,0.845),(0.52,0.95),(0.30,1.0),(0.0,1.0)]),
           "flat", "tbl_lit", direction=(9, 163), density=1.0, size=0.085,
           load=1.0, pressure="even", overhang=0)
s.block_in(polygon([(0.03,0.905),(0.20,0.878),(0.33,0.94),(0.26,1.0),(0.05,1.0)]),
           "flat", "tbl_hi", direction=(14, 158), density=1.0, size=0.065,
           load=1.0, pressure="even", overhang=0)

print("strokes:", s.stroke_count)
print(s.look(sketch=False))
