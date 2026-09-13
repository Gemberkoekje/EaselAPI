# A second, fainter beam leaving the lamp room to the right: the other lobe of
# a turning lens, which is what says the light is sweeping and not fixed.
# Rehearsed on its own so it can be dropped if it clutters.
s.dry()
s.glaze([(0.69, 0.245), (0.90, 0.262), (1.08, 0.285)], "beam_far", opacity=0.07, size=0.15,
        pressure=[0.4, 0.8, 1.0], note="subject counter-beam, wide")
s.glaze([(0.69, 0.245), (0.88, 0.26), (1.08, 0.28)], "beam_body", opacity=0.10, size=0.07,
        pressure=[1.0, 0.7, 0.35], note="subject counter-beam, body")
print(s.look())
