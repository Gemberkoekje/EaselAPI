# A greenhouse in winter, looking down the aisle at a low sun

A painting made from `PAINTER.md`, with no reference photograph. The subject was
chosen before anything in the repository was read: a small span-roof greenhouse in
winter, late afternoon, looking down the central aisle at the low sun behind the
fogged end wall. Staging down both sides, terracotta pots in a row — most empty or
holding dry stalks, two or three still green — and a galvanised watering can on the
aisle floor. The whole picture is one problem: light passing through glass, through
fog on the glass, through thin leaves, and stopping dead at the clay.

**To understand this, start by reading `prelude.py`** — the perspective helper `P(xm,
hm, dm)` that places every mass in metres, the palette mixed to planned values, each
mass as a function, and the pot/foliage/can recipes. Then the passes in order,
`p0_draw.py` … `p13_last.py`, `p11_sign.py` and `p12_export.py` last.

- Canvas 1024×768, linen, `toned_warm_grey` ground, seed 3.
- **297 strokes** of a 300 budget, plus two signature marks that did not count.
- Final painting: `painting.png`. Time-lapse: `painting.gif`.
- Reproducibility **not verified** from a clean session — the working session was
  built pass by pass with rehearsals, and the two `erase()` calls in `p12_export.py`
  were added after the fact. The scripts are the record of how it was made, not a
  byte-for-byte rebuild.

## No assisted modes

There was no reference, so `prepare`, `sketch`, `ref_shape` and `ref_outline` were not
used and nothing was traced. Every mass is a `polygon`, `ellipse`, `blob`, `Region` or
`s.circle()` built by the one perspective function, looked at in graphite with the grid
before any paint. `preview`, `rehearse` and `cost` were used before every pass.

## The one decision that carried the picture

**A frontal elevation of a greenhouse is a layer cake** — plinth, glass, transom,
eaves, ridge, all horizontal — and the closing checklist warns that no brushwork gets
that back. So the viewpoint is one-point perspective straight down the aisle: the
staging, the aisle, the glazing bars and the rafters all converge on a vanishing point
low and left of centre, and over the sun's third of the picture there is no horizontal
at all. Counting the bands before the first mass and choosing a viewpoint that crosses
them was the whole composition, made in `p0_draw.py` before a stroke was spent.

## The plan, and what it cost

Values were written down first as a `compare({place: value})` sheet in `prelude.py`:
the bloom's core `0.90`, lit end-wall glass `0.75`, right wall `0.58`, under the
staging `0.18`, the aisle `0.31`, the lit bench top `0.62`. Every mixture was made with
`at_value()`. On the finished canvas eight of nine planned places are inside `0.10`;
the ninth is the watering can, which reads `0.37` against a planned `0.46` because the
can turns to shadow on its right and the plan sampled across the whole thing.

The split written before the first stroke, and what was spent:

| Stage | Strokes | Share |
|---|---|---|
| Glass: end wall, side walls, roof wedges | 36 | 12% |
| Light: bloom, dirty lower panes, two warm glazes | 18 | 6% |
| Floor, plinth, the dark under both benches | 29 | 10% |
| Staging: two bench tops, edges, cast shadows | 49 | 16% |
| Glazing bars and rafters | 26 | 9% |
| Pots, left and right, far to near | 110 | 37% |
| Watering can | 10 | 3% |
| Condensation on the glass | 11 | 4% |
| Edges, legs, dead leaves, the finish | 8 | 3% |

The subject — the pots, the can, the light on them, marked `note="subject"` — took
**40%** of the marks against a planned ~30%. The pots began at stroke 132, 44% of the
budget, with the whole greenhouse standing to receive them.

## Rehearsing, and what it saved

Every pass was rehearsed before it was committed; the numbers below were all found on a
throwaway copy and cost nothing.

- **The first fog glass was a cool sage green.** Read against the grey-blue side walls
  it was a green sky, not fog on glass, and the swatch strip in `scratch/swatch1.py`
  showed six warm greys beside it before a mass went down. The end wall became a warm
  buff grey; the beam of warmth then had something cool to be warm against.
- **The bloom is an inward `scumble`, not a disc.** The engine picks the ring brush
  from its own step; ten rings from the wall's own value up to the core lay the sun as
  light on the glass with no edge anywhere.
- **The pots were rebuilt once.** The first recipe used `block_in(edge="clean")` on
  each little body and the contour warning fired on every one — a pot body is too
  narrow for the half-brush inset. The recipe became strokes: one to three vertical
  chisel strokes tapering to the base, a capsule rim closing the silhouette, a darker
  opening, and one tapered arc of light along the near rim. That reads as a backlit
  clay pot and costs about six marks.
- **The dark under the staging spilled up onto the end wall** at first, a sawtooth
  along the bench's far edge. Dropping the mass a hair below the bench top and giving it
  a clean contour stopped it at the wood.
- **The glazing bars were rehearsed as thick dark struts and came back as a cage.**
  Thinned to a few pixels at the end wall, thicker toward the viewer, cooler on the sky
  side and thinned to nothing where they cross the glare, they read as glazing bars.

## What went right

- Back to front throughout: glass, the bloom, the floor and the dark under the benches,
  the staging, then the pots far to near so every overlap is a nearer pot over a further
  one, then the can, then the condensation on the near panes. Every pot edge is where
  its paint stops and the wood or the glass still shows.
- The value structure holds in greyscale: the bloom the lightest thing, the benches and
  far glass the mid, the dark under the staging and the aisle shadow the dark, and the
  lit pot rims and the one highlight on the can the accents.
- The pots are a row of a kind and not a row of copies: no two the same size, some
  empty, one of dry stalks, two still green, one tipped on its side, the near ones with
  a lit sliver down the sun side. One thing varies per pot on purpose.
- The edges vary: the bloom and the drips are soft, the under-bench dark is smudged into
  the aisle along its own line, the pot rims and the bars are hard.

## What still bothers me

- The two green plants are the weakest passage. The last eight strokes broke their
  silhouettes with leaves, dark and lit, poking past the mass, but up close each is
  still more a clot with leaves added than a plant.
- The aisle floor is a large quiet mid-brown with little incident in it. It reads as a
  dim earth floor, which is right, but it is the emptiest sixth of the picture.
- The right bench carries the big pots and the left bench is sparse. The camera stands
  right of centre and the balance holds, but a viewer's eye goes right and stays there.

## The signature

Two short liner strokes meeting at a point, low in the dark under the left staging, a
step lighter than what they sit on: a chevron, which is a vanishing point in miniature.
Every line in this picture was placed by one, so the mark is the thing the picture is
built on, reduced to two strokes. It is not a name and it repairs nothing.
