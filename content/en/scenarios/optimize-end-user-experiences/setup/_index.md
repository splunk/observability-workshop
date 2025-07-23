---
title: Workshop Setup and Cleanup
weight: 99
linkTitle: Workshop Instructions
hidden: true
---

Please follow these steps for the Optimize End User Experiences workshop setup, "behind the scenes" instructions during the workshop, and cleanup.

## Before the workshop

1. See instructions on using [**SWiPE**](../../workshop-setup/1-swipe.md) for provisioning.
1. Come up with a simple **team name** that your attendees will use when naming dashboards, detectors, and synthetic tests. This is intended to help **you** during cleanup later. For example, a specific dog breed, flower name, etc.
   1. Remind attendees throughout the workshop to include the team name and their initials when they are creating asset names.
1. [**Create a SynCreator account**](https://splunko11y.com/syncreator/auth/register) if you do not have one already
   1. Click "Enable RUM" on the top right of the SynCreator screen. Enter your realm and your RUM token and save the form.
   1. Access your **Syncreator browser site URL** which is linked on the left side of the SynCreator screen. Perform some interactions and close your browser session, and make sure the data starts coming into RUM in your o11y org. Check the site's `<head>` code to make sure the RUM instrumentation is there.
   1. Start with the Default condition active in Syncreator.
1. Download the dashboard group and import into the workshop org if it's not already there. Participants will clone and edit this dashboard in section 4.

{{% resources sort="asc" style="primary" title="Download Dashboard Group JSON" /%}}

## During the workshop

1. Provide the **team name** and **SynCreator browser site URL** to your attendees.
1. Once everyone has saved both their [**RUM LCP detector**](../optimize_end_user_experiences/5-detectors/2-rum-detector.md) and their [**synthetic test detector**](../optimize_end_user_experiences/5-detectors/1-test-detector.md), **change the SynCreator condition to Hero Image**. This will mimic a large image being used on the homepage, which will spike the LCP metric. There is an exercise built in at the end of the [**RUM detector instructions**](../optimize_end_user_experiences/5-detectors/2-rum-detector.md).

## After the workshop

1. Please follow the [**cleanup**](../../workshop-setup/3-clean-up.md) instructions.
1. Please also use SWiPE to delete the [**detectors**](https://swipe.splunk.show/Delete_Detectors) and [**synthetic tests**](https://swipe.splunk.show/Delete_Synthetic_Tests) created in your workshop. Per the instructions, attendees should have included your "team name" and their initials in the asset names.
