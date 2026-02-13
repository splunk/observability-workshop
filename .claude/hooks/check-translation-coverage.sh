#!/bin/bash
# Check for untranslated files in /content/ja/
#
# This script is used as a Stop hook for the translation skill.
# It scans all .md files under /content/ja/ and checks if they
# contain Japanese characters (hiragana/katakana).
#
# Exit behavior:
#   - exit 0 with no stdout: allow stop
#   - exit 0 with JSON stdout: block stop if decision=block
#
# Usage (standalone):
#   echo '{"stop_hook_active": false}' | bash check-translation-coverage.sh
#
# Usage (as hook):
#   Automatically called by Claude Code Stop hook

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
JA_DIR="$PROJECT_DIR/content/ja"

# Read hook input from stdin
INPUT=$(cat)

# Prevent infinite loops: if already continuing from a previous stop hook, allow stop
STOP_ACTIVE=$(echo "$INPUT" | grep -o '"stop_hook_active"[[:space:]]*:[[:space:]]*[a-z]*' | grep -o '[a-z]*$' || echo "false")
if [ "$STOP_ACTIVE" = "true" ]; then
  exit 0
fi

# Skip if /content/ja/ doesn't exist (e.g., on ja-translation-system branch)
if [ ! -d "$JA_DIR" ]; then
  exit 0
fi

# Find untranslated .md files (no hiragana or katakana characters)
UNTRANSLATED=()

while IFS= read -r -d '' file; do
  # Skip very short files (frontmatter-only, typically _index.md with just weight/title)
  LINE_COUNT=$(wc -l < "$file")
  if [ "$LINE_COUNT" -lt 5 ]; then
    continue
  fi

  # Check for Japanese characters: hiragana (U+3040-309F) or katakana (U+30A0-30FF)
  if ! grep -Pq '[\x{3040}-\x{309F}\x{30A0}-\x{30FF}]' "$file"; then
    REL_PATH="${file#"$JA_DIR"/}"
    UNTRANSLATED+=("$REL_PATH")
  fi
done < <(find "$JA_DIR" -name "*.md" -type f -print0 2>/dev/null)

# If no untranslated files found, allow stop
if [ ${#UNTRANSLATED[@]} -eq 0 ]; then
  exit 0
fi

# Build the list of untranslated files (max 20 for readability)
COUNT=${#UNTRANSLATED[@]}
FILES_LIST=""
SHOWN=0
for f in "${UNTRANSLATED[@]}"; do
  if [ $SHOWN -ge 20 ]; then
    FILES_LIST="${FILES_LIST}  - ... and $((COUNT - 20)) more\n"
    break
  fi
  FILES_LIST="${FILES_LIST}  - ${f}\n"
  SHOWN=$((SHOWN + 1))
done

# Output JSON to block stop and report untranslated files
REASON="/content/ja/ に翻訳されていないファイルが ${COUNT} 件見つかりました。以下のファイルを翻訳してください:\n${FILES_LIST}"

# Use printf to handle escaping properly, then construct JSON
printf '{"decision":"block","reason":"%s"}' "$REASON"
exit 0
