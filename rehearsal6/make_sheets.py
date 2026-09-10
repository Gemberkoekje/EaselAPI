"""Side-by-side sheets for REHEARSAL6: each painting against what it is measured by.

REHEARSAL3's `make_sheets.py` is imported by path rather than copied, exactly as
REHEARSAL4's was, so every rehearsal's sheets are laid out identically and can be put
next to one another.

The references are REHEARSAL4's committed copies, which this run's own references were
taken from byte for byte.

Run from the repo root after a run has exported:  python rehearsal6/make_sheets.py
"""
from __future__ import annotations

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
R4 = f"{ROOT}/rehearsal4"


def _sheet():
    src = f"{ROOT}/rehearsal3/make_sheets.py"
    spec = importlib.util.spec_from_file_location("r3_make_sheets", src)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sheet


def main() -> int:
    sheet = _sheet()

    if os.path.exists(f"{HERE}/pass/copy_final.png"):
        print("The pass:")
        sheet([
            (f"{R4}/pass/ref.jpg", "the photograph"),
            (f"{HERE}/pass/copy_final.png", "REHEARSAL6"),
            (f"{ROOT}/rehearsal5/pass/copy_final.png", "REHEARSAL5"),
            (f"{R4}/pass/copy_final.png", "REHEARSAL4"),
        ], f"{HERE}/mug_compared.png")

    if os.path.exists(f"{HERE}/sitter/copy_final.png"):
        print("Reach:")
        sheet([
            (f"{R4}/sitter/ref.jpg", "the photograph"),
            (f"{HERE}/sitter/copy_final.png", "REHEARSAL6"),
            (f"{R4}/sitter/copy_final.png", "REHEARSAL4"),
            (f"{ROOT}/rehearsal3/sitter/copy_final.png", "REHEARSAL3"),
        ], f"{HERE}/sitter_compared.png")

    if os.path.exists(f"{HERE}/pass/own2_final.png"):
        print("The two unprompted paintings:")
        sheet([
            (f"{HERE}/pass/own1_final.png", "1 - no constraint at all"),
            (f"{HERE}/pass/own2_final.png", "2 - must not repeat the first's structure"),
        ], f"{HERE}/unprompted_pair.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
