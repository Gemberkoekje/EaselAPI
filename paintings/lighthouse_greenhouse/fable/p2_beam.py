# Pass 2: the beam, on the fog and before the tower. Light in the air is what
# the soft round tip's airbrush is for, so it is three glazes along the beam's
# axis and nothing else. A round tip's width follows pressure, so the two bright
# ones start at full pressure at the lamp and thin toward the far end, and the
# wide faint one does the opposite, so the cone is narrow and bright where it
# leaves the lamp room and wide and dissolving by the left edge. The glazes are
# mixed close to the fog: a glaze far from what it lands on has no usable
# opacity. Four versions were rehearsed first -- a bristle block-in of the
# wedge came back as a ribbed slab, five flat strokes as a fan of ribbons, and
# the first glazes were lime and brightest at the wrong end.
p["beam_far"]  = p.at_value(p.mix("fog", "beam", 0.50), 0.74)
p["beam_body"] = p.at_value(p.mix("beam", "fog", 0.25), 0.78)
s.dry()
s.glaze([(0.64, 0.24), (0.30, 0.335), (-0.08, 0.42)], "beam_far", opacity=0.09, size=0.20,
        pressure=[0.4, 0.8, 1.0], note="subject beam, wide and faint")
s.glaze([(0.64, 0.24), (0.30, 0.33), (-0.08, 0.41)], "beam_body", opacity=0.15, size=0.11,
        pressure=[1.0, 0.8, 0.4], note="subject beam, body")
s.glaze([(0.64, 0.24), (0.42, 0.295), (0.18, 0.355)], "beam_core", opacity=0.17, size=0.06,
        pressure=[1.0, 0.7, 0.12], note="subject beam, core")
print(s.look(values=True))
print(s.look())
