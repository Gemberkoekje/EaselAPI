# Pass 10 - model the pot as strokes down the form, then cut the silhouette back.
p = s.palette
s.dry()

lo, hi = p["terra_sh"], p["terra_hi"]
def at(v):                                   # a terracotta at a given value
    a, b = 0.0, 1.0
    for _ in range(22):
        m = (a + b) / 2
        a, b = (m, b) if p.value_of(p.mix(lo, hi, m)) < v else (a, m)
    return p.mix(lo, hi, (a + b) / 2)

body = polygon([(0.324,0.678),(0.418,0.690),(0.512,0.686),(0.498,0.782),(0.482,0.866),
                (0.440,0.880),(0.396,0.879),(0.352,0.860),(0.336,0.780)])
s.block_in(body.inset(0.022), "flat", "terra_mid", direction=(11, 169), density=1.0,
           size=0.044, load=1.0, pressure="even")

ramp = [(0.00,0.40),(0.07,0.46),(0.14,0.50),(0.22,0.49),(0.30,0.455),(0.38,0.425),
        (0.46,0.39),(0.54,0.35),(0.62,0.305),(0.70,0.26),(0.78,0.215),(0.86,0.19),
        (0.93,0.20),(0.99,0.245)]
sizes = [0.024,0.020,0.026,0.018,0.022,0.028,0.019,0.024,0.021,0.026,0.018,0.023,0.015,0.013]
for i, (t, v) in enumerate(ramp):
    xt = 0.3265 + t * 0.1855;  yt = 0.6845 + t * 0.004
    xb = 0.3525 + t * 0.1295;  yb = 0.8575 + t * 0.008
    xm = (xt + xb) / 2 + (0.004 if i % 3 else -0.003)
    s.stroke([(xt, yt + 0.012), ((xm), (yt + yb) / 2), (xb, yb - 0.006)],
             "flat", at(v), size=sizes[i % len(sizes)],
             pressure=("even" if i % 2 else [0.85, 1.0, 0.7]), load=1.0)

# a few marks around the form so it is not all one direction
s.stroke([(0.346,0.836),(0.400,0.856),(0.452,0.852)], "bristle", at(0.30),
         size=0.016, pressure="taper", load=0.8)
s.stroke([(0.340,0.716),(0.398,0.728),(0.446,0.724)], "bristle", at(0.42),
         size=0.013, pressure="taper", load=0.7)

# --- cut the ragged fringe back with the masses on the other side --------------
s.stroke([(0.312,0.690),(0.320,0.770),(0.336,0.856)], "flat", "bg", size=0.030,
         pressure="even", load=1.0)
s.stroke([(0.524,0.690),(0.514,0.764),(0.498,0.844)], "flat", "cast", size=0.030,
         pressure="even", load=1.0)
s.stroke([(0.352,0.888),(0.420,0.898),(0.486,0.884)], "flat", "cast", size=0.028,
         pressure="even", load=1.0)
s.stroke([(0.316,0.666),(0.380,0.646),(0.452,0.642)], "flat", "bg", size=0.024,
         pressure="even", load=1.0)
s.stroke([(0.470,0.642),(0.512,0.652),(0.526,0.672)], "flat", "bg", size=0.022,
         pressure="even", load=1.0)

# the contact shadow where the pot meets the wood
s.stroke([(0.358,0.872),(0.418,0.882),(0.478,0.872)], "round_hard",
         p.mix(p["cast"], "burnt_umber", 0.5), size=0.014, pressure=[0.6,1.0,0.5])

print("strokes:", s.stroke_count)
print(s.look(region=span("C5","F8"), sketch=False))
