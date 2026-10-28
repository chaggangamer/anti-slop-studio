# Anti-Slop Studio

An Agent Skill that helps AI-assisted creative work sound and look decided instead of generic: scripts, ad copy, captions, voiceover, reels, promo videos, motion graphics, thumbnails, landing pages and UI, in English or Hinglish.

It works in two parts. A short workflow makes the decisions before anything is generated (who it is for, the one idea, the proof, one visual direction, what is banned). Then scripts check the result for the tells that mark machine-made work, and a taste pass covers what scripts cannot see.

It follows the open Agent Skills format (a folder with a `SKILL.md`), so it runs in any agent that reads skills.

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

Restart or reload your agent afterwards so it rescans its skills. The PowerShell installer has not been tested on a Windows machine yet, so read it first (it is about 50 lines).

**By hand:** copy `skills/anti-slop-studio/` into your agent's skills folder.

| Agent | Personal folder | Project folder |
|---|---|---|
| Shared standard | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| GitHub Copilot | `~/.copilot/skills/` or `~/.agents/skills/` | `.github/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` |
| Codex, Cursor, Gemini CLI | `~/.agents/skills/` | `.agents/skills/` |

These paths follow vendor documentation as reported by third-party guides in October 2026. Vendors are converging on `.agents/skills`, and some keep older folders as aliases, so check your agent's docs if the skill does not show up.

**Claude.ai and the API:** zip the folder `skills/anti-slop-studio` (the folder itself, not its contents) as `anti-slop-studio.skill` or `.zip` and upload it under Skills. Those uploaders reject frontmatter keys outside the spec, which is why this skill uses only spec fields.

**Agents without skill support:** point them at `AGENTS.md`, which tells them to read `skills/anti-slop-studio/SKILL.md` directly.

## Requirements

- Python 3.8 or newer (standard library only; no `pip install`).
- `ffmpeg` and `ffprobe` on your PATH for two scripts: `probe_video.py` and `check_audio.py`. Everything else works without them.
- No network access is needed by the skill or its scripts.

On some systems the command is `python3`, on Windows it may be `py`.

## Use it

Ask your agent in plain words. A few examples:

- "Rewrite this ad copy. It sounds like an AI wrote it."
- "Plan a 15-second promo reel for my product, and make it different from the last one."
- "Review this storyboard and tell me what feels templated."
- "Meri Hinglish caption bahut translated lag rahi hai, theek karo."
- "QA this finished MP4: pacing, loudness, anything that looks like slop."

You can also run the scripts yourself.

| Script | What it checks | Example |
|---|---|---|
| `slop_scan.py` | Prose tells by density, English and Hinglish | `python skills/anti-slop-studio/scripts/slop_scan.py draft.md` |
| `lint_visuals.py` | Design and motion code: stock fonts and gradients, glow, bounce easing, particles, repeated presets, plus visible copy | `python .../lint_visuals.py index.html --with-copy` |
| `check_shots.py` | Edit rhythm, transition variety, text reading time, slow opens | `python .../check_shots.py shots.json --format reel` |
| `probe_video.py` | Size, fps, cut rate, contact sheet, exports `shots.json` from a real video | `python .../probe_video.py final.mp4 --contact-sheet sheet.jpg` |
| `check_audio.py` | Loudness, true peak, dead air, missing audio | `python .../check_audio.py final.mp4 --target -14` |

Every script has `--help`, prints findings with line numbers, and exits 0 (clean), 1 (findings) or 2 (usage error). A deliberate choice can be allowed with `--allow ID` or a `slop-ok: reason` comment on the line.

See [examples/before-after.md](examples/before-after.md) for real output on small fictional examples.

## What is inside

```
skills/anti-slop-studio/
  SKILL.md                      workflow, principles, gotchas
  references/                   concept and script, writing, Hinglish, visual design,
                                motion and video, code-rendered video, voice and sound, edit and QA
  scripts/                      the five scripts above
  assets/                       direction brief and shot plan templates
examples/                       before and after, with the files used
evals/trigger-queries.json      20 queries for testing when the skill should and should not load
install.sh, install.ps1         installers
AGENTS.md                       pointer for agents without skill support
```

## Limits

- A clean scan shows that known tells are gone. It does not show that the work is good. Use the taste pass in `SKILL.md`.
- The tells come from public practitioner lists, Wikipedia's field guide to AI-generated writing (kept by WikiProject AI Cleanup), and the repositories listed in `references/code-rendered-video.md`. Word lists age as models change, so the scanner leans on structure over vocabulary.
- The Hinglish rules are craft heuristics, not linguistics research. Have a native speaker of your audience read anything important.
- Cut detection in `probe_video.py` uses scene detection, which can miss dissolves and over-count busy footage.
- The skill raises craft. It is not for hiding AI involvement where disclosure is expected or required, and it is not a detector.

## Safety

Skills run with the permissions of your agent. Read what you install. Here the scripts are short, use only the standard library, make no network calls, and write only the files you name (`--contact-sheet`, `--shots-out`).

## License

See the `LICENSE` file.
