R="/home/user/refs/Level1.jpg"
for c in ["C2","D1","F2","D6","F3"]:
    print(c, s.look(reference=R, region=cell(c), grid="fine"))
