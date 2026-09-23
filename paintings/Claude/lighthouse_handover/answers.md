Here's what I can answer from this session. Where I have no evidence, I say so. I've also
sent the two misfires rebuilt as a small zip (question 5).

1. Default feather: yes for `edge="hard"`, but keep `clip=` hard when it's only
   containing paint.

   - My painting has 33 of these calls:
     - 9 draw an edge: the headland outline, two sea stacks, the cap, the horizon, and
       the tower, lit side and lantern (×2) via clips.
     - 24 only keep paint inside a shape: the rock planes and ledges inside the headland,
       the reflection glazes below the horizon, the door and warm glaze inside the tower.
   - What made the tower and headland look like vector graphics was the clean edge, not
     jaggies. The jaggies are invisible at 1024×768 unless you zoom. So "reads as paint by
     eye" is the right test.
   - A feather that reaches outward would break containment. The planes would leave a
     lighter fringe around the dark headland, which is an outline, mistake #1 in the
     guide. The reflection film would leak above the horizon. Feather inward, or leave
     containment clips hard.
   - The horizon was a deliberate ruled line, so `feather=0` needs to stay available.
   - Whether any of your candidates reads as paint, I can't say. I haven't seen them.

2. Which candidate: I can't choose; I haven't seen A1–A3. Two data points:

   - I built a wandering outline by hand. That's `roughen()` in the prelude (a
     correlated random walk, calmed where the tower stands), plus `blob(wobble=)` for the
     stacks. If A3 existed as a shape option, I'd have used it for rock.
   - The tower, lantern and cap wanted crisp-but-painted edges, not wandering ones. That
     sounds like A2, if A2 is what its name suggests.
   - A1 reading as blur fits my experience: aliasing wasn't the problem, the vector-clean
     edge was.

3. B: fix it in the engine.

   - I used the loads the docs recommend for broken marks (0.35–0.6) and got isolated
     dots, not streaks. That meant dark flecks in the sky, speckled first swells, and blue
     specks in the first surf. It fits "the gate reads the tooth".
   - A notice would only have told me to avoid the mark. I'd still have had no dry-brush
     mark that works. My workaround, glazes for the swells, dropped the texture I wanted.
   - My painting has 16 marks at load < 1 (11 bristle, 5 flat) that would replay
     differently. That's fine: the README pins 0.6.0.

4. Frames out of the file: yes. I exported the GIF once, at the end, and never needed the
   frames while painting. The session file was 16 MB of my 17 MB project download.
   Rebuilding from the log is pixel-exact, which I verified, and took about 35 s here.
   Paying that once for a GIF is fine.

5. Save the check's lines (C0): yes, but it wouldn't have caught mine.

   - Both misfires were printed by rehearsals, which commit nothing. To make misfires
     reconstructable, rehearsal reports need saving too.
   - I rebuilt both from the transcript, and each rerun prints the original line exactly:
     - headland: 42 marks, "19 marks … 0.020 apart … 0.006"
     - water: 19 marks, "7 marks … 0.009 apart … 0.006"
   - In both, the 0.006 brush is a thin dark mark (a crevice, a ripple), and neither
     group was meant as a gradient.

6. Parallel `vary=` panels: I have no evidence on speed, and none on Windows (this ran on
   Linux). What I can offer is a different data point:

   - I never used `vary=`. My variants were whole passes of scumbles, strokes and glazes,
     which as far as I could tell can't go into a plan.
   - Instead I wrote a harness around `s.scratch()`, which took about 15 s per variant,
     run one after another.
   - What would have replaced the harness is rehearsing scripts as side-by-side
     alternatives. `easel run --rehearse a.py b.py` stacks them instead. If D1 is built,
     making a script or function the unit of a panel would cover my case.

7. Documentation weight: agree, watch. This is one data point, from a reader that can
   take in a lot:

   - I read about 180 of the roughly 340 KB before the first mark. I never opened
     CALIBRATION or DIAGNOSIS, and never ran `explain` or `diagnose`; the one-line notices
     were enough.
   - What steered me was the notices at the call, the recipes with `demo`, and the plan's
     `lightest:` line.
   - I read three rules and then broke them anyway: go back to the drawing after two
     failures, no slabs on a hull, no spoon-shaped islands. Looking at rehearsals caught
     those, not reading.
   - The one factual error I found was in prose, the lit-air width sentence.
   - If you ever cut, start with what the notices already say at the call.

8. Version: agree, 0.7.0. Both changes move my painting (the 33 edge/clip calls and the
   16 low-load marks). I'd add a notice when a pre-0.7 session is replayed or rebuilt
   under 0.7, because my README promises a pixel-identical rebuild that relies on the
   0.6.0 pin.

9. Model: `claude-opus-5-5`, at max effort, from this session's metadata. The configured,
   current and last-served model are all `claude-opus-5-5`. A single-turn fallback
   earlier in the session wouldn't show there, so I can't strictly rule one out.
