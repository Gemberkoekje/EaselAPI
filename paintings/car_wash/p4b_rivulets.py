# Rivulets, three of them, each made of two marks: a soft wet trail from a starved
# bristle and a thin catch-light laid inside it. Ten single lines read as scratches.
s.stroke([(0.492, 0.385), (0.470, 0.590), (0.499, 0.778)], "bristle", "haze",
         size=0.020, opacity=0.30, load=0.50, pressure="taper")
s.stroke([(0.487, 0.400), (0.466, 0.592), (0.494, 0.760)], "liner", "foam",
         size=0.0045, pressure=[0.80, 1.0, 0.18])

s.stroke([(0.177, 0.598), (0.157, 0.764)], "bristle", "haze",
         size=0.016, opacity=0.28, load=0.45, pressure="lift_off")
s.stroke([(0.172, 0.612), (0.154, 0.752)], "liner", "foam",
         size=0.0040, pressure=[0.40, 1.0])

s.stroke([(0.737, 0.248), (0.718, 0.432)], "bristle", "frame_lt",
         size=0.014, opacity=0.32, load=0.40, pressure="taper")
s.stroke([(0.731, 0.262), (0.713, 0.424)], "liner", "foam_hi",
         size=0.0035, pressure=[0.30, 1.0])

# Two more, faint, in the quiet lower middle -- present, not announced.
s.stroke([(0.623, 0.598), (0.604, 0.736)], "liner", "cyan_md",
         size=0.0035, opacity=0.55, pressure="taper")
s.stroke([(0.554, 0.470), (0.537, 0.598)], "liner", "cyan_md",
         size=0.0030, opacity=0.45, pressure="lift_off")
print(s.look())
