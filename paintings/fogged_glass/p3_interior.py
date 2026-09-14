# Inside the glass: dark, because a greenhouse interior seen from a white winter
# day is dark. One mass, passes running along the eave so their ends land on the
# frame and not on a sloped boundary. A comb rather than a chisel -- ragged ends,
# and the warm ground breathing through a dark interior reads as the warmth in it.
p["innermid"] = p.at_value(p.desaturate(p.mix(p["neutral"], "viridian", 0.26), 0.28), 0.34)

s.block_in(GLASS.inset(0.024), "bristle", "innermid", direction=-23, density=1.0,
           size=0.068, load=1.0, load_falloff=0.0, note="glass")
