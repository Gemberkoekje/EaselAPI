import math
def body_poly():
    pts_l = [(0.4995,0.5660),(0.5060,0.6100),(0.5155,0.6580),(0.5235,0.6960),(0.5290,0.7255)]
    pts_r = [(0.6705,0.5600),(0.6645,0.6050),(0.6550,0.6540),(0.6470,0.6930),(0.6415,0.7245)]
    base  = [(0.5290,0.7255),(0.5480,0.7330),(0.5850,0.7355),(0.6210,0.7325),(0.6415,0.7245)]
    lip   = [(0.6705,0.5600),(0.6400,0.5760),(0.5850,0.5820),(0.5300,0.5755),(0.4995,0.5660)]
    return polygon(pts_l + base[1:-1] + list(reversed(pts_r)) + lip[1:-1])

body = body_poly()
rim  = ellipse((0.5855, 0.5525), 0.0895, 0.0300)
print("body area", round(body.area,4), "axis", round(body.axis,1))
print("rim  area", round(rim.area,4))
s.preview(body, region="D4:H8")
s.preview(rim, region="D4:H8")
