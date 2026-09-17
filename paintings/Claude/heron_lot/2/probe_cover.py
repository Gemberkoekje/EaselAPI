# A solid block-in that does not land its colour. Measured on bare ground,
# density=1.0, solid=True, opacity=1.0, pressure="even" - every clause of
# RECIPES' "a plane that is a plane".
from easel import Session, Region
tgt = None
print(" size    px   flat    bristle  round_hard   (mixture 0.865)")
for sz in (0.003, 0.0045, 0.006, 0.008, 0.010, 0.012, 0.016, 0.020, 0.030):
    row = []
    for br in ("flat", "bristle", "round_hard"):
        t = Session(600, 600, texture="linen", ground="#6d635a", seed=5, out_dir="out2")
        c = t.palette.at_value(t.palette.mix(
            t.palette.mix("titanium_white","ultramarine",0.10), "cadmium_red", 0.06), 0.865)
        t.block_in(Region(0.30, 0.30, 0.70, 0.70), br, c, size=sz, density=1.0,
                   solid=True, opacity=1.0, pressure="even")
        row.append(t.palette.value_of(t.sample((0.40, 0.40, 0.60, 0.60))))
    print(f" {sz:.4f} {sz*600:5.1f}  {row[0]:.3f}   {row[1]:.3f}      {row[2]:.3f}")
