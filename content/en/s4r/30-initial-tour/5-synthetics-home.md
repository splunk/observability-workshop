---
title: Splunk Synthetics Home Page
linkTitle: 5. Synthetics Home Page
description: This section of the workshop will equip you with a basic understanding of the Synthetics UI
weight: 50
---

{{% button icon="clock" %}}5 minutes{{% /button %}}

If you have not done so yet, select Splunk Synthetic from the menu bar on the right by selecting the (the robot icon) ![syntheticsMenu](../../images/synthetics-icon.png?classes=inline&height=25px). This will bring us to the Synthetic Home Page. It has 3 distinct sections that provide either useful information or allow you to pick or create a Synthetic Test.

![Synthetic main](../../8-synthetics/images/synthetics-main.png?width=40vw)

* 1. **Onboarding Pane:** Here you will find videos and information related to Splunk Synthetics. (Can be closed by pressing the X, if space is a premium)
* 2. **Test Pane:** Here you find the list of all the tests that are active in your org, and you can select them to see the results.
* 3. **Create Test Pane:** This drop-down pane gives you the option to create a new Synthetic test.

As part of the workshop we have created a default browser test against the application we are running, You find it in the Test Pane (2). It will have the following name **Workshop Browser Test for**, followed by the name of your Workshop (your instructor should have provided that to you).

To continue our tour, let's look at the result of our workshop's automatic browser test.  
{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* In the Test Pane, double-click on the line that contains the name of your workshop. The result should look like this:

![Synthetics-overview](../../8-synthetics/images/synthetics-test-overview.png?width=40vw)

* Note, On the Synthetic Tests Page, the first pane will show the performance of your site for the last day, 8 days and 30 days. As shown in the screenshot above, only if a test started far enough in the past, the corresponding chart will contain data. For the workshop, this depends on when it was created for you and if there is any data.
* In the Performance KPI Drop down box, change the time from the default 8 hours to last hour.  
  What can you conclude from the dotted chart, how often are these tests run, and from where?
* Click on a dot in the chart. This should bring you to a new screen. This is the detailed Test Run Results page for the selected test. We will examine this page in great detail later in the workshop, so for now  go back to the Synthetic Home page by clicking on the (the robot icon) ![syntheticsMenu](../../images/synthetics-icon.png?classes=inline&height=25px).

{{% /notice %}} Let's continue to Infra mon and examine the infrastructure our application is running on.
