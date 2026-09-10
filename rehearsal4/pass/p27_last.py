"""One stroke left. The reflected light at the base overshot onto the shadow
and reads as a white bar; bury the half of it that is not on the mug."""
s.dry()
s.stroke([(0.388, 0.7075), (0.470, 0.7205), (0.540, 0.7085)], "flat",
         s.palette.mix(s.palette["shad_core"], s.palette["shad_pen"], 0.35),
         size=0.022, pressure="even", load=1.0, note="bury the white bar")
print("total:", s.stroke_count)
print(s.look())
print(s.look(reference="ref.jpg"))
print(s.export("copy_final.png"))
print(s.timelapse_gif("copy_timelapse.gif"))
