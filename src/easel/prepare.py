"""Reference preparation: the photograph, cut into numbered masses.

Programmatic and dumb on purpose. No model, no LLM, no learned segmentation: the
reference is quantised in a perceptual colour space, connected areas are labelled,
fragments below a minimum size are merged into whichever neighbour they are
closest to in colour, and what comes out is an overlay with outlines and numbers
plus a table -- share of the picture, cells covered, mean value and colour, which
areas touch which, and how hard each shared edge is.

**The map is not the truth and the painter's job is to say so.** The automation
will join two things of the same colour and cut one thing along its shading. That is
why :meth:`Preparation.merge` and :meth:`Preparation.split` exist: the useful
sentence is "area 5 is one thing, less the strip that belongs to its neighbour", not "the
computer says there are eleven areas".

The outlines are for looking and naming. Painting them is a separate decision --
see :meth:`easel.session.Session.sketch`, which lays them as pencil and is an
assisted mode the definition of done reports separately.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from easel.color import linear_to_oklab, linear_to_srgb, luminance, srgb_to_linear
from easel.regions import GRID_COLS, GRID_ROWS, Polygon, Region

__all__ = ["Area", "Preparation", "prepare_reference", "LEVELS"]

#: How many masses each granularity aims at. Coarse is the one to start from: five
#: to eight masses is a value study, and a value study is what a painting is hung on.
LEVELS: dict[str, int] = {"coarse": 7, "medium": 20, "fine": 40}

#: Working resolution for the segmentation, on the long side. The masses of a
#: picture are visible at a couple of hundred pixels -- that is what squinting is --
#: and everything here runs per pixel in Python.
WORK_SIZE = 256

_OUTLINE_COLORS = [
    (255, 215, 60), (90, 220, 255), (255, 120, 90), (150, 255, 150),
    (255, 150, 230), (200, 200, 255), (255, 190, 120), (140, 255, 220),
]


@dataclass(frozen=True)
class Area:
    """One mass of the prepared reference."""

    number: int
    #: Normalised bounds (x0, y0, x1, y1).
    bounds: tuple[float, float, float, float]
    #: Share of the whole picture, 0..1.
    share: float
    #: Grid cells the area touches, e.g. ``["D4", "E4"]``.
    cells: list[str]
    #: Mean value 0..1, sRGB-encoded, the same number the greyscale view shows.
    value: float
    #: Mean colour as sRGB hex. Coarse on purpose.
    hex: str
    #: ``{neighbour number: edge hardness 0..1}``. 0 is a soft, lost edge; 1 is cut.
    neighbours: dict[int, float] = field(default_factory=dict)
    #: The area's boundary as normalised points.
    outline: list[tuple[float, float]] = field(default_factory=list)
    #: Where to write the area's number so it lands *on* the area. The centre of a
    #: bounding box does not: a wall wrapped round a mug has its box centre on the
    #: mug, and a label there says the wall is the mug.
    label_at: tuple[float, float] = (0.5, 0.5)

    @property
    def region(self) -> Region:
        return Region(*self.bounds, name=f"area{self.number}")

    def __str__(self) -> str:
        edges = ", ".join(f"{n}:{h:.2f}" for n, h in sorted(self.neighbours.items()))
        cells = ",".join(self.cells[:6]) + ("..." if len(self.cells) > 6 else "")
        return (f"{self.number:>3d}  {self.share * 100:5.1f}%  value {self.value:.2f}  "
                f"{self.hex}  cells {cells or '-'}  edges {edges or '-'}")


class Preparation:
    """The prepared reference: numbered areas, their table, and their outlines.

    Print it. Numbers are stable: merging keeps the lower number and splitting adds
    new ones at the end, so a note the painter made about "area 5" stays true.
    """

    def __init__(
        self,
        labels: np.ndarray,
        image: np.ndarray,
        level: str,
        source: Path | None = None,
    ) -> None:
        self.labels = labels                 # (h, w) int32, 1-based; 0 is unassigned
        self.image = image                   # (h, w, 3) float32 sRGB 0..1, working size
        self.level = level
        self.source = source
        #: Where the overlay was written, when this came from ``Session.prepare``.
        self.overlay_path: Path | None = None
        self._areas: dict[int, Area] = {}
        self._rebuild()

    # -- the areas --------------------------------------------------------------
    @property
    def areas(self) -> list[Area]:
        """Every area, largest first."""
        return sorted(self._areas.values(), key=lambda a: -a.share)

    @property
    def numbers(self) -> list[int]:
        return sorted(self._areas)

    def __len__(self) -> int:
        return len(self._areas)

    def __getitem__(self, number: int) -> Area:
        n = int(number)
        if n not in self._areas:
            raise KeyError(
                f"No area {n}. This preparation has {', '.join(map(str, self.numbers))}."
            )
        return self._areas[n]

    def region(self, number: int) -> Region:
        """An area's bounding rectangle, for ``look(region=...)`` or a block-in."""
        return self[number].region

    def shape(self, number: int) -> Polygon:
        """An area as a :class:`~easel.regions.Polygon`, ready to block in.

        Traced, and marked as such: see :meth:`easel.session.Session.ref_shape`.
        """
        return Polygon(tuple(self[number].outline), name=f"area {int(number)}",
                       traced=True)

    def outline(self, number: int) -> list[tuple[float, float]]:
        """An area's boundary as normalised points."""
        return list(self[number].outline)

    def outlines(self) -> list[list[tuple[float, float]]]:
        """Every area's boundary, largest area first."""
        return [list(a.outline) for a in self.areas]

    # -- the painter's corrections ----------------------------------------------
    def merge(self, number: int, *others: int) -> int:
        """Join areas into one. The lowest number survives.

        The automation joins what is the same colour, and a painting is not made of
        colours -- it is made of things. Two areas that are one mass get merged here.
        """
        group = sorted({int(number), *(int(o) for o in others)})
        for n in group:
            if n not in self._areas:
                raise KeyError(f"No area {n} to merge. Have {self.numbers}.")
        if len(group) < 2:
            raise ValueError("Merging needs at least two areas: prep.merge(5, 7).")
        keep = group[0]
        for n in group[1:]:
            self.labels[self.labels == n] = keep
        self._rebuild()
        return keep

    def split(self, number: int, into: int = 2, seed: int = 0) -> list[int]:
        """Cut one area into ``into`` parts by colour. New parts get new numbers.

        For when the automation has joined one thing to the thing behind it. Split,
        look at the overlay, and merge back whatever it got wrong.
        """
        n = int(number)
        area_mask = self.labels == n
        count = int(area_mask.sum())
        if count < into * 4:
            raise ValueError(
                f"Area {n} is only {count} working pixels -- too small to split into "
                f"{into}. Prepare at a finer level instead."
            )
        lab = linear_to_oklab(srgb_to_linear(self.image[area_mask]))
        assign = _kmeans(lab, int(into), seed=seed)

        # The first part keeps the number; the rest get fresh ones off the end, so a
        # note the painter already made about this area is still about this area.
        fresh = [n] + [max(self.numbers) + 1 + i for i in range(int(into) - 1)]
        flat = self.labels[area_mask]
        used: list[int] = []
        for part, new in enumerate(fresh):
            member = assign == part
            if not member.any():
                # k-means can converge with an empty cluster on duplicate-heavy
                # colour data (a large flat-coloured area is exactly that).
                # Handing back a number with the label map never assigns to it
                # means the very next prep[number]/region(number)/outline(number)
                # raises KeyError -- so skip it here instead of promising an
                # area that was never actually created.
                continue
            flat[member] = new
            used.append(new)
        self.labels[area_mask] = flat
        self._rebuild()
        return used

    # -- output ------------------------------------------------------------------
    def table(self) -> str:
        """Every area as a line: share, value, colour, cells, and its edges."""
        head = (f"prepared {self.source.name if self.source else 'reference'} "
                f"({self.level}): {len(self)} areas\n"
                f"  #  share  value  colour   cells                     "
                f"edges (neighbour:hardness, 0 soft .. 1 cut)")
        return "\n".join([head] + [str(a) for a in self.areas])

    def __str__(self) -> str:
        return self.table()

    def overlay(
        self,
        reference: Image.Image,
        canvas: Image.Image | None = None,
        numbers: bool = True,
    ) -> Image.Image:
        """Outlines and numbers on the reference, and the same outlines on the canvas.

        The canvas panel is the point: an outline drawn over the painting says where
        a mass *should* be, next to where it is.
        """
        ref = _with_outlines(reference.convert("RGB"), self.areas, numbers=numbers)
        if canvas is None:
            return ref
        h = ref.size[1]
        cav = canvas.convert("RGB")
        cav = cav.resize((max(1, round(cav.size[0] * h / cav.size[1])), h), Image.LANCZOS)
        cav = _with_outlines(cav, self.areas, numbers=numbers)
        gap = 12
        out = Image.new("RGB", (ref.size[0] + gap + cav.size[0], h), (24, 24, 24))
        out.paste(ref, (0, 0))
        out.paste(cav, (ref.size[0] + gap, 0))
        return out

    # -- internals ---------------------------------------------------------------
    def _rebuild(self) -> None:
        """Recompute every area's statistics from the label map."""
        h, w = self.labels.shape
        srgb = self.image
        linear = srgb_to_linear(srgb)
        value = linear_to_srgb(luminance(linear))
        # Edge hardness is measured in Oklab, not in value. Two masses can differ
        # entirely in hue at almost the same value -- a warm table against a cool
        # wall -- and a value gradient calls that boundary lost when the painter can
        # see it perfectly well.
        grad = _gradient_magnitude(linear_to_oklab(linear))
        total = float(h * w)

        self._areas = {}
        present = [int(n) for n in np.unique(self.labels) if n > 0]
        edges = _edge_hardness(self.labels, grad)

        for n in present:
            mask = self.labels == n
            ys, xs = np.nonzero(mask)
            bounds = (
                float(xs.min() / w), float(ys.min() / h),
                float((xs.max() + 1) / w), float((ys.max() + 1) / h),
            )
            mean_rgb = srgb[mask].mean(axis=0)
            self._areas[n] = Area(
                number=n,
                bounds=bounds,
                share=float(mask.sum() / total),
                cells=_cells_covered(mask),
                value=float(value[mask].mean()),
                hex="#{:02X}{:02X}{:02X}".format(
                    *np.clip(mean_rgb * 255 + 0.5, 0, 255).astype(int)),
                neighbours=edges.get(n, {}),
                outline=_trace_outline(mask),
                label_at=_label_point(ys, xs, w, h),
            )


# --------------------------------------------------------------------------------------
# Building one
# --------------------------------------------------------------------------------------
def prepare_reference(
    reference,
    level: str = "coarse",
    min_share: float = 0.004,
    seed: int = 0,
    work_size: int = WORK_SIZE,
) -> Preparation:
    """Cut a reference photograph into numbered masses.

    Args:
        reference: a path or a PIL image.
        level: ``"coarse"`` (five to eight masses -- start here), ``"medium"``
            (about twenty) or ``"fine"``.
        min_share: areas smaller than this share of the picture are merged into the
            neighbour closest to them in colour.
        seed: fixes the quantisation, so the same photograph prepares the same way.
        work_size: long side the segmentation runs at.

    Returns:
        A :class:`Preparation`.
    """
    if level not in LEVELS:
        raise ValueError(f"Unknown level {level!r}. Choose one of: {', '.join(LEVELS)}.")

    source = None
    if not isinstance(reference, Image.Image):
        source = Path(reference)
        if not source.exists():
            raise FileNotFoundError(f"Reference image not found: {source}")
        img = Image.open(source).convert("RGB")
    else:
        img = reference.convert("RGB")

    f = work_size / float(max(img.size))
    small = img.resize(
        (max(8, round(img.size[0] * f)), max(8, round(img.size[1] * f))), Image.LANCZOS
    ) if f < 1.0 else img
    srgb = np.asarray(small, dtype=np.float32) / 255.0

    target = LEVELS[level]
    lab = linear_to_oklab(srgb_to_linear(srgb)).reshape(-1, 3)
    # More clusters than masses wanted, then merged back: quantising straight to the
    # target number gives one cluster per *colour*, and a picture has more masses
    # than colours -- two separate things the same brown are two masses.
    assign = _kmeans(lab, min(max(target + 4, 6), 48), seed=seed)
    quant = assign.reshape(srgb.shape[:2])

    labels = _connected_components(quant)
    labels = _merge_small(labels, srgb, min_share=min_share, target=target)
    return Preparation(labels, srgb, level, source)


# --------------------------------------------------------------------------------------
# The pieces
# --------------------------------------------------------------------------------------
def _kmeans(points: np.ndarray, k: int, seed: int = 0, iterations: int = 14) -> np.ndarray:
    """k-means with k-means++ seeding. Deterministic for a given seed."""
    pts = np.asarray(points, dtype=np.float32)
    n = len(pts)
    k = int(max(1, min(k, n)))
    rng = np.random.default_rng(seed)

    centres = np.empty((k, pts.shape[1]), dtype=np.float32)
    centres[0] = pts[rng.integers(n)]
    d2 = ((pts - centres[0]) ** 2).sum(axis=1).astype(np.float64)
    for i in range(1, k):
        total = float(d2.sum())
        if total <= 1e-12:
            centres[i] = pts[rng.integers(n)]
        else:
            # Renormalised in float64: numpy's `choice` rejects a probability vector
            # that misses 1 by a float32 ulp, which a quarter of a million squared
            # distances comfortably does.
            p = d2 / total
            centres[i] = pts[rng.choice(n, p=p / p.sum())]
        d2 = np.minimum(d2, ((pts - centres[i]) ** 2).sum(axis=1))

    sq = (pts * pts).sum(axis=1)[:, None]
    assign = np.zeros(n, dtype=np.int32)
    for _ in range(iterations):
        # |a - b|^2 expanded, rather than a (points, centres, 3) difference array:
        # the difference array is a hundred megabytes on a modest photograph.
        dist = sq - 2.0 * (pts @ centres.T) + (centres * centres).sum(axis=1)[None, :]
        new = dist.argmin(axis=1).astype(np.int32)
        if np.array_equal(new, assign):
            break
        assign = new
        for i in range(k):
            members = pts[assign == i]
            if len(members):
                centres[i] = members.mean(axis=0)
    return assign


def _connected_components(quant: np.ndarray) -> np.ndarray:
    """Label 4-connected runs of equal value. Two-pass, with union-find.

    Two separate things that happen to be the same brown are two masses, and a
    quantiser alone cannot say that -- it only knows colours. This is the step that
    turns colours into places.
    """
    h, w = quant.shape
    labels = np.zeros((h, w), dtype=np.int32)
    parent: list[int] = [0]

    def find(a: int) -> int:
        root = a
        while parent[root] != root:
            root = parent[root]
        while parent[a] != root:          # path compression
            parent[a], a = root, parent[a]
        return root

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for y in range(h):
        row, prev = quant[y], quant[y - 1] if y else None
        for x in range(w):
            up = labels[y - 1, x] if y and prev[x] == row[x] else 0
            left = labels[y, x - 1] if x and row[x - 1] == row[x] else 0
            if up and left:
                labels[y, x] = min(up, left)
                union(up, left)
            elif up or left:
                labels[y, x] = up or left
            else:
                parent.append(len(parent))
                labels[y, x] = len(parent) - 1

    roots = np.array([find(i) for i in range(len(parent))], dtype=np.int32)
    flat = roots[labels]
    # Renumber to a dense 1..n so the painter reads small numbers.
    used = np.unique(flat[flat > 0])
    remap = np.zeros(int(flat.max()) + 1, dtype=np.int32)
    remap[used] = np.arange(1, len(used) + 1, dtype=np.int32)
    return remap[flat]


def _neighbour_pairs(labels: np.ndarray) -> np.ndarray:
    """Every adjacent (a, b) label pair with a < b, one row per boundary pixel."""
    pairs = []
    for a, b in ((labels[:, :-1], labels[:, 1:]), (labels[:-1, :], labels[1:, :])):
        differ = a != b
        if differ.any():
            pairs.append(np.stack([a[differ], b[differ]], axis=1))
    if not pairs:
        return np.zeros((0, 2), dtype=np.int32)
    out = np.concatenate(pairs, axis=0)
    return np.sort(out, axis=1)


def _merge_small(
    labels: np.ndarray, srgb: np.ndarray, min_share: float, target: int
) -> np.ndarray:
    """Merge fragments away until nothing is tiny and there are about ``target`` masses.

    The smallest area goes first, into whichever neighbour it is closest to in
    Oklab -- not the largest neighbour, which would swallow a highlight into the
    shadow beside it rather than into the light it belongs to.
    """
    labels = labels.copy()
    lab = linear_to_oklab(srgb_to_linear(srgb))
    total = float(labels.size)

    for _ in range(4000):
        present, counts = np.unique(labels[labels > 0], return_counts=True)
        if len(present) <= 1:
            break
        smallest = int(present[counts.argmin()])
        smallest_share = counts.min() / total
        if smallest_share >= min_share and len(present) <= target:
            break

        pairs = _neighbour_pairs(labels)
        touching = pairs[(pairs[:, 0] == smallest) | (pairs[:, 1] == smallest)]
        if not len(touching):
            break
        others = np.unique(np.where(touching[:, 0] == smallest, touching[:, 1],
                                    touching[:, 0]))
        mine = lab[labels == smallest].mean(axis=0)
        best, best_d = None, None
        for other in others:
            d = float(((lab[labels == other].mean(axis=0) - mine) ** 2).sum())
            if best_d is None or d < best_d:
                best, best_d = int(other), d
        if best is None:
            break
        labels[labels == smallest] = best

    # Renumber densely again: the painter should read 1..n with no gaps.
    used = np.unique(labels[labels > 0])
    remap = np.zeros(int(labels.max()) + 1, dtype=np.int32)
    remap[used] = np.arange(1, len(used) + 1, dtype=np.int32)
    return remap[labels]


def _gradient_magnitude(field: np.ndarray) -> np.ndarray:
    """Spatial rate of change of a (h, w) or (h, w, c) field, as (h, w)."""
    arr = np.asarray(field, dtype=np.float32)
    if arr.ndim == 2:
        gy, gx = np.gradient(arr)
        return np.hypot(gx, gy).astype(np.float32)
    gy, gx = np.gradient(arr, axis=(0, 1))
    return np.sqrt((gx * gx + gy * gy).sum(axis=2)).astype(np.float32)


def _edge_hardness(labels: np.ndarray, grad: np.ndarray) -> dict[int, dict[int, float]]:
    """Mean gradient along each shared boundary, normalised to 0..1.

    A painter's question about two touching masses is not "do they touch" but "is
    that edge cut or lost". This is the number for it: high where the photograph
    changes abruptly across the boundary, low where it melts.
    """
    out: dict[int, dict[int, float]] = {}
    sums: dict[tuple[int, int], list[float]] = {}
    for shift, (a, b, g) in {
        "x": (labels[:, :-1], labels[:, 1:], grad[:, :-1]),
        "y": (labels[:-1, :], labels[1:, :], grad[:-1, :]),
    }.items():
        del shift
        differ = a != b
        if not differ.any():
            continue
        aa, bb, gg = a[differ], b[differ], g[differ]
        lo, hi = np.minimum(aa, bb), np.maximum(aa, bb)
        for key, value in zip(zip(lo.tolist(), hi.tolist(), strict=True), gg.tolist(),
                              strict=True):
            sums.setdefault(key, [0.0, 0.0])
            sums[key][0] += value
            sums[key][1] += 1.0

    if not sums:
        return out
    means = {k: v[0] / v[1] for k, v in sums.items() if v[1] > 0}
    # Normalised against the hardest edge in this picture: hardness is comparative.
    top = max(means.values()) or 1.0
    for (a, b), m in means.items():
        h = float(min(m / top, 1.0))
        out.setdefault(a, {})[b] = h
        out.setdefault(b, {})[a] = h
    return out


def _cells_covered(mask: np.ndarray, min_fraction: float = 0.08) -> list[str]:
    """Which A-H by 1-8 cells the area really sits in."""
    h, w = mask.shape
    cells = []
    for ri, row in enumerate(GRID_ROWS):
        y0, y1 = round(ri * h / len(GRID_ROWS)), round((ri + 1) * h / len(GRID_ROWS))
        for ci, col in enumerate(GRID_COLS):
            x0, x1 = round(ci * w / len(GRID_COLS)), round((ci + 1) * w / len(GRID_COLS))
            block = mask[y0:max(y1, y0 + 1), x0:max(x1, x0 + 1)]
            if block.size and block.mean() >= min_fraction:
                cells.append(f"{col}{row}")
    return cells


def _label_point(ys: np.ndarray, xs: np.ndarray, w: int, h: int) -> tuple[float, float]:
    """A point inside the area, near its centre of mass, to write the number at."""
    cy, cx = float(ys.mean()), float(xs.mean())
    # The centroid of a C-shape is outside it, so snap to the nearest pixel that is
    # actually in the area.
    k = int(np.argmin((ys - cy) ** 2 + (xs - cx) ** 2))
    return (float(xs[k]) / w, float(ys[k]) / h)


_MOORE = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))


def _largest_component(mask: np.ndarray) -> np.ndarray:
    """The mask's largest 8-connected run of ``True`` pixels, alone.

    An area fresh out of :func:`prepare_reference` is always one connected run,
    but :meth:`Preparation.merge` can join two that do not touch at all (its own
    docstring's example is one thing cut in two by another), and :meth:`Preparation.split`
    partitions by colour with no regard for where the pieces sit. A Moore-neighbour
    trace only ever follows one run's boundary, so it needs to be handed the one
    the caller means -- the biggest -- rather than whichever run happens to
    contain the mask's topmost-then-leftmost pixel.
    """
    h, w = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    best: list[tuple[int, int]] = []
    ys_all, xs_all = np.nonzero(mask)
    for sy, sx in zip(ys_all.tolist(), xs_all.tolist(), strict=True):
        if visited[sy, sx]:
            continue
        stack = [(sy, sx)]
        visited[sy, sx] = True
        component = [(sy, sx)]
        while stack:
            y, x = stack.pop()
            for dy, dx in _MOORE:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not visited[ny, nx]:
                    visited[ny, nx] = True
                    stack.append((ny, nx))
                    component.append((ny, nx))
        if len(component) > len(best):
            best = component

    out = np.zeros_like(mask)
    if best:
        rows, cols = zip(*best, strict=True)
        out[rows, cols] = True
    return out


def _trace_outline(mask: np.ndarray, tolerance: float = 0.9) -> list[tuple[float, float]]:
    """The area's boundary as normalised points, by Moore-neighbour tracing.

    Only the outer boundary of the largest run: an area with holes in it is still
    one shape to draw, and a painter drawing a mass draws its silhouette.
    """
    h, w = mask.shape
    if not np.any(mask):
        return []
    mask = _largest_component(mask)
    ys, xs = np.nonzero(mask)

    # Start at the topmost-leftmost pixel: the boundary is guaranteed to pass through
    # it, and its left neighbour is guaranteed to be outside.
    start_y = int(ys.min())
    start_x = int(xs[ys == start_y].min())

    def inside(y: int, x: int) -> bool:
        return 0 <= y < h and 0 <= x < w and bool(mask[y, x])

    contour = [(start_y, start_x)]
    cy, cx = start_y, start_x
    back = 6                                   # came from the left
    for _ in range(8 * mask.size):
        found = False
        for step in range(1, 9):
            d = (back + step) % 8
            ny, nx = cy + _MOORE[d][0], cx + _MOORE[d][1]
            if inside(ny, nx):
                back = (d + 5) % 8             # the direction we arrived from
                cy, cx = ny, nx
                contour.append((cy, cx))
                found = True
                break
        if not found or (cy, cx) == (start_y, start_x) and len(contour) > 2:
            break

    pts = [(x / w, y / h) for y, x in contour]
    return _simplify(pts, tolerance / max(w, h))


def _simplify(points: list[tuple[float, float]], epsilon: float) -> list[tuple[float, float]]:
    """Douglas-Peucker. A traced boundary is one point per pixel; a drawing is not."""
    if len(points) < 3:
        return points
    pts = np.asarray(points, dtype=np.float64)
    keep = np.zeros(len(pts), dtype=bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        a, b = pts[i], pts[j]
        ab = b - a
        length = float(np.hypot(*ab))
        seg = pts[i + 1:j]
        if length < 1e-12:
            dist = np.hypot(*(seg - a).T)
        else:
            # The 2-D cross product, written out: numpy 2 dropped it from np.cross.
            rel = seg - a
            dist = np.abs(ab[0] * rel[:, 1] - ab[1] * rel[:, 0]) / length
        k = int(dist.argmax())
        if float(dist[k]) > epsilon:
            keep[i + 1 + k] = True
            stack.append((i, i + 1 + k))
            stack.append((i + 1 + k, j))
    return [(float(x), float(y)) for x, y in pts[keep]]


def _with_outlines(img: Image.Image, areas: list[Area], numbers: bool = True) -> Image.Image:
    """Draw every area's outline and number over an image."""
    out = img.convert("RGB").copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    for i, area in enumerate(areas):
        colour = _OUTLINE_COLORS[i % len(_OUTLINE_COLORS)]
        pts = [(x * w, y * h) for x, y in area.outline]
        if len(pts) > 1:
            draw.line(pts + pts[:1], fill=colour, width=2)
        if numbers:
            cx, cy = area.label_at[0] * w, area.label_at[1] * h
            label = str(area.number)
            draw.rectangle([cx - 8, cy - 8, cx + 6 * len(label) + 2, cy + 6],
                           fill=(16, 16, 18))
            draw.text((cx - 5, cy - 7), label, fill=colour)
    return out
