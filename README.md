# Anti-Slop Studio

An Agent Skill for creative work made with AI. It helps scripts, ad copy, reels, promo videos, motion graphics, UI and Hinglish copy come out decided and specific instead of generic.

It works in two parts. A short workflow makes the decisions before anything is generated: who it is for, the one idea, the proof, one visual direction, what is banned. Then scripts check the result for the tells that mark machine-made work, and a taste pass covers what scripts cannot see.

It follows the open Agent Skills format (a folder with a `SKILL.md`), so it runs in any agent that reads skills.

**Contents:** [Quick start](#quick-start) · [Starter prompt](#starter-prompt) · [How it works](#how-it-works) · [Install](#install) · [Scripts](#scripts) · [Examples](#examples) · [Limits](#limits) · [Safety](#safety) · [License](#license)

## Quick start

1. Install the skill (see [Install](#install)). One command with the installer, or copy one folder.
2. Restart your agent so it rescans its skills.
3. Ask in plain words, or paste the [starter prompt](#starter-prompt) above your task.

Plain requests that load it:

- "Rewrite this ad copy. It sounds like an AI wrote it."
- "Plan a 15-second promo reel for my product, and make it different from the last one."
- "Review this storyboard and tell me what feels templated."
- "Meri Hinglish caption bahut translated lag rahi hai, theek karo."
- "QA this finished MP4: pacing, loudness, anything that looks like slop."

## Starter prompt

A skill loads when your request matches its description, so you do not need a prompt. Use one when you want the whole workflow every time: brief first, plan before generating, scan the real files, then a taste pass.

Copy this above your task:

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

<details>
<summary>Full prompt (about 1,100 words, for bigger creative jobs)</summary>

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

</details>

Both prompts also live in [prompts/starter-prompt.md](prompts/starter-prompt.md). Swap the generic "other skills and tools" step for the skills and tools you actually have installed.

## How it works

| Stage | Question it answers | Check |
|---|---|---|
| Brief | Who, what one idea, what proof, what action | direction brief |
| Concept | Is the idea rooted in something true and specific | taste pass |
| Script and copy | Does every line carry information | `slop_scan.py` |
| Visual | Is there one committed direction | `lint_visuals.py` |
| Motion | Does every movement belong to something | `lint_visuals.py`, `check_shots.py` |
| Voice and sound | Is delivery directed and the mix intentional | `check_audio.py` |
| Edit and QA | Does it survive sound off, thumbnail size and a second watch | `probe_video.py` plus the rest |

The agent reads only the reference files the task needs, so the skill stays light in context. `SKILL.md` holds the workflow, and `skills/anti-slop-studio/references/` holds the detail.

## Install

Pick one.

**With the installer** (copies the skill folder; needs no network):

```bash
./install.sh                        # shared folder (~/.agents/skills)
./install.sh --agent claude         # Claude Code
./install.sh --agent all --scope project
./install.sh --dry-run              # show what would happen
```

```powershell
.\install.ps1                       # Windows PowerShell
.\install.ps1 -Agent claude
.\install.ps1 -Dest D:\my\skills
```

Restart or reload your agent afterwards. The PowerShell installer has not been tested on a Windows machine yet, so read it first (it is about 50 lines).

**With the skills CLI**, if you use it:

```bash
npx skills add https://github.com/chaggangamer/anti-slop-studio --skill anti-slop-studio
```

**By hand:** copy `skills/anti-slop-studio/` into your agent's skills folder.

| Agent | Personal folder | Project folder |
|---|---|---|
| Shared standard | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| GitHub Copilot | `~/.copilot/skills/` or `~/.agents/skills/` | `.github/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` |
| Codex, Cursor, Gemini CLI | `~/.agents/skills/` | `.agents/skills/` |

These paths follow vendor documentation as reported by third-party guides in October 2026. Vendors are converging on `.agents/skills`, and some keep older folders as aliases, so check your agent's docs if the skill does not show up.

**Claude.ai and the API:** zip the folder `skills/anti-slop-studio` (the folder itself, not its contents) as `anti-slop-studio.skill` or `.zip` and upload it under Skills, or download the `.skill` file from the latest release. Those uploaders reject frontmatter keys outside the spec, which is why this skill uses only spec fields.

**Agents without skill support:** point them at `AGENTS.md`, which tells them to read `skills/anti-slop-studio/SKILL.md` directly.

### Requirements

- Python 3.8 or newer (standard library only; no `pip install`).
- `ffmpeg` and `ffprobe` on your PATH for two scripts: `probe_video.py` and `check_audio.py`. Everything else works without them.
- No network access is needed by the skill or its scripts.

On some systems the command is `python3`, on Windows it may be `py`.

## Scripts

| Script | What it checks | Example |
|---|---|---|
| `slop_scan.py` | Prose tells by density, English and Hinglish | `python skills/anti-slop-studio/scripts/slop_scan.py draft.md` |
| `lint_visuals.py` | Design and motion code: stock fonts and gradients, glow, bounce easing, particles, repeated presets, plus visible copy | `python .../lint_visuals.py index.html --with-copy` |
| `check_shots.py` | Edit rhythm, transition variety, text reading time, slow opens | `python .../check_shots.py shots.json --format reel` |
| `probe_video.py` | Size, fps, cut rate, contact sheet, exports `shots.json` from a real video | `python .../probe_video.py final.mp4 --contact-sheet sheet.jpg` |
| `check_audio.py` | Loudness, true peak, dead air, missing audio | `python .../check_audio.py final.mp4 --target -14` |

Every script has `--help`, prints findings with line numbers, and exits 0 (clean), 1 (findings) or 2 (usage error). A deliberate choice can be allowed with `--allow ID` or a `slop-ok: reason` comment on the line.

## Examples

[examples/before-after.md](examples/before-after.md) shows real script output on small fictional examples: ad copy, Hinglish copy, UI code and an edit plan, each before and after.

## What is inside

```
skills/anti-slop-studio/
  SKILL.md                      workflow, principles, gotchas
  references/                   concept and script, writing, Hinglish, visual design,
                                motion and video, code-rendered video, voice and sound, edit and QA
  scripts/                      the five scripts above
  assets/                       direction brief and shot plan templates
prompts/starter-prompt.md       short and full starter prompts
examples/                       before and after, with the files used
evals/trigger-queries.json      20 queries for testing when the skill should and should not load
install.sh, install.ps1         installers
AGENTS.md                       pointer for agents without skill support
```

## Limits

- A clean scan shows that known tells are gone. It does not show that the work is good. Use the taste pass in `SKILL.md`.
- The tells come from public practitioner lists, Wikipedia's field guide to AI-generated writing (kept by WikiProject AI Cleanup), and the repositories listed in `references/code-rendered-video.md`. Word lists age as models change, so the scanner leans on structure over vocabulary.
- The Hinglish rules are craft heuristics, not linguistics research. Have a native speaker of your audience read anything important.
- Cut detection in `probe_video.py` uses scene detection, which can miss dissolves and cuts between dark scenes, and can over-count busy footage. Try `--threshold 0.04` or `--sweep`, and look at the contact sheet.
- The skill raises craft. It is not for hiding AI involvement where disclosure is expected or required, and it is not a detector.

## Safety

Skills run with the permissions of your agent. Read what you install. Here the scripts are short, use only the standard library, make no network calls, and write only the files you name (`--contact-sheet`, `--shots-out`).

## Feedback

Found something it flags wrongly, or misses? Open an issue with the input, the output, and what felt wrong.

## License

MIT. See [LICENSE](LICENSE).
