#!/usr/bin/env bash
# Thin launcher for launchd -> run_skill_generation_pipeline.py
#
# Install as launchd agent:
#   cp launchd/com.skill-library.skill-generation-weekly.plist ~/Library/LaunchAgents/
#   cp launchd/com.skill-library.skill-generation-daily.plist ~/Library/LaunchAgents/
#   launchctl load ~/Library/LaunchAgents/com.skill-library.skill-generation-weekly.plist
#   launchctl load ~/Library/LaunchAgents/com.skill-library.skill-generation-daily.plist
#
# Manual test:
#   bash scripts/run_skill_generation.sh --mode weekly --dry-run
#   bash scripts/run_skill_generation.sh --mode daily --dry-run
set -euo pipefail

# Allow claude -p subprocess calls even when launched from a Claude Code terminal
unset CLAUDECODE

export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:${HOME}/.local/bin:/usr/local/bin:$PATH"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}/.." || exit 1

# Load project-level .envrc (sets GH_TOKEN for the correct GitHub account)
if command -v direnv &>/dev/null && [ -f .envrc ]; then
    eval "$(direnv export bash 2>/dev/null)"
fi

python3 scripts/run_skill_generation_pipeline.py "$@"
