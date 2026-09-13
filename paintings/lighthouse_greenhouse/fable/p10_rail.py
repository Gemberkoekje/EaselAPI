# Pass 10: the stair again, named as the weakest passage -- it read as a dark
# hose wound round the tower. A handrail following each turn a little above
# the treads, and three balusters per turn at uneven spacing, set between the
# pots, is what says it is a stair. (Small lit tread marks along the band's top
# edge were rehearsed as the alternative and vanished at picture scale.)
p["rail"] = p.at_value("iron", 0.22)
for k, ths in ((0, (0.9, 1.9, 2.75)), (1, (0.25, 1.15, 2.0)), (2, (0.75, 1.55, 2.4))):
    arc = stair_arc(k)
    s.stroke([(x, y - 0.031) for x, y in arc], "liner", "rail", size=0.003, opacity=0.85,
             pressure="even", note="subject handrail")
    for th in ths:
        x, y = stair_point(k, th)
        s.stroke([(x, y - 0.006), (x, y - 0.031)], "liner", "rail", size=0.0025, opacity=0.8,
                 pressure="even", note="subject baluster")
print(s.look(region="E3:G7"))
print(s.look())
