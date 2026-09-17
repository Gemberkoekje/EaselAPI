def to_value(base, target):
    """Push `base` to read `target` in greyscale: white up, a blue-umber dark down."""
    p = s.palette
    dark = p.mix("ultramarine", "burnt_umber", 0.55)
    v = p.value_of(base)
    if abs(v - target) < 0.005:
        return base
    going_up = v < target
    other = "titanium_white" if going_up else dark
    a, b = 0.0, 1.0
    for _ in range(24):
        mid = (a + b) / 2
        mv = p.value_of(p.mix(base, other, mid))
        if (mv < target) == going_up:
            a = mid
        else:
            b = mid
    return p.mix(base, other, (a + b) / 2)
