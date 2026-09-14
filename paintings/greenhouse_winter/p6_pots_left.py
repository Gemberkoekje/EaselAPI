# Pass 6: the pots on the left staging, far to near. One is dry stalks, one is
# still green, one is empty and leaning a little.
s.dry()
n0 = len(s.history.records)
g = pot(XL, 3.8, 0.13, 0.12, lean=0.12)
g = pot(XL, 2.9, 0.18, 0.17)
foliage(g, 2.9, scale=0.9)
g = pot(XL, 2.2, 0.15, 0.14)
stalks(g, 2.2, n=3)
print(s.budget_line())
print(s.report(since=n0))
print(s.look(region="A5:C7"))
