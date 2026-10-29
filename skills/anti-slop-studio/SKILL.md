---
name: anti-slop-studio
description: "Production-house quality control for anything AI helps make, so it does not look or sound generic, templated or AI-written: briefs, concepts, scripts, captions, ad copy, voiceover, reels, promo videos, code-rendered motion graphics, thumbnails, landing pages and UI, in English or Hinglish. Use when the user wants work that avoids AI slop, asks to review, rewrite, storyboard, script, design, edit or QA creative output, says something feels generic, samey, robotic or like a template, or wants a promo, ad, reel, trailer or campaign that stands out, even without saying slop. Runs a decide-first workflow plus scanners for text, design and motion code, shot rhythm, finished video and audio. Not for fact-checking, code review, or detecting or hiding AI authorship."
license: MIT
compatibility: "Any agent that reads Agent Skills (SKILL.md). Scripts use Python 3.8+ standard library only; probe_video.py and check_audio.py also need ffmpeg and ffprobe on PATH. No network access needed."
metadata:
  version: "1.3.0"
---

# Anti-Slop Studio

Slop is the statistical average shipped because nobody decided anything. A model fills every undecided choice with the most probable one, and the sum of those choices is the look and sound people now recognise in a second. This skill makes the decisions first, replaces generic with specific and real, then checks the result with scripts and with taste.

## Principles

1. **Slop is a missing decision.** Every tell traces back to a choice nobody made. Fix the cause (decide), not only the symptom (delete the em dash).
2. **Density, not single hits.** One em dash, one "robust", one glow is style. Several stacked in one paragraph or one frame is the fingerprint. Judge clusters.
3. **Shape outlasts vocabulary.** Word lists age as models change. Structural habits last: symmetrical contrasts, lists of exactly three, even rhythm, restating the question, motion that belongs to nothing.
4. **Real beats generated.** Real numbers, names, footage, screens and voices. Generated text, logos, UI, charts and packaging get rebuilt as real type, vector and data.
5. **Guidance alone can backfire.** "Be distinctive" often makes a model add more, and more is slop. Every rule needs a check, so run the scripts.
6. **Subtract first.** Most slop is extra: openers, closers, hedges, effects, transitions. Delete before rewriting.
7. **Quality, not disguise.** This skill raises craft. Do not use it to hide AI involvement where disclosure is expected or required.

## Pipeline

| Stage | Question it answers | Read | Run |
|---|---|---|---|
| 0 Brief | Who, what one idea, what proof, what action | `assets/direction-brief.md` | |
| 1 Concept | Is this idea rooted in something true and specific | `references/concept-and-script.md` | |
| 2 Script and copy | Does every line carry information | `references/writing.md`, `references/hinglish.md` | `scripts/slop_scan.py` |
| 3 Visual | Is there one committed direction | `references/visual-design.md` | `scripts/lint_visuals.py` |
| 4 Motion | Does every movement belong to something and go somewhere | `references/motion-video.md`, `references/code-rendered-video.md` (when video is drawn in code) | `scripts/lint_visuals.py`, `scripts/check_shots.py` |
| 5 Voice and sound | Is delivery directed and the mix intentional | `references/voice-sound.md` | `scripts/check_audio.py` |
| 6 Edit and QA | Does it survive sound off, thumbnail size, and a second watch | `references/edit-and-qa.md` | `scripts/probe_video.py` plus all of the above |

Read only the references the task touches. A caption fix needs `writing.md`. A promo reel needs most of them.

## Workflow

### Step 1. Lock the direction before generating anything

Fill `assets/direction-brief.md`. If the user gave little, state the assumptions in one line and continue; do not interrogate. The brief decides: the one idea, the proof, the language register, one named visual direction, motion grammar, sound policy, and what is banned for this piece.

If the user supplied a style (a reference reel, a brand look, a requested effect such as glowing type), that is a decision, not a default. Log it under "Deliberate exceptions" so the checks do not fight it. A deliberate glow is craft; an unexamined glow is slop.

For campaigns with many pieces, reuse the visual system but make each concept clearly different in story, visual world, pacing, soundtrack and outro. Fill the sameness check in the brief and compare pieces against each other.

### Step 2. Produce with the relevant reference

Write or build using the matching reference file. Prefer a specific detail (a name, number, place, constraint, object) over a polished abstraction every time.

### Step 3. Gate with scripts

Run the scanners that fit the work, fix what they flag, and rerun until clean.

```bash
python scripts/slop_scan.py draft.md                    # prose, English and Hinglish
python scripts/lint_visuals.py index.html --with-copy   # design, motion code, visible copy
python scripts/check_shots.py shots.json --format reel  # edit rhythm and text readability
python scripts/probe_video.py final.mp4 --contact-sheet sheet.jpg --shots-out shots.json
python scripts/check_audio.py final.mp4 --target -14    # loudness, peaks, dead air
```

Script paths are relative to this skill's folder. Use `python`, `python3` or `py` depending on the machine. The scripts need only the Python standard library; the two video and audio scripts also need `ffmpeg` and `ffprobe`. `probe_video.py` can turn a finished video into the `shots.json` that `check_shots.py` reads, so the edit can be checked after the fact. Look at the contact sheet it writes.

Every script has `--help`, runs without prompts, prints findings with line numbers, and exits 0 (clean), 1 (findings), 2 (usage error). Suppress a deliberate choice with `--allow ID` or a `slop-ok: reason` comment on that line, and record it in the brief.

A clean scan proves the known tells are gone. It does not prove the work is good. Scripts cannot see a paragraph that sounds deep and says nothing, a concept that is merely competent, or a transition that is technically fine and emotionally dead.

### Step 4. Taste pass (the ceiling)

Run these on the actual output, not the plan:

- **One-sentence test.** Say the idea in one sentence without "and". If you cannot, there are two ideas.
- **Swap test.** Replace the client name with a competitor's. If it still works, it is generic.
- **Mute test.** Watch with sound off. Does the story still land? Then listen with eyes closed. Does the sound carry its own weight?
- **Thumbnail and squint test.** Shrink to thumbnail size. Is there one focal point and a hierarchy that survives blur?
- **Three-second test.** Would a stranger stay past second three, and why?
- **Specificity test.** Every claim should carry a number, a name, or an image. Otherwise cut or sharpen it.
- **Second-watch test.** Is there something new on the second viewing, or was the first pass all there was?

### Step 5. Report briefly

Say what changed, what is still weak, and what needs a human eye (native-speaker check for Hinglish, real footage for proof). Never present a scanner score as proof of quality.

## Your own tics

When writing user-facing copy, notice your own habits: bold-labelled bullets, tidy closing one-liners, "not X but Y" while explaining why "not X but Y" is bad. Run `slop_scan.py` on copy before delivering it, and delete before you rewrite.

## When rules conflict with a request

The user's explicit direction wins over any default in this skill. Record it as a deliberate exception and make it excellent. When two pieces in a campaign must look different from each other, vary the concept first, then the visual world; keep the typography system only if the user asked for it.

## Gotchas

- A clean scan is not a good piece. Never report a score as proof of quality.
- Hinglish rules are craft heuristics. Have a native speaker of the audience read important lines.
- `probe_video.py` finds cuts by scene detection. Dissolves and busy footage can be mis-counted, and cuts between dark scenes with small text can be missed at the default threshold. Try `--threshold 0.04` or `--sweep`, and trust the contact sheet over the number.
- Do not invent testimonials, statistics, prices, client names or contact details. Mark placeholders so they cannot ship.
- Generated text, logos and UI are rebuilt as real type and vectors; never ship them as generated.
- Respect deliberate exceptions the user asked for. Log them in the brief and move on.
- Nothing is published, uploaded, deployed or paid for without the user's say-so.

## Files

- `references/concept-and-script.md`: ideas, hooks, beat structure, specificity ladder
- `references/writing.md`: structural tells in prose and how to fix each
- `references/hinglish.md`: Hinglish and Hindi register, tells, TTS spelling
- `references/visual-design.md`: static design and imagery tells
- `references/motion-video.md`: effects to retire, motion grammar, AI footage handling
- `references/code-rendered-video.md`: video drawn in code: determinism, beat grids, self-review, shot sheets
- `references/voice-sound.md`: voiceover direction, music, SFX, mix targets
- `references/edit-and-qa.md`: review passes, keep/repair/replace/rebuild, delivery checklist
- `assets/direction-brief.md`, `assets/shot-plan-template.json`: templates
