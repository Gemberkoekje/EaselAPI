# Defect probe: after s.erase(region), the erased graphite is gone from the
# canvas but sketch_lines() still hands the line back, with all of its points --
# including the ones inside the erased region. There is no way to ask which
# lines are still actually drawn, so anything built on sketch_lines() (e.g.
# re-laying the drawing after a block-in buries it) silently resurrects the
# lines you deliberately rubbed out.
# Run from this directory:  python t2_erase_sketchlines.py
from easel import Session, span

s = Session(600, 400, ground="toned_grey", seed=1)
s.pencil([(0.05, 0.5), (0.45, 0.5)])          # wholly inside A1:B8
s.pencil([(0.55, 0.5), (0.95, 0.5)])          # wholly outside it

print("lines before erase:", len(s.sketch_lines()))
s.erase(span("A1", "D8"))                      # rub out the left half
print("lines after  erase:", len(s.sketch_lines()))
for i, ln in enumerate(s.sketch_lines()):
    xs = [q[0] for q in ln]
    print(f"  line {i}: x {min(xs):.2f}-{max(xs):.2f}  ({len(ln)} pts)")
print()
print("expected: the first line is gone, or comes back with no points.")
print("actual  : both lines come back whole; the erase is invisible to the API.")
