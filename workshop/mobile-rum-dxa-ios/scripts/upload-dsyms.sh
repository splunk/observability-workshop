#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${SPLUNK_REALM:-}" ]]; then
  echo "SPLUNK_REALM is required, for example us1." >&2
  exit 1
fi

if [[ -z "${SPLUNK_ACCESS_TOKEN:-}" ]]; then
  echo "SPLUNK_ACCESS_TOKEN is required. Use an organization API access token, not a RUM token." >&2
  exit 1
fi

if [[ -z "${DSYM_PATH:-}" ]]; then
  echo "DSYM_PATH is required, for example /path/to/MyApp.xcarchive/dSYMs." >&2
  exit 1
fi

if ! command -v splunk-rum >/dev/null 2>&1; then
  echo "splunk-rum was not found. Install it with: npm install @splunk/rum-cli --global" >&2
  exit 1
fi

splunk-rum ios upload --path "${DSYM_PATH}"
splunk-rum ios list
