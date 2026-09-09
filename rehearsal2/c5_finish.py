R = r"C:\temp\AntonConspiracy.jpg"
p = s.palette
p["red_dk"] = p.mix(p["red"], "burnt_umber", 0.4)
print("red_dk", p.hex(p["red_dk"]), round(p.value_of(p["red_dk"]), 2))

# --- the lower face: no outline. Dark outside the profile, mid flesh on the lip and chin, beard below
s.stroke([(0.398, 0.40), (0.405, 0.46), (0.41, 0.52)], "round_hard", "dark", size=0.024, pressure="even")
s.stroke([(0.428, 0.41), (0.436, 0.45), (0.442, 0.485)], "round_hard", "flesh_mid", size=0.02, pressure="even")
s.stroke([(0.445, 0.40), (0.455, 0.46)], "round_soft", "flesh", size=0.025, pressure="even")
s.dab(0.44, 0.437, "round_hard", "beard", size=0.011)
s.stroke([(0.44, 0.49), (0.455, 0.545), (0.49, 0.565), (0.525, 0.55)], "bristle", "beard", size=0.03, load=1.0, pressure="even")
s.smudge([(0.415, 0.395), (0.425, 0.42)], size=0.02)

# --- the green sliver at D2; two wisps at the crown
s.stroke([(0.402, 0.12), (0.408, 0.26)], "bristle", "wall_mid2", size=0.03, pressure="even")
s.stroke([(0.415, 0.14), (0.425, 0.22)], "bristle", "hair", size=0.025, load=1.0, pressure="even")
s.stroke([(0.50, 0.06), (0.56, 0.03)], "round_hard", "hair_hi", size=0.008, pressure="taper")
s.stroke([(0.62, 0.05), (0.68, 0.09)], "round_hard", "hair_lt", size=0.008, pressure="taper")

# --- the table edge, knocked back; the shirt, darker and narrower
s.stroke([(0.78, 0.635), (1.0, 0.625)], "bristle", "table", size=0.03, pressure="even", opacity=0.75)
s.stroke([(0.79, 0.45), (0.80, 0.60)], "bristle", "dark", size=0.05, pressure="even")
s.stroke([(0.83, 0.46), (0.95, 0.47), (1.0, 0.50)], "bristle", "red_dk", size=0.045, load=0.8, pressure="taper")
s.stroke([(0.84, 0.55), (0.93, 0.58)], "bristle", "red_dk", size=0.04, load=0.7, pressure="taper")

# --- break the striping on the left wall with two crossing broken marks
s.stroke([(0.02, 0.30), (0.20, 0.16)], "flat", "wall_mid2", size=0.09, load=0.5, pressure="taper")
s.stroke([(0.05, 0.22), (0.22, 0.10)], "flat", "wall_mid", size=0.08, load=0.5, pressure="taper")

print("strokes:", s.stroke_count)
print(s.look(reference=R))
print(s.look(reference=R, values=True))
print(s.look())
s.export("copy_final.png")
s.timelapse_gif("copy_timelapse.gif")
print("exported")
