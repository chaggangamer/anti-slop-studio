# Code-rendered video (HTML, Canvas, p5.js, Remotion and similar to MP4)

Contents: when to use it, pipeline, determinism rules, timing, rendering, audio, self-review, shot-sheet discipline, style discipline, studying references, gotchas, limits.

Many agents now make video by writing code that draws every frame, then rendering frames in a headless browser and encoding with ffmpeg. It suits motion graphics, explainers, kinetic type, launch films, lyric videos and stylised animation. It does not produce photoreal people; for that use real footage or a video model, and use code for planning, assembly and editing.

## Pipeline

1. **Brief and direction lock** (`assets/direction-brief.md`).
2. **Storyboard or shot sheet before any code.** Every shot: purpose, duration, what moves, what is read, how it hands off to the next. When music drives the piece, put every timing on the beat grid. Show it, get a yes, then build. The strongest builds in public prompt libraries all plan first; this also lets a single shot be changed later without redoing the film.
3. **Build shot by shot,** one file per scene or chapter, with shared tokens (palette, type, easing) in one place. Independent scenes can be built in parallel by sub-agents when they share a written style guide.
4. **Draft render** at reduced resolution and without motion blur. Review contact sheets.
5. **Fix, then final render,** then audio mix and QA (`scripts/probe_video.py`, `scripts/check_shots.py`, `scripts/check_audio.py`).

Budget for several passes. Single-pass results usually need at least a second iteration.

## Determinism rules

Render workers run in parallel and may restart, so every frame must be reproducible.

- Every visual state is a pure function of time `t` (for example a `seek(t)` function). No CSS transitions or animations, no timers, no state carried from one frame to the next.
- No `Math.random` in the scene. Use a seeded generator so frame 400 looks the same every time.
- No `<video>`, `<audio>`, `<iframe>`, or remote images inside the scene. Pre-extract clips to image sequences and swap sources per frame, waiting for decode.
- Springs as closed-form step responses. When a value changes target many times, sum one spring per change so it stays a pure function of time.
- A loop's last frame must equal its first, including cursor position and speed, or it stutters.

## Timing for the viewer

- Budget reading time per element; text that appears must stay long enough to be read once (see `check_shots.py`).
- One new thing to read at a time. Fast actions, slow meanings: let a simple movement be quick and give the idea behind it time to land.
- Lead the eye: the next element should enter where the viewer is already looking.
- Hold the payoff. The shot that delivers the idea gets the longest hold in the piece.
- Every scene must have something happen in it, and every scene should hand off into the next rather than simply ending.

## Rendering

- Capture frames with headless Chromium (Playwright or Puppeteer) and encode with ffmpeg: H.264, yuv420p, a constant-quality setting around crf 18, faststart. Make rendering resumable by writing frames to disk.
- For smooth UI motion at 60 fps, render a few sub-frames per frame and blend them with ffmpeg `tmix` for real motion blur. Skip blur in drafts.
- Software WebGL is slow; on machines without a GPU, avoid heavy fills (for example large watercolour fills) or lower the resolution for drafts.
- Keep dependencies local and pinned; keep API keys in a `.env` file the agent cannot read back (deny read access to it in the agent's settings).

## Audio in code-rendered video

- Analyse the track for tempo, beat grid and energy per bar, then calibrate the grid against the actual kick hits. Put cuts on downbeats and UI events on beats.
- Place each sound effect so its measured peak, not the file start, lands on the event. Keep effects under the music. Normalise once at the end (target in `voice-sound.md`).
- Use music and effects whose licence allows the intended use, commercial use included, and record the source.
- Generate narration with a TTS service or local model, with the spelling guidance in `hinglish.md` for Hindi or Hinglish scripts.

## Self-review loop

Do not trust the first render. Before the full render:

- Render one frame per beat or per second into a contact sheet and look at it.
- Probe 20 or more frames for overlap, clutter, hard-to-read text and elements off the grid.
- Print the visible text at several timestamps to catch typos and missing lines.
- Check the console for script errors.

After the full render run `python scripts/probe_video.py final.mp4 --contact-sheet sheet.jpg` and look at the sheet, then run the shot-rhythm and audio checks.

## Shot-sheet discipline

A disciplined sheet keeps a generated film from sprawling:

- Shot durations sum exactly to the runtime.
- One hero shot gets the most effort; the other shots are simpler (long holds, fewer drawings, limited animation).
- Animate acting on a slower frame cadence than fast effects; not everything needs full frame rate.
- A closed colour script: only the hex values listed on the sheet may appear.
- Dialogue and on-screen lines are exactly what the brief says, word for word, or absent.

## Style discipline

- Pick a named visual style (paper-craft, ink wash, risograph, blueprint, kinetic type, isometric, pixel and so on) rather than "modern and clean".
- When adapting an existing style, sort each property into safe to change (palette, type, pacing, sound), changes character (materials, rendering, camera grammar) and essence (change it and it is a different style). Change safe things freely, character things deliberately, never essence.
- Render one style frame first and compare it with the reference before building the whole film.

## Studying references

Before designing a promo, study two or three references by measurable facts, not adjectives: duration, cuts per 10 seconds, hook type, text in the first three seconds, structure beats, caption style, music and sound approach, and one line on why it works. `probe_video.py` gives the cut rate and shot lengths. Use this to set targets, then make something with a different idea. Credit creators, never copy their work, and do not redistribute their footage or frames.

## Gotchas

- `will-change` on anything the camera scales makes text render blurry.
- `opacity` or `filter` on a `preserve-3d` element flattens it; fade its wrapper instead.
- Text that swaps inside a morphing container needs its own enter and exit timing or the two overlap.
- Measure element positions at runtime for match cuts rather than hard-coding them.
- Heavy effects (particles, large blurs) make a render slow without making the piece better.
- Expect minutes to an hour per film, and a meaningful number of tokens; estimate for several iterations.

## Limits

Code-rendered video is stylised motion, not live action. When the brief needs photoreal footage, real products or real people, plan for real footage or a video model and keep code for graphics, captions and assembly.

## Sources consulted

Public repositories and prompt libraries on code-drawn video, including a hand-painted animation starter kit with its animation guide, a music-video source repository, an HTML anime shot-sheet harness, a library of film styles drawn in code, a launch-video renderer with a virtual clock, a reel-analysis tool, and community collections of agent video prompts. Techniques are generalised here; none of their assets are included.
