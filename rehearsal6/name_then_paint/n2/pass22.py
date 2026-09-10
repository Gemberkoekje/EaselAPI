p = s.palette; dk = p["dk"]
pale = p.mix("titanium_white", "yellow_ochre", 0.28)
def SV(t, b="burnt_umber"):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        m=(lo+hi)/2
        if p.value_of(p.mix(pale, b, m)) > t: lo=m
        else: hi=m
    return p.mix(pale, b, (lo+hi)/2)

s.dry()
# --- put back the dark the scumbles ran over ---
case = polygon([(-0.07,0.030),(0.118,0.070),(0.107,0.706),(-0.07,0.694)])
s.block_in(case, "flat", "case", density=1.0, size=0.046, direction=88, load=1.0)
s.block_in(case.inset(0.013), "flat", "case", density=0.9, size=0.038, direction=79, load=1.0)
s.stroke([(0.110,0.086),(0.106,0.255)], "flat", "case_lit", size=0.012, pressure="lift_off")
s.stroke([(0.107,0.300),(0.104,0.470)], "flat", "case_lit", size=0.010, pressure="taper")
s.stroke([(0.105,0.520),(0.102,0.660)], "flat", "reveal_d", size=0.009, pressure="press_in")

s.block_in(polygon([(-0.10,-0.09),(1.14,-0.09),(1.14,0.102),(0.520,0.106),
                    (0.050,0.090),(-0.10,0.114)]), "flat", "wall",
           density=1.0, size=0.050, direction=(-6,84), load=1.0)
s.block_in(polygon([(0.432,0.208),(0.522,0.214),(0.518,0.336),(0.428,0.330)]), "flat",
           "wall", density=1.0, size=0.024, direction=(72,158), load=1.0)

bar = polygon([(0.2705,0.094),(0.2995,0.096),(0.2960,0.652),(0.2670,0.650)])
s.block_in(bar, "flat", SV(0.31, dk), density=1.0, size=0.013, direction=89, load=1.0)
s.stroke([(0.2725,0.108),(0.2700,0.330)], "flat", SV(0.78), size=0.005, pressure="lift_off")
s.stroke([(0.2695,0.372),(0.2680,0.612)], "flat", SV(0.68), size=0.004, pressure="taper")
s.stroke([(0.2985,0.140),(0.2960,0.420)], "flat", SV(0.44), size=0.004, pressure="press_in")
s.block_in(polygon([(0.487,0.110),(0.508,0.113),(0.512,0.330),(0.485,0.328)]), "flat",
           "reveal", density=1.0, size=0.015, direction=88, load=1.0)

# the smudge lifted the far end of the sill; put it back down
s.block_in(polygon([(0.900,0.638),(1.06,0.652),(1.06,0.706),(0.900,0.692)]), "flat",
           SV(0.275, dk), density=1.0, size=0.020, direction=(5,93), load=1.0)
# one soft pass to settle the window down again
s.stroke([(0.140,0.310),(0.246,0.286)], "round_soft", "glow_p", size=0.038,
         load=0.5, opacity=0.35, pressure="even")
s.stroke([(0.330,0.400),(0.436,0.378)], "round_soft", "glow_w", size=0.034,
         load=0.5, opacity=0.35, pressure="even")
s.stroke([(0.160,0.568),(0.252,0.552)], "round_soft", "glow_g", size=0.032,
         load=0.5, opacity=0.35, pressure="even")
print("strokes:", s.stroke_count)
