"""Side-by-side sheets for REHEARSAL4: each painting against what it is measured by.

REHEARSAL3's `make_sheets.py` is imported by path rather than copied, so the panels
are laid out identically and the two runs' sheets can be put next to each other.

Run from the repo root after both runs have exported:
    python rehearsal4/make_sheets.py
"""
from __future__ import annotations

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _sheet():
    src = f"{ROOT}/rehearsal3/make_sheets.py"
    spec = importlib.util.spec_from_file_location("r3_make_sheets", src)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sheet


def main() -> int:
    sheet = _sheet()

    print("The pass:")
    sheet([
        ("C:/temp/Level1.jpg", "the photograph"),
        (f"{HERE}/pass/copy_final.png", "REHEARSAL4 - own pencil, under 300 strokes"),
        (f"{ROOT}/rehearsal3/pass/copy_final.png", "REHEARSAL3, for comparison"),
    ], f"{HERE}/mug_compared.png")

    print("Reach:")
    sheet([
        ("C:/temp/Level3.jpg", "the photograph"),
        (f"{HERE}/sitter/copy_final.png", "REHEARSAL4"),
        (f"{ROOT}/rehearsal3/sitter/copy_final.png", "REHEARSAL3"),
        (f"{ROOT}/rehearsal2/copy_final.png", "REHEARSAL2"),
    ], f"{HERE}/sitter_compared.png")

    print("The two unprompted paintings:")
    sheet([
        (f"{HERE}/pass/own1_final.png", "1 - no constraint at all"),
        (f"{HERE}/pass/own2_final.png", "2 - must not repeat the first's structure"),
    ], f"{HERE}/unprompted_pair.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
