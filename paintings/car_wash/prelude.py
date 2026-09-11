# Shared across every pass: the palette as planned values, the masses as shapes,
# and each depth layer as a named function so the stack can be re-run for a repair.
p = s.palette

# ---------------------------------------------------------------- the palette
# A dark cool interior, a wet tunnel beyond the glass, and two lights that are
# not daylight: a magenta foam arch overhead and a cyan-white bloom ahead.
def V(base, target, name=None):
    c = p.at_value(base, target)
    if name:
        print(f"  {name:9s} {p.hex(c)}  v={p.value_of(c):.2f}  (asked {target:.2f})")
    return c

def mixtures(verbose=False):
    n = (lambda k: k) if verbose else (lambda k: None)
    cool_black = p.mix("ultramarine", "burnt_umber", 0.35)
    teal       = p.desaturate(p.mix("ultramarine", "viridian", 0.42), 0.25)
    haze       = p.desaturate(p.mix("cerulean", "ultramarine", 0.30), 0.45)
    magenta    = p.mix("alizarin", "ultramarine", 0.22)
    cyan       = p.mix("cerulean", "titanium_white", 0.25)
    soap       = p.desaturate(p.mix("cerulean", "titanium_white", 0.55), 0.45)
    hot        = p.mix("cadmium_red", "alizarin", 0.30)

    p["frame"]    = V(cool_black, 0.15, n("frame"))     # pillars, header, dash
    p["rim"]      = V(p.desaturate(p.mix(cool_black, "cerulean", 0.45), 0.30), 0.44, n("rim"))
    p["frame_lt"] = V(p.mix(cool_black, "burnt_sienna", 0.25), 0.27, n("frame_lt"))
    p["brush_dk"] = V(p.mix(cool_black, "viridian", 0.22), 0.26, n("brush_dk"))
    p["brush_lt"] = V(p.desaturate(magenta, 0.55), 0.62, n("brush_lt"))
    p["tunnel"]   = V(teal, 0.32, n("tunnel"))          # the wet dark beyond
    p["haze"]     = V(haze, 0.46, n("haze"))            # soap fog on the glass
    p["mag_lo"]   = V(magenta, 0.40, n("mag_lo"))
    p["mag_hi"]   = V(p.mix(magenta, "cadmium_red", 0.20), 0.50, n("mag_hi"))
    p["cyan_lo"]  = V(p.desaturate(cyan, 0.20), 0.42, n("cyan_lo"))
    p["cyan_md"]  = V(p.desaturate(cyan, 0.10), 0.64, n("cyan_md"))
    p["cyan_hi"]  = V(cyan, 0.74, n("cyan_hi"))
    p["foam"]     = V(soap, 0.81, n("foam"))
    p["foam_hi"]  = V(p.mix(soap, "titanium_white", 0.6), 0.91, n("foam_hi"))
    p["hot"]      = V(hot, 0.42, n("hot"))              # the stop light
    p["hot_core"] = V(p.mix("cadmium_red", "cadmium_yellow", 0.40), 0.84, n("hot_core"))

mixtures()

# ---------------------------------------------------------------- the masses
# Nothing here is a rectangle except the tunnel, which is a field.
def dash():        # the cowl: rises at both sides, sags across the middle
    return polygon([(-0.05, 1.05), (1.05, 1.05), (1.05, 0.748), (0.855, 0.824),
                    (0.660, 0.880), (0.520, 0.866), (0.408, 0.812),
                    (0.250, 0.788), (0.090, 0.806), (-0.05, 0.842)]).smooth()

def binnacle():    # what you see through the wheel is the instrument hood, not glass:
                   # a hollow thing is the far mass, then the inside, then the near edge
    return polygon([(0.098, 0.906), (0.172, 0.766), (0.300, 0.712),
                    (0.436, 0.748), (0.528, 0.874), (0.498, 0.975),
                    (0.150, 0.975)]).smooth()

def pillar_l():    # near, wide, raked: its edge leans right going up
    return polygon([(-0.06, -0.05), (0.088, -0.05), (0.042, 1.05), (-0.06, 1.05)])

def pillar_r():    # further off, narrower, leaning left going up
    return polygon([(0.951, -0.05), (1.06, -0.05), (1.06, 1.05), (0.986, 1.05)])

def mirror():      # hangs into the light: the thing that says "driver's seat"
    return polygon([(0.500, 0.072), (0.638, 0.061), (0.644, 0.132),
                    (0.506, 0.146)]).smooth()

def wheel():       # the top arc of the steering wheel, low and left
    return [(0.106, 0.897), (0.188, 0.759), (0.322, 0.705),
            (0.452, 0.741), (0.534, 0.860)]

def brushmass():   # the side brush swinging in: a vertical mass, leading edge bulging left
    return polygon([(1.06, -0.05), (1.06, 0.82), (0.885, 0.755), (0.775, 0.560),
                    (0.712, 0.360), (0.728, 0.185), (0.805, -0.05)]).smooth()

def glow():        # the cyan bloom ahead, seen through the soap
    return blob((0.312, 0.425), 0.165, wobble=0.38, seed=11)

def archband():    # the arch light: down the left of the glass as well as over it,
                   # so its boundary runs oblique and interlocks instead of banding
    return polygon([(-0.05, -0.05), (1.05, -0.05), (1.05, 0.125), (0.82, 0.205),
                    (0.655, 0.150), (0.475, 0.265), (0.315, 0.205),
                    (0.195, 0.355), (0.075, 0.395), (-0.05, 0.545)]).smooth()

def archcore():    # the hottest part of it, upper left, small and soft
    return blob((0.225, 0.085), 0.155, wobble=0.42, seed=17)

# ---------------------------------------------------------------- value plan
PLAN = {
    span("A8", "H8"): 0.16,     # dashboard, the anchoring dark
    span("G2", "H4"): 0.56,     # the brush, foam-smothered
    span("C4", "D5"): 0.68,     # the cyan bloom, the lightest mass
    span("B1", "D2"): 0.47,     # upper glass under the arch
    span("A6", "D6"): 0.36,     # lower glass, fogged
}
