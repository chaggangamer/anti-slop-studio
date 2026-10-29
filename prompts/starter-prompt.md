# Starter prompts

A skill loads when your request matches its description, so you can simply ask. These prompts are for when you want the whole workflow every time: brief first, plan before generating, scan the real files, then a taste pass. Paste one above your task.

Replace the examples in the "other skills and tools" step with whatever you have installed.

## Short prompt

```text
Use the anti-slop-studio skill for this task.

1. Find the installed skill and read its SKILL.md. Load only the references this task needs.
2. Tell me which parts of the skill apply, and which other installed skills or tools would genuinely help. Do not load unrelated ones.
3. Before generating anything, lock the direction: audience, the one idea, proof, format and platform, duration, one visual direction, voice, and banned moves.
4. Plan first (script, shot plan), then produce.
5. Run the scanners that fit (slop_scan.py, lint_visuals.py, check_shots.py, probe_video.py, check_audio.py) on the real files. Treat findings as signals to review, not verdicts. Do not claim you ran or inspected anything you did not.
6. Finish with a taste pass: name the three weakest creative decisions and fix those first.
7. If a deliberate choice trips a heuristic, keep it and note why. A clean scan does not prove the work is good.

Do not push, deploy, delete, or expose secrets unless I explicitly say so.

My task:
```

## Full prompt

```text
You are working with the Anti-Slop Studio Agent Skill (https://github.com/chaggangamer/anti-slop-studio). Treat it as the primary creative quality system for this task. Use its references, scripts, assets and examples instead of inventing a parallel anti-slop method.

The goal is creative output that feels intentional, specific, human-directed, visually coherent, non-templated and non-generic. Do not generate something and call it finished.

## First action

1. Confirm the skill is installed. If it is not, say so and point me to the install steps in its README. Do not improvise a replacement.
2. Read its SKILL.md.
3. Load only the references this task needs: concept-and-script, writing, hinglish, visual-design, motion-video, code-rendered-video, voice-sound, edit-and-qa.
4. Tell me which capabilities of the skill apply.
5. Tell me which other installed skills or tools would genuinely help. Do not load unrelated ones just because they are installed.
6. Then do the task with the workflow below.

## Workflow

Brief, research, creative direction, prompt, shot plan, generation or implementation, edit, anti-slop review, technical QA, final.

## 1. Brief before generation

Decide before creating anything important:

- Audience: who exactly is this for?
- One idea: the single thing the viewer should remember.
- Proof: why should they believe it?
- Format and platform: reel, ad, promo, cinematic video, post, landing page, UI, and where it will appear.
- Duration: how much time we actually have.
- Visual direction: one coherent visual language.
- Voice: how the writing should actually sound.
- Banned moves: the clichés, visual tropes, phrases and techniques to avoid.

Do not begin with generic output.

## 2. Prompts for image and video models

Reason about subject, action, environment, composition, camera, camera movement, lighting, colour, motion, timing, material and texture, continuity, audio and constraints. Do not dump every category into every prompt. Use only what improves control of the chosen model, and prefer observable direction over adjectives.

Weak: "An epic breathtaking cinematic masterpiece with stunning lighting and incredible detail."

Better: "85mm close shot. Subject stays centred while the camera slowly pushes forward. Warm window light from camera-left, cooler practical light behind the subject. Shallow depth of field. Subject looks away for the first second, then meets the camera."

## 3. Writing

For scripts, hooks, captions, ad copy, voiceover, titles, landing-page copy and UI copy, apply the skill's writing rules. Do not default to generic marketing language such as unlock, elevate, revolutionise, game-changing, seamless, next-level, powerful, stunning or breathtaking. Do not remove personality just to make text grammatically perfect. Hinglish must sound spoken, not like English translated into Hindi; follow the skill's Hinglish guidance. Run slop_scan.py when relevant and treat its findings as signals, not truth.

## 4. Video planning

Before generating a multi-shot video, write a shot plan. For each shot: number, purpose, duration, subject, action, composition, camera, camera movement, lighting, colour, transition intent, audio or voiceover, and continuity requirements. Every shot must earn its place. Do not add B-roll just because videos are supposed to have it.

## 5. Continuity

Track the invariants across generated shots: character, wardrobe, face, hair, objects, product, location, time of day, light direction, colour palette, camera language and art direction. If a generation changes something unintentionally, name the continuity break instead of pretending the output is correct.

## 6. Edit rhythm

Use the skill's edit guidance. Look for a slow opening, unnecessary establishing shots, repeated shot lengths, too many or identical transitions, text that disappears too quickly, dead time, pointless camera motion, repeated presets, a weak ending, and rhythm that feels machine-made. When a shot-plan JSON exists, run check_shots.py.

## 7. Visual anti-slop

For UI, motion graphics and code-rendered visuals, look for generic AI aesthetics: needless gradients, random glow, heavy glassmorphism, generic cards, rounded rectangles everywhere, particle backgrounds, meaningless blobs, bounce animation on everything, arbitrary purple-blue palettes, giant empty hero sections, floating objects, repeated animation presets, stock typography. Do not ban something only because it is on this list. Ask why it is there. A strong creative reason keeps it. "Because it looks cool" is a reason to reconsider. Run lint_visuals.py when relevant.

## 8. Video QA

When I provide or produce a finished video, inspect the actual file when tooling allows; do not review from the script alone.

- probe_video.py for resolution, fps, duration, cut rate, shot detection, contact sheet and shot export. Dark scenes with small text may need a lower threshold.
- check_audio.py for loudness, true peak, dead air and missing audio.
- Use the contact sheet and detected shots for a visual taste review.

Passing a linter does not mean the video is good.

## 9. Taste pass

After the technical checks, review it separately as a person would. Does it feel decided? Is there one clear idea? Does the opening deserve attention? Is anything there only because AI commonly produces it? Could another AI-made piece have exactly this structure? Is the typography intentional? Is the camera motivated? Does motion communicate something? Are the cuts motivated? Does the sound support the rhythm? Is there a memorable moment? Does the ending resolve the idea? Would removing something make it stronger?

Name the three weakest creative decisions and fix those before polishing small details.

## 10. Other skills

Anti-Slop Studio stays the creative-quality authority. Other installed skills can supply specialist expertise (for example UI and design, motion and animation, implementation, planning). Use them for their domain, then pass their output through Anti-Slop Studio before calling the work finished.

## 11. Tools

Use available tools instead of pretending you inspected something: repository tools for repository work, documentation tools for current library docs, a browser tool for real interaction and testing, devtools for console and network, search tools for outside research, error-tracking tools for production errors. Do not claim something was tested or inspected if you did not do it.

## 12. Safety

Treat third-party skills as executable instructions and do not trust newly downloaded ones blindly. Do not expose API keys, credentials, environment secrets or private information. Do not deploy, push, force-push, delete production data, change production infrastructure, or run destructive commands unless I explicitly authorise it.

## 13. Output

For a creative or video task, return the sections that apply: creative direction, one idea, audience, banned moves, script or copy, visual direction, shot plan, generation prompts, editing notes, audio notes, anti-slop findings, technical QA, taste pass, final recommendations. Do not invent sections that are irrelevant.

## Core rule

Anti-Slop Studio is a creative quality-control system, not a detector whose score we optimise. A clean scan does not prove the work is good. The aim is not content that avoids detection. It is work that feels specific, deliberate and worth watching. When the skill flags a problem, understand why it exists before changing it. When a deliberate choice triggers a heuristic, keep the choice and document why.

My task:
```
