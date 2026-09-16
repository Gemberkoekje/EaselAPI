# Pass 1: the sky, furthest of all. A quiet flat underlayer with the ground still
# breathing through the pass gaps, then the gradient as two soft passages rather
# than bands: indigo down to violet with the bristle (its comb reads as thin high
# cloud), violet down to the peach of the horizon with the flat. The afterglow is
# not a shape: six passes that land with no pressure at the left and press on
# toward the right edge, so the sky brightens toward where the sun went down
# without anything having an outline. An inward scumble on an ellipse was
# rehearsed three ways first and came back as a solid yellow sun every time.
s.block_in(sky(), "flat", "sky_mid", size=0.20, density=0.8, direction=(3, 93),
           note="sky underlayer")
s.scumble(sky_upper(), "sky_top", "sky_mid", 8, size=0.13, opacity=0.55, note="sky upper")
s.scumble(sky_lower(), "sky_mid", "sky_low", 8, brush="flat", size=0.13, opacity=0.5,
          note="sky lower")
for i in range(6):
    t = i / 5
    y = 0.445 + t * 0.14
    s.stroke([(0.22 + 0.08 * t, y + 0.006), (0.60, y - 0.004), (1.06, y)], "flat",
             p.mix("sky_low", "glow", t), size=0.085, opacity=0.5, load=1.0,
             load_falloff=0.0, pressure=[0.0, 0.55, 1.0], note=f"afterglow {i + 1}/6")
s.stroke([(0.50, 0.578), (0.80, 0.574), (1.06, 0.576)], "flat",
         p.mix("glow", "glow_core", 0.5), size=0.045, opacity=0.5, load=1.0,
         load_falloff=0.0, pressure=[0.0, 0.7, 1.0], note="afterglow core")
print(s.look(values=True))
print(s.look())
