p = s.palette

def to_value(base, target):
    other = "titanium_white" if p.value_of(base) < target else "burnt_umber"
    lo, hi = 0.0, 1.0
    for _ in range(28):
        mid = (lo + hi) / 2.0
        v = p.value_of(p.mix(base, other, mid))
        if (v < target) == (other == "titanium_white"):
            lo = mid
        else:
            hi = mid
    return p.mix(base, other, (lo + hi) / 2.0)

warm = p.mix("yellow_ochre", "burnt_sienna", 0.45)
p["bg_mid"]   = to_value(warm, 0.36)
p["wall_m"]   = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.38), 0.44)
p["wall_l"]   = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.22), 0.58)
p["wall_h"]   = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.14), 0.70)
p["coat"]     = p.mix("ultramarine", "burnt_umber", 0.62)
p["coat_c"]   = p.mix("ultramarine", "burnt_umber", 0.38)
p["bg_dark"]  = to_value(p.mix(p["coat"], "burnt_sienna", 0.35), 0.15)
p["greyblur"] = to_value(p.desaturate(p.mix("ultramarine", "burnt_sienna", 0.5), 0.35), 0.38)
p["rightbg"]  = to_value(p.desaturate(p.mix("yellow_ochre", "burnt_umber", 0.5), 0.25), 0.36)
p["table"]    = to_value(p.mix("yellow_ochre", "burnt_sienna", 0.32), 0.34)
p["lowleft"]  = to_value(p.mix("yellow_ochre", "burnt_umber", 0.55), 0.27)

for n in ("bg_mid", "wall_m", "wall_l", "wall_h", "coat", "coat_c", "bg_dark",
          "greyblur", "rightbg", "table", "lowleft"):
    print(f"{n:9s} {p.hex(p[n])} v={p.value_of(p[n]):.3f}")

# ---- two masses: light above, dark below ----
s.block_in(region("upper-half"), "flat", "bg_mid", direction=8, size=0.22,
           density=1.0, load=1.0)
s.block_in(region("lower-half"), "flat", "coat", direction=-6, size=0.22,
           density=1.0, load=1.0)
print("after two masses:", s.stroke_count)
print(s.look(reference="ref.jpg", grid=True, values=True))
