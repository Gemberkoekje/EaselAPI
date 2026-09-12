"""``easel.__version__`` against the version pyproject.toml declares.

The version is written by hand in pyproject.toml and copied by hand into
``easel/__init__.py``, and the copy has already fallen behind once: 0.1.1 shipped
with ``__version__`` still reading 0.1.0. That is not cosmetic. ``build_server``
passes it to the MCP server as its advertised version, so for the whole of 0.1.1
every client that asked was told it was talking to 0.1.0 -- and nothing failed,
which is exactly why it went unnoticed.

The repository's habit is to write a version once and check every other copy
against it: the release workflow refuses a tag that disagrees with pyproject,
``scripts/pack_mcpb.py`` refuses to pack a bundle it cannot stamp, and
``test_server_json.py`` holds server.json to the same line. This is the copy that
had no such check.

Deriving ``__version__`` from ``importlib.metadata`` instead would remove the
second copy altogether, and is the obvious thing to reach for. It is not done
because the scripts in ``scripts/`` import easel straight off ``src/`` without
installing it, where there is no distribution metadata to read -- so it would
need a hardcoded fallback, which is the drifting copy again wearing a hat.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import easel

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def test_version_agrees_with_pyproject() -> None:
    """pyproject.toml decides; ``__init__.py`` follows."""
    assert easel.__version__ == PYPROJECT["version"]


def test_version_is_exported() -> None:
    """It is part of the public surface, and the MCP server reads it off the
    package rather than importing it by name."""
    assert "__version__" in easel.__all__
