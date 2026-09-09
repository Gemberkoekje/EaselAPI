"""Check the M6 pass criterion against the exported paintings, not the painters' reports.

The brief's definition of done, after M6:

    the human recognises the object, `compare()` reports no cell on it more than
    `0.10` from the reference's value, and the painter can point to strokes it
    rejected in `preview()` or `rehearse()` before painting them. Under 300 strokes.

Recognition is the human's call and stroke counts are in the logs. This checks the
number, on the object, from the exported PNG — and separately reports how many of any
failures are *unreachable*, because `probe_value_floor.py` shows the palette bottoms
out at 0.235 and both references have cells below that.

Run from the repo root:  python rehearsal3/verify_pass.py
"""
from __future__ import annotations

import os

import numpy as np
from PIL import Image

from easel.measure import compare_images

HERE = os.path.dirname(os.path.abspath(__file__))

#: The cells the mug itself covers in Level1.jpg, read off a gridded look of the
#: reference (rehearsal3/_ref_grid.png). Rim and spoon on row 2, tea and handle on
#: 3, body and crewmate on 4-5, foot on 6. Cells that are mostly table or cast
#: shadow are deliberately excluded: the criterion says "on the object".
MUG_CELLS = [
    "D2", "E2",
    "D3", "E3", "F3",
    "D4", "E4", "F4",
    "D5", "E5", "F5",
    "D6", "E6",
]
#: The same, plus the cells the mug only clips - its left edge and the handle's
#: outer sweep. Reported alongside so the choice of mask cannot flatter the result.
MUG_CELLS_WIDE = MUG_CELLS + ["C3", "C4", "C5", "F2", "G4"]

#: Measured by probe_value_floor.py: the darkest this palette reaches, anywhere.
VALUE_FLOOR = 0.235
THRESHOLD = 0.10


def check(painting: str, reference: str, cells: list[str], label: str) -> None:
    if not os.path.exists(painting):
        print(f"\n{label}: missing ({painting})")
        return
    canvas = np.asarray(Image.open(painting).convert("RGB"))
    ref = np.asarray(Image.open(reference).convert("RGB"))
    comparison = compare_images(canvas, ref)
    by_label = {c.label: c for c in comparison.cells}

    on_object = [by_label[name] for name in cells if name in by_label]
    out = [c for c in on_object if abs(c.delta) > THRESHOLD]
    # A cell whose reference sits more than a threshold below the floor cannot be
    # brought within the threshold by any stroke: the paint does not go that dark.
    unreachable = [c for c in out if c.ref < VALUE_FLOOR - THRESHOLD]
    real = [c for c in out if c not in unreachable]

    print(f"\n{label}")
    print(f"  cells on the object      {len(on_object)}")
    print(f"  more than {THRESHOLD:.2f} out       {len(out)}")
    print(f"    of those, unreachable  {len(unreachable)}"
          f"  (reference below the {VALUE_FLOOR:.3f} floor)")
    print(f"    of those, the painter's {len(real)}")
    if out:
        worst = max(out, key=lambda c: abs(c.delta))
        print(f"  worst on the object      {worst}")
    for c in sorted(out, key=lambda c: -abs(c.delta)):
        tag = "unreachable" if c in unreachable else "painter's"
        print(f"    {c.label}  ref {c.ref:.2f}  canvas {c.canvas:.2f}  "
              f"{c.delta:+.2f}   {tag}")

    whole = [c for c in comparison.cells if abs(c.delta) > THRESHOLD]
    print(f"  whole picture            {len(whole)} of {len(comparison.cells)} out")


if __name__ == "__main__":
    print("M6 pass criterion, checked from the exported PNGs.")
    print(f"Palette floor {VALUE_FLOOR:.3f} (probe_value_floor.py); threshold "
          f"{THRESHOLD:.2f}.")

    check(f"{HERE}/pass/copy_final.png", "C:/temp/Level1.jpg", MUG_CELLS,
          "HEADLINE - own pencil, mug on the object cells")
    check(f"{HERE}/pass/copy_final.png", "C:/temp/Level1.jpg", MUG_CELLS_WIDE,
          "HEADLINE - own pencil, mug plus the cells it only clips")
    check(f"{HERE}/assisted/copy_final.png", "C:/temp/Level1.jpg", MUG_CELLS,
          "ASSISTED - machine sketch, mug on the object cells")
