---
title: 6. Create Detector
weight: 6
---

{{% exercise title=" Preview a run-duration detector" %}}

* As you did earlier in this exercise, go to **Digital Experience** → **Synthetics tests**, *search* for your *workshop* name, and open your workshop’s *browser test*.
* Select {{% button %}}**Create Detector**{{% /button %}} button at the top of the test  page.
* Set the metric to **Run duration (1)** and the condition to **Static threshold (2)**.
* Set the **Trigger threshold (3)** to `50000 ms`. This represents a run duration of *50* seconds.
Set **Split by location (4)** to **No** so the detector evaluates the test across all configured locations.

The main chart compares the test’s run duration with the 50-second threshold. The shaded area represents values above the threshold, while the **yellow markers (5)** indicate detector events during the displayed period.

The **1m** label in the chart indicates that the data is displayed at one-minute resolution. The **lower timeline (6)** provides a longer historical view, and the **blue selection window (7)** shows the time range currently displayed in the main chart.

> [!WARNING] Do not add a recipient, activate, or save this detector. The workshop application is intentionally generating frequent slow runs, which could produce a large number of alerts.

![Detector](../images/synth-detector.png)

* In a production environment, you would tune the threshold and alert conditions to reflect normal application performance and avoid unnecessary alerts.

{{% /exercise %}}

When you have finished reviewing the preview, select **X** in the upper-right corner to close it without saving the detector.