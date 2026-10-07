---
title: 3. Event Definitions
weight: 3
---

**Event definitions** are the foundation of DXA analyses. They name and filter user interactions — clicks, navigation, errors, and custom events — so we can track the same behavior consistently across funnels, time series, and segments.

See [Create and manage event definitions](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/create-and-manage-event-definitions) for full details.

## Event categories

DXA recognizes four event categories:

| Category | Examples |
|----------|----------|
| **Interaction** | Click, tap, rage click |
| **Navigation** | Route change, document load, screen name change |
| **Error** | JavaScript error, application crash |
| **Custom** | User-defined events from our application |

## Filter templates

Event definitions use filter templates to match real user actions:

- **Click on element** — matches `click` events by `target_xpath`
- **Click on text** — matches `click` events by `target_text` (for example, "Show All Reviews")
- **Visited URL** — matches navigation events by `url.full`
- **Custom** — matches any ingested event name

The **element picker** lets product teams define click events by selecting elements directly on a live page — no code changes required. We will explore pre-built definitions in this exercise rather than creating new ones.

{{% exercise title="Explore pre-built event definitions" %}}

1. In the Astronomy Shop DXA project, select the **Event Definitions** tab.
2. Review the list of pre-built definitions. Look for events related to:
   - **Ask AI** interactions and quick prompts
   - Checkout steps (homepage, product page, cart, place order, order confirmation)
3. Select one definition and review its filter criteria — note how event category and tags define what counts as that event.
4. Check the **Occurrences** preview to see matching events from real workshop sessions.

![List of event definitions for Ask AI quick prompts](../images/event-definitions.png)

{{< quiz question="Your marketing team launches a newsletter signup campaign. What event definition would you create, and which filter template would you likely use?" >}}
{{< quiz-option correct=true >}}A Newsletter Signup event, using Click on text, Click on element, or Custom.{{< /quiz-option >}}
{{< quiz-option >}}A page-load event for the home page.{{< /quiz-option >}}
{{< quiz-option >}}No event is needed. RUM already counts every click.{{< /quiz-option >}}
{{< quiz-feedback >}}
You would create a custom event definition named something like **Newsletter Signup**. Depending on implementation, you might use **Click on text** (matching a "Subscribe" button label) or **Click on element** (matching the signup button's XPath). If the app emits a custom event on successful signup, you would use the **Custom** template instead. The same definition can then be reused across multiple analyses and funnels.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

These event definitions power the analyses we will explore next — starting with feature adoption.
