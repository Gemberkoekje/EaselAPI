# Pass 4: the tower, in front of the sky and the headland. First the lamp's light
# in the air, which is on the sky and so goes down before the tower: two glazes,
# a wide faint one and a small warmer one, the airbrush of the soft round tip
# being right for light in the air. (An inward scumble of rings was rehearsed
# first and came back as a dark cloud with a bulb in it.) Then the tower as one
# solid cool mass with a clean silhouette, and its lit face -- the side that looks
# right, toward the glow -- as a second shape on top of it, with one half-strength
# stroke down the join so the terminator turns instead of stepping. (A pass ramp
# across the whole width was rehearsed twice and came back nearly flat, with the
# light on the wrong side once.) Then, top down: the red band in shadow and its
# lit half, the gallery plate, the lit glass, its posts, the cap, and the one
# mark that is the lamp.
def lit_face():
    return polygon([(0.262, 0.632), (0.314, 0.632), (0.299, 0.163), (0.267, 0.163)])

def band_lit_face():
    return polygon([(0.265, 0.374), (0.3045, 0.374), (0.3020, 0.446), (0.266, 0.446)])

s.glaze([(0.19, 0.126), (0.27, 0.122), (0.35, 0.128)], "lamp_glow", opacity=0.22,
        size=0.11, pressure="swell", note="halo, wide")
s.glaze([(0.243, 0.121), (0.297, 0.127)], "lamp", opacity=0.25, size=0.06,
        pressure="swell", note="halo, close")

s.block_in(tower(), "flat", "tower_sh", size=0.02, density=1.0, solid=True,
           direction=90, edge="clean", note="tower mass")
s.block_in(lit_face(), "flat", "tower_lit", size=0.016, density=1.0, solid=True,
           direction=90, opacity=1.0, pressure="even", note="lit face")
s.stroke([(0.2635, 0.625), (0.2665, 0.40), (0.2685, 0.168)], "flat",
         p.mix("tower_sh", "tower_lit", 0.5), size=0.012, opacity=0.6, load=1.0,
         load_falloff=0.0, pressure="even", note="the terminator, softened")
s.block_in(band(), "flat", "band_sh", size=0.02, density=1.0, solid=True, direction=90,
           opacity=1.0, pressure="even", note="red band, shadow")
s.block_in(band_lit_face(), "flat", "band_lit", size=0.014, density=1.0, solid=True,
           direction=90, opacity=1.0, pressure="even", note="red band, lit")
s.stroke(gallery(), "flat", "iron", size=0.014, opacity=0.95, load=1.0, load_falloff=0.0,
         jitter=0.0, pressure="even", note="gallery plate")
s.block_in(lantern(), "flat", "lamp", size=0.012, density=1.0, solid=True, direction=90,
           note="lantern glass")
for x, sz in ((0.2515, 0.005), (0.2635, 0.004), (0.2765, 0.004), (0.2885, 0.005)):
    s.stroke([(x, 0.099), (x, 0.153)], "liner", "iron", size=sz, opacity=0.9,
             pressure="even", note="lantern post")
s.stroke([(0.244, 0.096), (0.296, 0.096)], "flat", "iron", size=0.012, opacity=0.95,
         load=1.0, load_falloff=0.0, jitter=0.0, pressure="even", note="cap, lower")
s.stroke([(0.256, 0.082), (0.284, 0.082)], "flat", "iron", size=0.013, opacity=0.95,
         load=1.0, load_falloff=0.0, jitter=0.0, pressure="even", note="cap, upper")
s.dab(0.270, 0.128, "round_hard", p.mix("lamp", "titanium_white", 0.5), size=0.012,
      press=3, note="the lamp")
print(s.look(values=True))
print(s.look())
print(s.look(region="B1:D3"))
