"""The optional ``pymixbox`` integration seam.

Skipped unless the ``mixbox`` extra is installed (``pip install
easel-paint[mixbox]``), which the main CI job deliberately does not do. That was
a real coverage gap, since the call site in ``color.mix_many`` has
no ``try``/``except`` of its own, so a pymixbox API break there would surface
as an uncaught crash for the one audience that opts in, with zero warning from
CI.

This checks the integration seam itself -- that it runs, returns a valid
colour, and behaves sanely -- not exact colour values: the rest of the suite
(``test_floor.py``, the golden images) hard-codes Kubelka-Munk-specific numbers
that were never meant to be mixbox-aware, so this file must not flip
``MIXBOX_AVAILABLE`` on for them. It only runs its own few checks, in a
separate CI job that installs the extra just for this file.
"""

from __future__ import annotations

import numpy as np
import pytest

from easel.color import MIXBOX_AVAILABLE, mix_many, parse_color

pytestmark = pytest.mark.skipif(
    not MIXBOX_AVAILABLE, reason="pymixbox is not installed (pip install easel-paint[mixbox])"
)


def test_mix_many_runs_and_returns_a_valid_colour():
    out = mix_many([parse_color("ultramarine"), parse_color("burnt_umber")], [0.5, 0.5])
    assert out.shape == (3,)
    assert out.dtype == np.float32
    assert np.isfinite(out).all()
    assert float(out.min()) >= 0.0 and float(out.max()) <= 1.0


def test_mixing_a_colour_with_itself_is_unchanged():
    c = parse_color("cadmium_red")
    out = mix_many([c, c], [0.3, 0.7])
    assert np.allclose(out, c, atol=1e-3)


def test_mix_many_is_order_independent_for_equal_weights():
    a, b = parse_color("cerulean"), parse_color("yellow_ochre")
    assert np.allclose(mix_many([a, b]), mix_many([b, a]), atol=1e-3)
