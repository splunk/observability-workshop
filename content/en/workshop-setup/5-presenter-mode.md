---
title: 5. Presenter Mode
weight: 5
---

##### **What is Presenter Mode?**

Presenter mode reveals delivery cues — timing hints, "kick this off in the background now" prompts, and other guidance for the person running the workshop — that are hidden from attendees by default. Notes are authored inline alongside the step they relate to, so you see them in context while presenting.

---

##### **Turning Presenter Mode On**

Append `?presenter=1` to **any** workshop URL and load the page once. For example:

```text
https://splunk.github.io/observability-workshop/en/?presenter=1
```

After that, a magenta **Presenter on** pill appears in the bottom-right corner of every page, and presenter notes become visible. The setting is remembered in your browser, so you only need to do this once per device.

{{% notice style="tip" title="Bookmark it" %}}
Bookmark the workshop home page with `?presenter=1` already in the URL. Opening that bookmark on a fresh browser/device flips presenter mode on for you.
{{% /notice %}}

---

##### **Turning Presenter Mode Off**

Click the magenta **Presenter on** pill in the bottom-right corner. The pill disappears and the notes are hidden again.

---

##### **Authoring Presenter Notes**

Wrap any guidance in the `presenter` shortcode. The note can contain regular Markdown (lists, code, links, images):

```markdown
{{</* presenter */>}}
Start the EC2 instance now — boot takes ~3 minutes.
{{</* /presenter */>}}

{{</* presenter title="Timing" */>}}
Allow ~10 minutes for attendees to finish this section.
{{</* /presenter */>}}
```

The optional `title` attribute changes the small label at the top of the note (defaults to "Presenter note").

Here's a live example — you'll only see it rendered if you're currently in presenter mode:

{{< presenter title="Example" >}}
This is what a presenter note looks like. If you can read this, presenter mode is on.
{{< /presenter >}}

---

##### **What Attendees See**

Nothing. The notes are not rendered, and the toggle pill is not displayed for them.

{{% notice style="warning" title="Hidden, not secret" %}}
Presenter notes are hidden via CSS but they **are** present in the page's HTML source. Use this feature for delivery cues and timing — do **not** use it for answer keys, credentials, or anything you genuinely need to keep from attendees.
{{% /notice %}}
