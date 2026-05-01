#!/usr/bin/env bash
# install_to_claude.sh — sync skills/ and agents/ from this repo to ~/.claude/
#
# Without arguments this syncs nothing; you must pick a target.
#
# Usage:
#   scripts/install_to_claude.sh --all                           # sync every skill and every agent
#   scripts/install_to_claude.sh <name>                          # sync skills/<name> AND agents/<name>.md if it exists
#   scripts/install_to_claude.sh --skill <name>                  # sync only skills/<name>
#   scripts/install_to_claude.sh --agent <name>                  # sync only agents/<name>.md
#   scripts/install_to_claude.sh --check [--all|<name>]          # diff-only; exits 1 on drift, useful in CI
#   scripts/install_to_claude.sh --dry-run --all                 # print what would happen, do nothing
#
# Notes:
#   - Skills are installed by removing ~/.claude/skills/<name>/ first, then copying. This guarantees
#     deleted files in the repo are also removed locally (rsync --delete equivalent without rsync).
#   - .DS_Store and __pycache__ are stripped after copy.
#   - Agents are single .md files, copied with `cp` (overwrite).
#   - Refuses to run if SKILLS_REPO does not look like this repository.

set -euo pipefail

SKILLS_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
SKILLS_DST="$CLAUDE_HOME/skills"
AGENTS_DST="$CLAUDE_HOME/agents"

DRY_RUN=0
CHECK_ONLY=0
MODE=""    # "all" | "skill" | "agent" | "both"
TARGET=""

die() { echo "error: $*" >&2; exit 2; }

usage() {
  sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's|^# \{0,1\}||'
  exit "${1:-0}"
}

# --- arg parsing -------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage 0 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --check)   CHECK_ONLY=1; shift ;;
    --all)     MODE="all"; shift ;;
    --skill)   MODE="skill"; TARGET="${2:-}"; shift 2 ;;
    --agent)   MODE="agent"; TARGET="${2:-}"; shift 2 ;;
    --) shift; break ;;
    -*) die "unknown flag: $1 (use --help)" ;;
    *)
      [[ -n "$MODE" && "$MODE" != "both" ]] && die "unexpected positional arg after $MODE: $1"
      MODE="both"; TARGET="$1"; shift ;;
  esac
done
[[ -z "$MODE" ]] && usage 2

# --- sanity check ------------------------------------------------------------
[[ -d "$SKILLS_REPO/skills" ]] || die "not a skills repo: $SKILLS_REPO"
[[ -d "$CLAUDE_HOME" ]] || die "$CLAUDE_HOME does not exist; create it first"
mkdir -p "$SKILLS_DST" "$AGENTS_DST"

run() {
  if (( DRY_RUN )); then
    printf '  [dry-run] %s\n' "$*"
  else
    eval "$@"
  fi
}

drift_count=0

note_drift() {
  echo "  drift: $*"
  drift_count=$((drift_count + 1))
}

# --- per-target operations ---------------------------------------------------
sync_skill() {
  local name="$1"
  local src="$SKILLS_REPO/skills/$name"
  local dst="$SKILLS_DST/$name"
  [[ -d "$src" ]] || die "skill not found in repo: $name"
  [[ -f "$src/SKILL.md" ]] || { echo "  skip $name (no SKILL.md, in-progress)"; return 0; }

  if (( CHECK_ONLY )); then
    if [[ ! -d "$dst" ]]; then
      note_drift "skill missing in ~/.claude: $name"
    elif ! diff -rq "$src" "$dst" 2>&1 | grep -v "__pycache__\|\.DS_Store" | grep -q .; then
      :  # in sync
    else
      note_drift "skill differs from repo: $name"
    fi
    return 0
  fi

  echo "  skill -> $name"
  run "rm -rf '$dst'"
  run "cp -r '$src' '$dst'"
  run "find '$dst' -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true"
  run "find '$dst' -name '.DS_Store' -delete 2>/dev/null || true"
}

sync_agent() {
  local name="$1"
  local src="$SKILLS_REPO/agents/$name.md"
  local dst="$AGENTS_DST/$name.md"
  [[ -f "$src" ]] || { echo "  skip agent $name (no agents/$name.md)"; return 0; }

  if (( CHECK_ONLY )); then
    if [[ ! -f "$dst" ]]; then
      note_drift "agent missing in ~/.claude: $name"
    elif ! diff -q "$src" "$dst" >/dev/null 2>&1; then
      note_drift "agent differs from repo: $name"
    fi
    return 0
  fi

  echo "  agent -> $name"
  run "cp '$src' '$dst'"
}

# --- dispatch ----------------------------------------------------------------
header="installing"; (( CHECK_ONLY )) && header="checking"; (( DRY_RUN )) && header="$header (dry-run)"

case "$MODE" in
  all)
    echo "$header all skills + agents from $SKILLS_REPO"
    for d in "$SKILLS_REPO"/skills/*/; do
      sync_skill "$(basename "$d")"
    done
    for f in "$SKILLS_REPO"/agents/*.md; do
      [[ -e "$f" ]] || continue
      sync_agent "$(basename "$f" .md)"
    done
    ;;
  both)
    [[ -n "$TARGET" ]] || die "missing skill/agent name"
    echo "$header $TARGET (skill + matching agent)"
    sync_skill "$TARGET"
    sync_agent "$TARGET"
    ;;
  skill)
    [[ -n "$TARGET" ]] || die "missing --skill name"
    echo "$header skill: $TARGET"
    sync_skill "$TARGET"
    ;;
  agent)
    [[ -n "$TARGET" ]] || die "missing --agent name"
    echo "$header agent: $TARGET"
    sync_agent "$TARGET"
    ;;
esac

if (( CHECK_ONLY )); then
  if (( drift_count > 0 )); then
    echo "FAIL: $drift_count drift(s) detected. Run without --check to sync."
    exit 1
  fi
  echo "OK: in sync"
fi
