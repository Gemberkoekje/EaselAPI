# Pass 5. The second of the hollow thing's three depths: what is inside it.
# The bays are used to keep the reading clear -- machines in the two left bays, the
# person in the right one, with a mullion between them so they do not run together.
s.dry()

# The folding table in the right bay. It goes down first because the figure sits in
# front of it, and that overlap is what will put the figure inside the shop rather
# than on the glass.
s.stroke([(0.628, 0.5150), (0.678, 0.5125), (0.719, 0.5140)], "flat",
         p.at_value("mach_hi", 0.620), size=0.011, load=1.0, load_falloff=0.0,
         opacity=0.85, pressure="press_in", note="subject table")
s.stroke([(0.620, 0.536), (0.670, 0.532), (0.719, 0.535)], "bristle",
         p.at_value("machine", 0.585), size=0.030, load=0.85, opacity=0.6,
         pressure="swell", note="subject table")

# The run of machines: one plane at one value, with the doors laid on it after.
# edge="clean" and almost no overhang: at 0.3 the pass ends wobbled past the top of
# the run and it came back a row of stepped fragments, which reads as damage rather
# than as machines. A solid tip, so the drawn contour is the right tool here.
s.block_in(machine_band(), "flat", p.at_value("machine", 0.490), density=1.0,
           solid=True, size=0.024, direction="axis", overhang=0.1, edge="clean",
           note="subject machines")
# the lit top edge of the run, and the dark recess at its foot
s.stroke([(0.176, 0.5180), (0.286, 0.5140)], "flat", "mach_hi",
         size=0.010, load=1.0, load_falloff=0.0, opacity=0.85, pressure="lift_off",
         note="subject machines")
s.stroke([(0.352, 0.5125), (0.462, 0.5165), (0.549, 0.5200)], "flat",
         p.at_value("mach_hi", 0.620), size=0.008, load=1.0, load_falloff=0.0,
         opacity=0.75, pressure=[0.3, 1.0, 0.5], note="subject machines")
s.stroke([(0.180, 0.6015), (0.365, 0.6045), (0.550, 0.6010)], "bristle", "mach_dk",
         size=0.016, load=0.9, opacity=0.7, pressure=[0.4, 1.0, 0.6],
         note="subject machines")
# the floor in the right bay, so the chair has something to stand on
s.stroke([(0.556, 0.5975), (0.640, 0.5995), (0.716, 0.5960)], "bristle",
         p.at_value("machine", 0.470), size=0.022, load=0.85, opacity=0.6,
         pressure="swell", note="subject floor")

# Measured: laid straight onto the wet band, these came back 0.443 against the
# 0.33 they were mixed at -- the dark sank into the light and the glass stopped
# reading as glass. The band has to set first.
s.dry()

# The doors. These really are discs, so they are laid as discs and stopped -- but
# four dabs from a round tip are four copies of one silhouette to within 7%, so
# every one of them differs in size, in value, and in how much outline the tip
# redraws. The leftmost is the faintest, and it is the one allowed to go soft.
for x, y, size, val, wob in ((0.228, 0.5545, 0.035, 0.365, 0.45),
                             (0.305, 0.5580, 0.038, 0.305, 0.15),
                             (0.392, 0.5525, 0.033, 0.340, 0.30),
                             (0.475, 0.5595, 0.036, 0.320, 0.00)):
    s.dab(x, y, "round_hard", p.at_value("mach_dk", val), size=size, press=3,
          tip_wobble=wob, note="subject doors")
# one of them has something light turning behind the glass, and one has a rim of
# chrome catching the tubes. One difference each; the recipe repeated is the tell.
s.dab(0.3065, 0.5605, "round_hard", p.at_value("machine", 0.560), size=0.016,
      press=3, tip_wobble=0.55, note="subject doors")
s.stroke([(0.4585, 0.5495), (0.4700, 0.5455), (0.4860, 0.5520)], "round_hard",
         "mach_hi", size=0.006, opacity=0.9, load=1.0, load_falloff=0.0,
         pressure=[0.1, 0.9, 0.15], note="subject doors")

# The figure. Backlit, so it is very nearly a flat silhouette, and the whole point
# of it is the edge: 0.24 against a 0.82 wall is the strongest contrast anywhere in
# the picture, which is where a viewer will look. Dry first, or the dark would sink
# into the wet wall and come back a mid grey.
s.dry()
# ...and mixed below its planned value, because the same sinking measured 0.290 out
# of a 0.24 silhouette. 0.185 in lands on 0.24 seen.
s.block_in(figure(), "flat", p.at_value("figure", 0.185), density=1.0, solid=True,
           size=0.013, direction="axis", edge="clean", note="subject figure")
print(s.budget_line())
