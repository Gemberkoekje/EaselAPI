# Recipes: the calls, in order, for things that have caught a painter out

[`PAINTER.md`](PAINTER.md) is strong on what not to do. This file is the other half:
what to lay *instead*, as the actual calls, for the kinds of thing three painters had
to find by rehearsing. Ten of one painting's eighteen rehearsals went on discovering
six of the recipes below.

**Read a recipe when you are about to paint one of these, not before.** It is not a
reading document and there is nothing here you need in your head.

Each one gives the calls, what it looks like when it goes wrong — which is how you
will recognise that you have made the mistake rather than the recipe — and, where a
painter recorded it, how many rehearsals it took to find. **Every recipe is a recipe
that worked once.** None has been re-measured on a second picture, and any of them is
worth abandoning the moment the look says so.

Nothing here names a subject. That is deliberate: a recipe that says what a thing is
*of* gets painted as that thing, and the name then does the choosing. So every heading
below says what the paint *does*. These are shapes of paint, and you decide what they
are shapes of.

| | |
|---|---|
| **Surfaces** | [a plane that is a plane](#a-plane-that-is-a-plane) · [a form that turns](#a-form-that-turns) · [a mass built of planes](#a-mass-built-of-planes) |
| **Light** | [a passage light in the middle](#a-passage-light-in-the-middle) · [a passage brightening toward one side](#a-passage-brightening-toward-one-side) · [a quiet gradient](#a-quiet-gradient) |
| **Marks** | [a small irregular bright mark](#a-small-irregular-bright-mark) · [a small round thing](#a-small-round-thing) · [a tapered arc](#a-tapered-arc) · [the one ruled line](#the-one-ruled-line) |
| **Edges** | [an edge that is actually lost](#an-edge-that-is-actually-lost) · [a mark that crosses a boundary](#a-mark-that-crosses-a-boundary) |
| **Order** | [a hollow thing](#a-hollow-thing) · [a repair under things that are standing on it](#a-repair-under-things-that-are-standing-on-it) |

---

## A plane that is a plane

A flat surface, facing one way, taking one light. The commonest mass in any picture
and the one most often laid by accident at the wrong settings.

```python
s.block_in(span("C4", "F6"), "flat", "mid", size=0.05, density=1.0,
           solid=True, opacity=1.0, pressure="even", direction="axis")
```

Four clauses and each one earns its place: `solid=True` so no pass runs dry along its
length, `opacity=1.0` so the overlapping dabs do not accumulate unevenly, `even`
pressure because a taper puts a light end on every pass, and `direction="axis"` so the
passes run the way the plane runs rather than the way the canvas does.

**Goes wrong as:** a mottled field with the ground showing through in flecks — that is
`density=1.0` without `solid=True`, which spaces the passes rather than filling them.
Or as faint horizontal striping, which is the pass structure itself: it sits at about
`0.03` of value whatever you do to `opacity`, so hide it with a **bigger brush or a
`bristle`**, never with an argument.

---

## A form that turns

A mass that is round rather than flat — the thing a value ramp across its width does
not give you. Three marks: the mass, the lit side, and the join.

```python
form = polygon([(0.30, 0.72), (0.44, 0.72), (0.42, 0.24), (0.32, 0.24)])
lit  = polygon([(0.36, 0.72), (0.44, 0.72), (0.42, 0.24), (0.37, 0.24)])

s.block_in(form, "flat", "shadow", size=0.02, density=1.0, solid=True,
           direction=90, edge="clean")                         # the whole mass, dark
s.block_in(lit, "flat", "light", size=0.016, density=1.0, solid=True,
           direction=90, opacity=1.0, pressure="even")         # the lit side, on it
s.stroke([(0.362, 0.71), (0.366, 0.46), (0.370, 0.25)], "flat",
         s.palette.mix("shadow", "light", 0.5),
         size=0.012, opacity=0.6, load=1.0, load_falloff=0.0,
         pressure="even")                                      # the join, half strength
```

The mass goes down solid in the **shadow** colour, not the mid, and the lit side is a
second *shape laid on it* rather than a value change inside it. The single
half-strength stroke down the join is what turns the form: without it the two shapes
meet at a step, and that step is the whole difference between a cylinder and two
stripes. Keep the lit shape's edge off the silhouette on the lit side by a hair, so the
dark mass reads round the whole thing.

**Goes wrong as:** two flat stripes side by side (no join stroke); or as a flat field,
which is what a pass ramp across the whole width gives you — one painter rehearsed that
twice, got something nearly flat both times, and once got the light on the wrong side
because the first pass of a stack is not where reading the call suggests
([`REFERENCE.md`](REFERENCE.md) has which side).

*Found in three rehearsals.*

---

## A mass built of planes

A big irregular solid thing with structure in it. The instinct is to lay the mass and
then put marks *on* it. That reads as things stuck to a smooth hull every time.

**A mass like this is not a mass with facets. It is the planes it is made of**, tiling
it, each one a shape at one value, with the block-in's dark left showing as the shadow
between them.

```python
whole = polygon([(0.05, 0.60), (0.22, 0.56), (0.40, 0.64), (0.52, 0.74),
                 (0.58, 0.92), (0.10, 0.92)])
faces = [(polygon([(0.06, 0.61), (0.24, 0.58), (0.38, 0.65), (0.30, 0.70),
                   (0.12, 0.66)]), "pale", 0.014),      # the plane facing the light
         (polygon([(0.40, 0.67), (0.52, 0.76), (0.56, 0.90), (0.42, 0.86)]),
          "mid", 0.016),                                # the plane facing sideways
         (polygon([(0.10, 0.70), (0.34, 0.74), (0.40, 0.88), (0.14, 0.90)]),
          "cool", 0.02)]                                # the body between them

s.block_in(whole, "flat", "dark", size=0.06, density=1.0, solid=True,
           direction="axis", edge="clean")
for face, colour, size in faces:
    s.block_in(face, "flat", colour, size=size, density=1.0, solid=True,
               direction="axis", opacity=1.0, pressure="even")
s.stroke([(0.27, 0.66), (0.32, 0.71), (0.40, 0.77)], "round_hard", "dark",
         size=0.014, opacity=0.9, pressure="taper")            # one crevice
s.stroke([(0.14, 0.72), (0.26, 0.76)], "bristle", "pale",
         size=0.03, load=0.35, opacity=0.6)                    # dry brush, for surface
```

Three or four planes is enough; the planes are what carry the form and the crevices are
punctuation. Keep each plane a brush's half-width inside the silhouette so nothing
fringes past it, and give the planes different brush sizes — they are different sizes
of thing.

**Goes wrong as:** slabs stuck on a smooth shape (planes laid as marks rather than as
tiles), or as a woven surface (bristle streaks used instead of planes). One painter got
both, in that order, before laying it this way.

*Found in three rehearsals.*

---

## A passage light in the middle

A glow, a bloom, light falling on a surface. It is dark at **every** edge, which is
what makes it not a gradient.

```python
s.scumble(patch, "shadow", "light", 8, direction="inward")     # 8 strokes
```

`direction="inward"` lays the passes *round* the place, the first along its boundary
and each one after it a part-brush further in, so the colour arrives from the edge to
the centre. **Leave `size` off.** The rings step `depth / n` apart and the brush has to
be under about three of those steps or the last rings bury the first; with no `size=`
the verb picks `3 × depth / n` itself, and warns when you hand it a wider one.

Give the first ring the value the patch **meets its surroundings at** — the ring lands
*on* the boundary, so anything darker draws a rim round your glow and melts nothing.

**Goes wrong as:** a solid disc with a thin ramp round it (brush too wide — a preset's
own default is about five ring steps on a patch this size); as a daisy (strokes
radiating out from a shared centre, which is the obvious hand-rolled answer and draws
petals); or as a rim with nothing in the middle (first ring darker than what it sits in).

*Found in three rehearsals in one painting and four in another; it is the single most
rehearsed thing in the repository.*

---

## A passage brightening toward one side

Not a glow and not a band between two masses — a whole area that simply gets lighter
toward one edge, with nothing in it having an outline.

```python
for i in range(6):
    t = i / 5
    y = 0.44 + t * 0.14
    s.stroke([(0.22 + 0.08 * t, y + 0.006), (0.60, y - 0.004), (1.06, y)],
             "flat", s.palette.mix("shadow", "light", t),
             size=0.085, opacity=0.5, load=1.0, load_falloff=0.0,
             pressure=[0.0, 0.55, 1.0])
```

Every pass runs the **same** way, one value step apart, each landing at no pressure on
one side and full pressure on the other — so the passage brightens without any pass
having a visible end. The ends run off the canvas on purpose. A pressure list is read
in canvas order on a `block_in`, a `scumble` and a `sweep` too, so the same thing works
as one call where a shape suits it better than six strokes.

**Goes wrong as:** a stack of bars, which is what a `scumble` gives you here if the
passes are too few or the brush too narrow to overlap; or as a passage that brightens
in stripes, which is a pressure list on passes that alternate direction — that is
fixed, but any pass you write by hand still runs the way you wrote it.

---

## A quiet gradient

There is no gradient tool and you should stop looking for one. What closes a join
between two values is many overlapping strokes at closely spaced values.

```python
s.scumble(span("A4", "H6"), "shadow", "light", 8)      # 8 strokes, and it costs 8
```

Eight passes along the band, stepping across it, one value step per pass. Below about
five passes the steps read as steps again. The overlap is the whole mechanism: the
brush is wider than the step between passes.

**Do not reach for a second smudge instead.** Measured on a hard join, the bare step is
`0.330`, one smudge pass takes it to `0.184`, and three passes take it back to `0.280`
— so a smudge removes about 40% of a step exactly once, and doing it again undoes most
of the first pass and leaves a thumbprint besides. When once is not enough the answer
is paint.

---

## A small irregular bright mark

Something small, light and not a shape: a catch of light, a clot, a fleck of something.
Wanted about fifteen times in one painting, and got wrong twice before it came out.

```python
s.stroke([(0.19, 0.26), (0.27, 0.31), (0.34, 0.30)], "bristle", "pale",
         size=0.048, load=0.75, opacity=0.75, pressure="swell")   # a smear with a bend
s.dab(0.42, 0.36, "round_hard", "pale", size=0.016, press=3, tip_wobble=0.7)
```

Two answers, and they are for different marks. **Give it a length and a bend** — a
short smear from a starved brush, which has a silhouette because the comb is redrawn
per stroke. Or, if it really is one small mark in one place, `tip_wobble=0.7` on a
round tip, which draws the tip's outline afresh for every mark: two `round_hard` dabs
share 97% of their silhouette at `0` and 76% at `0.7`.

**Goes wrong as:** a row of floating discs. Measured, five small `round_hard` dabs are
five copies of one disc to within 7% — a disc is not a figure of speech here, it is the
tip printing itself. The `bristle` is the only tip in the box that does not repeat
itself, at 26% shared silhouette, because its comb is drawn per stroke.

---

## A small round thing

Sometimes the thing **is** a disc, and the guide's warning against discs reads as if it
never is. A light in the distance, a catchlight, a berry, a stud: lay it as a disc and
stop.

```python
s.dab(0.62, 0.35, "round_hard", "pale", size=0.012, press=3)
```

`press=3` stamps the same spot three times with the middle stamp at full pressure, and
it is **one** mark against your budget. Use it for anything you actually want to land:
`press=1` and `press=2` are whispers, and a dark accent at `press=2` on a lit passage
did not register at all.

**Goes wrong as:** several of them. One disc is a thing; five discs are the brush. If
you want five, vary at least one thing per mark, or use the recipe above.

---

## A tapered arc

A curve that thins to nothing at both ends: a rim of light along something round, a
sliver of one thing showing past another. One stroke.

```python
import math
cx, cy, r = 0.72, 0.22, 0.05
arc = [(cx + r * math.cos(math.radians(a)),
        cy + r * s.aspect * math.sin(math.radians(a)))
       for a in (-62, -20, 30, 80, 122)]
s.stroke(arc, "round_hard", "pale", size=0.011, opacity=0.95,
         load=1.0, load_falloff=0.0, pressure=[0.05, 0.6, 1.0, 0.6, 0.05])
```

The pressure list is the recipe: a round tip's width follows pressure, so the horns
thin to a point and the middle is the width you asked for. `s.aspect` in the `y` term
is what keeps the arc circular on a canvas that is not square.

**Goes wrong as:** a ghost. The obvious construction — a disc with a second disc in the
background's colour bitten out of it — leaves the bitten edge visible as a seam,
because the second disc is paint and not an eraser.

---

## The one ruled line

Almost nothing in a painting should be perfectly straight, and the checklist asks you
about it. There are one or two exceptions, and when you want one you have to ask,
because every brush here wanders by default.

```python
s.stroke([(-0.05, 0.59), (1.05, 0.59)], "flat", "mid", size=0.026,
         opacity=0.9, load=1.0, load_falloff=0.0,
         jitter=0.0, size_jitter=0.0, pressure="even")
```

`jitter=0, size_jitter=0` is the ruled line. It has a middle setting too, which is
usually what you actually want: the default `jitter=0.02, size_jitter=0.06` wanders
about `1.2` px on a `size=0.1` `flat`, halving both halves the wander, and zero is
ruled. If a long edge is coming out scalloped, the halved setting is the one to try
before the ruled one.

**Goes wrong as:** a mechanical line in a painting that has none — which is the
checklist's question, and the reason this recipe carries a warning rather than a
recommendation. Run the ends off the canvas so it has no visible termination.

---

## An edge that is actually lost

A lost edge is one where two masses meet with **no boundary at all** for a stretch. Not
a soft edge; an absent one. It is the step that separates a painting from a diagram,
and the one most often done by halves.

```python
s.smudge([(0.30, 0.40), (0.45, 0.45), (0.60, 0.53), (0.73, 0.63)])
s.smudge(mass)                                       # or hand it the mass's own outline
s.stroke([(0.42, 0.30), (0.47, 0.35), (0.45, 0.43)], "bristle", "mid",
         size=0.028, load=0.60, opacity=0.55, pressure="taper")   # then paint across it
```

Run the smudge **along** the boundary, and *along* means along the boundary's own
shape — only a straight boundary is two points. Hand it the curve, or hand it the mass
and it walks that outline itself. One pass, never two. Then, if the boundary is still
there, **lay paint across it** in a value between the two masses, at a low opacity with
a starved brush: that is what actually loses an edge. The smudge softens; the paint is
what removes.

**Goes wrong as:** two edges that are *nearly* lost and read as neither — the commonest
outcome, and one painter's own verdict on its picture. Lose one edge completely rather
than four edges partly.

---

## A mark that crosses a boundary

When a smudge is not the answer, which is most of the time.

```python
s.stroke([(0.15, 0.32), (0.23, 0.36), (0.29, 0.33)], "bristle", "pale",
         size=0.036, load=0.55, opacity=0.50, pressure="swell")
```

A broken mark in a value between the two masses, laid *across* where they meet, with a
starved brush at half opacity so it is a suggestion rather than a third mass. Two or
three of them, no two alike.

**Goes wrong as:** a finger-shaped lobe of the lighter mass dragged into the darker
one. That is a smudge run across a boundary instead of along it, and it is the
expensive kind of damage: burying a thumbprint means repainting the mass it sits on,
which buries everything else standing there. Three separate painters made this one.

---

## A hollow thing

Anything you can see into is three masses at three depths, and the order is the whole
recipe: **the far edge, then what is inside, then the near edge.** This one lives in
[`PAINTER.md`](PAINTER.md) at step 2, because it is part of depth order rather than a
procedure — go and read it there. What belongs here is the mark that finishes it:

```python
s.stroke([(0.16, 0.81), (0.25, 0.74), (0.38, 0.71)], "round_hard", "pale",
         size=0.0085, opacity=0.95, pressure=[0.15, 1.0, 0.35])
```

**One broken catch-light along the near edge is what makes a hollow thing read as
hollow**, and it should be the only mark on it. Partial, off-centre, and let the rest
of the near edge stay lost into whatever is behind it.

---

## A repair under things that are standing on it

Repainting a mass buries every fine mark on it, and those are the expensive ones. The
only approach that has worked across six sessions is not a mark at all, it is how you
write your passes:

```python
def far_mass():  s.block_in("upper-half", "flat", "shadow", size=0.16)
def near_mass(): s.block_in(span("A4", "H6"), "flat", "mid", size=0.14)
def details():   s.stroke(path, "round_hard", "light", size=0.02)

for layer in (far_mass, near_mass, details):     # fix one, re-run all of them
    layer()
```

**Keep every mass and every near thing in its own named function, in a `prelude.py`
beside the session, and re-run the whole stack in depth order.** The repair goes in at
its own depth and the near things go back on top of it, because they were never a
one-off. That is what back-to-front costs at repair time, and it is cheaper than the
alternative the second time you need it.

For a repair with nothing standing on it, `s.cover(place, color)` is the whole burying
recipe already mixed — see *When something is wrong, paint over it* in
[`PAINTER.md`](PAINTER.md).

---

## Where these came from

Every recipe above was taken out of a pass script of a painting in
[`paintings/`](paintings), along with the painter's own note on what it replaced. Those
scripts are the fuller version of this file: the calls in the order they were actually
made, with the rehearsals that failed described in the comments above each pass.

**They name their subjects, so the decide-first rule applies to them and not to this
file.** If you chose what to paint before opening this repository, go and read them. If
you have not chosen yet, do not — a named subject chooses for you.

And the standing caveat, which matters more here than anywhere else in the
documentation: a recipe is a thing that worked once, on one picture, for one painter.
The engine has a checklist question about mechanical repetition and **a recipe repeated
across three similar things is exactly that fault one level up.** Vary one thing per
object on purpose.
