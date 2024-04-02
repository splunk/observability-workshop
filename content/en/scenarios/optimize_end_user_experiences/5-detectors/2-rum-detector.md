---
title: RUM Detectors
linkTitle: 2. RUM Detectors
weight: 2
hidden: false
---

Let's say we want to know about an issue in production without waiting for a ticket from our support center. This is where [creating detectors in RUM](https://docs.splunk.com/observability/en/rum/rum-alerts.html) will be helpful for us.


1. Go to the RUM view of the Syncreator App. Scroll to the LCP chart, click the chart menu icon, and click Create Detector.
![chart options icon](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/4e83e000-969f-4e5f-8034-d7d7a606a48b/ascreenshot.jpeg?tl_px=115,569&br_px=1835,1530&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,276)<br/>
![create detector option](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/0f8e3c7f-9b8a-4603-9a78-f3112550d82e/ascreenshot.jpeg?tl_px=5,575&br_px=1724,1536&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,276)

1. Rename the test to include your **team name** and **initials**, and change the scope of the detector to App so we are not limited to a single URL or page. Change the threshold and sensitivity until there is at least one alert event in the time frame.
![alert details](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/d3acb0d8-2d37-4efb-ab00-291fd80c6f74/ascreenshot.jpeg?tl_px=0,284&br_px=1719,1245&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=427,277)

1. Change the alert severity and add a recipient if you'd like, and click Activate to save the Detector.
![activate the RUM detector](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/ea3895cc-f7fb-419a-aed6-d3a944b0131a/ascreenshot.jpeg?tl_px=0,838&br_px=1719,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=140,464)

{{% notice title="Exercise" style="green" icon="running" %}}
Now, your workshop instructor will change something on the website. How do you find out about the issue, and how do you investigate it?
{{% /notice %}}

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
Wait a few minutes, and take a look at the online store homepage in your browser. How is the experience in an incognito browser window? How is it different when you refresh the page?
{{% /notice %}}





