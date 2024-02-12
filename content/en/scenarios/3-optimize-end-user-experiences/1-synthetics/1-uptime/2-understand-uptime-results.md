---
title: 1.2 Understanding results
weight: 2
---

1. Click into a test summary view and play with the Performance KPIs chart filters to see how you can slice and dice your data. This is a good place to get started understanding trends in your data. Later we will see what custom charts look like, so that you can have a consistent view of what you care about most.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
How does the data look? Is it consistent across time and locations? Do certain locations run slower than others? Are there any spikes or failures?
{{% /notice %}}

![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-09/c040b5f6-a868-4977-8d3b-bc3e431ffcc8/user_cropped_screenshot.jpeg?tl_px=1160,0&br_px=2880,961&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=755,44)

2. How's your test running? Click into a recent run either in the chart or in the table below. If there are failures, look at the response to see if you need to add a response code assertion (302 is a common one), if there is some authorization needed, or something else.

![image](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-01/dd23b173-e567-4858-997e-bdcc5233d4e4/ascreenshot.jpeg?tl_px=0,838&br_px=1719,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=167,363)

3. Here we have information about this particular test run including if it succeeded or failed, the location, timestamp, and duration in addition to the other Uptime test metrics. Click through to see the response, request, and connection info as well.

![image](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-01/719d3bab-606e-4f67-9f2d-2835f0d136af/ascreenshot.jpeg?tl_px=0,240&br_px=1719,1201&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=216,276)

4. Once you have your Uptime test running successfully, let's move on to the next test type.
