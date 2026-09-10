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

def dv(base, target, dark):
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if p.value_of(p.mix(base, dark, mid)) > target:
            lo = mid
        else:
            hi = mid
    return p.mix(base, dark, (lo + hi) / 2)

darkest = p.mix("ultramarine", "burnt_umber", 0.5)
warm_dark = p.mix("ultramarine", "burnt_umber", 0.72)
wood = p.desaturate(p.mix("yellow_ochre", "burnt_sienna", 0.35), 0.30)

p["darkest"]    = darkest
p["warm_dark"]  = warm_dark
p["wood_field"] = tv(wood, 0.53)
p["wood_light"] = tv(wood, 0.60)
p["wood_hot"]   = tv(wood, 0.64)
p["wood_mid"]   = dv(wood, 0.46, warm_dark)
p["wood_dark"]  = dv(wood, 0.37, warm_dark)
p["wood_far"]   = dv(wood, 0.43, warm_dark)
p["corner"]     = warm_dark

for n in ("wood_field", "wood_light", "wood_hot", "wood_mid", "wood_dark", "wood_far"):
    print(f"{n:<11} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")

# --- 1. the whole table: a quiet warm field, grain-wards ------------------
s.block_in(region("all"), "flat", "wood_field", direction=-10, density=0.85,
           size=0.22, load=1.0, note="table field")
print("after field", s.stroke_count)

# --- 2. the dark left of the table ---------------------------------------
left = polygon([(0.0, -0.02), (0.30, -0.02), (0.255, 0.34), (0.285, 0.60),
                (0.215, 1.02), (0.0, 1.02)])
s.preview(left, reference=REF)
s.block_in(left, "bristle", "wood_dark", direction=-10, density=0.70,
           size=0.14, load=1.0, note="left dark")
print("after left", s.stroke_count)

# --- 3. the band of light, bottom-centre up to the right -----------------
band = ribbon([(0.42, 1.06), (0.58, 0.74), (0.70, 0.42), (0.80, 0.08)], 0.32)
s.block_in(band, "flat", "wood_light", direction="axis", density=0.75,
           size=0.12, load=1.0, note="light band")
print("after band", s.stroke_count)

# --- 4. the far corner of the table falls away ---------------------------
far_top = polygon([(0.86, -0.02), (1.02, -0.02), (1.02, 0.42), (0.93, 0.30)])
s.block_in(far_top, "bristle", "wood_far", direction=-30, density=0.8,
           size=0.09, load=1.0, note="far top right")
br = polygon([(1.02, 0.72), (1.02, 1.02), (0.72, 1.02), (0.86, 0.80)])
s.block_in(br, "bristle", "wood_far", direction=-14, density=0.8,
           size=0.09, load=1.0, note="bottom right")
print("after corners", s.stroke_count)

# --- 5. beyond the table: the dark wedge ---------------------------------
wedge = polygon([(0.918, -0.02), (1.02, -0.02), (1.02, 0.10)])
s.block_in(wedge.inset(0.012), "flat", "corner", direction=-40, density=1.0,
           size=0.028, load=1.0, note="dark corner")
print("after wedge", s.stroke_count)

print(s.look(reference=REF))
print(s.look(reference=REF, values=True))
print(s.compare(REF))
