# c10 - repairs + the two things that make it a mug rather than a glass.
#  * crewmate repainted with `flat`/even/load=1.0: at size 0.030 a BRISTLE
#    covers ~3/4 of its width, so the comb left ceramic showing between the
#    columns and the mass averaged out brick-red instead of near-black.
#  * rim front lip knocked back - as painted it read as a doughnut laid on top.
#  * silhouette cut properly this time: brush centre at exactly wall +/- size/2,
#    FOLLOWING the wall, so its inner half stops on the edge instead of crossing it.
#  * handle and spoon.
import math

REF = r"C:\temp\Level1.jpg"
p = s.palette


def at_value(base, target):
    lo, hi = 0.0, 1.0
    if p.value_of(base) > target:
        for _ in range(26):
            mid = (lo + hi) / 2
            if p.value_of(p.shade(base, mid)) > target:
                lo = mid
            else:
                hi = mid
        return p.shade(base, (lo + hi) / 2)
    for _ in range(26):
        mid = (lo + hi) / 2
        if p.value_of(p.tint(base, mid)) < target:
            lo = mid
        else:
            hi = mid
    return p.tint(base, (lo + hi) / 2)


def edge(knots):
    def at(x):
        if x <= knots[0][0]:
            return knots[0][1]
        for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return knots[-1][1]
    return at


CERAMIC = p.desaturate(p.mix("cerulean", "burnt_sienna", 0.22), 0.62)
p["crew2"] = at_value(p.desaturate(p.mix("alizarin", "burnt_umber", 0.6), 0.45), 0.225)
p["lip_fr"] = at_value(CERAMIC, 0.520)
p["handle"] = at_value(CERAMIC, 0.610)
p["handle_d"] = at_value(CERAMIC, 0.470)
p["metal"] = at_value(p.desaturate("cerulean", 0.5), 0.640)
p["spoon"] = p.desaturate(p.mix("ultramarine", "burnt_umber", 0.45), 0.30)
print("crew2", p.hex(p["crew2"]), round(p.value_of(p["crew2"]), 3),
      "| spoon", p.hex(p["spoon"]), round(p.value_of(p["spoon"]), 3))

n0 = s.stroke_count
s.dry()

# ---- crewmate, solid this time ----------------------------------------
ctop = edge([(0.377, 0.492), (0.383, 0.430), (0.402, 0.404), (0.470, 0.396),
             (0.500, 0.416), (0.511, 0.468), (0.519, 0.474), (0.560, 0.478)])
cbot = edge([(0.377, 0.653), (0.4275, 0.656), (0.4285, 0.610), (0.4710, 0.610),
             (0.4720, 0.654), (0.5215, 0.651), (0.5225, 0.556), (0.560, 0.552)])
x, k = 0.383, 0
while x < 0.558:
    t, b = ctop(x), cbot(x)
    if b - t > 0.02:
        a, z = ((x, t + 0.004), (x, b - 0.004)) if k % 2 else ((x, b - 0.004), (x, t + 0.004))
        s.stroke([a, z], "flat", "crew2", size=0.026, load=1.0, pressure="even",
                 load_falloff=0.08)
    x += 0.013
    k += 1
print("crewmate:", s.stroke_count - n0)
s.dry()

# ---- rim: drop the front lip to nearly the body's value ---------------
s.stroke([(0.322, 0.245), (0.360, 0.300), (0.430, 0.330), (0.500, 0.333),
          (0.570, 0.310), (0.618, 0.268)], "round_hard", "lip_fr", size=0.026,
         load=1.0, pressure="swell")
s.stroke([(0.345, 0.283), (0.420, 0.318), (0.510, 0.320), (0.588, 0.290)],
         "round_hard", "lip_fr", size=0.016, load=1.0, pressure="swell",
         opacity=0.8)
s.dry()

# ---- cut both silhouettes with the ground, centre offset by size/2 ----
S = 0.026
lw = [(0.310, 0.190), (0.316, 0.330), (0.332, 0.500), (0.355, 0.655)]
rw = [(0.638, 0.216), (0.632, 0.350), (0.612, 0.500), (0.578, 0.626)]
s.stroke([(x - S / 2, y) for x, y in lw[:3]], "flat", "tbl_cut", size=S,
         load=1.0, pressure="even")
s.stroke([(x - S / 2, y) for x, y in lw[2:]], "flat", "sh_c", size=S,
         load=1.0, pressure="even")
s.stroke([(x + S / 2, y) for x, y in rw[:3]], "flat", "tbl_cut2", size=S,
         load=1.0, pressure="even")
s.stroke([(x + S / 2, y) for x, y in rw[2:]], "flat", "tbl_lt", size=S,
         load=1.0, pressure="even")
s.dry()

# ---- the handle -------------------------------------------------------
mid = [(0.649, 0.243), (0.699, 0.275), (0.718, 0.349), (0.700, 0.431),
       (0.648, 0.470), (0.618, 0.476)]
s.stroke(mid, "flat", "handle_d", size=0.034, load=1.0, pressure="even")
s.stroke([(0.652, 0.236), (0.706, 0.268), (0.727, 0.348), (0.708, 0.436),
          (0.652, 0.480)], "round_hard", "handle", size=0.016, load=1.0,
         pressure="swell")
# the hole: the table shows through it
s.stroke([(0.664, 0.298), (0.672, 0.360), (0.660, 0.418)], "flat", "tbl_cut2",
         size=0.038, load=1.0, pressure="swell")
s.stroke([(0.646, 0.330), (0.686, 0.395)], "flat", "tbl_cut", size=0.026,
         load=1.0, pressure="swell", opacity=0.8)
s.dry()

# ---- the spoon --------------------------------------------------------
s.stroke([(0.538, 0.000), (0.530, 0.062), (0.518, 0.132)], "flat", "spoon",
         size=0.036, load=1.0, pressure="lift_off")
s.stroke([(0.516, 0.126), (0.506, 0.180), (0.498, 0.222)], "flat", "spoon",
         size=0.020, load=1.0, pressure="even")
s.stroke([(0.496, 0.224), (0.514, 0.258), (0.538, 0.296)], "round_hard",
         "metal", size=0.014, load=1.0, pressure="press_in")
s.dab(0.528, 0.278, "round_hard", "metal", size=0.012)

print("strokes:", s.stroke_count)
print(s.look(reference=REF))
