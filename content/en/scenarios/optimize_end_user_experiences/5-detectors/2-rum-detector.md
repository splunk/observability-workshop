---
title: RUM Detectors
linkTitle: 2. RUM Detectors
weight: 2
hidden: false
---

Let's say we want to know about an issue in production without waiting for a ticket from our support center. This is where [creating detectors in RUM](https://docs.splunk.com/observability/en/rum/rum-alerts.html) will be helpful for us.


1. Go to the RUM overview of our App. Scroll to the LCP chart, click the chart menu icon, and click Create Detector.
![RUM LCP chart with action menu flyout](../_img/rum-lcp.png)

1. Rename the detector to include your **team name** and **initials**, and change the scope of the detector to App so we are not limited to a single URL or page. Change the threshold and sensitivity until there is at least one alert event in the time frame.
![RUM alert details](../_img/rum-detector.png)

1. Change the alert severity and add a recipient if you'd like, and click {{% button style="blue" %}}Activate{{% /button %}} to save the Detector.

{{% notice title="Exercise" style="green" icon="running" %}}
Now, your workshop instructor will change something on the website. How do you find out about the issue, and how do you investigate it?
{{% /notice %}}

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
Wait a few minutes, and take a look at the online store homepage in your browser. How is the experience in an incognito browser window? How is it different when you refresh the page?
{{% /notice %}}





