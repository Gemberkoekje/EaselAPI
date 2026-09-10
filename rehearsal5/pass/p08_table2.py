REF = "C:/temp/Level1.jpg"
p = s.palette

def tv(base, target):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if p.value_of(p.mix(base, "titanium_white", mid)) < target:
            lo = mid
        else:
            hi = mid
    return p.mix(base, "titanium_white", (lo + hi) / 2)

wood = p.desaturate(p.mix("burnt_umber", "yellow_ochre", 0.38), 0.22)
p["wood_dark"]  = tv(wood, 0.355)
p["wood_mid"]   = tv(wood, 0.45)
p["wood_field"] = tv(wood, 0.525)
p["wood_light"] = tv(wood, 0.595)
p["wood_hot"]   = tv(wood, 0.635)
p["wood_far"]   = tv(wood, 0.415)
for n in ("wood_dark", "wood_mid", "wood_field", "wood_light", "wood_hot", "wood_far"):
    print(f"{n:<11} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")

left = polygon([(0.0, -0.02), (0.305, -0.02), (0.258, 0.17), (0.292, 0.35),
                (0.243, 0.55), (0.284, 0.73), (0.212, 1.02), (0.0, 1.02)])

# --- rehearse the left field's grain three ways before paying for it -----
def band(brush, size, dens, direction):
    return [{"points": [(0.02, y), (0.30, y - 0.05)], "brush": brush, "size": size,
             "color": "wood_dark"} for y in (0.18, 0.34, 0.50, 0.66, 0.82)]
print("A bristle 0.13:", s.rehearse(band("bristle", 0.13, 0.7, -10), region=span("A2", "C7")))
print("B flat 0.13   :", s.rehearse(band("flat", 0.13, 0.7, -10), region=span("A2", "C7")))
print("C bristle 0.06:", s.rehearse(band("bristle", 0.06, 0.7, -10), region=span("A2", "C7")))

# --- 1. the whole table again, muted --------------------------------------
s.block_in(region("all"), "flat", "wood_field", direction=-10, density=0.9,
           size=0.20, load=1.0, note="table field 2")
print("field", s.stroke_count)

# --- 2. the dark left -----------------------------------------------------
s.block_in(left, "bristle", "wood_dark", direction=-10, density=0.7,
           size=0.155, load=1.0, note="left dark 2")
print("left", s.stroke_count)

# --- 3. a step between them, so the join is three values not two ----------
join = ribbon([(0.315, -0.03), (0.275, 0.35), (0.315, 0.62), (0.235, 1.03)], 0.13)
s.block_in(join, "flat", "wood_mid", direction="axis", density=0.85,
           size=0.055, load=1.0, note="join step")
print("join", s.stroke_count)

# --- 4. the light band ----------------------------------------------------
lit = ribbon([(0.42, 1.06), (0.58, 0.74), (0.70, 0.42), (0.80, 0.08)], 0.32)
s.block_in(lit, "flat", "wood_light", direction="axis", density=0.8,
           size=0.115, load=1.0, note="light band 2")
hot = ellipse(span("D8", "F8"))
s.block_in(hot.inset(0.03), "flat", "wood_hot", direction=-8, density=0.8,
           size=0.06, load=1.0, note="hot foreground")
print("light", s.stroke_count)

# --- 5. the table falling away at the far corners -------------------------
s.block_in(polygon([(0.885, -0.02), (1.02, -0.02), (1.02, 0.34), (0.945, 0.21)]),
           "flat", "wood_far", direction=-32, density=0.85, size=0.06,
           load=1.0, note="far top right")
s.block_in(polygon([(1.02, 0.80), (1.02, 1.02), (0.755, 1.02), (0.905, 0.87)]),
           "flat", "wood_far", direction=-14, density=0.85, size=0.06,
           load=1.0, note="far bottom right")
s.block_in(polygon([(0.923, -0.02), (1.02, -0.02), (1.02, 0.088)]).inset(0.010),
           "flat", "warm_dark", direction=-42, density=1.0, size=0.026,
           load=1.0, note="beyond the table")
print("corners", s.stroke_count)

print(s.look(reference=REF))
print(s.look(reference=REF, values=True))
print(s.compare(REF))
