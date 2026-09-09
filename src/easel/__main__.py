"""Run the CLI as ``python -m easel``.

``pip install`` puts an ``easel`` executable in the interpreter's scripts
directory, and on plenty of installs -- Windows especially -- that directory is
not on ``PATH``. A painter following the guide should not have to debug their
shell before they can look at their canvas, so the module entry point is always
available:

    python -m easel look painting.easel --grid
"""

from __future__ import annotations

from easel.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
