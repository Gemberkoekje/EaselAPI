R = "/home/user/refs/Level1.jpg"
p = s.palette
def at(base, mixer, target):
    a,b = 0.0,1.0
    for _ in range(24):
        m=(a+b)/2
        a,b = (m,b) if p.value_of(p.mix(base,mixer,m)) < target else (a,m)
    return (a+b)/2
p["sh_core"] = p.mix("burnt_umber","ultramarine",0.30)
p["sh_mid"]  = p.mix(p["sh_core"], p["wood_l2"], at(p["sh_core"], p["wood_l2"], 0.26))
p["sh_soft"] = p.mix(p["sh_core"], p["wood_l2"], at(p["sh_core"], p["wood_l2"], 0.355))
for n in ("sh_core","sh_mid","sh_soft"):
    print(f"{n:8s} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")

# 1. the penumbra: one soft mass, laid along its own axis
soft = blob((0.452, 0.706), 0.170, 0.108, wobble=0.34, seed=4)
s.block_in(soft, "bristle", "sh_soft", direction="axis", density=0.8, size=0.055, load=1.0)
print("penumbra", s.stroke_count)

# 2. the core, under and to the left of the foot
core = blob((0.415, 0.716), 0.098, 0.062, wobble=0.38, seed=9)
s.block_in(core, "flat", "sh_mid", direction=(-12), density=0.95, size=0.032,
           load=1.0, pressure="even")
print("core", s.stroke_count)
s.block_in(blob((0.398,0.706), 0.058, 0.038, wobble=0.4, seed=3), "flat", "sh_core",
           direction=(-16), density=1.0, size=0.022, load=1.0, pressure="even")
print("core2", s.stroke_count)

# 3. the handle's shadow: an open loop, not a filled disc
s.stroke([(0.600,0.612),(0.622,0.560),(0.664,0.522),(0.700,0.545)], "bristle",
         "sh_mid", size=0.030, load=0.95, pressure="swell")
s.stroke([(0.700,0.548),(0.706,0.594),(0.668,0.628),(0.615,0.632)], "bristle",
         "sh_soft", size=0.028, load=0.9, pressure="taper")
s.stroke([(0.640,0.565),(0.676,0.560)], "round_hard", "wood_lit", size=0.026,
         load=1.0, opacity=0.6, pressure="even")

# 4. lose the outer edge in two places, keep it found under the foot
s.smudge([(0.315,0.660),(0.345,0.640)], size=0.038)
s.smudge([(0.495,0.792),(0.545,0.775)], size=0.040)
print("total", s.stroke_count)
print(s.look())
print(s.look(reference=R, region=span("C5","G8")))
