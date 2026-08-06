# Template contract: .conf26 lab guide

## Reference

- Source: `/Users/kylwang/Downloads/conf26 TEMPLATE - [Workshop Name] - Lab Guide - [Date] (1).docx`
- SHA-256: `eff93f7c9d6b7825dac64b3f0e0f95b602422794b834658f9b8886322635931e`
- Rendered reference: `.tmp/conf26_labguide/template-render`
- Page count: 7
- Section count: 2
- Package parts: 64. Baseline sizes and SHA-256 values were inventoried before editing.

## Page system

- US Letter portrait throughout.
- Section 1: 8.50 x 11.00 inches; margins L/R/T/B = 0.40/0.40/0.80/0.50 inches; different first page enabled.
- Section 2: 8.49 x 11.00 inches; margins L/R/T/B = 0.40/0.54/0.50/0.50 inches; linked header and footer.
- Both sections begin on a new page.
- The first page uses a wide .conf26 banner. Later pages use page-number footers and no visible running header in the reference render.

## Typography and recurring components

- Preserve the reference theme, embedded fonts, styles, numbering, page geometry, header/footer parts, and .conf26 imagery.
- Cover session identifier: 24 pt, bold, black, direct formatting in `word/document.xml` body paragraph 1.
- Cover subtitle: 16 pt, black, direct formatting in body paragraph 2.
- Heading 1: 16 pt, bold, 24 pt before, keep-with-next, thin bottom rule.
- Heading 2: 13 pt, bold, 10 pt before, keep-with-next.
- Body copy uses the template's Normal style and direct paragraph rhythm; left indent is 0.25 inches where inherited from Normal.
- Numbered steps use the existing numbering definition (`numId=12`) and 1.5-line spacing.
- Code blocks clone the reference gray-shaded Consolas paragraph with 0.5-inch left indent; no fixed height.
- Notes clone the reference pale-cyan callout with top/bottom borders and a bold `Note:` label.
- TOC entries preserve the original hyperlinks, bookmarks, dotted leaders, PAGEREF fields, and TOC 1/TOC 2 styles.
- No tables occur in the reference. Do not introduce layout tables.

## Content flow

1. Cover and table of contents.
2. Prerequisites and connectivity troubleshooting.
3. Splunk Show event enrollment and instance access, with four instructional screenshots.
4. Three exercise shells, each containing Description, Steps, numbered placeholders, a code example block, and a note callout.

## Slot map

- `word/document.xml`, first body paragraph, text `[SESSION ID]`: replace with confirmed session ID `OBS1184`.
- Second body paragraph `Lab Guide`: retain `Lab Guide` while adding the workshop name within the same cover slot.
- Fourth body paragraph author instruction `**UPDATE THIS TABLE...**`: replace with workshop duration and Collector version; this is template-only instructional text.
- TOC hyperlinks with visible text `Exercise 1/2/3 - [Title]`: replace only the visible title text. Preserve anchors and PAGEREF field structure.
- Heading 1 bookmarks `_Toc230171192`, `_Toc230171195`, `_Toc230171198`: replace only visible heading text; preserve bookmark wrappers and bottom rules.
- Exercise description paragraphs `[Description]`: replace with attendee-facing workshop summaries.
- Placeholder step/code/note blocks beneath each exercise: replace with numbered procedures, cloned code blocks, explanatory body paragraphs, and cloned note callouts. Additional cloned paragraphs are allowed inside each exercise to fit the complete workshop flow.
- Existing prerequisites, troubleshooting, Splunk Show access text, screenshots, links, and help callouts: preserve unchanged.

## Package preservation

- Preserve all 27 embedded-font and image parts, `customXml`, `docMetadata`, theme, styles, numbering, headers, footers, footnotes, endnotes, relationships, bookmarks, hyperlinks, and field codes unless a planned content replacement requires a document-body update.
- The only expected rewritten OOXML parts are those normally rewritten by `python-docx` for the body and package metadata. Verify that preserve-only media, header/footer, font, theme, numbering, custom XML, and relationship parts remain present.
- Set `w:updateFields=true` so TOC page references can refresh in Word. Do not flatten PAGEREF or PAGE fields.

## Fidelity gates

- The .conf26 banner, Splunk Show screenshots, callout styling, heading rules, page margins, and page-number footers remain recognizable and correctly positioned.
- Every original meaningful prerequisite, troubleshooting, portal-enrollment, and environment-access instruction remains present.
- No `[Title]`, `[Description]`, `[Step]`, placeholder SPL text, template author instruction, or unresolved session placeholder remains.
- All code blocks use Consolas and gray shading; notes use the cyan callout pattern.
- No clipped text, overlapping content, stranded headings, broken numbering, or unexpectedly blank pages.
- Render and inspect every final page at 100% zoom; compare with the reference using `render_and_diff.py`.
