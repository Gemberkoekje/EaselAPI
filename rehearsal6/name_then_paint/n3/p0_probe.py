p = s.palette

# Neutral cool grey base: ultramarine + burnt_sienna are near-complements
cool = p.mix("ultramarine", "burnt_sienna", 0.50)
warm = p.mix("burnt_umber", "yellow_ochre", 0.45)

def tests(name, base):
    for t in (0.0, 0.3, 0.5, 0.6, 0.7, 0.8, 0.86, 0.92, 1.0):
        c = p.tint(base, t) if t else base
        print(f"  {name:6s} tint {t:4.2f}  {p.hex(c)}  v={p.value_of(c):.3f}")

tests("cool", cool)
print()
tests("warm", warm)
print()
darkest = p.mix("ultramarine", "burnt_umber", 0.5)
print("darkest  ", p.hex(darkest), round(p.value_of(darkest), 3))
tea = p.mix("burnt_umber", "ultramarine", 0.22)
print("tea      ", p.hex(tea), round(p.value_of(tea), 3))
tea2 = p.mix(p.mix("burnt_umber","burnt_sienna",0.35), "ultramarine", 0.18)
print("tea2     ", p.hex(tea2), round(p.value_of(tea2), 3))
print("ground?  blank canvas look below")
print(s.look())
