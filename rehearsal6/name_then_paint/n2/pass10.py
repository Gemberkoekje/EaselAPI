p = s.palette; dk = p["dk"]
pale = p.mix("titanium_white", "yellow_ochre", 0.28)
def at_val(target, b, base=None):
    base = pale if base is None else base
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(base, b, m)) > target: lo=m
        else: hi=m
    return p.mix(base, b, (lo+hi)/2)

s.dry()
# --- the tongue of dark beside the rim was never there: put the light back ---
s.block_in(polygon([(0.408,0.512),(0.489,0.518),(0.487,0.580),(0.406,0.574)]), "flat",
           "glow_c", density=1.0, size=0.020, direction=(7,95), load=1.0)
s.block_in(polygon([(0.486,0.516),(0.518,0.520),(0.521,0.580),(0.484,0.578)]), "flat",
           p.mix(p["reveal_d"], dk, 0.42), density=1.0, size=0.014, direction=87, load=1.0)

# --- a mullion: the window needs a bar, and the sill needs its shadow ---
bar = polygon([(0.2705,0.094),(0.2995,0.096),(0.2960,0.652),(0.2670,0.650)])
s.block_in(bar, "flat", at_val(0.31, dk), density=1.0, size=0.013, direction=89, load=1.0)
s.stroke([(0.2725,0.108),(0.2700,0.330)], "flat", at_val(0.78,"burnt_umber"),
         size=0.005, pressure="lift_off")
s.stroke([(0.2695,0.372),(0.2680,0.612)], "flat", at_val(0.68,"burnt_umber"),
         size=0.004, pressure="taper")
s.stroke([(0.2985,0.140),(0.2960,0.420)], "flat", at_val(0.44,"burnt_umber"),
         size=0.004, pressure="press_in")
cast = polygon([(0.2745,0.648),(0.3055,0.650),(0.4230,0.799),(0.3880,0.801)])
s.block_in(cast, "flat", at_val(0.475,"burnt_umber"), density=1.0, size=0.020,
           direction="axis", load=1.0)
s.block_in(polygon([(0.2860,0.650),(0.3010,0.651),(0.4110,0.799),(0.3960,0.800)]), "bristle",
           at_val(0.415,"burnt_umber"), density=0.7, size=0.012, direction="axis", load=0.7)
s.smudge([(0.3130,0.678),(0.3490,0.724)], size=0.030)
s.smudge([(0.3760,0.756),(0.4090,0.796)], size=0.028)

# --- deepen the far corner of the room so the dark is not one flat field ---
s.block_in(blob((0.905,0.155), 0.22, 0.20, wobble=0.45, seed=23), "bristle",
           p.mix(dk,"ultramarine",0.20), density=0.35, size=0.055, direction=(63,146), load=0.45)
s.block_in(blob((0.640,0.215), 0.13, 0.20, wobble=0.5, seed=29), "bristle", "wall_hi",
           density=0.30, size=0.045, direction=(78,158), load=0.40)
print("strokes:", s.stroke_count)
