# Pass 9. The weakest passage, named from the greyscale and confirmed by cropping
# into it: the left third. The facade's left edge is raw vertical combing running
# off the canvas, the pier between it and the window is a flat dark with an even
# all-over speckle and no incident whatever, and the bottom-left corner has one
# streak in it. It is the mass nobody made me draw, which is exactly the one the
# guide says will give me away -- so the last third of the budget goes here.
s.dry()

# Two flyers taped to the pier. A short flat stroke is a rectangle with chisel ends,
# which is the wrong mark for almost everything and the right one for a sheet of
# paper stuck to a wall -- so for once the tool's own geometry is the thing itself.
s.stroke([(0.0885, 0.4155), (0.1265, 0.4125)], "flat",
         p.at_value("facade_lt", 0.250), size=0.030, load=1.0, load_falloff=0.0,
         opacity=0.95, pressure="even", jitter=0.004, note="pier flyer")
s.stroke([(0.1075, 0.4805), (0.1330, 0.4775)], "flat",
         p.at_value("facade_lt", 0.212), size=0.022, load=1.0, load_falloff=0.0,
         opacity=0.90, pressure="even", jitter=0.004, note="pier flyer")
# the upper one has curled off the wall along its top edge and catches the window
s.stroke([(0.0900, 0.4020), (0.1240, 0.3995)], "round_hard",
         p.at_value("spill_cool", 0.355), size=0.0045, opacity=0.8, load=1.0,
         load_falloff=0.0, pressure=[0.25, 1.0, 0.15], note="pier flyer")

# A soil pipe, which answers the downpipe on the right without repeating it: it is
# shorter, it stops at a bracket instead of running the whole height, and it is on
# the shadow side so it reads by a hair rather than a value.
s.stroke([(0.0705, 0.5245), (0.0685, 0.6150), (0.0715, 0.7020)], "bristle",
         p.at_value("facade_lt", 0.238), size=0.011, load=0.9, opacity=0.70,
         jitter=0.02, pressure="even", note="pier pipe")
s.stroke([(0.0595, 0.5320), (0.0825, 0.5305)], "flat",
         p.at_value("facade_lt", 0.262), size=0.010, load=1.0, load_falloff=0.0,
         opacity=0.85, pressure="even", note="pier pipe")

# The raw combing at the canvas edge: four marks crossing it at four angles, which
# is the fix for a surface whose grain has come out as a row of parallel strokes.
# Three marks that describe a texture beat thirty that repeat it.
for pts, sz, val, ld, op in (
        ([(-0.04, 0.268), (0.038, 0.300), (0.092, 0.286)], 0.034, 0.215, 0.75, 0.50),
        ([(0.088, 0.360), (0.020, 0.392), (-0.04, 0.386)], 0.026, 0.150, 0.70, 0.45),
        ([(-0.04, 0.512), (0.046, 0.478), (0.098, 0.498)], 0.030, 0.200, 0.80, 0.45),
        ([(0.074, 0.628), (0.018, 0.652), (-0.04, 0.640)], 0.022, 0.235, 0.70, 0.40)):
    s.stroke(pts, "bristle", p.at_value("facade_lt", val), size=sz, load=ld,
             opacity=op, pressure="swell", note="pier surface")

# The seam where the wall meets the sidewalk runs dead straight across this side.
# One mark across it, in a value between, to take the ruled look off it.
s.stroke([(0.020, 0.694), (0.086, 0.712), (0.152, 0.700)], "bristle",
         p.mix("facade", "kerb", 0.45), size=0.024, load=0.70, opacity=0.45,
         pressure="swell", note="pier surface")

# ---------------------------------------------------------------- the puddle
# The bottom-left corner gets the one thing the foreground does not have yet: a
# puddle, which reflects the SKY rather than the shop, so it is the coolest and
# quietest light in the picture and it balances the sodium on the far right. It also
# says the road is wet, which everything else here has been asserting.
# Rebuilt. The first one was a tall soft blob at 0.33 and read as a pale amoeba
# against a 0.21 road. The reason recorded at the time -- that relief lifts a solid
# mass off its planned value -- was measured in #33 and is false; what was
# actually wrong is that 0.33 is simply too light for a night puddle, which is a
# judgement about the subject and not about the engine. Mixed lower, and shallow,
# because a puddle seen from across a street is a long flat sliver rather than a
# shape with a width.
puddle = polygon([(0.046, 0.9280), (0.098, 0.9155), (0.164, 0.9185),
                  (0.214, 0.9330), (0.166, 0.9600), (0.092, 0.9585),
                  (0.052, 0.9455)]).smooth(1)
s.block_in(puddle, "flat", p.at_value("sky_lo", 0.235), density=1.0, solid=True,
           size=0.013, direction="axis", overhang=0.25, note="puddle")
# its near edge catches a little more, and one streak of the shop's light reaches
# across it -- the two lights meeting, which is the whole picture in one mark
s.stroke([(0.058, 0.9530), (0.112, 0.9605), (0.170, 0.9500)], "round_hard",
         p.at_value("sky_lo", 0.355), size=0.0045, opacity=0.85, load=1.0,
         load_falloff=0.0, pressure=[0.15, 1.0, 0.25], note="puddle")
s.stroke([(0.176, 0.9215), (0.150, 0.9370), (0.126, 0.9530)], "bristle",
         p.at_value("refl_hi", 0.330), size=0.011, load=0.9, load_falloff=0.25,
         opacity=0.50, pressure=[0.9, 0.5, 0.0], note="puddle")
# and a wet rim outside it, so it sits in the road rather than on it
s.stroke([(0.034, 0.9115), (0.106, 0.9015), (0.200, 0.9145)], "bristle",
         p.at_value("kerb", 0.248), size=0.015, load=0.75, opacity=0.45,
         pressure="swell", note="puddle")
print(s.budget_line())
