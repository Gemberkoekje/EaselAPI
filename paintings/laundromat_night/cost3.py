fig = figure()
print("area", round(fig.area, 5), " inset(0.0065)", round(fig.inset(0.0065).area, 5))
print(s.preview([{"shape": fig.inset(0.0065), "label": "figure inset"}],
                region="E4:F6", grid="fine"))
