R="/home/user/refs/Level1.jpg"
for c in ["C4","E4","C7","F6"]:
    print("=====",c)
    print(s.compare(R, region=cell(c)))
