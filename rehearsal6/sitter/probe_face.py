for c in ["D3","D4","D5","E3"]:
    print("=====", c)
    print(s.compare("ref.jpg", region=cell(c)))
