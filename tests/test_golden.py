"""Golden-image regression: what a mark looks like must not change by accident.

Each case in :mod:`golden_cases` is repainted and hashed against a stored value.
A failure writes the new render to ``tests/golden/<case>.actual.png`` beside the
stored ``<case>.png`` and reports how far apart they are, because the only useful
response to one of these failing is to look at both images.

An exact hash mismatch falls back to :func:`golden_cases.close_enough`, a tight
numeric tolerance, before failing -- see that function's docstring for why: a
same-source numpy build has been observed to round a handful of pixels +-1 of 255
differently with nothing about the painting having changed.

If the change was intended: ``python scripts/make_golden.py``.
"""

from __future__ import annotations

import json

import golden_cases as gc
import numpy as np
import pytest
from PIL import Image


def _stored() -> dict:
    if not gc.HASH_FILE.exists():  # pragma: no cover - only before the first generate
        pytest.fail(
            f"No golden hashes at {gc.HASH_FILE}. Generate them with "
            f"`python scripts/make_golden.py` and commit the result."
        )
    return json.loads(gc.HASH_FILE.read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", sorted(gc.CASES))
def test_golden_marks_unchanged(name):
    expected = _stored().get(name)
    if expected is None:  # pragma: no cover - only for a newly added case
        pytest.fail(f"Golden case {name!r} has no stored hash. Run scripts/make_golden.py.")

    arr = gc.build(name)
    actual = gc.digest(arr)
    if actual == expected:
        return
    if gc.close_enough(arr, name):
        return

    # Failed: leave the evidence on disk and say how far it moved.
    out = gc.GOLDEN_DIR / f"{name}.actual.png"
    Image.fromarray(arr, mode="RGB").save(out)
    detail = ""
    ref_path = gc.LOOK_AT.get(name, gc.GOLDEN_DIR / f"{name}.png")
    if name not in gc.HASH_ONLY and ref_path.exists():
        ref = np.asarray(Image.open(ref_path).convert("RGB"), dtype=np.int16)
        if ref.shape == arr.shape:
            delta = np.abs(ref - arr.astype(np.int16))
            changed = (delta.max(axis=2) > 0).mean() * 100.0
            detail = (f" {changed:.2f}% of pixels differ, "
                      f"max channel delta {int(delta.max())}, "
                      f"mean {float(delta.mean()):.3f}.")
        else:
            detail = f" Size changed: {ref.shape} -> {arr.shape}."

    pytest.fail(
        f"Golden case {name!r} changed.{detail}\n"
        f"  expected: {ref_path}\n"
        f"  actual:   {out}\n"
        f"Look at both. If the new marks are better, regenerate with "
        f"`python scripts/make_golden.py {name}`."
    )


def test_golden_cases_are_deterministic():
    """The same case built twice is the same pixels. Without this the rest is noise."""
    a = gc.build("marks_linen")
    b = gc.build("marks_linen")
    assert gc.digest(a) == gc.digest(b)


def test_every_case_has_a_stored_hash():
    stored = _stored()
    missing = sorted(set(gc.CASES) - set(stored))
    assert not missing, f"Golden cases without a stored hash: {missing}"
