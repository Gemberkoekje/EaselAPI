"""``easel_paint`` -- the same engine as :mod:`easel`, under the name on the tin.

The distribution is **easel-paint** and the import is ``easel``, which is one name
too many for something a painter meets in the first two minutes. A session installed
the wheel, typed ``import easel_paint`` because that is what it had just installed,
and got ``ModuleNotFoundError``; and the guess the other way round is worse, because
PyPI carries an unrelated distribution called ``easel`` that a painter who reads the
import name and types ``pip install easel`` will get instead of this one.

So both import names are real. Everything here is :mod:`easel` -- the same module
object, the same classes, the same session -- re-exported, so
``easel_paint.Session`` *is* ``easel.Session`` and a painting made through one name
loads through the other. The documents teach ``easel``, which stays the short name
and the one in every example.

    import easel_paint as easel        # if that is the name you installed
    from easel_paint import Session    # or straight out of it
"""

from __future__ import annotations

import easel as _easel
from easel import *  # noqa: F401, F403  (the whole public API, by its own __all__)
from easel import __version__

#: Everything :mod:`easel` exports, so ``from easel_paint import *`` is the same
#: import by the other name -- and so a name added there is exported here the same
#: day rather than the next time somebody remembers this file.
__all__ = [*_easel.__all__, "__version__"]


def __getattr__(name: str):
    """Anything else :mod:`easel` has: submodules, and whatever it grows next.

    ``easel.session``, ``easel.docs`` and the rest are attributes of the package
    rather than names in ``__all__``, and a painter who reached this module by
    typing the distribution's own name should not find it a narrower thing than the
    one the documents describe.
    """
    return getattr(_easel, name)


def __dir__() -> list[str]:
    return sorted(set(__all__) | set(dir(_easel)))
