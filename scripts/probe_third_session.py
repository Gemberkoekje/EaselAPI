"""The measurements behind the third session's list in SUGGESTIONS.md.

Seven probes on a 512x384 canvas, each printing the numbers quoted there: what the
palette makes of a raw triple, which edge a pass stack starts on, why the inward
scumble fills solid at the default brush size, the flat's wander by jitter, whether
opacity changes a solid block-in, whether a pressure list flips on alternate passes,
and whether a rehearsal copy can diff against the painting's last look.

    python scripts/probe_third_session.py            # writes out/probe_third_*.png
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from easel import Region, Session, ellipse, polygon

OUT = Path("out")


def srgb(c: np.ndarray) -> np.ndarray:
    c = np.clip(np.asarray(c, dtype=np.float64), 0.0, 1.0)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def values(s: Session) -> np.ndarray:
    """The value look(values=True) shows, per pixel."""
    sr = srgb(np.asarray(s.canvas.rgb, dtype=np.float64))
    return 0.2126 * sr[..., 0] + 0.7152 * sr[..., 1] + 0.0722 * sr[..., 2]


def new(ground: str = "toned_grey", seed: int = 1) -> Session:
    return Session(512, 384, ground=ground, seed=seed, timelapse=False, out_dir=OUT)


def red_in(s: Session, y0: float, y1: float, x0: float, x1: float) -> float:
    rgb = np.asarray(s.canvas.rgb, dtype=np.float64)
    h, w = rgb.shape[:2]
    return float(rgb[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w), 0].mean())


def probe_triple() -> None:
    print("== a raw triple is read as sRGB ==")
    s = new()
    p = s.palette
    lin = np.asarray(s.canvas.rgb, dtype=np.float64).reshape(-1, 3).mean(axis=0)
    p["as_tuple"] = tuple(float(v) for v in lin)
    p["as_array"] = np.asarray(lin, dtype=np.float32)
    p["as_hex"] = "#" + "".join(f"{int(round(v * 255)):02x}" for v in srgb(lin))
    print(
        f"  ground reads {values(s).mean():.2f}; its mean handed back as a tuple reads "
        f"{p.value_of('as_tuple'):.2f}, as a float32 array {p.value_of('as_array'):.2f}, "
        f"encoded to hex first {p.value_of('as_hex'):.2f}"
    )


def probe_first_pass() -> None:
    print("\n== which edge the first pass of a stack lands on ==")
    for direction in (0, 90, "horizontal", "vertical", "axis", 45):
        s = new()
        s.scumble(Region(0.1, 0.1, 0.9, 0.9), "cadmium_red", "ultramarine", 5,
                  brush="flat", size=0.08, opacity=1.0, direction=direction)
        strips = {
            "top": red_in(s, 0.12, 0.2, 0.3, 0.7),
            "bottom": red_in(s, 0.8, 0.88, 0.3, 0.7),
            "left": red_in(s, 0.3, 0.7, 0.12, 0.2),
            "right": red_in(s, 0.3, 0.7, 0.8, 0.88),
        }
        where = max(strips, key=strips.get)
        detail = "  ".join(f"{k} {v:.2f}" for k, v in strips.items())
        print(f"  direction={direction!r:14} colour a (red) is at the {where:6}  {detail}")
    s = new()
    square = polygon([(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)])
    s.scumble(square, "cadmium_red", "ultramarine", 5, brush="flat", size=0.08,
              opacity=1.0, direction=90)
    print(f"  polygon, direction=90: left red {red_in(s, 0.3, 0.7, 0.12, 0.2):.2f}, "
          f"right red {red_in(s, 0.3, 0.7, 0.8, 0.88):.2f}")


def inward(size: float, brush: str = "bristle", small: bool = False) -> tuple[float, np.ndarray]:
    """Share of an inward-scumbled patch flat at the centre value, and its profile."""
    s = new()
    p = s.palette
    a = p.at_value(p.mix("ultramarine", "alizarin", 0.5), 0.45)
    b = p.at_value(p.mix("cadmium_yellow", "cadmium_red", 0.3), 0.75)
    rx, ry = (0.1, 0.1 * s.aspect) if small else (0.36, 0.12)
    s.scumble(ellipse((0.5, 0.5), rx, ry), a, b, 7, brush=brush, size=size,
              opacity=0.5, direction="inward")
    v = values(s)
    h, w = v.shape
    yy, xx = np.mgrid[0:h, 0:w]
    x, y = (xx + 0.5) / w, (yy + 0.5) / h
    mask = ((x - 0.5) / rx) ** 2 + ((y - 0.5) / ry) ** 2 <= 1.0
    flat = float((v[mask] >= 0.75 - 0.06).mean())
    col = v[:, w // 2]
    top = int((0.5 - ry) * h)
    step = max(1, (h // 2 - top) // 6)
    return flat, np.round(col[top:h // 2 + 1][::step], 2)


def probe_inward() -> None:
    print("\n== the inward scumble, by brush size (share flat at the centre value) ==")
    for size in (0.09, 0.05, 0.03, 0.02):
        flat, prof = inward(size)
        print(f"  ellipse 0.72x0.24, n=7, bristle {size}: {flat * 100:5.1f}%  edge->centre {prof}")
    flat, prof = inward(0.09, brush="round_soft")
    print(f"  ellipse 0.72x0.24, n=7, round_soft 0.09: {flat * 100:5.1f}%  edge->centre {prof}")
    for size in (0.05, 0.02):
        flat, prof = inward(size, small=True)
        print(f"  round patch r=0.10, n=7, bristle {size}: {flat * 100:5.1f}%  edge->centre {prof}")


def probe_wander() -> None:
    print("\n== the flat's wander, by jitter (one stroke, size 0.1 = 51 px) ==")
    for jitter, size_jitter in ((0.02, 0.06), (0.01, 0.03), (0.005, 0.0), (0.0, 0.0)):
        s = new(ground="white")
        s.stroke([(0.05, 0.5), (0.95, 0.5)], "flat", "ultramarine", size=0.1, opacity=1.0,
                 load=1.0, load_falloff=0.0, pressure="even", jitter=jitter,
                 size_jitter=size_jitter)
        v = values(s)
        h, w = v.shape
        edge = []
        for xi in range(int(0.15 * w), int(0.85 * w)):
            rows = np.where(v[:, xi] < 0.6)[0]
            if len(rows):
                edge.append(rows[0])
        e = np.array(edge)
        print(f"  jitter={jitter:<5} size_jitter={size_jitter:<4}: top edge sd {e.std():4.1f} px, "
              f"peak to peak {int(e.max() - e.min()):3d} px")


def probe_solid() -> None:
    print("\n== solid=True by opacity and pressure (flat 0.03, interior of a region) ==")
    for opacity, pressure in ((0.85, "taper"), (1.0, "taper"), (0.85, "even"), (1.0, "even")):
        s = new()
        s.block_in(Region(0.15, 0.15, 0.85, 0.85), "flat", "burnt_umber", size=0.03,
                   density=1.0, solid=True, opacity=opacity, pressure=pressure)
        v = values(s)
        h, w = v.shape
        inner = v[int(0.25 * h):int(0.75 * h), int(0.25 * w):int(0.75 * w)]
        rows = inner.mean(axis=1)
        print(f"  opacity={opacity} pressure={pressure:<5}: interior sd {inner.std():.3f}, "
              f"row-mean peak to peak {rows.max() - rows.min():.3f}")


def probe_pressure_list() -> None:
    print("\n== a pressure list on the passes of a scumble ==")
    s = new(ground="white")
    s.scumble(Region(0.1, 0.3, 0.9, 0.7), "ultramarine", "ultramarine", 4, brush="flat",
              size=0.05, opacity=1.0, load=1.0, load_falloff=0.0, direction=0,
              pressure=[0.0, 1.0])
    cover = 1.0 - values(s)
    h, w = cover.shape
    for i in range(4):
        y0 = 0.3 + i * 0.1
        band = cover[int(y0 * h):int((y0 + 0.1) * h)]
        left = band[:, int(0.12 * w):int(0.3 * w)].mean()
        right = band[:, int(0.7 * w):int(0.88 * w)].mean()
        heavy = "right" if right > left else "left"
        print(f"  pass {i + 1}: paint at the left end {left:.2f}, right end {right:.2f} "
              f"-> heavy end is the {heavy}")


def probe_diff_in_rehearsal() -> None:
    print("\n== look(diff=True) on a rehearsal copy ==")
    s = new()
    s.block_in("upper-half", "flat", "ultramarine", size=0.2)
    s.look(path=OUT / "probe_third_before.png")
    t = s.scratch()
    t.stroke([(0.2, 0.75), (0.8, 0.75)], "flat", "cadmium_yellow", size=0.1)
    print(f"  the copy's _last_look is {t._last_look!r}, so the diff has nothing to tint "
          f"against; wrote {t.look(diff=True, path=OUT / 'probe_third_rehearsal_diff.png')}")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    probe_triple()
    probe_first_pass()
    probe_inward()
    probe_wander()
    probe_solid()
    probe_pressure_list()
    probe_diff_in_rehearsal()


if __name__ == "__main__":
    main()
