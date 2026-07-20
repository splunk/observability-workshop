# Frontmatter Reference

Every workshop file has YAML frontmatter at the top. Three flavors: workshop landing page, chapter `_index.md`, and topic page. Keep frontmatter minimal — only include fields that are actually doing work. Every extra field is something that might rot.

## Workshop landing page (`<workshop-slug>/_index.md`)

```yaml
---
title: Observability Cloud (Shortened 1h)
weight: 2
authors: ["Robert Castley", "Pieter Hagen"]
time: 60 minutes
description: Experience Splunk Observability Cloud's end-to-end visibility from front-end to back-end services through hands-on troubleshooting exercises.
params:
  images:
    - images/featured-o11y.png
---
```

| Field | Required? | Notes |
|-------|-----------|-------|
| `title` | yes | Full display title shown on the workshop landing page. Can include a parenthetical qualifier ("Shortened 1h", "Original 3h"). |
| `weight` | yes | Orders this workshop within its category (`splunk4rookies/`, etc.). Lower numbers come first. Pick a value that fits the existing siblings. |
| `authors` | optional | List of author names. Rendered in the page header by the theme. |
| `time` | yes | Human-readable duration shown in the workshop list. Use the exact form `"60 minutes"` or `"3 hours"`. |
| `description` | yes | One-line summary, used in workshop list cards and meta description. Aim for ~20–30 words. |
| `params.images` | optional | Featured image(s) for cards. Path is relative to the workshop folder unless prefixed with `/` (which makes it relative to `static/`). |
| `aliases` | optional | Legacy URL redirects, e.g., `aliases: ["/en/s4r/"]`. Only use if migrating from an old path. |

## Chapter `_index.md` (`<workshop>/N-<slug>/_index.md`)

```yaml
---
title: Digital Experience (RUM)
linkTitle: 3. Digital Experience (RUM)
weight: 3
archetype: chapter
time: 15 minutes
description: This section helps you understand how to use Splunk RUM to monitor the performance of your applications from the end user's perspective.
---
```

| Field | Required? | Notes |
|-------|-----------|-------|
| `title` | yes | Chapter title without a number prefix — used as the page H1. |
| `linkTitle` | yes | Same title with a leading number ("3. ...") — this is what shows in the left-nav. The number must match the chapter's `weight`. |
| `weight` | yes | Position within the workshop. Match the folder-name prefix (`3-rum/` → `weight: 3`). |
| `archetype: chapter` | recommended for compatibility | Common in existing workshop content and keeps chapter rendering/layout consistent with current repo conventions. |
| `time` | recommended | Per-chapter time estimate, e.g., `"15 minutes"`. |
| `description` | yes | One-line summary of what the chapter covers. |

The chapter body is usually:

1. A short context paragraph (1–3 lines).
2. A `Persona` notice (orange, icon `user`) — see `shortcodes.md`.
3. A `> [!splunk]` callout introducing the scenario.
4. An optional intro image, often `images/messages.png?width=750px`.

## Topic page (`<workshop>/<chapter>/N-<slug>.md`)

```yaml
---
title: 1. RUM Overview
weight: 1
---
```

That's it. Topic pages are intentionally light on frontmatter:

| Field | Required? | Notes |
|-------|-----------|-------|
| `title` | yes | Full topic title with leading number (the `1.` is part of the title, unlike chapters where it lives in `linkTitle`). |
| `weight` | yes | Position within the chapter. Restart from 1 in each chapter folder. |

Don't add `description`, `linkTitle`, or `archetype` to topic pages unless there's a specific reason — the theme handles them fine without these.

## Common mistakes to avoid

- **Mismatched weight and prefix.** If the folder is `4-apm/` but the frontmatter says `weight: 5`, the rendered nav will not match the file tree, which makes the repo confusing to navigate.
- **Numbering inside `title` for chapters.** Chapter `title` should be clean ("Logs"); the number lives in `linkTitle` ("5. Logs"). Topic pages do put the number in `title` because they don't have `linkTitle`.
- **Inconsistent chapter metadata.** If surrounding chapters use `archetype: chapter`, keep it for new siblings to avoid visual/layout drift within the same workshop.
- **`time` mismatched between top `_index.md` and the sum of chapter `time` fields.** The top-level total should add up to roughly the chapter sum. If it doesn't, the workshop list will show one number while attendees experience another.
