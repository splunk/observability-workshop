---
title: Synthetics Home Page
linkTitle: 2. Synthetics Home Page
weight: 2
---

{{% button icon="clock" color="#ed0090" %}}2 minutes{{% /button %}}
(remove ninja stuff , general padding screen shot rmove 4)
Click on **Synthetics** in the main menu. This will bring us to the Synthetics Home Page. It has 3 distinct sections that provide either useful information or allow you to pick or create a Synthetic Test.

![Synthetic main](../images/synthetics-main.png)

1. **Onboarding Pane:** Training videos and links to documentation to get you started with Splunk Synthetics.
2. **Test Pane:** List of all the tests that are configured (**Browser**, **API** and **Uptime**)
3. **Create Test Pane:** Drop-down for creating new Synthetic tests.
4. **Private Locations & Global Variables:** Manage your [**Private locations**](https://docs.splunk.com/observability/en/synthetics/test-config/private-locations.html) and [**Global variables**](https://docs.splunk.com/observability/en/synthetics/test-config/global-variables.html).
(Ninja remove)
As part of the workshop we have created a default browser test against the application we are running, You find it in the Test Pane (2). It will have the following name **Workshop Browser Test for**, followed by the name of your Workshop (your instructor should have provided that to you).

To continue our tour, let's look at the result of our workshop's automatic browser test.  

{{% notice title="Exercise" style="green" icon="running" %}}

* In the Test Pane, double-click on the line that contains the name of your workshop. The result should look like this:

![Synthetics-overview](../images/synthetics-test-overview.png)

* Note, On the Synthetic Tests Page, the first pane will show the performance of your site for the last day, 8 days and 30 days. As shown in the screenshot above, only if a test started far enough in the past, the corresponding chart will contain data. For the workshop, this depends on when it was created for you and if there is any data.
* In the Performance KPI drop-down, change the time from the default 4 hours to the 1 last hour.  
* What can you conclude from the dotted chart, how often are these tests run, and from where?
{{% /notice %}}

Now let’s examine the infrastructure our application is running on using Splunk Infrastructure Monitoring (IM).
