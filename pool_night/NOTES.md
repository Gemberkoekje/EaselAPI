# A municipal pool at night, lit from underwater

**To understand this, start by reading [`prelude.py`](prelude.py) (the palette and the
four ground masses), then the passes in order `p1_draw.py` … `p30_sign.py`.** Every
pass was rehearsed against a copy before it was committed; the comment at the top of
each says what the rehearsal changed.

Final: **221 of a 300-stroke budget**, 37% of marks noted `subject` against a planned
40%. Output: [`pool_at_night.png`](pool_at_night.png),
[`pool_at_night.gif`](pool_at_night.gif).

## The subject, and why this one

An empty municipal pool at night, lit only from the lamps in its walls. Chosen for
three reasons the engine rewards: one light source and it is *underneath* everything,
so every form is underlit; geometry that is already primitive-shaped (a rectangle of
water, a coping, a ladder, roof members); and a value structure that cannot fail — one
bright plane against near-black.

The composition question came first, before any paint. Square on, this subject is a
layer cake: ceiling / wall / far deck / water / near deck, five horizontal bands. So
the viewpoint is a high corner and the pool is a diamond crossing every band, with the
roof members crossing them again on the other diagonal, a chair crossing them on the
left and a board entering from the right edge.

## Decisions that mattered

- **The deck was repainted early and it saved the picture.** At `0.40` it was the
  second-brightest thing in a night scene, which left the water no range to be dark
  in — the pool read as a flat cyan cut-out. Taking the deck to `0.30` and re-running
  the stack (`p6_redeck.py`) cost 21 strokes and fixed the whole value hierarchy. It
  was cheap because nothing was standing on the deck yet. It would not have been
  later.
- **Measure, don't look.** Twice my eye was simply wrong. The deck "looked" too light
  at 0.40 when it was exactly the 0.39 I had mixed — the contrast against the dark room
  fooled me. Later, `sample()` showed the coping had quietly reached `0.50` against
  water at `0.45–0.55`: the frame around the subject had become as light as the subject.
  Neither was visible by eye; both were obvious in one line of numbers.
- **The water is mostly reflected dark, not lit water.** The version where the whole
  pool was one bright value never read. What made it water was laying the room's
  darkness across it in soft films and letting the lamps come up through the gaps.
- **Two lamps, two methods.** The near lamp is films plus a doubled core plus a fan of
  glazes; the far one is a single film halo and one core, no fan. The recipe repeated
  exactly is what gives you three copies of one object.

## Pitfalls, each of which cost a rehearsal and nothing else

- **`direction` as a sequence is priced at the steepest angle in it.** A list of ten
  varied angles on the room mass cost **51** strokes where `"axis"` cost 4 and
  `"cross"` cost 15. `"cross"` is the affordable way to break a comb.
- **A `flat` steps a diagonal silhouette into a staircase.** The pool's straight edges
  are its whole drawing; `edge="clean"` draws the contour along a shape's *own* edges
  and fixed it. It wants a solid tip and a brush under a quarter of the shorter extent
  — it says so.
- **An inward scumble has a narrow window.** Its brush is `3 × depth / n`, so more rings
  means a *smaller* brush, not finer banding: at n=12 on a patch this shallow the brush
  drops under `0.025` and combs. And a wide value span across 8 rings reads as a contour
  map. Narrow the span, or lay the glow as films instead.
- **A block-in bleeds half a brush past the two edges `direction` does not lengthen.**
  At `size=0.15` that chewed a sawtooth out of the wall above the deck. Dropping the
  floor polygon's top edge `0.055` below the wall base put the bleed *at* the junction
  for the same 11 strokes.
- **Glazes are weak until they are not.** At `opacity` 0.11–0.20 the fan glazes were
  invisible; at 0.30–0.45 they read. But a glaze laid *across* a passage introduces a
  new column — the far-deck repair had to be re-done with films running *along* the
  band instead.
- **`at_value` raises rather than substituting.** Asking for `0.135` from a
  ultramarine/umber mix fails outright: the floor is `0.136`. Better than being handed
  `0.14` silently.
- **Pressure lists on a chisel tip change paint, not width.** Flagged three times by the
  post-pass check before I stopped writing them.
- **The correction that buried something.** The deck glazes in `p18`/`p20`/`p21` ran
  straight over the chair and erased it. Found only by cropping in for the checklist's
  "did a correction bury something?" question. Re-laid in `p22_repair.py` at its own
  depth, a step darker to suit the darker deck it now stands on.
- **One rehearsed pass was dropped entirely.** A glaze to mute a pale streak on the
  deck landed darker than the deck around it and read as a post — worse than the
  blemish. The rehearsal cost a look; committing it would have cost a repaint.

## Stopping

Stopped at 221 of 300 **deliberately**, not by running out of things to do. The last
six passes all went to passages I had named as weak — the far deck, the foreground
water, the near coping, the blotchy lower-right deck, the left deck, the speckle
crowding the near lamp. What remains thin is the dark: the upper-left quarter and the
deck corners. Those are quiet because a night picture needs them quiet, and marks there
would be incident for its own sake.

## The signature

A short horizontal stroke with a single dot beneath it, bottom left, four value steps
above the deck it sits on. A surface, and a light under it — which is the whole picture
in two marks. I chose it because it is the only thing this painting is about, and
because it is a mark rather than a name.

## File map

| File | What it is |
|---|---|
| `prelude.py` | palette, the pool/room/floor geometry, the four ground masses as named functions |
| `p1_draw.py` | the pencil drawing, and the band count |
| `p2_room.py` – `p4_water.py` | room dark, wall glow, deck, water mass |
| `p6_redeck.py` | the value repair: deck down to 0.30, stack re-run |
| `p7_surface.py` – `p9_ripples.py` | the water's reflected darks, the lamps, the ripples |
| `p10_spill.py` – `p12_things.py` | the coping, the roof and caustics, chair/board/ladder/sign |
| `p13_deck.py` – `p15_highlights.py` | deck falloff, lifting the water, the highlights |
| `p16_fardeck.py` – `p21_recede.py` | the weak-passage work, edges, the empty left half |
| `p22_repair.py` – `p29_leftdeck.py` | the buried chair, the far water, the coping, the left deck |
| `p30_sign.py` | the signature |
| `exercises/` | the nine exercises, run before any of the above |
