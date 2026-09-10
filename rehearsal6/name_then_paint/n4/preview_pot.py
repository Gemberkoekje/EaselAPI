exec(open("_pal.py").read())
exec(open("_geom.py").read())
exec(open("_pot.py").read())
print(s.preview(SIL, region="E4:G7"))
