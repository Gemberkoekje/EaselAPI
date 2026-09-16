from easel import Region
print(s.compare({
    Region(0.05, 0.05, 0.60, 0.30): 0.66,   # sky, upper
    Region(0.02, 0.52, 0.22, 0.85): 0.42,   # yard, near
    Region(0.30, 0.34, 0.45, 0.50): 0.62,   # the far end of the glass, in haze
    Region(0.62, 0.26, 0.76, 0.42): 0.42,   # mid glass, fogged
    Region(0.84, 0.42, 0.99, 0.72): 0.44,   # the near pane -- the subject
    Region(0.86, 0.14, 0.99, 0.24): 0.34,   # glass under the near eave
}))
