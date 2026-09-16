# The signature. Not a name -- I do not have one. The whole painting is made of one
# gesture repeated: a line that runs downward and loses itself -- the runnels, the
# drips, the dead grass, the branches. So the mark is that gesture made once, alone,
# in the corner, on ground where no water is running. Two strokes, close in value to
# the frozen ground they sit on, small enough that you find them only if you look.
p["sign"] = p.at_value(p.mix(p["neutral"], "burnt_umber", 0.36), 0.28)

s.stroke([(0.0385, 0.9405), (0.0400, 0.9720)], "liner", "sign", size=0.0034,
         pressure=[0.9, 0.0], load=1.0, opacity=0.80, note="signature")
s.stroke([(0.0330, 0.9480), (0.0455, 0.9455)], "liner", "sign", size=0.0026,
         pressure=[0.0, 0.7], load=1.0, opacity=0.70, note="signature")
