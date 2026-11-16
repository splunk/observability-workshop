#!/usr/bin/env bash
# Trigger the "Deploy Workshop to GitHub Pages" workflow and follow the run.
#
# Usage: ./deploy-workshop.sh <branch> <major|minor|patch> "<reason>"
# Example: ./deploy-workshop.sh main minor "Add new OTel discovery module"

set -euo pipefail

WORKFLOW="Deploy Workshop to GitHub Pages"

usage() {
  echo "Usage: $0 <branch> <major|minor|patch> \"<reason>\"" >&2
  exit 1
}

[[ $# -eq 3 ]] || usage

BRANCH="$1"
TYPE="$2"
REASON="$3"

case "$TYPE" in
  major|minor|patch) ;;
  *) echo "Error: type must be major, minor or patch (got '$TYPE')" >&2; usage ;;
esac

[[ -n "$REASON" ]] || { echo "Error: reason cannot be empty" >&2; usage; }

echo "Triggering '$WORKFLOW' on '$BRANCH' ($TYPE): $REASON"
gh workflow run "$WORKFLOW" --ref "$BRANCH" \
  -f release_type="$TYPE" \
  -f release_reason="$REASON"

# Give GitHub a moment to register the run, then watch it
sleep 3
RUN_ID=$(gh run list --workflow="$WORKFLOW" --branch="$BRANCH" --limit 1 \
  --json databaseId -q '.[0].databaseId')

gh run watch "$RUN_ID" --exit-status
