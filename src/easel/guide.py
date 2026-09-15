"""The older name for :mod:`easel.docs`, kept so that nothing breaks.

`easel.guide` collided with :meth:`easel.Session.guide`, which draws scaffolding
on the view: two unrelated things under one name, both reached from one session.
The module is :mod:`easel.docs` since 0.5.0 and everything that teaches it says
so; this forwards the whole of it, and is not going away.
"""

from __future__ import annotations

from easel.docs import (
    DOCUMENTS,
    FRONT_PAGE,
    FRONT_PAGE_WORDS,
    document_path,
    front_page,
    read,
    write,
)

__all__ = [
    "DOCUMENTS",
    "FRONT_PAGE",
    "FRONT_PAGE_WORDS",
    "document_path",
    "front_page",
    "read",
    "write",
]
