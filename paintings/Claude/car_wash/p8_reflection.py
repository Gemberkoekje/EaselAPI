# The screen reflects the top of the dash: a pale band lying along the cowl, fading
# upward. It does three jobs at once -- it fills the quietest part of the glass, it
# ties the dash to the screen, and its lower half laps onto the cowl and loses the
# hard edge that two smudges had made a mess of.
s.stroke([(0.495, 0.850), (0.662, 0.862), (0.858, 0.806), (1.025, 0.732)],
         "bristle", "haze", size=0.046, load=0.80, opacity=0.58, pressure="swell")
s.stroke([(0.612, 0.828), (0.790, 0.800), (0.930, 0.746)],
         "bristle", "cyan_md", size=0.019, load=0.70, opacity=0.52, pressure="taper")
# The one place round_soft earns its keep: a reflection fades upward, and above
# size 0.05 this tip airbrushes, which is exactly the mark wanted here and nowhere else.
s.stroke([(0.520, 0.796), (0.700, 0.808), (0.890, 0.752), (1.030, 0.688)],
         "round_soft", "haze", size=0.055, opacity=0.17, pressure="swell")
s.stroke([(0.028, 0.792), (0.086, 0.772)],
         "bristle", "haze", size=0.026, load=0.60, opacity=0.45, pressure="lift_off")

# The stop light bleeding down the wet glass, so it is part of the picture and not a
# dot sitting in it.
s.stroke([(0.578, 0.358), (0.566, 0.512), (0.574, 0.616)], "bristle", "hot",
         size=0.020, load=0.45, opacity=0.26, pressure="lift_off")
s.stroke([(0.572, 0.362), (0.564, 0.470)], "liner", "hot_core",
         size=0.0045, opacity=0.35, pressure=[1.0, 0.1])

# Two low-contrast marks so the quiet passage is quiet rather than flat.
s.stroke([(0.665, 0.452), (0.652, 0.706)], "bristle", "tunnel",
         size=0.038, load=0.50, opacity=0.30, pressure="taper")
s.stroke([(0.700, 0.548), (0.688, 0.768)], "bristle", "haze",
         size=0.016, load=0.35, opacity=0.22, pressure="swell")
print(s.look())
