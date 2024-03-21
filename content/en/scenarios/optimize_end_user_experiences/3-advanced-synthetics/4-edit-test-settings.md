---
title: 1.4 Settings
weight: 4
---

The simple settings allow you to configure the basics of the test:

- **Name**: The name of the test (e.g. RWC - Online Boutique).
- **Details**:
  - **Locations**: The locations where the test will run from.
  - **Device**: Emulate different devices and connection speeds. Also, the viewport will be adjusted to match the chosen device.
  - **Frequency**: How often the test will run.
  - **Round-robin**: If multiple locations are selected, the test will run from one location at a time, rather than all locations at once.
  - **Active**: Set the test to active or inactive.

![Return to Test]For this workshop, we will configure the locations that we wish to monitor from. Click in the **Locations** field and you will be presented with a list of global locations (over 50 in total).

![Global Locations](../../_img/global-locations.png)

Select the following locations:

- **AWS - N. Virginia**
- **AWS - London**
- **AWS - Melbourne**

Once complete, scroll down and click on Click on {{% button style="blue" %}}Submit{{% /button %}} to save the test.

The test will now be scheduled to run every 5 minutes from the 3 locations that we have selected. This does take a few minutes for the schedule to be created.

So while we wait for the test to be scheduled, click on {{% button %}}Edit test{{% /button %}} so we can go through the Advanced settings.
