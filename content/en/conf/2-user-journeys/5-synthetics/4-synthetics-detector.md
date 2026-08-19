---
title: 4. Synthetics Detector
weight: 4
---

Given you can run these tests 24/7, it is an ideal tool to get warned early if your tests are failing or starting to run longer than your agreed SLA—instead of getting informed by social media or uptime websites.

![Social media](../images/social-media-post.png)

To stop that from happening, let's detect if our test is taking more than 50 seconds.

{{% exercise title="Getting Alerted" %}}

* Go to **Digital Experience → Synthetics tests** from the main menu.
* Select the workshop test **[NAME OF WORKSHOP]**.
* Click on the test.
* Click {{% button %}}**Create Detector**{{% /button %}} button at the top of the page:
* Change the alert criteria so that the metric is **Run Duration** **(1)** (instead of Uptime) and the condition is **Static Threshold**.
* Set the **Trigger threshold** **(2)** to be around `50000` ms.
* Set **Split by location** **(3)** to **No**.
* Note that there is now a row of red and white triangles appearing below the spikes in the chart.
* The red triangles let you know that your detector found that your test was above the given threshold and the white triangle indicates that the result returned below the threshold. Each red triangle will trigger an alert.

> [!WARNING] We will not add a recipient or activate the detector as we don't want to flood your email with alerts.

![Detector](../images/synth-detector.png)

This application is designed to fail often, hence the large number of alerts that would be generated. In a real-world scenario, you would want to fine-tune the threshold to avoid false positives.

{{% /exercise %}}