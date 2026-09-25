"""The ``easel`` MCP server: the CLI's verbs, with the pictures coming back.

The library is the interface and the CLI is a thin wrapper over it; this is a
second wrapper of the same thickness, for a painter whose client speaks MCP. One
tool per CLI verb, the same arguments under the same names, and the same
``.easel`` file as the only state -- every tool loads it, does one thing and saves
it back, so a painting can be worked on through the server, the shell and a Python
script in any order.

What the server adds is that **the looking tools hand back the image**. ``look``,
``preview``, ``rehearse``, ``compare`` and ``prepare`` return their PNG inline
beside the path they wrote it to, so the loop the guide asks for -- look every five
to fifteen strokes -- costs one call instead of a call and a file read. ``run`` does
the same for a pass it rehearses.

It adds three tools the CLI has not got, and they are the three questions about a
mark that has not been made yet: ``preview`` (where does it go), ``rehearse`` (what
will it look like) and ``cost`` (what does it charge). They take the plan the
Python API takes, written as JSON, and hand back the Python that paints it -- so
the plan that was checked is the plan that lands, rather than one retyped from it.

Painting itself goes through ``run``, exactly as it does from the shell: the script
has ``s``, ``palette`` and the whole public API already in scope, and the server
takes it as text so nothing has to be written to disk first. That means the server
executes Python sent by its client, which is the same trust boundary ``easel run``
has always had -- the painter's own script is the point. Launch it for a painter
you would hand a shell to, and no other.

Launch it with the ``easel-mcp`` command, or, when the scripts directory is not on
``PATH`` (Windows, mostly)::

    python -m easel.mcp_server --dir ~/paintings

The ``mcp`` package is an opt-in extra, like ``mixbox``: ``pip install
easel-paint[mcp]``. Nothing else in the engine imports it.
"""

from __future__ import annotations

import argparse
import contextvars
import dataclasses
import functools
import os
import traceback
import warnings
from pathlib import Path
from typing import Any

from PIL import Image as _PILImage

from easel import demo as _demo
from easel import diagnosis as _diagnosis
from easel import docs as _docs
from easel import notices as _notices
from easel import regions as _regions
from easel.brush import Brush
from easel.cli import parse_size, reference_text, run_alternatives, run_script
from easel.look import DEFAULT_LOOK_SIZE
from easel.notices import EaselWarning
from easel.regions import Region, as_place
from easel.session import PLAN_ACCEPTS, Session

try:
    from mcp.server.mcpserver import Image, MCPServer
    from mcp.server.mcpserver.exceptions import ToolError

    MCP_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised only where the extra is absent
    Image = MCPServer = ToolError = None  # type: ignore[assignment]
    MCP_AVAILABLE = False

__all__ = ["MCP_AVAILABLE", "build_server", "main"]

_NEEDS_MCP = (
    "The MCP server needs the `mcp` package, which is an opt-in extra: "
    "pip install -e '.[mcp]' (or `pip install easel-paint[mcp]`). "
    "Everything else in easel works without it."
)

#: A place, as it arrives over JSON. The five forms are the ones the API takes --
#: a named region, a grid cell, a span of cells, a rectangle, or an outline as a
#: list of points -- plus a sixth the wire needs: an object naming one of the shape
#: builders, because a painter should not have to invent coordinates to describe a
#: mass. See :func:`_place`.
Place = str | list[float] | list[list[float]] | dict[str, Any]

#: Every field of a :class:`~easel.brush.Brush`, which every painting call takes as
#: an override beside its own arguments.
_BRUSH_FIELDS = frozenset(f.name for f in dataclasses.fields(Brush))


#: What each kind of plan entry may carry, from the engine, which now refuses the
#: same keys at the same moment -- while the plan is still free. This check was the
#: server's alone for a release: `cost` walks the passes and never touches the brush
#: overrides, so a misspelled `size` priced happily at the default and then raised
#: when the echoed Python was pasted into `run`. A quote for a plan that cannot be
#: painted is worse than no quote: it is the drift the echo exists to prevent,
#: arriving as a price.
_ACCEPTS = PLAN_ACCEPTS

#: The shape builders, by the key that names one in a place object. The value under
#: that key is the builder's first argument; everything else in the object is a
#: keyword argument to it.
_BUILDERS = {
    "polygon": _regions.polygon,
    "ellipse": _regions.ellipse,
    "blob": _regions.blob,
    "hull": _regions.hull,
    "ribbon": _regions.ribbon,
    "roughen": _regions.roughen,
}

# The CLI turns these into one clean `easel: ...` line instead of a traceback, and
# the server says the same words for the same input. Anything outside the set is a
# crash rather than bad input, and is reported differently -- see `_tool`.
_EXPECTED = (OSError, ValueError, KeyError, SyntaxError, _PILImage.DecompressionBombError)

_PLACE_HELP = (
    "a named region ('upper-band'), a grid cell ('D4'), a span of cells ('C3:F6'), "
    "a rectangle [x0, y0, x1, y1], an outline [[x, y], ...], or a shape builder "
    "like {'blob': 'D5', 'radius': 0.12, 'seed': 3} -- also 'ellipse', 'hull', "
    "'ribbon' and 'polygon', each taking its first argument under its own name, and "
    "'roughen', which walks another place's outline off its line: "
    "{'roughen': {'blob': 'D5'}, 'amp': 0.006, 'seed': 4}"
)

_PLAN_HELP = (
    "A plan is a list of entries, or one entry on its own. A mark is a list of "
    "points, or an object with 'points' and any stroke argument. A film is a mark "
    "with 'glaze': true, and the glaze verb's own 'brush': \"round_soft\" and an "
    "'opacity' such as 0.18 written beside it, since a mark takes a stroke's "
    "defaults. A mass is an "
    "object with 'shape' (a place) and any block_in argument -- 'brush', 'color', "
    "'size', 'direction', 'density', 'edge': \"clean\" for a drawn contour or "
    "\"hard\" for one no paint crosses -- broken against the tooth over 'feather', "
    "0.002 left off and 0 to cut it on the line -- and 'solid': true for paint with "
    "no ground showing through it. "
    "A sweep is an object with 'edge' (a place, or "
    "an open run of points) and any sweep argument -- 'into', 'depth', 'cross', "
    "'passes', 'closed'. A passage is an object with 'band' (a place), 'color_a', "
    "'color_b' and any scumble argument -- 'n', 'direction': \"inward\" for a "
    "centred fall-off. A burial is an object with 'cover' (a place) and 'color', "
    "held to that place unless 'edge' says \"ragged\". "
    "A bare place on its own is a mass. A whole pass is a plan: its masses, "
    "passages, marks and films, in the order they are laid."
)


# --------------------------------------------------------------------------------------
# Places and plans, as they arrive over the wire
# --------------------------------------------------------------------------------------
def _place(value, *, point_ok: bool = False):
    """One place, in any of the forms :data:`Place` describes.

    ``point_ok`` allows a bare ``[x, y]``, which ``ellipse`` and ``blob`` accept as
    a centre to sit around. Everywhere else a two-number list is a mistake worth
    naming, because it is one point short of a rectangle and one short of an
    outline.
    """
    if isinstance(value, dict):
        return _build(value)
    if isinstance(value, str):
        return as_place(value)
    try:
        items = list(value)
    except TypeError:
        # A number, or anything else that is not a run of things. Named here rather
        # than left to raise somewhere further in, where the message would be about
        # iteration and not about places.
        raise ValueError(f"{value!r} is not a place. Give {_PLACE_HELP}.") from None
    if items and all(isinstance(p, (list, tuple)) for p in items):
        return _regions.polygon([(float(x), float(y)) for x, y in items])
    if point_ok and len(items) == 2:
        return (float(items[0]), float(items[1]))
    if len(items) == 4:
        return Region(*(float(v) for v in items))
    raise ValueError(
        f"{value!r} is not a place. Give {_PLACE_HELP}."
    )


def _build(spec: dict):
    """A place object: one builder's name, its first argument, and its keywords."""
    named = [k for k in spec if k in _BUILDERS]
    if len(named) != 1:
        raise ValueError(
            f"A shape object names exactly one of {', '.join(sorted(_BUILDERS))}, "
            f"got {sorted(spec) or 'nothing'}. For example "
            f"{{'blob': 'D5', 'radius': 0.12, 'seed': 3}}."
        )
    key = named[0]
    kwargs = {k: v for k, v in spec.items() if k != key}
    first = spec[key]
    if key in ("hull", "ribbon"):
        # Both take a *list* of things: points, and for hull also shapes or regions.
        # A bare string would iterate as its characters, which is a confusing way to
        # be told that a hull of one place is not a hull.
        if not isinstance(first, (list, tuple)):
            example = ("{'ribbon': [[0.2, 0.8], [0.5, 0.5]], 'width': 0.09}"
                       if key == "ribbon"
                       else "{'hull': [[0.3, 0.2], [0.55, 0.12], [0.6, 0.45]]}")
            raise ValueError(
                f"{key!r} runs along a list of places, not {first!r}. "
                f"For example {example}."
            )
        first = [p if isinstance(p, (int, float)) else _place(p, point_ok=True)
                 for p in first]
    elif key == "roughen":
        # An outline to walk, so never a bare point -- and a run of points is the
        # closed outline it is everywhere else here. `calm` is places too.
        first = _place(first)
        if "calm" in kwargs:
            kwargs["calm"] = _calm(kwargs["calm"])
    elif key != "polygon":
        first = _place(first, point_ok=True)
    try:
        return _BUILDERS[key](first, **kwargs)
    except TypeError as exc:
        raise ValueError(
            f"{key}(...) does not take that: {exc}. A place object carries the "
            f"builder's own arguments only -- brush, colour and the rest of a mass "
            f"go beside it, under 'shape'."
        ) from exc


def _calm(value):
    """Where a roughened outline is still: a place, a point, or a list of either.

    A list of points is that many points, as ``roughen`` reads it, and not an
    outline -- an outline to calm along arrives as a shape object.
    """
    if isinstance(value, (list, tuple)) and value and not _numbers(value):
        return [_calm(one) for one in value]
    return _place(value, point_ok=True)


def _numbers(value) -> bool:
    """A point or a rectangle: a place written as numbers, not a list of places."""
    return all(isinstance(v, (int, float)) for v in value)


def _is_place_object(entry: dict) -> bool:
    """True for a shape object standing on its own, which is a mass like any place.

    It carries the builder's arguments and nothing else: a mass that wants a brush
    or a colour is written the long way, under ``shape``, so that there is never a
    question of whose keyword a keyword is.
    """
    return (not {"shape", "region", "edge", "points"} & set(entry)
            and len([k for k in entry if k in _BUILDERS]) == 1)


def _plan(entries) -> tuple[list, list[str]]:
    """A JSON plan, as the planning tools take it, and the Python that paints it.

    The second half is the point. Through the server a plan is JSON and a painting
    is Python, so a plan that is checked and then *retyped* into a script is a plan
    that will drift between the two -- which is the one thing ``preview``,
    ``rehearse`` and ``cost`` exist to prevent. Every one of them hands back the
    call it just priced, ready to paste into ``run``.
    """
    if isinstance(entries, (dict, str)) or _one_path(entries):
        entries = [entries]
    specs: list = []
    lines: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            if _one_path(entry):
                specs.append({"points": _points(entry)})
                lines.append(f"s.stroke({_py_points(entry)})")
                continue
            specs.append(_place(entry))
            lines.append(f"s.block_in({_py_place(entry)})")
            continue

        if _is_place_object(entry):
            specs.append(_place(entry))
            lines.append(f"s.block_in({_py_place(entry)})")
            continue

        if "cover" in entry:
            _check("cover", entry)
            source = entry["cover"]
            specs.append(dict(entry, cover=_place(source)))
            lines.append(f"s.cover({_py_place(source)}"
                         f"{_echo_args(entry, 'cover', 'points', 'label')})")
        elif "points" not in entry and ("band" in entry or (
                ("shape" in entry or "region" in entry)
                and ("color_a" in entry or "color_b" in entry))):
            # A passage names the two colours it steps between, which is what tells
            # it from a mass filling the same place -- and what used to be missed:
            # a scumble-shaped entry carrying `shape=` was priced as a block-in.
            _check("scumble", entry)
            source = entry.get("band", entry.get("shape", entry.get("region")))
            key = "band" if "band" in entry else (
                "shape" if "shape" in entry else "region")
            specs.append(dict(entry, **{key: _place(source)}))
            lines.append(f"s.scumble({_py_place(source)}"
                         f"{_echo_args(entry, 'band', 'shape', 'region', 'points', 'label')})")
        elif "points" not in entry and ("shape" in entry or "region" in entry):
            # ``edge`` is kept here and dropped for a sweep: on a mass it is
            # block_in's ragged/clean/hard boundary and belongs in the echoed call,
            # and on a sweep it is the boundary, which is passed positionally.
            _check("mass", entry)
            source = entry.get("shape", entry.get("region"))
            specs.append(dict(entry, shape=_place(source)))
            lines.append(f"s.block_in({_py_place(source)}"
                         f"{_echo_args(entry, 'shape', 'region', 'points', 'label')})")
        elif "points" not in entry and "edge" in entry:
            _check("sweep", entry)
            edge = entry["edge"]
            specs.append(dict(entry, edge=_edge(edge)))
            lines.append(f"s.sweep({_py_edge(edge)}"
                         f"{_echo_args(entry, 'shape', 'region', 'edge', 'points', 'label')})")
        elif "points" in entry:
            _check("stroke", entry)
            specs.append(dict(entry, points=_points(entry["points"])))
            lines.append(f"s.stroke({_py_points(entry['points'])}"
                         f"{_echo_args(entry, 'shape', 'region', 'edge', 'points', 'label')})")
        else:
            raise ValueError(
                f"A plan entry is a mark ('points'), a mass ('shape'), a sweep "
                f"('edge'), a passage ('band' with 'color_a' and 'color_b') or a "
                f"burial ('cover'), and {sorted(entry)} is none of them. A place on "
                f"its own is a mass, and a bare list of points is a mark."
            )
    return specs, lines


def _echo_args(entry: dict, *drop: str) -> str:
    """A plan entry's keywords as Python, less the ones passed positionally.

    Which keys are dropped depends on the kind, because ``edge`` means two things:
    a sweep's boundary, which is its first argument, and a mass's
    ragged/clean/hard boundary, which is a keyword like any other and has to survive
    into the echo.
    """
    rest = {k: v for k, v in entry.items() if k not in drop}
    return "".join(f", {k}={v!r}" for k, v in rest.items())


def _check(kind: str, entry: dict) -> None:
    """Refuse a keyword the call would not take, while the plan is still free."""
    unknown = sorted(set(entry) - _ACCEPTS[kind] - _BRUSH_FIELDS - {"label"})
    if unknown:
        raise ValueError(
            f"A {kind} does not take {', '.join(repr(k) for k in unknown)}. It takes "
            f"{', '.join(sorted(_ACCEPTS[kind]))} -- and any brush field, to override "
            f"one for this mark alone."
        )


def _edge(value):
    """A sweep's boundary: a shape, or an open run of points that need not close."""
    if isinstance(value, (list, tuple)) and value and all(
            isinstance(p, (list, tuple)) for p in value):
        return _points(value)
    return _place(value)


def _points(value) -> list[tuple[float, float]]:
    return [(float(x), float(y)) for x, y in value]


def _one_path(value) -> bool:
    """True for a single run of points -- one mark -- rather than a list of entries."""
    if isinstance(value, (str, dict)):
        return False
    try:
        items = list(value)
    except TypeError:
        return False
    return bool(items) and all(
        isinstance(p, (list, tuple)) and len(p) == 2
        and all(isinstance(v, (int, float)) for v in p)
        for p in items
    )


def _py_points(value) -> str:
    return "[" + ", ".join(f"({float(x):.4g}, {float(y):.4g})" for x, y in value) + "]"


def _py_place(value) -> str:
    """The Python call that builds this place, exactly as the painter would type it."""
    if isinstance(value, dict):
        named = [k for k in value if k in _BUILDERS][0]
        first = value[named]
        if named == "roughen":
            # A run of points here is the outline `_place` closed, and `roughen`
            # handed a bare run in Python walks it open and returns a run.
            head = _py_place(first)
        elif _one_path(first):
            head = _py_points(first)
        elif named in ("hull", "ribbon"):
            head = "[" + ", ".join(_py_place(p) for p in first) + "]"
        else:
            head = _py_place(first)
        rest = "".join(f", {k}={_py_calm(v) if k == 'calm' else repr(v)}"
                       for k, v in value.items() if k != named)
        return f"{named}({head}{rest})"
    if isinstance(value, str):
        text = value.strip()
        if ":" in text:
            first, last = (p.strip() for p in text.split(":", 1))
            return f"span({first!r}, {last!r})"
        return (f"cell({text!r})" if as_place(text).name == text.upper()
                else f"region({text!r})")
    items = list(value)
    if _one_path(items):
        return f"polygon({_py_points(items)})"
    if len(items) == 2:
        return f"({float(items[0]):.4g}, {float(items[1]):.4g})"
    return "Region(" + ", ".join(f"{float(v):.4g}" for v in items) + ")"


def _py_calm(value) -> str:
    """``roughen``'s ``calm`` as Python: :func:`_calm`, the other way round."""
    if isinstance(value, (list, tuple)) and value and not _numbers(value):
        return "[" + ", ".join(_py_calm(one) for one in value) + "]"
    return _py_place(value)


def _py_edge(value) -> str:
    if isinstance(value, (list, tuple)) and _one_path(value):
        return _py_points(value)
    return _py_place(value)


# --------------------------------------------------------------------------------------
# Saying what went wrong, and what the file said as it opened
# --------------------------------------------------------------------------------------
#: What the session files a tool opened said as they opened, for :func:`_tool` to hand
#: back first. ``None`` outside a tool.
_OPENED: contextvars.ContextVar[list | None] = contextvars.ContextVar("easel_opened",
                                                                     default=None)


def _load(path) -> Session:
    """Open a session file for a tool, keeping what opening it said.

    What a file says as it opens -- an ``out_dir`` somewhere foreign, an engine older
    than this one -- was warned to this process's stderr, which a painter working
    through a client never sees: the gap 0.6.0 closed for what a *call* says, left
    open for what a *file* says. Every tool opens its file here, and :func:`_tool`
    puts what was said at the top of the answer.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=EaselWarning)
        session = Session.load(path)
    said = _OPENED.get()
    if said is not None:
        said.extend(session._load_notices)
    return session


def _said_first(said: list, result):
    """A tool's answer with what its file said at load above it, the way the shell prints it."""
    head = _notices.block(said, when="at load")
    if not head:
        return result
    if isinstance(result, str):
        return _join(head, result)
    if isinstance(result, list):
        if result and isinstance(result[0], str):
            return [_join(head, result[0]), *result[1:]]
        return [head, *result]
    return result


def _tool(fn):
    """Turn a failure into words the painter can act on, and say what the file said.

    The CLI catches the bad-input exceptions and prints one ``easel: ...`` line;
    this says the same words for the same input. Anything else is a crash, and gets
    its type and traceback rather than the generic "error executing tool" the SDK
    would otherwise hand the client -- there is no console for a painter to read
    here, so a withheld message is a message nobody sees. For the same reason,
    whatever the session file said as the tool opened it (:func:`_load`) comes back
    at the top of the answer, or of the failure.
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        said: list = []
        token = _OPENED.set(said)
        try:
            return _said_first(said, fn(*args, **kwargs))
        except _EXPECTED as exc:
            raise ToolError(_join(_notices.block(said, when="at load"),
                                  f"easel: {exc}")) from exc
        except Exception as exc:
            raise ToolError(_join(
                _notices.block(said, when="at load"),
                f"easel: {type(exc).__name__}: {exc}\n\n{traceback.format_exc()}",
            )) from exc
        finally:
            _OPENED.reset(token)

    return wrapper


def _join(*parts: str) -> str:
    """The parts of a result that are present, one per block.

    A notice block is empty when the call said nothing, and an empty line at the top
    of an answer is the kind of thing a painter reads as a missing sentence.
    """
    return "\n".join(p for p in parts if p)


def _grid(value) -> bool | str:
    """``grid`` as the API takes it, with a JSON client's near-misses refused.

    ``render_look`` draws the coarse grid for *any* truthy string, which is right
    for Python -- where the two spellings are in the docstring in front of you --
    and wrong here. A client that guessed ``"none"`` or ``"off"`` from the schema
    would get A-H drawn over the picture instead of nothing, and a grid that appears
    when it was asked not to is a quiet wrong answer rather than a failure. So the
    two spellings are taken, the obvious near-misses are taken, and anything else is
    named.
    """
    if value is None or isinstance(value, bool):
        return bool(value)
    text = str(value).strip().lower()
    if text == "fine":
        return "fine"
    if text in ("true", "on", "grid", "coarse"):
        return True
    if text in ("false", "off", "none", ""):
        return False
    raise ValueError(
        f'grid is true for the A-H by 1-8 grid, "fine" for tenths of what is on '
        f"screen, or false for neither -- not {value!r}."
    )


def _scale(value: int | None) -> int | None:
    """``None`` for the default long side, ``0`` for full resolution, as the CLI has it."""
    if value is None:
        return DEFAULT_LOOK_SIZE
    return None if int(value) == 0 else int(value)


def _shown(path) -> list:
    """A written image, as the path it went to and the picture itself."""
    return [str(path), Image(path=str(path))]


# --------------------------------------------------------------------------------------
# The server
# --------------------------------------------------------------------------------------
def build_server() -> MCPServer:
    """The server, with every tool registered. Separate from :func:`main` so tests
    can call the tools directly rather than over a transport."""
    if not MCP_AVAILABLE:  # pragma: no cover - exercised only where the extra is absent
        raise ImportError(_NEEDS_MCP)

    server = MCPServer(
        name="easel",
        version=__import__("easel").__version__,
        instructions=(
            "A headless painting engine. Paint, look, repeat.\n\n"
            "Call `guide` before painting: it returns the method, which matters "
            "more than the tool list. The short version -- tone the ground, establish "
            "the big value shapes with a large brush, check them with look(values=True), "
            "then mid-tones, then edges, and highlights last with the smallest brush "
            "and the fewest strokes. Look every five to fifteen strokes; a stroke you "
            "did not look at was a guess.\n\n"
            "Every tool takes the path to a .easel session file, which holds the whole "
            "painting. Marks are made by `run`, which executes a Python script with the "
            "session bound to `s` and the whole API already in scope. Before a mass is "
            "paid for, `cost`, `preview` and `rehearse` say what it charges, where it "
            "goes and what it will look like, and hand back the Python that paints it.\n\n"
            "Coordinates are normalised 0..1 with the origin at the top-left; nothing "
            "here takes a pixel. `brushes` lists every name that can be said."
        ),
    )

    # -- the CLI verbs -------------------------------------------------------------
    @server.tool()
    @_tool
    def new(session: str, size: str = "1024x768", texture: str = "linen",
            ground: str = "white", seed: int = 0, out_dir: str = "out",
            timelapse: bool | int = True, force: bool = False,
            budget: int | None = None) -> str:
        """Create a session file: the canvas, and the painting's only state.

        Args:
            session: where to write the .easel file.
            size: WIDTHxHEIGHT in pixels, e.g. "900x675".
            texture: canvas tooth -- "smooth", "linen" or "rough".
            ground: a named ground ("white", "toned_grey", ...), or a hex colour.
                Painting on white is the hardest thing to judge values against.
            seed: the determinism seed. Same seed and same calls, same painting.
            out_dir: where look(), preview() and compare() write their PNGs.
            timelapse: keep a time-lapse. A number is the frame's long side in
                pixels; the default is 360. The session file keeps no frames, so
                `timelapse` rebuilds the film from the log at this size when it is
                asked for.
            force: overwrite an existing session file.
            budget: how many strokes this painting is allowed. Nothing is refused
                when it runs out, but `run` then reports spent and remaining and
                `cost` says when one plan would eat a large share of what is left.
        """
        path = Path(session)
        if path.exists() and not force:
            raise FileExistsError(
                f"{path} already exists. Pass force=true to overwrite it, or paint "
                f"into it as it is."
            )
        w, h = parse_size(size)
        s = Session(w, h, texture=texture, ground=ground, seed=seed,
                    timelapse=timelapse, out_dir=out_dir, budget=budget)
        s.save(path)
        return f"Created {path} ({w}x{h}, {texture}, ground {ground}, seed {seed})"

    @server.tool()
    @_tool
    def run(session: str, script: str = "", script_path: str = "",
            rehearse: bool = False, count: bool = False, prelude: str = "",
            prelude_path: str = "",
            alternatives: list[str] | dict[str, str] | None = None) -> list:
        """Paint: run a Python script against the session.

        This is where every mark is made. The script has `s` (the session),
        `palette`, and the whole public API already in scope -- `blob`, `cell`,
        `span`, `hull`, `ribbon`, `region` -- so it needs no imports::

            s.palette["dark"] = s.palette.mix("ultramarine", "burnt_umber", 0.45)
            s.block_in(blob(cell("D5"), 0.12, seed=3), "bristle", "dark",
                       direction="axis", density=0.8)
            s.stroke([(0.31, 0.62), (0.55, 0.58)], "bristle", "ochre", size=0.05)

        Whatever was painted before an error is saved: a half-finished pass is still
        work. A script that raises comes back with its traceback and the stroke
        count that survived.

        Args:
            session: the .easel file to paint into.
            script: the Python to run, as text.
            script_path: a file to run instead, if the script is already on disk.
            rehearse: run the whole pass against a *copy* and commit nothing. The
                strokes are seeded as if they were the next marks of the real
                painting, so what is rehearsed is what lands when the same pass is
                run for real. `rehearse` (the planning tool) tries a plan; this tries
                a script, which is what a pass actually is. Costs nothing but a look,
                and about sixty of one painting's 224 strokes went on masses
                that were repainted because rehearsing meant retyping the pass. The
                look comes back as the picture, beside the path it was written to,
                as `look` hands back its own. The one thing it keeps is what the
                check said, in the session file, where `log` with `reports` reads it
                back.
            count: price the pass without painting it -- a rehearsal with the pixel
                work skipped, so a helper that calls a dozen verbs comes back with a
                stroke count and a check in about a thirtieth of the time. No look,
                nothing committed. Implies `rehearse`. Rehearse instead when the
                question is what it looks like: this one lays no paint.
            prelude: Python run first, in the same scope -- helpers, mixtures and
                landmarks a pass should not have to redefine.
            prelude_path: a file to use as the prelude instead.
            alternatives: versions of one pass, in place of `script` -- a list of
                scripts, or an object naming each one, {"bristle": "...", "flat":
                "..."}. Each is rehearsed on a copy of its own, with its own check,
                and their looks come back side by side in one sheet, each panel
                labelled with the version and the strokes it laid: two skies judged
                against each other rather than one on top of the other. Implies
                `rehearse`; with `count`, prices each and lays no sheet. Each copy is
                seeded as the next marks of the painting, so the version then run for
                real lands as its panel shows it. At most twelve on a sheet.
        """
        if prelude and prelude_path:
            raise ValueError(
                "run takes either prelude (the Python itself) or prelude_path (a "
                "file), not both."
            )
        pre_name = prelude_path or "<prelude>"
        pre = (Path(prelude_path).read_text(encoding="utf-8-sig") if prelude_path
               else prelude)
        if alternatives:
            if script or script_path:
                raise ValueError(
                    "run takes alternatives in place of script and script_path: each "
                    "version is one script of its own."
                )
            versions = (list(alternatives.items()) if isinstance(alternatives, dict)
                        else [(f"<alternative {i}>", text)
                              for i, text in enumerate(alternatives, 1)])
            s = _load(session)
            tried = run_alternatives(
                s, [(str(text), str(label)) for label, text in versions],
                prelude=pre, prelude_name=pre_name, count_only=count)
            # What each version's check said is kept, as a rehearsal's is.
            if any(one.code == 0 for one in tried.tried):
                s.save(session)
            if tried.sheet is None:
                return [tried.text]
            return [tried.text, Image(path=str(tried.sheet))]
        if bool(script) == bool(script_path):
            raise ValueError(
                "run takes either script (the Python itself) or script_path (a file), "
                "and needs exactly one of them -- or alternatives, several versions of "
                "one pass."
            )
        name = script_path or "<script>"
        source = Path(script_path).read_text(encoding="utf-8-sig") if script_path else script

        s = _load(session)
        trying = rehearse or count
        target = s.scratch(count_only=count) if trying else s
        before = target._open_pass()
        told = len(target.notices())
        result = run_script(target, source, name, prelude=pre, prelude_name=pre_name)
        # The post-pass check the CLI prints beside the budget line, here too, and
        # above it what the engine said at the calls themselves. Until 0.6.0 that
        # second half reached nobody through this server: the warnings went to the
        # process's stderr, which a painter working through a client never sees, so
        # "the tool warns you" was false here for everything except this check.
        check = target.report(since=before)
        said = target.notices(since=told)
        block = _notices.block(said, check)
        short = Path(name).name
        # Every answer is a list, because a rehearsal's look and a sheet of alternatives
        # come back as pictures: a tool the SDK is told answers in text has its answer
        # checked as text.
        if trying:
            if result.code != 0:
                return [_join(_notices.block(said), result.text)]
            left = s.remaining
            laid = target.history.stroke_count      # the copy's own log: this pass
            cost = (f"{laid} strokes" if left is None
                    else f"{laid} strokes of the {left} left")
            if count:
                answer = [f"Counted {short}: {cost}. Nothing painted, "
                          f"nothing committed.\n{block}"]
            else:
                # The look is what a rehearsal is for, and a path is no use to a client
                # that cannot open a file: the picture comes back beside the text, as
                # the looking tools hand theirs back, and the path stays in the text.
                looked = target.look()
                answer = [f"Rehearsed {short}: {cost}. Nothing committed.\n"
                          f"{block}\n{looked}", Image(path=str(looked))]
            # What the check said is the one thing a rehearsal keeps: on the
            # painting, as `easel run --rehearse` keeps it. See `Session.reports`.
            s._keep_report(target, short, before, block)
            s.save(session)
            return answer
        if result.code == 0:
            s._keep_report(target, short, before, block)
        if result.save:
            s.save(session)
        if result.code != 0:
            return [_join(_notices.block(said), result.text)]
        return [f"{result.text}\n{block}"]

    @server.tool()
    @_tool
    def look(session: str, region: Place | None = None, grid: bool | str = False,
             values: bool = False, reference: str = "", diff: bool = False,
             scale: int | None = None, sketch: bool = True, marks: bool = True,
             output: str = "") -> list:
        """Look at the canvas. Returns the PNG, and the path it was written to.

        The most important call in the API. Look every five to fifteen strokes.

        Args:
            session: the .easel file.
            region: crop to a place, enlarged so a small crop is readable. With a
                reference, **both** panels are cropped to the same place. Takes
                """ + _PLACE_HELP + """.
            grid: true overlays the labelled A-H by 1-8 grid; "fine" divides what is
                on screen into labelled tenths instead, which is how a place inside
                a cell gets named.
            values: greyscale, for judging the value structure -- squinting, in
                other words. Use it early and often.
            reference: a photograph to place alongside, for the copy stage.
            diff: tint what has changed since the previous look.
            scale: long-side pixels. 0 for full resolution.
            sketch: show the drawing: the pencil the paint has not covered, and the
                guides drawn on the view. false hides both.
            marks: draw the landmarks. false hides them and their labels, which sit
                over the details they name -- take them off before judging the
                picture.
            output: where to write the PNG. Defaults to out_dir/look_NNN.png.
        """
        s = _load(session)
        path = s.look(
            scale=_scale(scale),
            grid=_grid(grid),
            values=values,
            region=None if region is None else _place(region),
            reference=reference or None,
            diff=diff,
            sketch=sketch,
            marks=marks,
            path=output or None,
        )
        s.save(session)
        return _shown(path)

    @server.tool()
    @_tool
    def compare(session: str, reference: str = "", region: Place | None = None,
                threshold: float = 0.10, output: str = "",
                plan: list[Any] | None = None) -> list:
        """Per-cell value of the reference, of the canvas, and the difference.

        Squinting says something is off; this says which mass and by how much. The
        threshold that matters is 0.10 -- two masses closer than that read as one,
        so a cell further out than that is a separation the painting has lost.

        Returns the table and the heat map. Matching it cell by cell is tracing;
        read it for the masses that are out, fix those, and look again.

        **Without a photograph, measure against the plan.** Pass `plan` instead of
        `reference`: a list of `{"place": <a place>, "value": 0.0..1.0}`, the value
        plan a painter working from their head is told to write down in numbers.
        Each place is measured against the value it was promised, and the sheet
        shows the plan, the canvas and what is out. Give a place a name it will be
        listed under by building it with one: `{"blob": "D5", "name": "near_mass"}`.

        Args:
            session: the .easel file.
            reference: the image to measure against. Leave empty when passing a plan.
            region: measure inside a place, in its own tenths, instead of over the
                whole canvas. The labels are the ones look(grid="fine") shows.
                Ignored when comparing against a plan.
            threshold: what counts as out.
            output: where to write the heat map.
            plan: planned values, instead of a reference image.
        """
        if bool(reference) == bool(plan):
            raise ValueError(
                "compare takes either reference (an image) or plan (the values you "
                "meant to paint), and needs exactly one of them."
            )
        s = _load(session)
        if plan is not None:
            targets = {}
            for i, entry in enumerate(plan):
                if not isinstance(entry, dict) or "place" not in entry \
                        or "value" not in entry:
                    raise ValueError(
                        f"Entry {i + 1} of the plan is {entry!r}. Each one is "
                        f'{{"place": <a place>, "value": 0.0..1.0}}.'
                    )
                targets[_place(entry["place"])] = float(entry["value"])
            result = s.compare(targets, threshold=threshold, path=output or None)
        else:
            result = s.compare(reference,
                               region=None if region is None else _place(region),
                               threshold=threshold, path=output or None)
        s.save(session)
        return [str(result), Image(path=str(result.path))]

    @server.tool()
    @_tool
    def prepare(session: str, reference: str, level: str = "coarse",
                merge: list[list[int]] | None = None, sketch: bool = False,
                output: str = "") -> list:
        """Cut a reference into numbered masses, and return the map to read.

        No model and no learned segmentation: the photograph is quantised in a
        perceptual colour space and its connected areas are labelled. The map will
        be wrong in places -- it joins two things of the same colour and cuts one
        thing along its shading -- so read it, then correct it with `merge`.

        Args:
            session: the .easel file.
            reference: the photograph to cut up.
            level: "coarse" (five to eight masses -- start here), "medium", "fine".
            merge: area numbers to join, as pairs or longer runs: [[3, 7], [2, 5]].
            sketch: also lay the outlines as pencil. ASSISTED MODE -- a run that
                starts from a machine-laid sketch measures the segmenter and not the
                painter, and says so in its write-up. See PAINTER.md.
            output: where to write the overlay.
        """
        s = _load(session)
        prep = s.prepare(reference, level=level, path=output or None)
        for group in merge or []:
            numbers = [int(n) for n in group]
            if len(numbers) < 2:
                raise ValueError(
                    f"merge joins two or more area numbers, got {group!r}. "
                    f"For example: merge=[[3, 7]]."
                )
            prep.merge(*numbers)
        if merge:
            # The overlay has to show the map the table describes.
            s.look_areas(reference, path=output or None)
        report = str(prep)
        if sketch:
            drawn = s.sketch()
            report = (f"ASSISTED: laid {len(drawn)} outlines as pencil. The definition "
                      f"of done reports a run that starts from this separately -- see "
                      f"PAINTER.md.\n\n{report}")
        s.save(session)
        return [report, Image(path=str(prep.overlay_path))]

    @server.tool()
    @_tool
    def mark(session: str, name: str = "", x: float | None = None,
             y: float | None = None, forget: bool = False) -> str:
        """Record, list or forget a named landmark.

        Six or seven verified points are a drawing, and the masses get hung on them.
        Called with no name, this lists what is already marked.

        Args:
            session: the .easel file.
            name: the landmark's name. Omit to list them all.
            x: position across, 0..1 from the left.
            y: position down, 0..1 from the top.
            forget: remove the named landmark instead of setting it.
        """
        s = _load(session)
        if forget and not name:
            raise ValueError("Forgetting a landmark needs its name.")
        if not name:
            if not s.marks:
                return "No landmarks yet. mark(session, 'top_l', 0.42, 0.31)"
            return "\n".join(f"{n:16s} {px:.3f} {py:.3f}"
                             for n, (px, py) in sorted(s.marks.items()))
        if forget:
            s.unmark(name)
        elif x is None or y is None:
            raise ValueError(
                f"Marking {name!r} needs a position: mark(session, {name!r}, 0.42, 0.31)"
            )
        else:
            s.mark(name, x, y)
        s.save(session)
        return (f"{len(s.marks)} landmark(s): "
                f"{', '.join(sorted(s.marks)) or '(none)'}")

    @server.tool()
    @_tool
    def undo(session: str, n: int = 1) -> str:
        """Scrape back the last N log records.

        Records, not marks paid for: a `dry` or a pencil line is one record and is
        free, as `log` and `replay` count. The file keeps no snapshots, so this
        rebuilds the painting from its log, with the engine installed, up to the
        record before the first one undone -- any N, at the price of a repaint.

        Not a free action -- it is a palette knife, and the guide would rather you
        painted over the mistake. `rehearse` is the cheaper way to not make it.

        Args:
            session: the .easel file.
            n: how many log records to scrape back.
        """
        s = _load(session)
        undone = s.undo(n)
        s.save(session)
        return f"Undid {undone} stroke(s). {s.stroke_count} remain."

    @server.tool()
    @_tool
    def export(session: str, output: str, impasto: bool = True,
               sketch: bool = True) -> str:
        """Write the finished painting as a PNG, at full resolution.

        Args:
            session: the .easel file.
            output: where to write the PNG.
            impasto: shade paint height as relief.
            sketch: include whatever pencil the paint has not covered.
        """
        s = _load(session)
        return str(s.export(output, impasto=impasto, sketch=sketch))

    @server.tool()
    @_tool
    def timelapse(session: str, output: str, fps: float = 8.0, every: int = 1,
                  scale: int | None = None, from_log: bool = False) -> str:
        """Write the painting happening: .gif for the animation, .png for a contact sheet.

        The session file keeps no frames, so the film is rebuilt from the log at the
        session's frame size: a full repaint, about half a minute for a painting of a
        couple of hundred marks. A file saved before 0.7.0 that kept its frames uses
        them.

        Args:
            session: the .easel file.
            output: where to write it. The suffix picks which of the two you get.
            fps: frames per second, for the GIF.
            every: keep every nth frame (GIF only). Consecutive frames differ by one
                stroke, so a couple of hundred marks make a couple of megabytes at
                every=1 and a third of that at every=3, reading the same. The
                finished painting is always the last frame.
            scale: long side in pixels (GIF only). Frames are made at 360 unless the
                session asked for another size, and this only shrinks them -- with
                from_log it is the size they are built at instead.
            from_log: build the frames at `scale` rather than at the session's frame
                size -- the canvas's own when `scale` is left off. Also a full
                repaint, and it works on a painting made with the time-lapse off.
        """
        s = _load(session)
        out = Path(output)
        path = (s.contact_sheet(out) if out.suffix.lower() == ".png"
                else s.timelapse_gif(out, fps=fps, every=every, scale=scale,
                                     from_log=from_log))
        return str(path)

    @server.tool()
    @_tool
    def log(session: str, n: int = 20, reports: bool = False) -> str:
        """The recent marks, and what the painting has cost so far.

        Args:
            session: the .easel file.
            n: how many marks to show -- or with reports, how many reports.
            reports: what `run` handed back after each pass instead, as the session
                file kept it: what the calls said and the post-pass check, rehearsed
                and counted passes included, each saying which it was.
        """
        s = _load(session)
        head = f"{s.stroke_count} strokes, seed {s.seed}, {s.size[0]}x{s.size[1]}"
        if reports:
            return f"{head}\n{_notices.saved(s.reports(), last=n)}"
        return f"{head}\n{s.log(n)}"

    @server.tool()
    @_tool
    def check(session: str, subject_share: float | None = None) -> str:
        """The closing checklist, answered -- run it when the painting looks finished.

        Every line of the guide's closing checklist that has a number behind it: the
        values and whether the picture has a clear light, how the edges divide
        between hard and soft, what is left of the ground, how many masses were laid
        in a rectangle, the subject's share, and what is left of the budget. Then the
        three questions nothing can measure, with your own `why` quoted back.

        The `run` tool's post-pass check is the same measurements after one pass.
        This is the end of the painting, and it is read-only: it changes nothing.

        Args:
            session: the .easel file.
            subject_share: the share of the budget the subject was to get, 0..1.
                The plan's own is used when this is left off.
        """
        return _load(session).checklist(subject_share=subject_share)

    @server.tool()
    @_tool
    def brushes() -> str:
        """Every name that can be said: brushes, pigments, grounds, textures, regions
        and the shape builders. The same reference `easel brushes` prints."""
        return reference_text()

    @server.tool()
    @_tool
    def guide(document: str = "guide", full: bool = False) -> str:
        """The method this engine is built around, returned as text.

        Read this before painting. The engine is only the brush; this is how to
        use it, the workflow matters more than the tool list, and a client that
        reached the engine over MCP has no repository to go and read.

        The default is *The first hour*: the whole workflow in about 1,400
        words, written to be read on its own and enough to start from.

        Args:
            document: which of the six to return.
                "guide" (PAINTER.md) -- the method: the loop, the order of work,
                    the mistakes, nine warm-up exercises, the closing checklist.
                    Required reading, and the only one that is.
                "painting" (PAINTING.md) -- how the paint, the brushes and the
                    planning tools behave, and copying a photograph in its last
                    chapter. The reasons: `explain` prints the passage a
                    notice points at, which is how most of it arrives.
                "recipes" (RECIPES.md) -- one situation at a time: the calls in
                    order, what it looks like when it goes wrong, and the number
                    behind it. Read one when you are about to lay that thing.
                "reference" (REFERENCE.md) -- units, defaults, what each
                    argument does.
                "calibration" (CALIBRATION.md) -- the measured numbers behind
                    the rules, which you do not need in order to paint.
                "diagnosis" (DIAGNOSIS.md) -- an index of symptoms, and not for
                    reading: it is a list of ways to fail, which teaches you to
                    see faults you were not going to make. Use `diagnose`
                    instead, which is this index with the pointer followed.
            full: for "guide", the whole of it rather than its first page. The
                other documents always come back whole.
        """
        if document != "guide":
            return _docs.read(document)
        return _docs.read("guide") if full else _docs.front_page()

    @server.tool()
    @_tool
    def diagnose(symptom: str = "", brief: bool = False) -> str:
        """You have looked, it is wrong: the passage of the guide that measured it.

        Describe what is on the canvas in your own words and this returns the
        passage that says why it happened and what it costs to repair -- `easel
        diagnose` and `DIAGNOSIS.md`'s symptom index, with the pointer already
        followed.

        Say what you can **see** (`concentric rings`, `a stringy edge`, `the ground
        shows through in flecks`) rather than what you think caused it; the index is
        written in the words a painter uses for the thing in front of them. Reach
        for this after a rehearsal you do not like, which is the moment it is for.

        The index itself is not worth reading -- it is a list of ways to fail, and
        a session that read it front to back then repaired five faults from memory
        rather than from the measurement, one of them the expensive way.

        Args:
            symptom: what you are looking at. Left off, every symptom it covers.
            brief: the matching symptoms only, without their passages -- for
                finding the wording to ask again with.
        """
        return _diagnosis.listing(symptom) if brief else _diagnosis.answer(symptom)

    @server.tool()
    @_tool
    def explain(code: str = "") -> str:
        """Why the engine said that: the passage that holds the measurement.

        Every notice a call gives carries a code -- `chisel-blank`,
        `direction-default`, `scumble-wedge` -- printed above the post-pass check by
        `run`, `cost`, `preview` and `rehearse`. This turns one back into the section
        of the guide that measured it, so the reason arrives at the moment it
        applies rather than having to have been read in advance.

        Args:
            code: the notice's code, exactly as the pass printed it. Left off, every
                code there is with a line saying what each one is about.
        """
        if not code:
            rows = "\n".join(
                f"  {name:20s} {spec.kind:6s} {spec.about}"
                for name, spec in sorted(_notices.NOTICES.items())
            )
            return f"The engine says these at a call. Ask for any one by its code:\n{rows}"
        return _notices.explain(code)

    @server.tool()
    @_tool
    def demo(recipe: str = "", out_dir: str = "out") -> list:
        """A recipe painted beside what it looks like when it goes wrong, and the fix.

        One recipe of the guide's RECIPES.md, three ways side by side: the recipe, the
        call that goes wrong -- with what the tool says about it, a notice code or a
        line of the post-pass check -- and the smallest fix, where that is not the
        recipe itself. Returns what each panel was told, the calls that differ, and the
        sheet. Reach for it before painting a thing a recipe covers, or after a
        rehearsal that came back looking like the failure.

        Needs no session: every panel is a fresh canvas with the guide's own context
        laid under it.

        `mistakes` paints the six failures a painter meets most on one sheet, each
        under what it looks like and what the tool says about it. That is where the
        guide's own entry path sends a painter, after the card and before the
        exercises.

        Args:
            recipe: the recipe, by the words of its heading ("crosses a boundary"),
                or "mistakes" for the six on one sheet. Left off, every recipe and
                which of them have a demo.
            out_dir: where the sheet is written, as demo-<recipe>.png.
        """
        text, path = _demo.answer(recipe, out_dir=out_dir)
        return [text] if path is None else [text, *_shown(path)]

    @server.tool()
    @_tool
    def plan(session: str, why: str = "", values: dict[str, float] | None = None,
             lightest: str = "", subject_share: float | None = None,
             bands: str = "", ground: str = "", clear: bool = False) -> str:
        """Declare what this painting is for, and what the check should hold it to.

        Not to be confused with the `plan` **argument** of `cost`, `preview` and
        `rehearse`, which is a list of marks to be priced. This is the painter's plan
        for the *picture*: the four things the guide asks to be settled before the
        first mark, plus the two standing warnings a picture can declare its way out
        of. `Session(budget=)` was the first of these declarations; these are the rest.

        Every one of them changes what the post-pass check says after each pass, so
        declaring them is how the check stops being generic advice. Called with only a
        session it prints the plan already declared.

        Args:
            session: the .easel file.
            why: what the picture is for, in a sentence. Nothing measures it; the
                closing check quotes it back.
            values: `{place: value}` -- a place name and the value you mean to paint
                it, `{"A1:H3": 0.70, "lower-band": 0.39}`. The check then says how
                many places are painted as promised, and declaring them prices the
                pairs: two places closer than 0.10 read as one where they meet, which
                is the question that is free to answer now and expensive later.
            lightest: the place meant to be the lightest thing in the picture. The
                check ranks the plan's places and says when something else has taken
                the light.
            subject_share: the share of the budget the subject gets, 0..1. The
                subject line then always carries *against N% planned*.
            bands: "subject" declares that this picture's subject really does run in
                one direction, so the stack-of-bars line counts what crosses the bars
                instead of warning about them.
            ground: "showing", the default expectation, or "buried" -- this picture
                covers its ground on purpose, as a graded field edge to edge does, so
                the ground line stops asking for some back.
            clear: start from nothing rather than from what is already declared.
        """
        s = _load(session)
        told = len(s.notices())
        declared = s.plan(
            why=why or None,
            values=values,
            lightest=lightest or None,
            subject_share=subject_share,
            bands=bands or None,
            ground=ground or None,
            clear=clear,
        )
        s.save(session)
        parts = [str(declared)]
        if declared.values:
            parts.append(declared.pairs_text(s.plan_pairs()))
        return _join(_notices.block(s.notices(since=told)), *parts)

    # -- the three questions about a mark that has not been made yet ---------------
    @server.tool()
    @_tool
    def preview(session: str, plan: list[Any] | dict[str, Any] | str,
                reference: str = "", region: Place | None = None,
                grid: bool | str = False, values: bool = False,
                scale: int | None = None, output: str = "") -> list:
        """Draw intended marks over the canvas -- and the reference -- without painting.

        Nothing is painted and nothing is logged. The points and the brush's width
        are drawn as an overlay on both panels, with what each mass charges beside
        it, so a guess about where a mark goes is checked against the photograph
        before it is paid for in paint.

        Returns the overlay and the Python that paints the plan, ready for `run`.

        Args:
            session: the .easel file.
            plan: """ + _PLAN_HELP + """
            reference: shown alongside, with the same overlay.
            region: crop both panels to a place, enlarged. Use one -- the point is
                feature scale.
            grid: as look. "fine" for tenths.
            values: greyscale.
            scale: long-side pixels. 0 for full resolution.
            output: where to write the PNG.
        """
        s = _load(session)
        told = len(s.notices())
        specs, lines = _plan(plan)
        path = s.preview(specs, reference=reference or None,
                         region=None if region is None else _place(region),
                         grid=_grid(grid), values=values, scale=_scale(scale),
                         path=output or None)
        s.save(session)
        return [_join(_notices.block(s.notices(since=told)),
                      f"{path}\n\n# Paints as:\n" + "\n".join(lines)),
                Image(path=str(path))]

    @server.tool()
    @_tool
    def rehearse(session: str, plan: list[Any] | dict[str, Any] | str,
                 reference: str = "", region: Place | None = None,
                 grid: bool | str = False, values: bool = False,
                 scale: int | None = None, output: str = "",
                 vary: dict[str, list[Any]] | None = None) -> list:
        """Paint the plan on a *copy* of the canvas, and look at the result.

        Nothing is committed and nothing is logged. The preview shows where a mark
        will go; this shows what it will look like -- the brush's tooth breakup, how
        it mixes with what is already wet, whether it reads at all at this size. The
        trial marks are seeded as if they were the next marks of the real painting,
        so what is rehearsed is what lands, pixel for pixel.

        A mass is the thing worth rehearsing: one call, twenty passes, and the most
        expensive mark a painter can get wrong.

        Returns the trial and the Python that paints it for real.

        Args:
            session: the .easel file.
            plan: """ + _PLAN_HELP + """
            reference: shown alongside, cropped to the same place.
            region: crop both panels, enlarged.
            grid: as look. "fine" for tenths.
            values: greyscale.
            scale: long-side pixels. 0 for full resolution. With vary, the sheet's.
            output: where to write the PNG.
            vary: settings to try the same marks at, {"size": [0.02, 0.05, 0.08]} --
                one labelled panel per combination, in place, in one image. Every
                entry of the plan takes the setting, so this is for one mark being
                calibrated rather than for a pass. Free, like any rehearsal, and a
                question about size is a question only comparison answers. At most
                twelve panels: two arguments vary together as their combinations.
        """
        s = _load(session)
        told = len(s.notices())
        specs, lines = _plan(plan)
        path = s.rehearse(specs, reference=reference or None,
                          region=None if region is None else _place(region),
                          grid=_grid(grid), values=values, scale=_scale(scale),
                          path=output or None, vary=vary or None)
        s.save(session)
        return [_join(_notices.block(s.notices(since=told)),
                      f"{path}\n\n# Paints as:\n" + "\n".join(lines)),
                Image(path=str(path))]

    @server.tool()
    @_tool
    def cost(session: str, plan: list[Any] | dict[str, Any] | str) -> str:
        """What a plan would charge against the stroke budget, without painting it.

        A mark costs one. A mass costs what its passes come to, and that is the
        number no painter can work out by hand: a mass is priced on the extent of
        its box along the passes' normal *and* on how many times a pass line crosses
        it, so anything curved or concave costs more than the box it sits in. A
        ribbon 0.029 wide at brush 0.015 is 4 passes straight and 75 round a bend.

        Nothing is painted, nothing is logged, and the stroke stream is not spent,
        so ask as often as it is useful -- and ask before widening a brush rather
        than after.

        Args:
            session: the .easel file.
            plan: """ + _PLAN_HELP + """
        """
        s = _load(session)
        told = len(s.notices())
        specs, lines = _plan(plan)
        # Why, not only how much: a number four to twelve times what a painter would
        # have guessed is a crossed direction, a bounding box much bigger than the
        # mass, or a concave outline cutting every pass -- and all three are cheap to
        # fix once named. It rides in the echoed line's own comment so that what
        # comes back is still Python to paste into `run`.
        priced = [(n, why, line) for (n, why), line
                  in zip(s.cost_of(specs), lines, strict=True)]
        total = sum(n for n, _, _ in priced)
        body = "\n".join(f"{line}  # {n}{': ' + why if why else ''}"
                          for n, why, line in priced)
        left = "" if s.remaining is None else f" {s.budget_line()}."
        # A price walk says things -- a mass with `direction` left off costing many
        # times its axis is exactly what a quote is asked for -- and the walk happens
        # on a throwaway copy, so `Session._adopt_notices` carries them back here.
        return _join(_notices.block(s.notices(since=told)),
                     f"{total} stroke(s).{left} Paints as:\n\n{body}")

    return server


def main(argv: list[str] | None = None) -> int:
    """Entry point for ``easel-mcp``. Serves over stdio until the client goes away."""
    parser = argparse.ArgumentParser(
        prog="easel-mcp",
        description="Serve the easel painting engine over MCP (stdio).",
    )
    parser.add_argument("--dir", type=Path, default=None,
                        help="work here, so session and reference paths are relative "
                             "to the painting rather than to wherever the client "
                             "happened to launch the server")
    args = parser.parse_args(argv)

    if not MCP_AVAILABLE:  # pragma: no cover - exercised only where the extra is absent
        print(_NEEDS_MCP)
        return 1
    if args.dir is not None:
        os.chdir(args.dir)
    build_server().run(transport="stdio")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
