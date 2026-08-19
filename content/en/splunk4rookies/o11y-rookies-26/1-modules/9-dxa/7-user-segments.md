---
title: 7. User Segments
weight: 7
time: 8 minutes
---

**User segments** group users by attributes (device type, location), session properties, or behaviors. Segments let you run targeted analyses — for example, comparing checkout conversion on mobile versus desktop — without rebuilding filters each time.

See [Create user segments](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/create-user-segments) for full details.

Segment definitions can combine:

- **User attributes** — device type, browser, geography
- **Session attributes** — session duration, entry page
- **User actions** — same criteria used in event definitions
- **Other segments** — nested segment references (circular references are not allowed)

{{% exercise title="Compare segments on the checkout funnel" %}}

1. Return to the **`Homepage to Order Confirmation`** funnel in the **Analyses** tab.
2. Note the drop-off pattern with the **All users** filter applied.
3. Switch the filter to a pre-built user segment. Your facilitator will confirm the segment name — common examples include **Mobile users** or **New users**.
4. Compare drop-off rates and segment sizes between **All users** and your selected segment.

<!-- TODO screenshot: Checkout funnel filtered by a user segment such as Mobile users, showing different drop-off rates than All users -->

![Checkout funnel filtered by a user segment showing segment-specific drop-off rates](images/funnel-segment-comparison.png)

{{< tabs >}}
{{% tab title="Question" %}}
When would segmenting by device type change your remediation priority?
{{% /tab %}}
{{% tab title="Answer" %}}
If mobile users drop off at checkout at a significantly higher rate than desktop users, you would prioritize mobile-specific fixes — responsive layout issues, payment form usability, or touch-target problems — before investing in desktop-only improvements. Segments turn a generic "checkout is broken" finding into a targeted action plan.
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

{{% notice title="Info" style="info" %}}
Once defined, a user segment can be reused across any analysis in the project. Create segments for the audiences you care about most — new users, high-value customers, campaign traffic — and compare their experience consistently over time.
{{% /notice %}}

You have now explored the core DXA workflow. Let's connect what you learned to business outcomes.
