#!/bin/bash
set -euo pipefail

# Only needed on Claude Code on the web: a local checkout likely already has a
# suitable Python and the package installed some other way.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# Easel requires Python >=3.12 (pyproject.toml), but this environment's
# default `python3` is 3.11. python3.12 is present separately -- use it (or
# 3.13) explicitly rather than the default.
PYTHON=python3.12
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  PYTHON=python3.13
fi

# A venv checked into nothing but the container's own disk: it survives
# between session starts in the same environment, so a second start is a
# near-instant no-op instead of a fresh install.
VENV="$CLAUDE_PROJECT_DIR/.venv"
if [ ! -x "$VENV/bin/python" ]; then
  "$PYTHON" -m venv "$VENV"
fi

"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -e ".[dev]"

# Put python/pytest/ruff/easel on PATH for the rest of the session, so
# `pytest -q`, `ruff check ...` and `easel ...` all work without anyone
# having to `source .venv/bin/activate` first.
echo "export PATH=\"$VENV/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
