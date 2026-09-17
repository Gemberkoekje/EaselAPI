# Furthest first. A bristle at low density for the tunnel so the warm ground keeps
# breathing through it, and an arch whose edge runs oblique and down the left.
s.block_in(Region(-0.04, -0.05, 1.04, 0.885), "bristle", "tunnel",
           size=0.16, density=0.65, direction=(14, 100))

s.block_in(archband(), "bristle", "mag_lo",
           size=0.11, density=0.75, direction=(160, 28))

s.block_in(archcore(), "bristle", "mag_hi",
           size=0.06, density=0.55, direction=(148, 40))
print(s.look())
