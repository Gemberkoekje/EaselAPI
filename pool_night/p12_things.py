s.dry()
p["edge_lit"] = p.at_value(p.mix("deck", "watlit", 0.35), 0.46)
p["metal"]    = p.at_value(p.mix("deck", "watlit", 0.45), 0.62)
p["chair"]    = p.at_value(p.mix("ultramarine", "burnt_umber", 0.50), 0.19)
p["board"]    = p.at_value(p.mix("ultramarine", "burnt_umber", 0.45), 0.24)

# A chair on the left deck: the one upright in the picture. Kept small and only a
# step darker than the deck -- at full dark it became a second subject and owned
# the empty half, which is not what the empty half wants.
s.stroke([(0.134, 0.524), (0.146, 0.390), (0.153, 0.272)], "flat", "chair",
         size=0.006, opacity=0.90, load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(0.192, 0.536), (0.184, 0.398), (0.177, 0.278)], "flat", "chair",
         size=0.0055, opacity=0.90, load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(0.138, 0.498), (0.188, 0.320)], "flat", "chair",
         size=0.0035, opacity=0.75, load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(0.131, 0.272), (0.196, 0.281)], "flat", "chair",
         size=0.012, opacity=0.90, load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(0.166, 0.268), (0.163, 0.244)], "flat", "chair",
         size=0.022, opacity=0.90, load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(0.177, 0.276), (0.175, 0.246)], "liner", "edge_lit",
         size=0.0035, opacity=0.75, load=0.5, load_falloff=0.8, pressure=[1.0, 0.3])

# a board reaching out over the far end, lit from underneath by the water it is over
s.stroke([(1.04, 0.508), (0.900, 0.552), (0.768, 0.592)], "flat", "board",
         size=0.008, opacity=0.90, load=1.0, load_falloff=0.0, pressure="even")
s.stroke([(0.980, 0.532), (0.856, 0.572), (0.772, 0.598)], "liner", "edge_lit",
         size=0.003, opacity=0.80, load=0.5, load_falloff=0.85, pressure=[0.2, 1.0, 0.7])

# a ladder at the near coping: two rails out of the water, and one rung
s.stroke([(0.733, 0.858), (0.739, 0.812), (0.757, 0.795)], "liner", "metal",
         size=0.0050, opacity=0.95, load=0.9, load_falloff=0.45, pressure=[0.15, 1.0, 0.7])
s.stroke([(0.764, 0.876), (0.770, 0.830), (0.788, 0.813)], "liner", "metal",
         size=0.0045, opacity=0.90, load=0.9, load_falloff=0.45, pressure=[0.15, 0.95, 0.6])
s.stroke([(0.744, 0.834), (0.775, 0.851)], "liner", "metal",
         size=0.0035, opacity=0.70, load=0.6, load_falloff=0.7, pressure=[0.7, 0.2])

# the one warm thing in the picture, and the only light that is not the water
s.stroke([(0.094, 0.223), (0.117, 0.226)], "flat", "warm",
         size=0.011, opacity=0.95, load=1.0, load_falloff=0.0, pressure="even")
s.glaze([(0.092, 0.238), (0.118, 0.243)], p.at_value("warm", 0.30), opacity=0.45,
        size=0.030, pressure="swell")
print(s.look())
