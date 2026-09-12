"""Entry point for the MCPB desktop bundle.

There is nothing to do here but hand off. The manifest declares
``server.type = "uv"``, so the host has already resolved ``easel-paint[mcp]`` from
the sibling ``pyproject.toml`` before this runs; the engine is installed, not
vendored. See ``scripts/pack_mcpb.py`` for why it has to be that way.

``--dir`` arrives from the manifest's ``user_config``, so the directory the user
picked in the install dialog reaches :func:`easel.mcp_server.main` as the argument
it already understands.
"""

from easel.mcp_server import main

if __name__ == "__main__":
    raise SystemExit(main())
