p = s.palette
p["sky"]      = p.tint(p.mix("alizarin", "cerulean", 0.55), 0.80)
p["sky_hi"]   = p.tint(p.mix("alizarin", "cerulean", 0.6), 0.9)
p["sky_warm"] = p.tint(p.mix("yellow_ochre", "cadmium_red", 0.15), 0.72)
p["glow"]     = p.tint("lemon_yellow", 0.6)
p["far"]      = p.tint(p.mix("ultramarine", "burnt_umber", 0.5), 0.30)
p["head"]     = p.tint(p.mix("ultramarine", "burnt_umber", 0.6), 0.12)
p["water"]    = p.desaturate(p.tint(p.mix("cerulean", "burnt_umber", 0.3), 0.45), 0.3)
p["water_lt"] = p.mix(p["water"], p["sky_warm"], 0.7)
p["mud"]      = p.mix("burnt_umber", "yellow_ochre", 0.4)
p["mud_lt"]   = p.tint(p.mix("burnt_umber", "yellow_ochre", 0.6), 0.35)
p["mud_dk"]   = p.mix("burnt_umber", "ultramarine", 0.3)
p["post"]     = p.mix("ultramarine", "burnt_umber", 0.5)
for n in ("sky", "sky_hi", "sky_warm", "glow", "water", "water_lt"):
    print(f"{n:9s} {p.hex(p[n])} {p.value_of(p[n]):.2f}")

def edge(knots):
    def at(x):
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1]
    return at

# --- sky, worked wet: cool above, warm low, a glow at the horizon
s.block_in(Region(0.0, 0.0, 1.0, 0.57), "flat", "sky", direction="horizontal", density=1.0, size=0.2)
s.stroke([(0.0, 0.06), (0.5, 0.04), (1.0, 0.07)], "flat", "sky_hi", size=0.14, pressure="even")
for y in (0.36, 0.44, 0.50):
    s.stroke([(0.0, y), (0.5, y - 0.01), (1.0, y + 0.01)], "bristle", "sky_warm", size=0.12, load=1.0, pressure="even")
s.stroke([(0.20, 0.53), (0.50, 0.51), (0.80, 0.53)], "round_soft", "glow", size=0.09, opacity=0.8, pressure="swell")
s.stroke([(0.30, 0.55), (0.65, 0.545)], "round_soft", "glow", size=0.05, opacity=0.9, pressure="swell")
s.dry()

# --- the far headland, as a silhouette; the nearer spit on the right, darker
top = edge([(-0.02, 0.41), (0.12, 0.37), (0.24, 0.40), (0.38, 0.46), (0.52, 0.52), (0.60, 0.555)])
x = 0.0
while x < 0.60:
    s.stroke([(x, top(x)), (x, 0.58)], "bristle", "far", size=0.11, load=1.0, pressure="lift_off")
    x += 0.037
s.stroke([(0.0, 0.415), (0.12, 0.375), (0.24, 0.405), (0.38, 0.465), (0.52, 0.525), (0.60, 0.56)],
         "bristle", "far", size=0.07, load=1.0, pressure="even")
top2 = edge([(0.62, 0.565), (0.72, 0.545), (0.84, 0.535), (0.94, 0.545), (1.02, 0.56)])
x = 0.63
while x < 1.0:
    s.stroke([(x, top2(x)), (x, 0.61)], "bristle", "head", size=0.08, load=1.0, pressure="lift_off")
    x += 0.04
s.dry()

# --- water, then the path of light while it is wet
s.block_in(Region(0.0, 0.575, 1.0, 0.75), "flat", "water", direction="horizontal", density=1.0, size=0.11)
s.stroke([(0.52, 0.575), (0.50, 0.65), (0.46, 0.75)], "round_soft", "water_lt", size=0.09, pressure="press_in")
s.stroke([(0.55, 0.58), (0.54, 0.66), (0.52, 0.75)], "round_soft", "water_lt", size=0.06, pressure="press_in")
s.stroke([(0.10, 0.62), (0.35, 0.615)], "bristle", "water_lt", size=0.02, load=0.6, pressure="taper")
s.dry()

# --- mudflats
s.block_in(Region(0.0, 0.73, 1.0, 1.0), "bristle", "mud", direction="horizontal", density=1.0, size=0.16)
for y, x0, x1 in ((0.78, 0.05, 0.60), (0.84, 0.30, 0.95), (0.90, 0.0, 0.50), (0.95, 0.40, 1.0)):
    s.stroke([(x0, y), ((x0 + x1) / 2, y + 0.01), (x1, y)], "bristle", "mud_lt", size=0.07, load=0.5, pressure="taper")
s.stroke([(0.0, 0.96), (0.3, 1.0)], "bristle", "mud_dk", size=0.12, load=0.8, pressure="even")
s.stroke([(0.7, 0.98), (1.0, 0.94)], "bristle", "mud_dk", size=0.12, load=0.8, pressure="even")

print("strokes:", s.stroke_count)
print(s.look())
print(s.look(values=True))
