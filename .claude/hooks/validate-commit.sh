#!/bin/bash
# Prevent .claude directory files from being committed on translate/* branches
set -e

# Read hook input from stdin (JSON format from Claude Code)
input=$(cat)

# Extract the command being executed (without jq dependency)
# Input format: {"tool_input": {"command": "..."}}
command=$(echo "$input" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' || echo "")

# Only validate git commit commands
if [[ ! "$command" =~ git[[:space:]]+commit ]]; then
  exit 0
fi

# Check current branch
current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

# Only apply restriction on translate/* branches
if [[ ! "$current_branch" =~ ^translate/ ]]; then
  exit 0
fi

# Check if any .claude files are staged for commit
staged_claude_files=$(git diff --cached --name-only 2>/dev/null | grep '^\.claude/' || true)

if [[ -n "$staged_claude_files" ]]; then
  echo "ERROR: Cannot commit .claude directory files on translate/* branches." >&2
  echo "Staged .claude files detected:" >&2
  echo "$staged_claude_files" | sed 's/^/  - /' >&2
  echo "" >&2
  echo "The .claude directory should only be modified on the ja-translation-system branch." >&2
  echo "Please unstage these files: git reset HEAD .claude/" >&2
  # Exit code 2 blocks the tool call
  exit 2
fi

exit 0
