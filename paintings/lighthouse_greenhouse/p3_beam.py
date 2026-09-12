# Pass 3: the beam, on the fog, before the tower -- like the halo in
# PAINTER.md's own worked example, light in the air belongs to the air, so it
# goes down before the thing that casts it.
#
# First attempt used scumble(beam(), ..., direction="vertical") on the wedge
# shape and it was wrong twice over: left to its own default, the brush sized
# itself off the wedge's *width* (3 x extent/n), which is far wider than the
# wedge's own narrow end, so the source bloomed out instead of tapering; and
# the colour -- cadmium_yellow only lightly cut with viridian -- rendered as a
# saturated highlighter streak, not light in fog. Rehearsing it made both
# faults obvious at once.
#
# Second attempt: thirteen vertical cross-section strokes on round_soft,
# joining the wedge's own two edges so the taper came from the geometry. That
# fixed the bloom, but round_soft airbrushes above size 0.05 and mine were
# 0.075 with real gaps between centres -- rehearsed, it came back as a chain
# of separate soft blobs, beads on a string rather than one wedge.
#
# Third attempt: one round_soft stroke down the centreline, its pressure
# tapering size from thin to the wedge's full far width. Rehearsing that came
# back a sun -- round_soft's airbrush spreads a wide pass so thin per unit
# area that the far, wide end all but vanished while the near, narrow end
# (small area, same dabs) stayed solid, so nearly everything visible sat
# close to the source: a disc, not a wedge.
#
# What actually worked: stop asking one brush call to do five different
# widths. The wedge cut into five straight trapezoids, each block_in at its
# *own* matching brush size (roughly a quarter of its local width) and its
# own step of colour from "beam" at the source to "beam_far" at the horizon.
# Ragged edges (the default) let each trapezoid's brush overhang a little
# into its neighbour, which is what actually closes the seams between them --
# clean edges would have drawn five visible trapezoids instead of one wedge.
BEAM_STEPS = [i / 8 for i in range(9)]

def beam_pt(t, top):
    x = 0.478 + t * (1.06 - 0.478)
    y = (0.155 + t * (0.30 - 0.155)) if top else (0.20 + t * (0.72 - 0.20))
    return x, y

def beam_seg(t0, t1):
    return polygon([beam_pt(t0, True), beam_pt(t1, True), beam_pt(t1, False), beam_pt(t0, False)])

for i in range(len(BEAM_STEPS) - 1):
    t0, t1 = BEAM_STEPS[i], BEAM_STEPS[i + 1]
    tmid = (t0 + t1) / 2
    width0 = beam_pt(t0, False)[1] - beam_pt(t0, True)[1]
    width1 = beam_pt(t1, False)[1] - beam_pt(t1, True)[1]
    brush_size = (width0 + width1) / 2 / 4
    colour = p.mix("beam", "beam_far", tmid)
    s.block_in(beam_seg(t0, t1), "flat", colour, size=brush_size, density=1.0,
               solid=True, direction="axis", opacity=0.62, pressure="even",
               note=f"beam segment {i + 1}/{len(BEAM_STEPS) - 1}")

# Five flat trapezoids in a row draw a staircase along both long edges --
# "ragged" softened the seams *between* segments but not this. One smudge
# along each edge's own shape (not a straight line: this boundary bends)
# is what a lost edge actually costs; see PAINTER.md step 5.
top_edge = [beam_pt(t, True) for t in BEAM_STEPS]
bot_edge = [beam_pt(t, False) for t in BEAM_STEPS]
s.smudge(top_edge, note="lose the beam's upper edge")
s.smudge(bot_edge, note="lose the beam's lower edge")
print(s.look(values=True))
print(s.look())
