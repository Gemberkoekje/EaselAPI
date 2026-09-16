# Pass 3: fix the curtain while it is cheap, clean the left jamb, then sill and lower wall.
p = s.palette
p["curtain"] = p.desaturate(p["curtain"], 0.55)
print("curtain now", p.hex(p["curtain"]), "value", round(p.value_of(p["curtain"]), 2))

# left jamb: the wall laid up to where the pane stops, brush centre on the wall side
s.stroke([(0.11, -0.02), (0.115, 0.30), (0.11, 0.63)], "flat", "wall", size=0.07,
         pressure="even", load=1.0, note="left jamb, wall side")

curtain = polygon([(0.715, -0.02), (1.03, -0.02), (1.03, 0.67), (0.80, 0.675),
                   (0.705, 0.645), (0.725, 0.55), (0.708, 0.40), (0.73, 0.20)])
plan = {"shape": curtain.inset(0.025), "brush": "flat", "size": 0.06,
        "density": 1.0, "direction": (88, 72)}
print("curtain cost", s.cost(plan))
s.block_in(curtain.inset(0.025), "flat", "curtain", density=1.0, size=0.06,
           direction=(88, 72), load=1.0, note="curtain, quiet")

# sill: a flat plane, passes along it, a hair off horizontal
s.block_in(Region(-0.02, 0.60, 1.02, 0.78), "flat", "sill", density=1.0, size=0.10,
           direction=3, load=1.0, note="sill")
# wall below the sill: a band, so a band is the right answer
s.block_in(Region(-0.02, 0.78, 1.02, 1.03), "flat", "wall_low", density=1.0, size=0.13,
           direction=6, load=1.0, note="wall below sill")
print("strokes:", s.stroke_count)
print(s.look(grid=True))
print(s.look(values=True))
