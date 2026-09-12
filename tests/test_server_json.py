"""`server.json` against the package it claims to describe.

The MCP registry stores metadata, not artefacts: what it publishes is this file's
word for where the package is and what it is called. Three of those words are
written down twice in this repository and can drift apart silently -- the version,
the package name, and the server name, which also has to appear verbatim in the
README because that is the string the registry reads out of the published package
description to prove the namespace is ours. A mismatch is not a failing import; it
is a rejected publish, or a registry entry pointing at a release that does not
exist. So the second copy is checked here rather than at the registry.
"""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
README = (ROOT / "README.md").read_text(encoding="utf-8")

#: The one package entry: the PyPI release the registry will point a client at.
PACKAGE = SERVER["packages"][0]


def test_server_name_matches_the_readme_ownership_marker() -> None:
    """The registry proves ownership by finding this string in the published
    description, which is README.md. The name must match it character for
    character, capitals included -- the registry preserves the case it is given."""
    marker = re.search(r"mcp-name:\s*(\S+)", README)
    assert marker, "README.md has lost the mcp-name marker the registry verifies against"
    assert marker.group(1) == SERVER["name"]


def test_package_identifier_is_the_distribution_name() -> None:
    assert PACKAGE["identifier"] == PYPROJECT["name"]


def test_versions_agree_with_pyproject() -> None:
    """Both versions name a PyPI release that has to exist by the time this is
    published, and pyproject.toml is what decides which one that is."""
    assert PACKAGE["version"] == PYPROJECT["version"]
    assert SERVER["version"] == PYPROJECT["version"]


def test_description_fits_the_registry_limit() -> None:
    """The schema caps it at 100 characters, and it is shared with pyproject."""
    assert SERVER["description"] == PYPROJECT["description"]
    assert len(SERVER["description"]) <= 100


def test_the_launch_command_is_written_where_the_website_url_points() -> None:
    """`websiteUrl` sends a client that cannot assemble the arguments to the
    README, so the README has to actually carry the command."""
    assert 'uvx --from "easel-paint[mcp]" easel-mcp' in README


def test_the_mcp_extra_the_launch_command_asks_for_exists() -> None:
    extra = PACKAGE["runtimeArguments"][0]["value"]
    name, bracket = extra.split("[")
    assert name == PYPROJECT["name"]
    assert bracket.rstrip("]") in PYPROJECT["optional-dependencies"]
