plan = {
    span("A1", "D3"):  0.35,   # the fall of light on the table, upper left
    span("F6", "H8"):  0.23,   # the table, dead corner
    BOWL_OUT:          0.42,   # the bowl
    BOWL_IN:           0.30,   # beans in the bowl
    CUP_PALM:          0.55,   # the cupped hand
    CUP_HOLLOW:        0.36,   # the palm's hollow, beans in shadow
    PICK_BACK:         0.62,   # the back of the picking hand
    PICK_CURL:         0.48,   # its curled fingers, turning away
    polygon(ribbon(*CUP_ARM).closed):   0.44,   # the forearm, dropping back
    polygon(ribbon(*PICK_INDEX).closed): 0.70,  # the lit descending finger
}
print(s.compare(plan))
