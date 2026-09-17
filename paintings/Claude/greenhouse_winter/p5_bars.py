# Pass 5: the glazing bars, on the glass and behind everything inside. Thin
# strokes converging on the vanishing point: a few pixels wide at the end wall,
# thicker near the viewer, thinned almost to nothing where they cross the glare.
# No two the same width. The ones on the sky side are lighter and cooler than
# the ones silhouetted against the sun.
p["bar_sun"] = p.at_value("bar", 0.32)
p["bar_cool"] = p.at_value(p.mix("bar", "glass_right", 0.45), 0.40)

def bar(a, b, size, color, pressure="even", brush="liner", note="bar"):
    s.stroke([a, b], brush, color, size=size, pressure=pressure, opacity=0.85,
             load=1.0, load_falloff=0.05, note=note)

# the right wall: a vertical every pane down to the bench, the transom, the eaves beam
for d, size in ((2.0, 0.008), (2.6, 0.0065), (3.2, 0.0055), (3.8, 0.005), (4.4, 0.0045)):
    bar(P(HALF, EAVES, d), P(HALF, BENCH + 0.03, d), size, "bar_cool",
        pressure=[0.8, 1.0, 0.9], brush="round_hard" if size > 0.006 else "liner")
bar(P(HALF, 1.35, 4.6), P(HALF, 1.35, 1.15), 0.006, "bar_cool", pressure=[0.4, 0.8, 1.0], brush="round_hard")
bar(P(HALF, EAVES, 4.6), P(HALF, EAVES, 1.4), 0.007, "bar_cool", pressure=[0.5, 1.0], brush="round_hard")

# the left wall: what little of it shows
for d, size in ((3.8, 0.0045), (4.4, 0.004)):
    bar(P(-HALF, EAVES, d), P(-HALF, BENCH + 0.03, d), size, "bar_sun", pressure=[0.9, 1.0, 0.7])
bar(P(-HALF, EAVES, 4.6), P(-HALF, EAVES, 2.7), 0.006, "bar_sun", pressure=[0.6, 1.0], brush="round_hard")

# the end wall: five verticals from the plinth up to the roof line, the two that
# cross the glare thinned where they cross it; then the transoms and the gable
for xm, size, pressure in ((-0.93, 0.004, [1.0, 0.9, 0.75]), (-0.47, 0.0037, [1.0, 0.5, 0.25, 0.8]),
                           (0.0, 0.0037, [1.0, 0.5, 0.3, 0.85]), (0.47, 0.004, [1.0, 0.7, 0.55, 0.9]),
                           (0.93, 0.0042, [1.0, 0.9, 0.85])):
    top = RIDGE - (RIDGE - EAVES) * abs(xm) / HALF
    bar(P(xm, BASE, FAR), P(xm, top, FAR), size, "bar_sun", pressure=pressure)
bar(P(-HALF, 1.35, FAR), P(HALF, 1.35, FAR), 0.004, "bar_sun", pressure=[0.9, 0.45, 0.7, 1.0])
bar(P(-HALF, EAVES, FAR), P(HALF, EAVES, FAR), 0.0045, "bar_sun", pressure=[1.0, 0.5, 0.8, 1.0])
bar(P(-HALF, EAVES, FAR), P(0, RIDGE, FAR), 0.0045, "bar_sun", pressure=[1.0, 0.75])
bar(P(0, RIDGE, FAR), P(HALF, EAVES, FAR), 0.0045, "bar_sun", pressure=[0.75, 1.0])

# the roof: rafters running up to the ridge, and a purlin each side
for d, size in ((2.6, 0.007), (3.2, 0.006), (3.8, 0.005), (4.4, 0.0045)):
    bar(P(HALF, EAVES, d), P(0, RIDGE, d), size, "bar_cool", pressure=[1.0, 0.7],
        brush="round_hard" if size > 0.006 else "liner")
bar(P(-HALF, EAVES, 4.4), P(0, RIDGE, 4.4), 0.004, "bar_sun", pressure=[1.0, 0.7])
bar(P(0.7, 2.7, 2.9), P(0.7, 2.7, FAR), 0.005, "bar_cool", pressure=[1.0, 0.6])

# the glare, once more, over the bars that cross it
s.dry()
field = s.sample(bloom(0.10))
p["glare_film"] = p.at_value(p.mix(field, "bloom_core", 0.5), min(0.95, p.value_of(field) + 0.04))
s.glaze([(SUN[0] - 0.06, SUN[1] - 0.05), SUN, (SUN[0] + 0.05, SUN[1] + 0.06)], "glare_film",
        opacity=0.09, size=0.16, pressure=[0.6, 1.0, 0.6], note="glaze")
print(s.budget_line())
print(s.look(grid=True))
print(s.look(region="B2:E5"))
