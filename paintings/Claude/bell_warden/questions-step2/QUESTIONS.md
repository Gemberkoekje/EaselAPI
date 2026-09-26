# Four questions, a follow-up, and one the bench raised

Every picture here was made by your own passes, rebuilt through the code `easel run` uses,
in the order your saved reports record -- or by your versions, recovered from your session,
laid on the canvas you rehearsed them on. Each candidate was patched into the engine for
one bench and taken out again. The plan's numbering is kept: these are questions 4, 9 and
10 of the ten it put to you, and a follow-up to your answer to 5.

---

## Part 1 -- blind: `blind/` and nothing else

### 4a. At which size does an arrangement read?

You asked for *a free silhouette and value thumbnail at drawing time -- the painter's classic
notan*, and said *the cat ears would have been obvious before a single rehearsal*. Here is
the candidate: every mass a pass laid, filled flat at the value its colour was mixed to, in
the order you laid them, on the ground's value -- no paint, no brush, no light -- drawn at
the canvas's size and brought down the way a look is. It costs 14 to 36 ms and nothing
against the budget.

Four of your arrangements, each at four sizes, **lettered W to Z in the same order on
every sheet** (a letter is one size, whatever the sheet):

| sheet | the arrangement |
|---|---|
| `q4_cat.png` | your first typed silhouette and its lit planes (`p04_v1_cat.py`) |
| `q4_piebald.png` | the redrawn profile with its planes laid as tiles (`p04_v2_piebald.py`) |
| `q4_arch.png` | one lit side joined to the shade (`p04_v3_arch.py`) |
| `q4_final.png` | the committed pass, with the details pass's masses on it |

**For each sheet: at which letters can you see what the arrangement reads as -- the ears,
the islands, the band -- and at which can you not?** Then: which letter would you want a
thumbnail drawn at if you gave no size?

### 4b. Which drawing would you judge a silhouette on?

Your second drawing -- the one after the room and the plinth -- was drawn with `guide()`
over the paint, and you judged it on a throwaway canvas with a light ground instead, because
on the real one you could not see it. Four ways of drawing the same guides, **lettered E to
H in the same order on both sheets**, at the look's own pixels:

| sheet | under the drawing |
|---|---|
| `q4_guides_bell_after_room.png` | your canvas after the room, where the second drawing went |
| `q4_guides_mid_grey.png` | a flat mid-grey canvas, where a line of two tones could hide what it is drawn over |

**Rank E to H, the one you would judge a silhouette on first.** Does any of them shout over
the picture so that you would switch it off to look at the paint?

### 9a. Which reads as a form turning in stone?

Your subject's pass, `p04_gargoyle.py`, laid seven ways on the canvas it opened on: the
same masses, the same copies of the silhouette shifted away from the light, the same
budget within ten strokes. **Lettered A to G in the same order on every sheet.**

| sheet | what it is |
|---|---|
| `q9_whole_1024x768.png` | the creature, at the painting's size, 1:1 |
| `q9_chest_1024x768.png` | the neck and chest, enlarged twice |
| `q9_whole_1440x960.png`, `q9_chest_1440x960.png` | the same passes rebuilt at 1440x960 |

**Rank A to G, most like carved stone turning away from a lamp to least.** Which read as a
cut-out? Which read as damaged, speckled or smeared?

### 10a. Two versions of your painting

`q10_P.png` and `q10_Q.png` are your painting rebuilt from your passes twice. One of them
is your painting; the other lays every colour darker than `0.20` further down, so that
what landed at the box's floor lands at `0.07` instead -- what a darker dark in the box
would have let you lay.

**Which reads more as the picture you meant -- a stone figure in a dark undercroft,
low-key by design?** And in which do the room's darks -- the wall, the floor, the pillar,
the plinth's shadow side -- read as more than one mass?

**Write Part 1's answers in `answers-step2.md` now, then open `KEY.md`.**

---

## Part 2 -- open: `KEY.md`, `labelled/`, `numbers/`

### 4c. The thumbnail's signature

The candidate is `s.thumbnail({place: value, ...}, size=None, path=None)`: places as
`plan()` reads them, each at a value or at a colour's value (a slot like `"stone_mid"`),
in the order they would be painted, later over earlier. **With no argument it draws the
plan's own places** -- and for your painting that is `labelled/thumbnail_plan_128.png`:
the room, the plinth's planes and the head's top, and no creature, because your plan named
no mass of it. Is the signature right? Should no argument draw something else -- the
masses the painting has laid so far, say, which the log knows? And should a clip be a place
too (`{rim: 0.36}` held to the body), the way your committed copies were?

### 4d. The drawing over the thumbnail, and the drawing alone

`labelled/thumbnail_final_256_guides.png` is your final arrangement at 256 px with your
drawing over it, in the cased line. Would you want the drawing drawn over a thumbnail, or
never? And with guides that read on any ground -- your pick in 4b -- would you still have
wanted **a look of the drawing alone, on a plain light ground, at full size**: your
throwaway canvas as a flag?

### 9b. The terminator, by name

Now that you know the letters: which candidate would you have painted your creature with,
and what should the recipe for a silhouette lit from one side say? The bench's numbers are
in `KEY.md`. In short: a join along each terminator widens the step there from under a pixel
to about ten while the silhouette stays a step; a feather does not widen a terminator until
`0.03`, and there it speckles every held edge, the silhouette's included. And the plan
proposes to say, beside `feather=`, that **a feather breaks a held edge against the tooth;
it does not soften one**. Is that the sentence you would have needed?

### 10b. A darker dark

Your cast shadow wanted `0.13`; burnt umber alone reaches `0.128`. Knowing what Q is, had
the box held a dark at `0.07`, would you have used it -- and where? The plan does not
propose a black this round; if it ever does, it proposes a dark with a hue, a deeper
masstone of one the box has, rather than a neutral tube black. Say if that is wrong.

### D. The marks that landed nothing

You asked for *a fact at the call for any mark that lands far short of its own value,
whatever the cause, saying the cause the engine can see*. The bench measured every mark
laid by hand over the corpus, and it splits in two:

- **A mark that lands short** has no gap to put a threshold in: how far a mark gets toward
  its value runs smoothly from nought up, and a fact under any share of the way would speak
  on 14% to 39% of the corpus's passes -- mostly on dry-brush strokes and translucent ones
  that land short on purpose. It is not proposed.
- **A round dab that lands nothing is a cliff in pixels**: a one-touch dab lays nothing
  under about 6.5 px, a two-touch under 5.6, a three-touch under 2 or 3, whatever the
  canvas size. 56 of the corpus's 57 round dabs that laid nothing were under their cliff,
  on 11 passes of 341, and your spark is one. The plan now proposes this one as a fact at
  the call: *this dab laid no paint: a round tip at press=1 lays none under about 6.5 px
  -- press=3, or size over 0.0065*.

What is left is the rest of the marks that laid nothing -- a starved bristle mostly, as the
second painting's flour was, eight strokes that laid nothing and on 33 corpus passes in all.
Too many for a fact at the call by the plan's own measure, but each one a mark that laid
nothing. **Should the post-pass check name them** -- a line printed only when a pass laid
one, saying which marks, at which lines, and why the engine thinks they landed nothing? Or is
the dearest line's *N landing nothing* per call, and `easel log`, enough? (Over the guide's
own code blocks such a line would speak once, on the dry-brush stroke of *A mass built of
planes*, which lays nothing at the check's small canvas -- a recipe to fix.) Your ember is the
case neither catches: it landed, `1.6` units, and read a tenth of its way -- which is what a
two-touch dab does at any size, as `dab()` says.

### 5f. Your answer to question 5, once more

You chose the median, one reading for `plan:` and `lightest:`. The second painting of the
round, a lantern by a face, is the median's own failure: the lantern's iron is most of its
place, so it reads `0.491` by its mean and `0.506` by its median against a plan of `0.76`,
and only the top of it -- `0.58` at its 90th percentile, `0.71` at its brightest -- finds the
lit panes. Its painter answered that its plan was wrong -- it should have planned the panes,
and the face -- and that if `lightest:` reads a light by its brightest part, it should read
the 95th percentile inside the place and print it beside the whole: *lantern 0.49 as a
place, 0.59 at its brightest twentieth*. **For a light whose lit part is under a tenth of its
place, would you keep the median for `lightest:` too?** Your own head's top reads `0.606`
by its median, `0.626` at its 90th percentile and `0.63` at its 95th: under either it is the
lightest of your seven places.
