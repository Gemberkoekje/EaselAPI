# Pass 2: the light. The sun behind the fogged end wall is a bloom on the glass,
# laid as an inward scumble from the wall's own value up to the core. Then the
# lower panes, dirtier and greener toward the foot of the glass, as a graded
# passage rather than a band, and two warm glazes carrying the light down the
# wall and off to the left, mixed close to what they land on.
s.dry()
p["bloom_edge"] = s.sample(bloom(0.15))            # what the bloom meets
print("bloom edge value", round(p.value_of(p["bloom_edge"]), 2))
s.scumble(bloom(), "bloom_edge", "bloom_core", 10, direction="inward", note="bloom")

# the lower panes of the end wall: dirt and algae, heaviest at the foot of the
# glass and gone by the transom
low = polygon([P(-HALF, BASE, FAR), P(-HALF, 1.35, FAR), P(HALF, 1.35, FAR), P(HALF, BASE, FAR)])
s.scumble(low, "glass_far", "glass_low", 6, brush="flat", direction=2, overhang=0,
          load=1.0, load_falloff=0.0, opacity=0.9, jitter=0.01, size_jitter=0.03,
          note="glass low")

# the warmth spreading from the sun: films a step above the field, leaning to its hue
s.dry()
field = s.sample(Region(0.15, 0.45, 0.55, 0.60))
p["warm_film"] = p.at_value(p.mix(field, "bloom_mid", 0.4), p.value_of(field) + 0.05)
s.glaze([SUN, (0.31, 0.50), (0.33, 0.62)], "warm_film", opacity=0.10, size=0.22,
        pressure=[0.9, 0.7, 0.3], note="glaze")
s.glaze([SUN, (0.12, 0.38), (-0.02, 0.42)], "warm_film", opacity=0.09, size=0.18,
        pressure=[0.9, 0.6, 0.2], note="glaze")
print(s.budget_line())
print(s.look(grid=True))
print(s.look(values=True))
