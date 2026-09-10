import random

p = s.palette
rng = random.Random(4)

p["ab"] = p.mix(p["sky_a"], p["sky_b"], 0.5)
p["bc"] = p.mix(p["sky_b"], p["sky_c"], 0.5)
p["cd"] = p.mix(p["sky_c"], p["sky_d"], 0.5)
p["cirrus"] = p.shade(p["sky_a"], 0.18)
p["hot"] = p.tint(p.mix("cadmium_yellow", "cadmium_red", 0.18), 0.55)

# scumble across each join with the two colours either side of it, broken and angled
joins = [
    (0.150, ("sky_a", "sky_b", "ab"), (0.030, 0.055)),
    (0.258, ("sky_b", "sky_c", "bc"), (0.026, 0.048)),
    (0.322, ("sky_c", "sky_d", "cd"), (0.020, 0.038)),
]
for y, cols, (smin, smax) in joins:
    x = 0.02
    while x < 0.98:
        ln = rng.uniform(0.11, 0.26)
        dy = rng.uniform(-0.020, 0.020)
        tilt = rng.uniform(-0.016, 0.016)
        col = cols[rng.randrange(3)]
        s.stroke([(x, y + dy), (min(0.99, x + ln), y + dy + tilt)], "bristle", col,
                 size=rng.uniform(smin, smax), load=rng.uniform(0.55, 0.85),
                 pressure="taper")
        x += ln * rng.uniform(0.55, 0.85)

# a few streaks of cloud - not bands
s.stroke([(0.06, 0.062), (0.41, 0.048)], "bristle", "cirrus", size=0.028, load=0.6)
s.stroke([(0.55, 0.038), (0.88, 0.058)], "bristle", "cirrus", size=0.021, load=0.5)
s.stroke([(0.30, 0.118), (0.72, 0.104)], "bristle", "ab", size=0.024, load=0.55)
s.stroke([(0.14, 0.296), (0.52, 0.303)], "bristle", "hot", size=0.017, load=0.7)
s.stroke([(0.58, 0.284), (0.91, 0.290)], "bristle", "hot", size=0.013, load=0.6)
s.stroke([(0.36, 0.348), (0.79, 0.344)], "bristle", "sky_d", size=0.014, load=0.8)

print("strokes", s.stroke_count)
print(s.look())
