# PT-BR Localization Rollout

The Brazilian Portuguese localization is staged in this branch, but it is hidden by default.

## Why PT-BR is hidden

- Only the language infrastructure and the first review slice are translated.
- Publishing `/pt-br/` now would make the site look officially available in Portuguese before the full workshop set, terminology, and tone have been reviewed.
- Keeping the language disabled prevents incomplete localized pages from appearing in the language switcher or being indexed.

## What is included

- `pt-br` language configuration in `hugo.toml`
- Brazilian Portuguese UI strings in `i18n/pt-br.yaml`
- Minimal PT-BR landing pages needed for navigation
- First translated review slice: `content/pt-br/splunk4rookies/observability-cloud-short/1-login/_index.md`

## How to review locally

Create a temporary config that enables PT-BR without changing tracked files:

```bash
python3 - <<'PY'
from pathlib import Path

config = Path("hugo.toml").read_text()
config = config.replace("    disabled   = true\n", "")
Path("/tmp/hugo-ptbr-review.toml").write_text(config)
PY

hugo server \
  --config /tmp/hugo-ptbr-review.toml \
  --bind 127.0.0.1 \
  --port 1314 \
  --baseURL http://127.0.0.1:1314/
```

Open:

```text
http://127.0.0.1:1314/pt-br/splunk4rookies/observability-cloud-short/1-login/
```

## How to publish later

When PT-BR is approved for public release:

1. Translate and review the remaining approved workshop scope.
2. Remove `disabled = true` from `[languages.pt-br]` in `hugo.toml`.
3. Run a full Hugo build and review the language switcher.
4. Merge only after the localized navigation, terminology, screenshots, and build output are approved.
