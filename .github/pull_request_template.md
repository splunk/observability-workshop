## Summary

What this PR changes and why. One or two sentences.

Fixes # (optional — link an issue / ticket)

## Type of change

- [ ] New workshop
- [ ] New chapter or page in an existing workshop
- [ ] Content edits (clarity, correctness, polish) to existing pages
- [ ] Restructure / reorganize (move, split, merge, renumber)
- [ ] URL change — `aliases:` added for any renamed or moved page
- [ ] Image / screenshot refresh
- [ ] Translation sync (`content/en` ↔ `content/ja`)
- [ ] Content removal / archival
- [ ] Theme bump or shortcode / layout adoption
- [ ] Frontmatter-only changes (weight, `draft`, `hidden`, `archetype`, …)
- [ ] Lint / formatting cleanup (low-risk, scan-approve)
- [ ] CI / build / tooling
- [ ] Bug fix (broken link, busted shortcode, etc.)
- [ ] Other — describe:

## What's affected

- **Workshop(s) / area:** e.g. `splunk4rookies/observability-cloud-short/`, `ninja-workshops/foundations/3-opentelemetry-collector-workshops/`
- **Languages:** [ ] `content/en` &nbsp;&nbsp; [ ] `content/ja`

## Reviewer focus

Anything you'd specifically like the reviewer to check? (e.g. "verify the `kubectl` command in step 3 against the current OTel collector"). Leave blank if not applicable.

## Screenshots / preview

For visual changes, paste a before/after screenshot or a Hugo preview link.

## Verification

- [ ] `hugo` builds cleanly (no warnings or errors)
- [ ] `npx markdownlint-cli2 '<paths/*.md>'` passes for touched files
- [ ] Any new images have meaningful alt text
- [ ] No TODO image placeholders left unintentionally
- [ ] No published URLs changed, OR `aliases:` frontmatter added for any renamed / moved pages
- [ ] Identified and updated parallel / sibling pages where this workshop shares content with another (e.g. `observability-cloud-short` ↔ `observability-cloud`), OR confirmed none exist
