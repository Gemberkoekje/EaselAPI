# c4 - the ground plane. Big flat brush, three value bands read off compare:
#   left band A-B  ref 0.31-0.44  -> 0.39
#   band C         ref 0.40-0.45  -> 0.44
#   band F         ref 0.50-0.58  -> 0.54
#   band G-H       ref 0.42-0.51  -> 0.47
#   bright shelf below the shadow, D8:F8 ref 0.56-0.62 -> 0.58
#   dark corner H1 ref 0.29
REF = r"C:\temp\Level1.jpg"
p = s.palette


def at_value(base, target):
    """tint `base` until value_of hits `target` - the palette's own number,
    so a mass lands on the value I measured instead of one I guessed."""
    lo, hi = 0.0, 1.0
    if p.value_of(base) > target:          # need it darker: shade instead
        lo, hi = 0.0, 1.0
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


wood = p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.50), 0.30)
p["tbl_dk"] = at_value(wood, 0.39)
p["tbl_md"] = at_value(wood, 0.45)
p["tbl_lt"] = at_value(p.desaturate(wood, 0.15), 0.53)
p["tbl_br"] = at_value(p.desaturate(wood, 0.25), 0.58)
p["corner"] = at_value(p.desaturate(p.mix("ultramarine", "burnt_umber", 0.5), 0.5), 0.27)
for n in ("tbl_dk", "tbl_md", "tbl_lt", "tbl_br", "corner"):
    print(f"{n:8s} {p.hex(p[n])} {p.value_of(p[n]):.3f}")

n0 = s.stroke_count
# whole field first, mid value, ground still breathing through
s.block_in(region("all"), "flat", "tbl_md", density=0.78, size=0.22,
           direction="diagonal")
print("after field:", s.stroke_count - n0)

# left band, darker
s.block_in(span("A1", "B8"), "flat", "tbl_dk", density=0.8, size=0.18,
           direction="vertical")
# right side, lighter
s.block_in(span("F1", "H8"), "flat", "tbl_lt", density=0.75, size=0.20,
           direction="horizontal")
s.block_in(span("G1", "H8"), "flat", at_value(p["tbl_lt"], 0.47), density=0.6,
           size=0.18, direction="diagonal")
# the bright shelf below the shadow and the lit patch right of the mug
s.block_in(span("D8", "F8"), "flat", "tbl_br", density=0.85, size=0.14,
           direction="horizontal")
s.block_in(span("F4", "F6"), "flat", "tbl_br", density=0.6, size=0.12,
           direction="diagonal")
print("after bands:", s.stroke_count - n0)

# dark corner top right - two marks, not a block-in
s.stroke([(0.905, 0.004), (1.01, 0.030)], "flat", "corner", size=0.035,
         pressure="even", load=1.0)
s.stroke([(0.94, 0.000), (1.01, 0.008)], "flat", "corner", size=0.03,
         pressure="lift_off", load=1.0)

print("strokes:", s.stroke_count)
print(s.look(reference=REF))
print(s.look(reference=REF, values=True))
