#!/usr/bin/env sh
# Install the anti-slop-studio skill into an agent's skills folder.
#
#   ./install.sh                         # shared folder, user scope  (~/.agents/skills)
#   ./install.sh --agent claude          # Claude Code               (~/.claude/skills)
#   ./install.sh --agent all --scope project
#   ./install.sh --dest /some/skills/dir # any folder you choose
#   ./install.sh --dry-run               # show what would happen
#
# Agents: shared (default), claude, copilot, opencode, codex, cursor, gemini, all.
# codex, cursor and gemini use the shared folder; check your agent's docs if it scans elsewhere.
set -eu

AGENT=shared
SCOPE=user
DEST=
DRY=0
SRC=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/skills/anti-slop-studio

while [ $# -gt 0 ]; do
  case "$1" in
    --agent) AGENT=${2:?missing value for --agent}; shift 2 ;;
    --scope) SCOPE=${2:?missing value for --scope}; shift 2 ;;
    --dest)  DEST=${2:?missing value for --dest}; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

[ -f "$SRC/SKILL.md" ] || { echo "error: cannot find $SRC/SKILL.md" >&2; exit 2; }
case "$SCOPE" in user|project) ;; *) echo "error: --scope must be user or project" >&2; exit 2 ;; esac

dir_for() {
  case "$1:$SCOPE" in
    shared:user|codex:user|cursor:user|gemini:user) echo "$HOME/.agents/skills" ;;
    shared:project|codex:project|cursor:project|gemini:project) echo ".agents/skills" ;;
    claude:user) echo "$HOME/.claude/skills" ;;
    claude:project) echo ".claude/skills" ;;
    copilot:user) echo "$HOME/.copilot/skills" ;;
    copilot:project) echo ".github/skills" ;;
    opencode:user) echo "${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills" ;;
    opencode:project) echo ".opencode/skills" ;;
    *) echo "error: unknown agent '$1'" >&2; return 1 ;;
  esac
}

if [ -n "$DEST" ]; then
  TARGETS=$DEST
elif [ "$AGENT" = all ]; then
  TARGETS=$(for a in shared claude copilot opencode; do dir_for "$a"; done | sort -u)
else
  TARGETS=$(dir_for "$AGENT") || exit 2
fi

echo "$TARGETS" | while IFS= read -r base; do
  [ -n "$base" ] || continue
  target="$base/anti-slop-studio"
  if [ "$DRY" = 1 ]; then echo "would copy $SRC -> $target"; continue; fi
  mkdir -p "$base"
  rm -rf "$target"
  cp -R "$SRC" "$target"
  echo "installed: $target"
done
echo "Done. Restart or reload your agent so it rescans its skills."
