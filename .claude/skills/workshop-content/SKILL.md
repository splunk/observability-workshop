---
name: workshop-content
description: Scaffold and author Splunk Observability Workshop content for this Hugo + hugo-theme-splunk-workshop repo. Use this skill whenever the user asks to create a new workshop, add a chapter, draft topic pages, set up the directory tree, write workshop frontmatter, or produce content using the repo's notice/tabs/persona conventions - even if they only describe the topic without saying "workshop" (for example: "I need a hands-on guide for X", "outline some lab pages for Y", "spin up a new walk-in lab").
---

# Workshop Content Author

This skill helps the user scaffold and write workshops for the Splunk Observability Workshop repo. Workshops are Hugo pages rendered with `hugo-theme-splunk-workshop`, so content should follow the repository's current layout, frontmatter, and shortcode conventions.

The goal is to make it fast to produce a workshop that looks and feels like the rest of the repo without the user having to remember every shortcode by hand. Use canonical patterns by default, but adapt when a target workshop already uses a different convention.

## When to use

Trigger on requests like:

- "Create a new workshop on `<topic>`"
- "Add a chapter about `<feature>` to the `<workshop-name>` workshop"
- "Draft the synthetics section for the `<x>` lab"
- "Scaffold the directory tree for a 1-hour `<topic>` walk-in lab"
- "Write the persona block and exercise for the new RUM chapter"

If the user is editing existing pages or asking content questions about a workshop, use this skill's references for conventions, but do not force the full scaffold workflow.

## Where workshop content lives

Primary language content is under `content/en/` and currently follows this top-level grouping:

```text
content/en/
├── splunk4rookies/            # short, walk-in-lab style workshops
├── ninja-workshops/           # deeper, opinionated technical workshops
├── scenarios/                 # scenario-based labs
└── unsupported-field-workshops/
```

A workshop is a directory under one of these categories.

Language guidance:

- Default to `content/en/` unless the user asks for another language.
- Be aware this repo also contains `content/ja/` and `content/pt-br/`.
- Keep slugs and ordering aligned across languages only when the user explicitly asks for multilingual parity.

## Shape of a workshop

```text
<workshop-slug>/
├── _index.md                    # landing page (workshop overview)
├── images/                      # workshop-level images (e.g., featured-*.png)
├── 1-<chapter-slug>/
│   ├── _index.md                # chapter intro (usually a Persona block)
│   ├── images/                  # chapter-level screenshots
│   ├── 1-<topic>.md             # numbered topic pages
│   ├── 2-<topic>.md
│   └── ...
├── 2-<chapter-slug>/
│   └── ...
└── N-wrap-up/
    └── _index.md                # short congratulatory closer
```

Notes:

- Numbering in folder and file names is for human ordering, but Hugo orders by `weight`. Keep them aligned (prefix `1-` should use `weight: 1` for the same level).
- A chapter folder can be only `_index.md` if no sub-pages are needed.
- Each chapter usually has its own `images/`; topic pages typically reference with `![alt](../images/foo.png)`.
- Wrap-up chapters are short and usually contain one `_index.md` plus a celebratory image.

## Workflow

### 1. Gather the essentials

Before scaffolding, gather at minimum:

- workshop title and slug (kebab-case),
- category (`splunk4rookies`, `ninja-workshops`, etc.),
- total time budget,
- one-line workshop description,
- chapter outline (ordered),
- authors (optional).

If the user only gives a topic, propose a right-sized outline first and confirm before writing files.

### 2. Scaffold the directory tree

Once the outline is agreed, scaffold the tree. Use templates in `assets/templates/` as starting points and then adapt to the target workshop's established style.

Match `weight` to the numeric prefix:

- `1-login/_index.md` -> `weight: 1`
- `2-online-boutique/_index.md` -> `weight: 2`
- `3-rum/1-overview.md` -> `weight: 1` (within chapter)
- `3-rum/2-app-view.md` -> `weight: 2`

Weights restart at 1 *within each chapter folder* — they're scoped to siblings, not global.

### 3. Author the content

Workshop pages in this repo usually follow a clear rhythm. The detailed conventions are in `references/shortcodes.md` and `references/examples.md`.

Common structure:

- **Chapter `_index.md`**: brief context + Persona notice (common pattern), often with a scene-setting Splunk callout and intro image.
- **Topic pages**: brief conceptual intro (when needed), then Exercise notice with step-by-step actions.
- **Question/Answer reveal**: use `tabs` with Question and Answer when the user should pause and think.
- **Button chip references**: use `button` shortcode for literal UI button labels.
- **Info notices**: use for context that supports learning, not for core click flow.

Writing style:

- bold for UI labels (`**Service Map**`),
- backticks for identifiers and fields (`paymentservice`, `version`),
- numbered callouts like `**(1)**` in text if screenshot annotations depend on them.

### 4. Stub images with TODOs

The user often captures screenshots after draft content is in place. For each referenced image:

- Use final relative path in markdown.
- Add an HTML TODO comment immediately above the image.
- Ensure the corresponding `images/` folder exists at the right level.

### 5. Sanity-check before declaring done

Before finishing:

- every chapter folder has `_index.md`,
- topic pages have `weight`,
- weight and filename prefixes are aligned,
- image references and TODO comments are coherent,
- no accidental placeholders remain,
- workshop summary matches actual content.

If asked to verify render, use `hugo serve` from repo root.

## Reference files

Read these when you need them — they're not loaded by default to keep the skill lean.

- `references/frontmatter.md` - frontmatter patterns for workshop `_index.md`, chapter `_index.md`, and topic pages.
- `references/shortcodes.md` - shortcodes used in this repo with practical usage guidance.
- `references/examples.md` - annotated excerpts from `content/en/splunk4rookies/observability-cloud-short/` (primary canonical reference).

## Templates

Bundled in `assets/templates/` — copy and fill in:

- `workshop-index.md` — top-level `_index.md` for a new workshop.
- `chapter-index.md` — chapter `_index.md` with persona block.
- `topic-page.md` — numbered topic page with intro + exercise + Q&A.
- `wrap-up-index.md` — short congrats closer for the final chapter.

These are starting points. Keep them lightweight and adapt only what the target workshop needs.

## Adapting, not enforcing

Other workshops in the repo use different legacy and transitional patterns. When adding to an existing workshop, match that workshop's conventions first (frontmatter shape, folder style, shortcode usage), then apply canonical guidance where no local pattern exists.

Compatibility rules for this skill:

- Keep guidance for patterns still used in current content (for example: `archetype: chapter`, `linkTitle` on chapter `_index.md`).
- Mark those patterns as repository compatibility, not hard requirements for all new content.
- Prefer consistency within a target workshop over global uniformity.

When in doubt, use `content/en/splunk4rookies/observability-cloud-short/` as the canonical style reference.
