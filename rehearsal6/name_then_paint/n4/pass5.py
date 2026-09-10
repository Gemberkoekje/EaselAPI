exec(open("_pal.py").read())
exec(open("_geom.py").read())
s.dry()
s.block_in(GLASS, "flat", "glass", direction=(98, 14), density=1.0,
           size=0.15, pressure="even", load=1.0, load_falloff=0.2)
s.block_in(WALL, "flat", "wall", direction=(104, 20), density=1.0,
           size=0.135, pressure="even", load=1.0, load_falloff=0.2)

hot = polygon([(0.020, 0.0), (0.566, 0.0), (0.556, 0.230), (0.290, 0.200), (0.028, 0.275)])
s.block_in(hot.inset(0.028), "flat", "glass_hot", direction=(8, 96), density=1.0,
           size=0.055, pressure="even", load=1.0)
# lose that join by running the smudge ALONG it
s.smudge([(0.035, 0.272), (0.180, 0.246)], size=0.040)
s.smudge([(0.160, 0.243), (0.330, 0.212)], size=0.036)
s.smudge([(0.310, 0.208), (0.470, 0.222)], size=0.042)
s.smudge([(0.450, 0.226), (0.560, 0.238)], size=0.034)

dk = polygon([(0.930, 0.0), (1.0, 0.0), (1.0, 0.665), (0.945, 0.650)])
s.block_in(dk.inset(0.012), "flat", "wall_dk", direction=(92,), density=1.0,
           size=0.030, pressure="even", load=1.0)
s.smudge([(0.936, 0.03), (0.944, 0.31)], size=0.045)
s.smudge([(0.941, 0.28), (0.950, 0.62)], size=0.045)
print(s.stroke_count)
print(s.look())
