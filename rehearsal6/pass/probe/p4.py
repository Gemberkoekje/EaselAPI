R="/home/user/refs/Level1.jpg"
for c in ["H1","E1","D4"]:
    print(c, s.look(reference=R, region=cell(c), grid="fine"))
