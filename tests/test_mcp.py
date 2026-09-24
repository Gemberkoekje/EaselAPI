"""M9: the MCP server, and whether it is as thin as it claims to be.

Two things are worth asserting about a wrapper. The first is that it *is* a
wrapper -- that every CLI verb is here, that the reference it prints is the one
the CLI prints, and that the ``.easel`` file is still the only state, so a
painting can be worked on through the server, the shell and a plain script in any
order. The second is the translation the server has to do that the CLI does not:
a place and a plan arrive as JSON here, and JSON has no ``blob(cell("D5"))`` in
it.

The load-bearing test is :func:`test_the_quoted_price_is_what_the_echoed_python_pays`.
Through this server a plan is checked in JSON and painted in Python, so the two
can disagree -- and a plan that is checked and then retyped is exactly the drift
``preview``, ``rehearse`` and ``cost`` exist to prevent. Every one of them hands
back the call it just priced; that test runs the call and counts what it charged.

Skipped unless the ``mcp`` extra is installed (``pip install easel-paint[mcp]``),
which the main CI job deliberately does not do -- see ``.github/workflows/ci.yml``.
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass

import numpy as np
import pytest
from PIL import Image, ImageDraw

from easel import Session, blob, cell, ellipse, hull, polygon, ribbon, roughen, span
from easel.cli import build_parser, reference_text
from easel.mcp_server import MCP_AVAILABLE

pytestmark = pytest.mark.skipif(
    not MCP_AVAILABLE, reason="the mcp extra is not installed (pip install easel-paint[mcp])"
)

if MCP_AVAILABLE:
    from mcp.server.mcpserver.exceptions import ToolError

    from easel.mcp_server import _place, _plan, build_server


@dataclass
class Reply:
    """What a client gets back: the text, and any pictures beside it."""

    text: str
    images: list[bytes]

    @property
    def picture(self) -> Image.Image:
        assert len(self.images) == 1, f"expected one image, got {len(self.images)}"
        import base64
        import io

        return Image.open(io.BytesIO(base64.b64decode(self.images[0])))


@pytest.fixture
def server():
    return build_server()


@pytest.fixture
def call(server):
    """Make a tool call the way a client does, and unpack what comes back."""

    def _call(tool, /, **arguments) -> Reply:
        result = asyncio.run(server.call_tool(tool, arguments))
        text = "\n".join(c.text for c in result.content if c.type == "text")
        images = [c.data for c in result.content if c.type == "image"]
        return Reply(text, images)

    return _call


@pytest.fixture
def painting(tmp_path, call):
    """A session file with one mark in it, and somewhere to write looks."""
    path = str(tmp_path / "p.easel")
    call("new", session=path, size="480x360", ground="toned_grey", seed=11,
         out_dir=str(tmp_path / "out"))
    call("run", session=path,
         script="s.stroke([(0.1, 0.2), (0.8, 0.3)], 'bristle', 'ochre')")
    return path


@pytest.fixture
def reference(tmp_path):
    """A synthetic photograph: three masses at three values, with real edges."""
    img = Image.new("RGB", (320, 240), (176, 168, 152))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 320, 120], fill=(96, 104, 116))
    d.ellipse([90, 70, 220, 200], fill=(58, 44, 36))
    d.rectangle([0, 205, 320, 240], fill=(140, 120, 92))
    path = tmp_path / "ref.png"
    img.save(path)
    return str(path)


# -- it is a wrapper ------------------------------------------------------------------
def test_every_cli_verb_is_a_tool(server):
    """One tool per CLI verb, so a verb added later has to arrive here
    too -- which this notices and a hand-written list of tool names would not."""
    sub = next(a for a in build_parser()._actions if hasattr(a, "choices") and a.choices)
    verbs = set(sub.choices)
    tools = {t.name for t in asyncio.run(server.list_tools())}
    assert verbs <= tools, f"CLI verbs with no tool: {sorted(verbs - tools)}"
    # And what it adds beyond them: the three questions about a mark not yet made.
    assert tools - verbs == {"preview", "rehearse", "cost"}


def test_the_reference_is_the_one_the_cli_prints(call, capsys):
    """One list of names, or the two drift the first time a pigment is added."""
    from easel.cli import main

    main(["brushes"])
    printed = capsys.readouterr().out.rstrip("\n")
    assert call("brushes").text == printed == reference_text()


def test_the_guide_tool_hands_back_the_same_method_the_shell_prints(call):
    """The point of this tool: a client that reached the engine over MCP has no
    repository to read, so the method has to come back through the wire. One
    source for it, or the two drift the first time the guide is edited."""
    from easel import guide

    assert call("guide").text == guide.front_page()
    assert call("guide", full=True).text == guide.read("guide")
    assert call("guide", document="reference").text == guide.read("reference")


def test_the_guide_tool_is_reachable_without_a_session(server):
    """It takes no session, like `brushes` -- a painter has to be able to read the
    method before there is a canvas to read it against."""
    tool = next(t for t in asyncio.run(server.list_tools()) if t.name == "guide")
    assert "session" not in (tool.input_schema.get("properties") or {})


def test_the_readme_counts_the_tools_this_server_has(server):
    """The same sentence in the other place a client reads it. The README said
    *fifteen tools: the twelve CLI verbs* while this server had twenty and the parser
    seventeen, because the manifest's copy of that count was held to the parser
    (`tests/test_server_json.py`) and the README's was held to nothing. It lives here
    rather than beside that one because counting the tools means building the server,
    which needs the extra this job installs.
    """
    from pathlib import Path

    readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
    sub = next(a for a in build_parser()._actions if hasattr(a, "choices") and a.choices)
    tools = asyncio.run(server.list_tools())
    words = dict(enumerate(
        "zero one two three four five six seven eight nine ten eleven twelve thirteen "
        "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()))
    said = f"{words[len(tools)].capitalize()} tools: the {words[len(sub.choices)]} CLI verbs"
    assert said in readme, f"the README does not say {said!r}"


def test_undo_says_what_it_counts_and_claims_no_snapshots(server):
    """It said *the last N marks* and *at most 24 are kept*. It counts log records,
    as the library's `undo` does, and a session file carries no snapshots, so every
    `undo` through the server is a rebuild from the log and has no such limit."""
    tool = next(t for t in asyncio.run(server.list_tools()) if t.name == "undo")
    assert "record" in tool.description
    assert "24" not in tool.description


def test_the_server_instructions_send_a_client_to_the_guide_tool(server):
    """They used to say to read PAINTER.md, which a client over MCP cannot open."""
    assert "`guide`" in server.instructions


def test_the_session_file_is_the_only_state(tmp_path, call, painting):
    """Painted through the server, read by the library -- and the other way round."""
    call("run", session=painting,
         script="s.block_in(cell('D5'), 'bristle', 'burnt_umber', size=0.06)")
    loaded = Session.load(painting)
    assert loaded.stroke_count == call_count(call, painting)

    loaded.mark("top_l", 0.33, 0.31)
    loaded.save(painting)
    assert "top_l" in call("mark", session=painting).text


def call_count(call, session) -> int:
    return int(re.match(r"(\d+) strokes", call("log", session=session).text).group(1))


def test_a_look_comes_back_as_a_picture(call, painting):
    reply = call("look", session=painting, grid=True)
    assert reply.text.endswith(".png")
    assert reply.picture.size[0] > 0 and reply.picture.format == "PNG"


@pytest.mark.parametrize("tool", ["look", "compare", "prepare"])
def test_the_looking_tools_return_their_image_inline(call, painting, reference, tool):
    """The point of the server: look, preview and compare return their images."""
    extra = {} if tool == "look" else {"reference": reference}
    assert len(call(tool, session=painting, **extra).images) == 1


def test_scale_zero_is_full_resolution(call, painting):
    """As the CLI's --scale 0 is, and not the 1024 the default stands for."""
    assert call("look", session=painting, scale=0).picture.size == (480, 360)
    assert call("look", session=painting).picture.size[0] <= 1024


def test_a_grid_that_was_asked_for_is_the_one_drawn(call, painting):
    """`render_look` draws the coarse grid for any truthy string, which is right in
    Python and wrong on a wire a client fills in from a schema: "none" would draw
    A-H over the picture instead of nothing. Asserted on the pixels, because the
    failure this guards against is a call that succeeds and returns the wrong view."""
    plain = np.asarray(call("look", session=painting, grid=False).picture)
    for spelling in ("none", "off", "false"):
        assert np.array_equal(
            np.asarray(call("look", session=painting, grid=spelling).picture), plain
        ), f"grid={spelling!r} drew something"
    for spelling in (True, "true", "coarse"):
        assert not np.array_equal(
            np.asarray(call("look", session=painting, grid=spelling).picture), plain
        ), f"grid={spelling!r} drew nothing"
    assert not np.array_equal(
        np.asarray(call("look", session=painting, grid="fine").picture),
        np.asarray(call("look", session=painting, grid=True).picture),
    )
    with pytest.raises(ToolError, match="grid is true"):
        call("look", session=painting, grid="sideways")


# -- places, as they arrive over the wire ---------------------------------------------
@pytest.mark.parametrize(
    ("wire", "built"),
    [
        ("upper-band", "upper-band"),
        ("D4", cell("D4")),
        ("C3:F6", span("C3", "F6")),
        ([0.1, 0.2, 0.5, 0.6], (0.1, 0.2, 0.5, 0.6)),
        ([[0.2, 0.2], [0.6, 0.15], [0.7, 0.5]],
         polygon([(0.2, 0.2), (0.6, 0.15), (0.7, 0.5)])),
        ({"blob": "D5", "radius": 0.12, "seed": 3}, blob(cell("D5"), 0.12, seed=3)),
        ({"ellipse": [0.4, 0.6], "rx": 0.2, "ry": 0.12}, ellipse((0.4, 0.6), 0.2, 0.12)),
        ({"hull": [[0.3, 0.2], [0.55, 0.12], [0.6, 0.45]]},
         hull([(0.3, 0.2), (0.55, 0.12), (0.6, 0.45)])),
        ({"ribbon": [[0.2, 0.8], [0.5, 0.5]], "width": 0.09},
         ribbon([(0.2, 0.8), (0.5, 0.5)], 0.09)),
        ({"hull": ["D4", "F6", [0.2, 0.9]]}, hull([cell("D4"), cell("F6"), (0.2, 0.9)])),
        ({"roughen": {"blob": "D5", "radius": 0.12, "seed": 3}, "amp": 0.004, "seed": 2},
         roughen(blob(cell("D5"), 0.12, seed=3), amp=0.004, seed=2)),
        ({"roughen": [[0.2, 0.2], [0.6, 0.15], [0.7, 0.5]], "seed": 1,
          "calm": [[0.6, 0.15], "D2"]},
         roughen(polygon([(0.2, 0.2), (0.6, 0.15), (0.7, 0.5)]), seed=1,
                 calm=[(0.6, 0.15), cell("D2")])),
    ],
)
def test_a_place_arrives_as_the_shape_the_python_builds(wire, built):
    """Six forms on the wire, and each has to land on the object the API takes."""
    from easel.regions import as_place

    got, want = _place(wire), as_place(built)
    assert type(got) is type(want)
    assert np.allclose(got.bounds, want.bounds)
    if hasattr(want, "points"):
        assert np.allclose(got.points, want.points)


@pytest.mark.parametrize(
    ("bad", "says"),
    [
        ([0.1, 0.2], "is not a place"),
        ("Z9", "Unknown region"),
        ({"blobb": "D5"}, "names exactly one of"),
        ({"blob": "D5", "ellipse": "D5"}, "names exactly one of"),
        ({"blob": "D5", "brush": "bristle"}, "does not take that"),
        ({"blob": 0.5}, "is not a place"),
        ({"hull": "D4"}, "runs along a list of places"),
        ({"ribbon": 3, "width": 0.1}, "runs along a list of places"),
        ([], "is not a place"),
    ],
)
def test_a_bad_place_says_what_a_place_is(bad, says):
    with pytest.raises((ValueError, KeyError), match=says):
        _place(bad)


# -- plans, and the one thing that can drift ------------------------------------------
PLANS = [
    {"shape": {"blob": "D5", "radius": 0.12, "seed": 3}, "brush": "bristle",
     "color": "burnt_umber", "size": 0.05, "direction": "axis"},
    {"shape": {"ellipse": [0.4, 0.6], "rx": 0.2, "ry": 0.12, "rotate": 30},
     "size": 0.06, "density": 0.8},
    {"shape": {"ribbon": [[0.2, 0.8], [0.5, 0.5], [0.8, 0.42]], "width": 0.09},
     "size": 0.03},
    {"shape": {"hull": ["D4", "F6", [0.2, 0.9]]}, "size": 0.06},
    {"shape": "C3:F6", "size": 0.07, "direction": "vertical"},
    {"shape": [0.1, 0.1, 0.45, 0.3], "size": 0.05},
    {"shape": [[0.2, 0.2], [0.6, 0.15], [0.7, 0.5], [0.25, 0.55]], "size": 0.05},
    {"band": "C3:F6", "color_a": "burnt_umber", "color_b": "titanium_white", "n": 6},
    {"band": {"ellipse": "D5", "rx": 0.2, "ry": 0.15}, "color_a": "burnt_umber",
     "color_b": "titanium_white", "n": 5, "direction": "inward"},
    {"cover": "D4", "color": "burnt_umber", "size": 0.05},
    {"edge": [[0.15, 0.75], [0.5, 0.62], [0.85, 0.70]], "into": "down",
     "depth": 0.2, "cross": 25, "size": 0.05},
    {"edge": {"blob": "D5", "radius": 0.15, "seed": 1}, "depth": 0.12, "size": 0.04},
    {"points": [[0.2, 0.6], [0.5, 0.55]], "brush": "liner", "size": 0.004},
    [[0.2, 0.6], [0.5, 0.55], [0.8, 0.6]],
    {"blob": "D5", "radius": 0.12, "seed": 3},
    "D4",
    {"shape": {"roughen": "C3:F6", "amp": 0.005, "seed": 2,
               "calm": {"ellipse": [0.45, 0.3], "rx": 0.05}},
     "size": 0.05, "edge": "hard", "feather": 0},
    {"points": [[0.2, 0.6], [0.8, 0.55]], "brush": "flat", "size": 0.08,
     "clip": [[0.1, 0.4], [0.9, 0.4], [0.9, 0.8], [0.1, 0.8]], "feather": 0.004},
]


@pytest.mark.parametrize("plan", PLANS, ids=range(len(PLANS)))
def test_the_quoted_price_is_what_the_echoed_python_pays(tmp_path, call, plan):
    """The plan that was priced is the plan that lands, in words, not in principle.

    A price nobody can act on without retyping the plan is a price on a different
    plan. So the quote is run, and what it charged is counted off the log.
    """
    session = str(tmp_path / f"q{abs(hash(str(plan)))}.easel")
    call("new", session=session, size="480x360", seed=5, out_dir=str(tmp_path / "out"))
    quoted = call("cost", session=session, plan=plan)
    # What the walk said comes first when it said anything -- a square scumbled in six
    # passes is told it lays over twice its place -- and the price line after it.
    price = re.search(r"^(\d+) stroke", quoted.text, re.M)
    total = int(price.group(1))

    script = quoted.text[price.start():].splitlines()[2:]
    call("run", session=session, script="\n".join(script))
    assert call_count(call, session) == total


def test_a_bare_shape_object_is_a_mass(call, painting):
    """As a bare 'D4' is, and as a bare Polygon is in Python."""
    assert "s.block_in(blob(" in call("cost", session=painting,
                                      plan={"blob": "D5", "radius": 0.12}).text


def test_a_bare_run_of_points_is_a_mark(call, painting):
    """The one ambiguity JSON has that Python has not: [[x, y], ...] is a path."""
    quoted = call("cost", session=painting, plan=[[0.2, 0.6], [0.5, 0.55]])
    assert quoted.text.startswith("1 stroke") and "s.stroke(" in quoted.text


@pytest.mark.parametrize(
    ("plan", "says"),
    [
        ({"shape": "D4", "bogus": 1}, "A mass does not take 'bogus'"),
        ({"points": [[0.1, 0.2], [0.5, 0.5]], "sze": 0.04}, "A stroke does not take"),
        ({"edge": [[0.1, 0.2], [0.5, 0.5]], "dept": 0.2}, "A sweep does not take"),
        ({"band": "C3:F6", "color_a": "burnt_umber", "color_b": "titanium_white",
          "into": "down"}, "A scumble does not take"),
        ({"cover": "D4", "color": "burnt_umber", "wander": False},
         "A cover does not take"),
        ({"brush": "bristle"}, "is none of them"),
    ],
)
@pytest.mark.parametrize("tool", ["cost", "preview", "rehearse"])
def test_a_keyword_the_call_would_refuse_is_refused_while_the_plan_is_free(
        call, painting, tool, plan, says):
    """`cost` walks the passes and never touches the brush overrides, so a misspelled
    `size` used to price happily at the default and then raise when the echoed Python
    was pasted into `run`. A quote for a plan that cannot be painted is worse than no
    quote -- it is the drift the echo exists to prevent, arriving as a price."""
    with pytest.raises(ToolError, match=says):
        call(tool, session=painting, plan=plan)


def test_a_brush_field_is_not_a_misspelling(call, painting):
    """Every painting call takes any Brush field as an override, so the check above
    has to let them through -- it is derived from the signature, not a list."""
    assert call("cost", session=painting,
                plan={"shape": "D4", "hardness": 0.9, "jitter": 0.1, "label": "x"}
                ).text.startswith("2 stroke")


def test_a_plan_that_cannot_be_painted_raises_when_it_is_priced(call, painting):
    """Rather than when it is paid for -- the quote goes through the same arithmetic."""
    with pytest.raises(ToolError, match="cross"):
        call("cost", session=painting,
             plan={"edge": [[0.1, 0.2], [0.5, 0.5]], "cross": 0})


def test_the_echoed_python_is_python(call, painting):
    """Every line of it, including the header, so the whole block pastes into run."""
    reply = call("preview", session=painting,
                 plan={"shape": {"blob": "D5", "radius": 0.12}, "size": 0.05})
    compile("\n".join(reply.text.splitlines()[1:]), "<echo>", "exec")


# -- what the planning tools must not do ----------------------------------------------
def test_a_rehearsed_mass_is_the_painted_one(tmp_path, call, painting):
    """Pixel for pixel, across the save and reload every tool call does.

    The engine promises this of a rehearsal; the server reloads the session between
    the rehearsal and the painting, which is exactly where a stream state gets lost.
    """
    plan = {"shape": {"blob": "D5", "radius": 0.14, "seed": 3}, "brush": "bristle",
            "color": "burnt_umber", "size": 0.05, "direction": "axis"}
    trial = call("rehearse", session=painting, plan=plan, scale=0)
    call("run", session=painting, script="\n".join(trial.text.splitlines()[2:]))
    real = call("look", session=painting, scale=0)

    assert np.array_equal(np.asarray(trial.picture.convert("RGB")),
                          np.asarray(real.picture.convert("RGB")))


def test_planning_does_not_spend_the_stream(tmp_path, call):
    """Three rounds of asking, and the painting that follows is byte for byte the one
    that would have been painted without asking at all."""
    plan = {"shape": {"blob": "D5", "radius": 0.14, "seed": 3}, "size": 0.05}
    mass = "s.block_in(blob(cell('D5'), 0.14, seed=3), size=0.05)"
    rendered = []
    for name, rounds in (("quiet", 0), ("asked", 3)):
        session = str(tmp_path / f"{name}.easel")
        call("new", session=session, size="480x360", seed=11,
             out_dir=str(tmp_path / "out"))
        call("run", session=session,
             script="s.stroke([(0.1, 0.2), (0.8, 0.3)], 'bristle', 'ochre')")
        for _ in range(rounds):
            call("cost", session=session, plan=plan)
            call("preview", session=session, plan=plan)
            call("rehearse", session=session, plan=plan)
        call("run", session=session, script=mass)
        out = str(tmp_path / f"{name}.png")
        call("export", session=session, output=out)
        rendered.append(np.asarray(Image.open(out).convert("RGB")))
    assert np.array_equal(*rendered)


def test_preview_and_cost_paint_nothing(call, painting):
    before = call_count(call, painting)
    plan = {"shape": {"blob": "D5", "radius": 0.14}, "size": 0.05}
    call("cost", session=painting, plan=plan)
    call("preview", session=painting, plan=plan)
    call("rehearse", session=painting, plan=plan)
    assert call_count(call, painting) == before


# -- the rest of the verbs -------------------------------------------------------------
def test_marks_are_set_listed_and_forgotten(call, painting):
    call("mark", session=painting, name="top_l", x=0.33, y=0.31)
    call("mark", session=painting, name="base", x=0.5, y=0.8)
    assert "0.330 0.310" in call("mark", session=painting).text
    call("mark", session=painting, name="base", forget=True)
    assert call("mark", session=painting).text.count("\n") == 0


def test_undo_scrapes_back_and_says_what_is_left(call, painting):
    call("run", session=painting,
         script="s.block_in(cell('D5'), 'bristle', 'burnt_umber', size=0.08)")
    before = call_count(call, painting)
    assert call("undo", session=painting, n=2).text == (
        f"Undid 2 stroke(s). {before - 2} remain."
    )
    assert call_count(call, painting) == before - 2


def test_prepare_merges_and_redraws_the_map(call, painting, reference):
    plain = call("prepare", session=painting, reference=reference, level="coarse")
    merged = call("prepare", session=painting, reference=reference, level="coarse",
                  merge=[[1, 2]])
    assert len(merged.images) == 1
    assert merged.text.count("\n") < plain.text.count("\n")


def test_prepare_says_when_it_laid_the_sketch(call, painting, reference):
    """An assisted mode has to be impossible to use without noticing."""
    reply = call("prepare", session=painting, reference=reference, sketch=True)
    assert "ASSISTED" in reply.text
    assert Session.load(painting).assisted


def test_export_and_timelapse_write_what_they_say(tmp_path, call, painting):
    png = call("export", session=painting, output=str(tmp_path / "final.png")).text
    sheet = call("timelapse", session=painting, output=str(tmp_path / "sheet.png")).text
    assert Image.open(png).size == (480, 360)
    assert Image.open(sheet).size[0] > 0


def test_what_a_file_says_as_it_opens_comes_back_with_the_answer(call, painting):
    """What a file said as it opened was warned to the server's stderr, which a painter
    working through a client never sees: 0.6.0 closed that gap for what a *call* says
    and left it open for what a *file* says. An older file's rebuild notice comes back
    at the top of whatever the tool answers -- until a tool saves the file, which
    stamps it with this release."""
    import json

    call("run", session=painting, script="s.smudge([(0.3, 0.5), (0.7, 0.5)])")
    with np.load(painting, allow_pickle=False) as data:
        arrays = {k: data[k] for k in data.files}
    meta = json.loads(str(arrays["meta"]))
    del meta["engine"], meta["notices"]              # as 0.5.0 wrote it
    arrays["meta"] = np.array(json.dumps(meta))
    with open(painting, "wb") as fh:
        np.savez_compressed(fh, **arrays)

    told = call("log", session=painting).text
    assert told.startswith("at load, 1 thing said:") and "older-engine" in told
    assert "older-engine" in call("log", session=painting).text     # log does not save
    looked = call("look", session=painting)
    assert "older-engine" in looked.text and len(looked.images) == 1
    assert "at load" not in call("log", session=painting).text


# -- failures ---------------------------------------------------------------------------
def test_a_missing_session_says_how_to_make_one(call, tmp_path):
    with pytest.raises(ToolError, match="No session at"):
        call("look", session=str(tmp_path / "nothing.easel"))


def test_an_existing_session_is_not_overwritten_by_accident(call, painting):
    with pytest.raises(ToolError, match="already exists"):
        call("new", session=painting)
    call("new", session=painting, force=True)


def test_a_script_that_raises_keeps_what_it_painted(call, painting):
    """A half-finished pass is still work, as it is from the shell."""
    before = call_count(call, painting)
    reply = call("run", session=painting, script=(
        "s.stroke([(0.1, 0.5), (0.6, 0.5)], 'bristle', 'ochre')\n"
        "raise RuntimeError('mid-pass')\n"))
    assert "session saved with" in reply.text and "RuntimeError" in reply.text
    assert call_count(call, painting) == before + 1


def test_a_script_that_does_not_parse_paints_nothing(call, painting):
    before = call_count(call, painting)
    assert "does not parse" in call("run", session=painting, script="s.stroke(").text
    assert call_count(call, painting) == before


def test_run_needs_exactly_one_of_script_and_script_path(call, painting):
    with pytest.raises(ToolError, match="exactly one"):
        call("run", session=painting)
    with pytest.raises(ToolError, match="exactly one"):
        call("run", session=painting, script="pass", script_path="x.py")


def test_a_bad_argument_keeps_the_engine_s_own_words(call, painting):
    """The CLI turns these into one `easel: ...` line; so does this, in the same words."""
    with pytest.raises(ToolError, match=r"easel: .*Unknown region 'Q9'"):
        call("look", session=painting, region="Q9")
    with pytest.raises(ToolError, match="Size must look like"):
        call("new", session=painting, size="big", force=True)


def test_a_plan_is_one_entry_or_a_list_of_them(call, painting):
    """Both are natural to write, so both are taken -- as the Python API takes them."""
    one = {"shape": {"blob": "D5", "radius": 0.12}, "size": 0.06}
    assert (_plan(one)[1]) == _plan([one])[1]


def test_run_hands_back_the_post_pass_check(call, painting):
    """The line `easel run` prints beside the budget line, through the wire too -- the
    same words for the same pass, whichever way the pass was run."""
    reply = call("run", session=painting,
                 script="s.stroke([(0.1, 0.5), (0.9, 0.5)], 'flat', 'ochre')")
    assert "check over this pass" in reply.text
    stack = ("s.block_in(Region(0.1, 0.1, 0.9, 0.4), 'flat', 'ochre', size=0.04)\n"
             "s.block_in(Region(0.1, 0.5, 0.9, 0.8), 'flat', 'ochre', size=0.04)\n")
    reply = call("run", session=painting, rehearse=True, script=stack)
    assert "Nothing committed" in reply.text and "from 2 calls" in reply.text

    # And the same pass counted: the price and the check, no paint and no look.
    counted = call("run", session=painting, count=True, script=stack)
    assert "Nothing painted, nothing committed" in counted.text
    assert "from 2 calls" in counted.text and ".png" not in counted.text
    laid = re.search(r"Rehearsed .*?: (\d+) strokes", reply.text).group(1)
    assert f"Counted <script>: {laid} strokes" in counted.text


# -- what the calls themselves said ----------------------------------------------------
#
# The half of the post-pass check that never arrived here. Every call-time warning was a
# `warnings.warn` going to this process's stderr, which a painter working through a
# client never sees -- so `the tool warns you` was false through this server for
# everything except the check above. Since 0.6.0 each one carries a code and rides in
# the returned text; see `easel.notices`.
def test_run_hands_back_what_the_calls_said(call, painting):
    reply = call("run", session=painting,
                 script="s.block_in(cell('D5'), 'flat', 'ochre', size=0.001)\n"
                        "s.block_in(cell('E5'), 'flat', 'ochre', size=0.001)\n")
    assert "at the call" in reply.text
    # Said once for the two calls that said it, and above the check it belongs beside.
    assert reply.text.count("chisel-blank") == 1
    assert "(2 calls)" in reply.text
    assert reply.text.index("at the call") < reply.text.index("check over this pass")


def test_a_pass_that_raised_still_hands_back_what_it_said(call, painting):
    reply = call("run", session=painting,
                 script="s.block_in(cell('D5'), 'flat', 'ochre', size=0.001)\n"
                        "raise ValueError('stopped here')\n")
    assert "chisel-blank" in reply.text and "script raised" in reply.text


def test_a_quote_says_why_it_is_that_large(call, painting):
    """A mass with `direction` left off costing many times its own axis is exactly what
    a quote is asked for -- and the walk that works it out happens on a throwaway copy,
    so what it says has to be carried back to the session to reach here at all."""
    tall = {"shape": {"ellipse": "D5", "rx": 0.02, "ry": 0.30}, "brush": "flat",
            "color": "ochre", "size": 0.01}
    assert "direction-default" in call("cost", session=painting, plan=tall).text


def test_run_keeps_what_it_handed_back_rehearsals_included(call, painting):
    """0.7.0's C0 through the wire: the block `run` hands back after a pass is kept in
    the session file, a rehearsal's too, and `log` with `reports` reads it back."""
    stack = ("s.block_in(Region(0.1, 0.1, 0.9, 0.4), 'flat', 'ochre', size=0.04)\n"
             "s.block_in(Region(0.1, 0.5, 0.9, 0.8), 'flat', 'ochre', size=0.04)\n")
    reply = call("run", session=painting, rehearse=True, script=stack)
    kept = Session.load(painting).reports()
    assert [r.mode for r in kept] == ["painted", "rehearsed"]
    assert kept[-1].text in reply.text and "from 2 calls" in kept[-1].text
    assert Session.load(painting).stroke_count == 1       # and nothing else was kept

    log = call("log", session=painting, reports=True, n=1)
    assert "rehearsed <script>, from record 1" in log.text
    assert "painted <script>" not in log.text


def test_run_hands_back_the_look_it_rehearsed(call, painting):
    """A rehearsal is for looking at, and the path its text ends in is no use to a
    client that cannot open a file: the look comes back beside it, as the looking
    tools hand theirs back. A counted pass lays no paint and has no look to hand back."""
    import base64
    from pathlib import Path

    stroke = "s.stroke([(0.1, 0.5), (0.9, 0.5)], 'flat', 'ochre')"
    rehearsed = call("run", session=painting, rehearse=True, script=stroke)
    assert len(rehearsed.images) == 1
    written = Path(rehearsed.text.splitlines()[-1])      # the path, still in the text
    assert base64.b64decode(rehearsed.images[0]) == written.read_bytes()

    counted = call("run", session=painting, count=True, script=stroke)
    assert not counted.images


def test_run_rehearses_versions_side_by_side_and_hands_the_sheet_back(call, painting):
    """0.7.0's D0 through the wire: versions of one pass, each on a copy of its own and
    each told what a rehearsal is told, and their sheet inline -- a client has no shell
    to open a PNG from. An object names each version; a list numbers them."""
    dark = "s.block_in(cell('D5'), 'flat', 'burnt_umber', size=0.02)"
    blue = "s.block_in(cell('D5'), 'flat', 'ultramarine', size=0.02)"
    reply = call("run", session=painting, alternatives={"dark": dark, "blue": blue})
    assert "Rehearsed dark (1 of 2)" in reply.text and "Rehearsed blue (2 of 2)" in reply.text
    assert "dark and blue side by side" in reply.text
    wide, tall = reply.picture.size
    assert wide > 1.8 * tall
    kept = Session.load(painting)
    assert kept.stroke_count == 1                      # the fixture's mark, and no more
    assert [(r.mode, r.scripts) for r in kept.reports()[-2:]] == [
        ("rehearsed", "dark"), ("rehearsed", "blue")]

    counted = call("run", session=painting, alternatives=[dark, blue], count=True)
    assert "Counted <alternative 2> (2 of 2)" in counted.text and not counted.images

    with pytest.raises(ToolError, match="in place of script"):
        call("run", session=painting, script=dark, alternatives=[blue])


def test_look_takes_the_landmarks_off(call, painting):
    """The lighthouse painter's `clean_look.py` in one argument, through the wire."""
    bare = np.asarray(call("look", session=painting, scale=0).picture.convert("RGB"))
    call("mark", session=painting, name="lamp", x=0.5, y=0.4)
    marked = call("look", session=painting, scale=0).picture.convert("RGB")
    clean = call("look", session=painting, scale=0, marks=False).picture.convert("RGB")
    assert not np.array_equal(np.asarray(marked), bare)
    assert np.array_equal(np.asarray(clean), bare)


def test_the_plan_help_names_every_kind_and_the_film():
    """The grammar a client reads is `_PLAN_HELP`, quoted by preview, rehearse and cost."""
    from easel.mcp_server import _PLAN_HELP

    for key in ("'points'", "'shape'", "'edge'", "'band'", "'cover'", "'glaze': true"):
        assert key in _PLAN_HELP, key
    assert "whole pass is a plan" in _PLAN_HELP


def test_rehearse_and_preview_say_what_they_found(call, painting):
    small = {"shape": {"ellipse": "D5", "rx": 0.10, "ry": 0.10}, "brush": "flat",
             "color": "ochre", "size": 0.001}
    assert "chisel-blank" in call("rehearse", session=painting, plan=small).text
    assert "chisel-blank" in call("preview", session=painting, plan=small).text


def test_explain_hands_back_the_passage_that_measured_it(call):
    """Where the reason goes once its paragraph leaves the reading path: not deleted,
    handed over at the moment it applies -- and a client has no repository to read."""
    reply = call("explain", code="chisel-blank")
    assert "What a solid mass actually lands at" in reply.text
    assert "chisel-blank (fact)" in reply.text

    everything = call("explain").text
    assert "chisel-blank" in everything and "smudge-wide" in everything

    with pytest.raises(ToolError, match="unknown notice"):
        call("explain", code="chisel-blanc")


def test_diagnose_hands_back_the_passage_rather_than_the_pointer(call):
    """`DIAGNOSIS.md` was a file to grep, which over MCP is not a thing a client can
    do -- and the file was not even in the wheel. The index arrives as an answer here:
    words describing the canvas in, the measurement out, with the pointer followed.

    The row's own wording is the weakest part of the promise, so the assertion is on
    the target: `easel.diagnosis` decides which section that is, and this checks the
    section came through the wire whole."""
    from easel import diagnosis

    row = next(r for r in diagnosis.rows() if "concentric rings" in r.symptom)
    reply = call("diagnose", symptom="a glow with concentric rings")
    assert row.symptom in reply.text
    assert row.pointers[0].passage().strip() in reply.text

    brief = call("diagnose", symptom="a glow with concentric rings", brief=True).text
    assert row.symptom in brief and len(brief) < len(reply.text)

    assert call("diagnose").text == diagnosis.listing()


def test_demo_paints_a_recipe_beside_its_failure_and_hands_the_sheet_back(call, tmp_path):
    """A client has no shell to open a PNG from, so the sheet comes back inline, beside
    what each panel was told -- the notice itself, not only its code."""
    from easel import demo

    reply = call("demo", recipe="container", out_dir=str(tmp_path))
    assert "the call says round-fringe" in reply.text
    assert "round-fringe: " in reply.text
    width, height = reply.picture.size
    assert width > 2 * height                    # the recipe and its failure, side by side
    assert call("demo").text == demo.listing()


# -- what the painter declares ---------------------------------------------------------
def test_the_plan_tool_declares_what_the_check_then_holds_the_painting_to(call, painting):
    """The third way of declaring one, beside `s.plan()` and `easel plan`. It is the one
    that matters most for this server: a painter working through a client cannot write a
    `prelude.py`, so without a tool the declarations would be reachable from a shell and
    from Python and not from here."""
    reply = call("plan", session=painting, values={"A1:H4": 0.40, "A5:H8": 0.44},
                 lightest="A1:H4", subject_share=0.4, bands="subject", ground="buried",
                 why="the light arrives from below")
    assert 'why: "the light arrives from below"' in reply.text
    # The pairs, on the empty canvas, and through the notice channel as well as the table.
    assert "plan-pairs" in reply.text
    assert "A1:H4 / A5:H8: 0.04 apart, and they meet" in reply.text

    # Saved, so the next pass through any of the three routes is held to it.
    held = Session.load(painting).plan()
    assert held.bands == "subject" and held.ground == "buried"
    assert held.subject_share == 0.4 and held.lightest.name == "A1:H4"

    # And the declarations reach the check the `run` tool hands back.
    ran = call("run", session=painting,
               script="s.block_in(span('A1', 'H4'), 'flat', 'titanium_white',\n"
                      "           direction='axis', note='subject')\n")
    assert "plan: " in ran.text and "lightest: " in ran.text
    assert "against 40% planned" in ran.text

    # Called again it changes one thing and keeps the rest, and clears on request.
    again = call("plan", session=painting, why="a different sentence")
    assert "a different sentence" in again.text and "bands: subject" in again.text
    assert Session.load(painting).plan().values, "the values were dropped"
    assert "no plan registered" in call("plan", session=painting, clear=True).text
