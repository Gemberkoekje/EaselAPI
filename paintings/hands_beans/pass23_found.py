# The one cold passage in a warm picture, and the edges that make the subject read.
# An edge is sharpened by painting the mass on the OTHER side of it: the table's
# own colour run along the boundary with the brush's centre outside the hand. A
# dark line along a silhouette would read as a drawn line, which is the same
# mistake wearing a different hat.
s.dry()

# the cold grey left beside the bowl: the only thing in the picture that is not warm
s.glaze([(0.268, 0.742), (0.320, 0.790), (0.352, 0.848)], "grain",
        opacity=0.26, size=0.075, note="table")
s.glaze([(0.300, 0.856), (0.352, 0.900), (0.386, 0.946)], "grain",
        opacity=0.22, size=0.060, note="table")
s.glaze([(0.236, 0.706), (0.286, 0.736)], "grain", opacity=0.18,
        size=0.050, note="table")

# sampled from patches that are pure table -- a span that straddles the hand
# reports the average of both in a confident voice, and that is how a found edge
# turns into a pale halo
p["bg_cup"]   = s.sample(polygon([(0.320, 0.292), (0.462, 0.292),
                                  (0.462, 0.348), (0.320, 0.348)]))
p["bg_pick"]  = s.sample(polygon([(0.500, 0.160), (0.596, 0.160),
                                  (0.596, 0.220), (0.500, 0.220)]))
p["bg_thumb"] = s.sample(polygon([(0.430, 0.790), (0.548, 0.790),
                                  (0.548, 0.848), (0.430, 0.848)]))

# the top of the cupped hand, found against the table
s.stroke([(0.520, 0.404), (0.436, 0.370), (0.356, 0.366), (0.294, 0.388)],
         "flat", "bg_cup", size=0.034, opacity=0.90, load=1.0,
         load_falloff=0.30, pressure="swell", note="subject")
# the upper-left of the picking finger, found against the table
s.stroke([(0.592, 0.262), (0.556, 0.302), (0.526, 0.344)], "flat", "bg_pick",
         size=0.030, opacity=0.85, load=1.0, load_falloff=0.35,
         pressure="swell", note="subject")
# and under the thumb, where the hand stops and the table begins
s.stroke([(0.612, 0.726), (0.540, 0.748), (0.462, 0.742)], "flat", "bg_thumb",
         size=0.028, opacity=0.75, load=1.0, load_falloff=0.40,
         pressure="swell", note="subject")
print(s.look())
