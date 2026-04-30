---
name: workshop-content
description: Scaffold and author Splunk Observability Workshop content for this Hugo + Relearn repo. Use this skill whenever the user asks to create a new workshop, add a chapter, draft topic pages, set up the directory tree, write workshop frontmatter, or produce content using the repo's notice/tabs/persona conventions — even if they only describe the topic without saying "workshop" (e.g., "I need a hands-on guide for X", "outline some lab pages for Y", "spin up a new walk-in lab").
---

# Workshop Content Author

This skill helps the user scaffold and write workshops for the Splunk Observability Workshop repo. Workshops are Hugo pages rendered with the [Relearn theme](https://mcshelby.github.io/hugo-theme-relearn/), so the content has a specific directory shape and a small set of shortcodes that consistently appear across every workshop.

The goal here is to make it fast to produce a workshop that *looks and feels like the rest of the repo* without the user having to remember every shortcode by hand. You should use the canonical patterns by default but adapt when the user has a reason to deviate — these are conventions, not laws.

## When to use

Trigger on requests like:

- "Create a new workshop on `<topic>`"
- "Add a chapter about `<feature>` to the `<workshop-name>` workshop"
- "Draft the synthetics section for the `<x>` lab"
- "Scaffold the directory tree for a 1-hour `<topic>` walk-in lab"
- "Write the persona block and exercise for the new RUM chapter"

If the user is editing existing pages or asking content questions about a workshop, you can use this skill's references for conventions but you don't need to follow the full scaffold workflow.

## Where workshops live

Workshops are organized by category under `content/en/`:

```
content/en/
├── splunk4rookies/        # short, walk-in-lab style workshops
├── ninja-workshops/       # deeper, opinionated technical workshops
├── scenarios/             # scenario-based labs
└── unsupported-field-workshops/
```

A workshop is a directory under one of these categories. Each workshop has its own `_index.md` (the landing page) plus numbered chapter folders. Pick the category from context — if the user says "walk-in lab" or "rookies", use `splunk4rookies`; "deep dive" or "advanced" suggests `ninja-workshops`. Ask if it's not clear.

## Shape of a workshop

```
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

- **Numbering in folder/file names is for human ordering**, but Hugo orders by the `weight` frontmatter field. Keep them in sync (1- prefix = `weight: 1`) so the file tree reads like the rendered nav.
- **A chapter folder can be just `_index.md`** if the chapter has no sub-pages (e.g., `2-online-boutique` and `7-wrap-up` in the short workshop). Don't add sub-pages just to fill space.
- **Each chapter usually has its own `images/`**; topic pages reference them with a relative path: `![alt](../images/foo.png)`.
- **The wrap-up chapter** is short and celebratory — typically one `_index.md` with a congrats notice and an image. See `assets/templates/wrap-up-index.md`.

## Workflow

### 1. Gather the essentials

Before scaffolding, you need at minimum:

- **Workshop title** and a short slug (kebab-case). The slug becomes the folder name.
- **Category** (`splunk4rookies`, `ninja-workshops`, etc.).
- **Total time budget** (e.g., "60 minutes", "3 hours").
- **One-line description** for the frontmatter (this shows up in the workshop list).
- **Chapter outline**: ordered list of chapters. For each, ideally: chapter title, persona (if applicable), per-chapter time budget, and a rough list of topic pages.
- **Authors** (optional but used in the top `_index.md`).

If the user gave you only a topic and a vibe, propose an outline and have them edit it before you start writing files. Don't speculate a 7-chapter workshop when they asked for a quick lab.

### 2. Scaffold the directory tree

Once the outline is agreed, create the tree. Use the templates in `assets/templates/` as the starting point for each file type — they encode the frontmatter conventions (see `references/frontmatter.md`) so you don't have to remember field-by-field which workshops use `archetype: chapter` vs. `params.images` vs. `linkTitle`.

Match `weight` to the numeric prefix:

| Folder/file              | weight |
|--------------------------|--------|
| `1-login/_index.md`      | 1      |
| `2-online-boutique/_index.md` | 2 |
| `3-rum/1-overview.md`    | 1 (within chapter) |
| `3-rum/2-app-view.md`    | 2 |

Weights restart at 1 *within each chapter folder* — they're scoped to siblings, not global.

### 3. Author the content

Workshop pages have a recognizable rhythm. The conventions are documented in `references/shortcodes.md` and `references/examples.md`, but the high-level pattern is:

- **Chapter `_index.md`**: short context paragraph, then a **Persona** notice (orange, icon `user`) explaining who the reader is in this chapter and a `> [!splunk]` callout setting the scene. Often ends with an image.
- **Topic pages**: introductory prose explaining *what* the user is about to look at and *why* it matters, then an **Exercise** notice (green, icon `running`) with the click-by-click steps. Use bold for UI element names (**Digital Experience**, **Service Map**), backticks for technical identifiers (`paymentservice`, `frontend:/cart/checkout`), and numbered callouts like **(1)**, **(2)** to refer to spots on screenshots.
- **Question/Answer reveals**: when there's a moment where the user should pause and think, wrap the question in a `{{< tabs >}}` block with a Question tab and an Answer tab. This gives the rendered page a "click to reveal" feel without spoiling the answer above the fold.
- **Buttons in instructions**: when telling the user to click a real UI button, use `{{% button style="blue" %}}Apply{{% /button %}}` so it renders as a button-shaped chip in the prose. The styles match Splunk Observability's button colors (`blue`, `grey`, `red` for danger).
- **Info notices**: for sidebar-style explanations of a feature ("what is Trace Analyzer?"), use `{{% notice title="..." style="info" %}}` blocks. Use them sparingly — they're for context the user *might* want, not the main flow.

The why behind these patterns: workshops are read while the reader is also clicking around in a product. The notice blocks chunk the page into "read this", "do this", and "think about this" so the reader can keep their place while context-switching to the UI.

### 4. Stub images with TODOs

The user takes the screenshots themselves. For every image referenced in the markdown:

- Reference it with the final relative path you expect (`![desc](../images/foo.png)`).
- Add an HTML comment immediately above with what the screenshot should show: `<!-- TODO screenshot: paymentservice highlighted in service map, side panel showing 100% error rate -->`.
- Make sure the `images/` folder exists at the right level (chapter or workshop), even if empty — Hugo doesn't care, but it's a clear visual cue that screenshots go here.

### 5. Sanity-check before declaring done

Run a quick mental pass:

- Every chapter folder has an `_index.md`.
- Every topic page has a `weight`.
- Every image reference has a TODO comment and a corresponding (empty) folder.
- No literal placeholder text like `[NAME OF WORKSHOP]` left in unless that's intentional (the short workshop uses this on purpose so instructors can find-and-replace at delivery time — see `references/examples.md`).
- The top `_index.md` description matches what the workshop actually covers.

If the user wants to preview the build, the repo has a Hugo setup; `hugo serve` from the repo root will render. You don't need to run it unless asked.

## Reference files

Read these when you need them — they're not loaded by default to keep the skill lean.

- `references/frontmatter.md` — exact frontmatter fields per file type (workshop `_index`, chapter `_index`, topic page) with rationale for each field.
- `references/shortcodes.md` — full catalog of shortcodes used in the repo (notice variants, tabs, button, icon, badge) with examples and when to use which.
- `references/examples.md` — annotated excerpts from the `observability-cloud-short` workshop showing patterns in context.

## Templates

Bundled in `assets/templates/` — copy and fill in:

- `workshop-index.md` — top-level `_index.md` for a new workshop.
- `chapter-index.md` — chapter `_index.md` with persona block.
- `topic-page.md` — numbered topic page with intro + exercise + Q&A.
- `wrap-up-index.md` — short congrats closer for the final chapter.

These are starting points. Don't over-customize them — adapt only the parts the workshop actually needs.

## Adapting, not enforcing

Other workshops in the repo follow slightly different conventions (the longer `observability-cloud` workshop uses double-digit chapter prefixes like `30-im-exercise/` to insert chapters out of original order). When adding to an existing workshop, *match that workshop's existing conventions* even if they differ from the canonical pattern here. Open one of its chapters first and follow its lead — frontmatter style, image-folder layout, level of prose, depth of exercises.

When in doubt, the `observability-cloud-short` workshop at `content/en/splunk4rookies/observability-cloud-short/` is the cleanest reference for the canonical style.
