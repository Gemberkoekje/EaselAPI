# Pass 1: the fog, furthest of all and most of the picture. A quiet flat
# underlayer with the ground still breathing through the pass gaps, then the
# gradient as two soft passages rather than bands: a cooler, darker fog at the
# top coming down to the fog value with the bristle (its comb reads as drift),
# and the fog brightening toward the horizon band with the flat, where it is
# thickest and lightest.
s.block_in(fog(), "flat", "fog", size=0.20, density=0.8, direction=(4, 94),
           note="fog underlayer")
s.scumble(fog_upper(), "fog_top", "fog", 8, size=0.13, opacity=0.55, note="fog upper")
s.scumble(fog_lower(), "fog", "fog_low", 8, brush="flat", size=0.13, opacity=0.5,
          note="fog lower")
print(s.look(values=True))
print(s.look())
