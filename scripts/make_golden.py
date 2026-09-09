"""Regenerate the golden images and their hashes.

    python scripts/make_golden.py            # all cases
    python scripts/make_golden.py marks_linen sampler

Run this **only** after looking at what changed and deciding the change is an
improvement. `pytest tests/test_golden.py` writes the new render beside the stored
one as ``<case>.actual.png`` when a case fails; open both, then come back here.

A golden regenerated without looking is worse than no golden at all: it records
that a mark changed and asserts that nobody minded.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tests"))

import golden_cases as gc  # noqa: E402


def main(argv: list[str]) -> int:
    names = argv or list(gc.CASES)
    unknown = [n for n in names if n not in gc.CASES]
    if unknown:
        print(f"Unknown case(s): {', '.join(unknown)}. "
              f"Have: {', '.join(gc.CASES)}", file=sys.stderr)
        return 1

    gc.GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    hashes = {}
    if gc.HASH_FILE.exists():
        hashes = json.loads(gc.HASH_FILE.read_text(encoding="utf-8"))

    for name in names:
        arr = gc.build(name)
        new = gc.digest(arr)
        old = hashes.get(name)
        hashes[name] = new
        if name not in gc.HASH_ONLY:
            Image.fromarray(arr, mode="RGB").save(gc.GOLDEN_DIR / f"{name}.png")
        if name in gc.POOL_BLOCK:
            pooled = gc.pool_average(arr, gc.POOL_BLOCK[name])
            Image.fromarray(pooled, mode="RGB").save(gc.tolerance_reference_path(name))
        actual = gc.GOLDEN_DIR / f"{name}.actual.png"
        if actual.exists():
            actual.unlink()
        state = "unchanged" if old == new else ("new" if old is None else "CHANGED")
        print(f"{name:16s} {arr.shape[1]}x{arr.shape[0]}  {new[:16]}  {state}")

    gc.HASH_FILE.write_text(
        json.dumps(dict(sorted(hashes.items())), indent=2) + "\n", encoding="utf-8"
    )
    print(f"\nWrote {gc.HASH_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
