# Motion and video

Contents: the governing rule, effects to retire, motion grammar, typography in motion, AI footage, vertical framing, rhythm, verification.

## The governing rule

Every movement must belong to an element already on screen and must go somewhere. A burst, glow, flash or shake that is connected to nothing is filler. Before adding an effect, say what it is attached to and what it communicates. If you cannot, cut it.

## Effects to retire by default

These recur in banned lists written by working creators because they are the signature of unexamined AI motion. Retire them unless the brief names them as deliberate choices.

| Effect | Why it reads as AI | Replace with |
|---|---|---|
| Neon or colour glow on text and shapes | Default "premium" gloss | Contrast, scale and a single accent |
| Particle bursts, shockwave rings, sparkles | Motion attached to nothing | A real object reacting to a real event |
| Crossfades between scenes | The default blend | Scenes that grow out of the previous one: match cut, shared shape, continuous move |
| Bouncy or elastic easing everywhere | Spring preset on all | One easing family with a clear speed profile |
| RGB split, camera shake, lens flares, glitch | Instant "energy" | Hold the frame and cut on the sound |
| Grid floors, floating orbs, abstract blobs | Backdrop filler | A real environment or a plain field |
| Same fade-up on every element | One animation reused | Stagger by meaning, different entries for different roles |
| Text in the corners, tiny labels | Template chrome | Fewer words, larger, placed with intent |
| Long holds, frozen frames, dead time | Waiting on the render | Cut earlier or give the held frame a purpose |
| Anything that looks like a template | Presets | Build from the concept, then reuse only the system |

A short banned list per project works best: five to nine items, each with a replacement ("no crossfades: every scene grows out of the one before").

## Motion grammar (decide once per piece)

- **Easing:** one family for the piece, with ease-out for entries and ease-in for exits. Overshoot only as a character decision, applied sparingly.
- **Transitions:** choose a grammar (hard cuts on beats, match cuts, wipes that reveal something) and keep it, with one deliberate break at the turn.
- **Duration:** UI-scale motion in the 150 to 400 ms range; story-scale motion as long as the idea needs. Avoid uniform durations; variation reads as intent.
- **Staging:** one thing moves at a time unless the scene is about chaos. Direct the eye.
- **Loops:** match first and last frames, cursor and type position, so the loop does not stutter.

## Typography in motion

- One typeface family per piece, with real kerning and sensible line breaks; do not rely on a template's default font.
- Give each word or line enough time to be read. As a rule of thumb, allow roughly a quarter second per word plus a short settle, more for unfamiliar words or Devanagari. `check_shots.py` flags lines that outrun this.
- Keep captions and key content out of the platform UI zones. On a 1080x1920 frame, keep clear of roughly the top 12 percent and bottom 20 percent, and verify against each platform.
- Kinetic type that is one word per beat should land on audible beats, with the emphasis word carrying the meaning, not the loudest effect.

## AI-generated footage

- Lock look and characters first in stills (a casting sheet and a style reference), then generate image-to-video from those frames. Pure text-to-video across shots is gambling on continuity.
- Plan the edit before generating: for each shot, the message, the visual purpose, shot size, movement, duration, continuity reference, and safe area for type.
- Use generated footage for mood, scenario and metaphor. Use real footage, real screens and real assets for evidence.
- Fix or replace: crop, retime, track over, or rebuild anything with warped hands, drifting faces, garbled text or impossible physics. If a shot cannot be made consistent, change strategy (closer crop, hands or environment instead of the face, a designed graphic panel, a static frame with subtle movement).
- Keep or cut: a generated shot stays only if it helps the viewer. Cut shots that repeat the narration, show an artifact, or exist because they were hard to generate.
- Nothing is happening is the loudest slop tell. Give every shot a stake, an action or a change.

## Rhythm

- Vary shot length deliberately; a metronome edit (every shot the same length) is a fingerprint. Let some shots breathe and some snap.
- Cut on sound or action, not on a fixed grid. Not every beat needs a cut.
- Hold the first frame long enough to register, but start on something already in motion or in tension.
- Put the longest hold on the line that matters most.

## Verification

- `python scripts/lint_visuals.py animation.html` checks CSS and JS motion code for glow, bounce easing, particles, repeated presets and similar.
- `python scripts/check_shots.py shots.json --format reel` checks shot rhythm, transition variety, text readability and the opening.
- Render one frame per beat and check pacing before the full export.
- Watch at full size, at thumbnail size, with sound off, and with eyes closed.
