---
title: Chart Detectors
linkTitle: Chart Detectors
weight: 3
hidden: false
---

With our custom dashboard charts, we can create detectors focussed directly on the data and conditions we care about. In building our charts, we also built signals that can trigger alerts.

## Static detectors

For many KPIs, we have a static value in mind as a threshold. 

1. In the End User Experience dashboard, scroll down to the Syncreator Web Vitals chart. 

1. Click the bell icon on the top right of the Syncreator Web Vitals chart, and select "New detector from chart"
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/2e7a0adf-f4f7-4183-b7e9-08bbe7350232/ascreenshot.jpeg?tl_px=1160,297&br_px=2880,1258&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=886,277)

2. Change the detector name to include your **team name** and **initials**, and adjust the alert details.
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/4a6f44da-2559-49bf-8c5a-a58220c6e64d/ascreenshot.jpeg?tl_px=0,152&br_px=1719,1113&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=444,277)

3. Change the severity, and add yourself as a recipient before you save this detector.
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/1c2a7f23-c076-45e8-80b0-3a99e3989048/user_cropped_screenshot.jpeg?tl_px=0,652&br_px=1719,1614&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=216,453)

## Dynamic detectors

Sometimes we have metrics that vary naturally, so we want to create a more dynamic detector that isn't limited by the static threshold we decide in the moment.

1. To create dynamic detectors on your chart, click the link to the "old" detector wizard.
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/877e9402-3634-4b44-8585-fe27331674c6/user_cropped_screenshot.jpeg?tl_px=901,0&br_px=2621,961&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,109)

1. Change the detector name to include your **team name** and **initials**, and Click {{% button style="blue" %}}Create alert rule{{% /button %}}
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/fa9714b1-1fa0-47c4-9361-5753c0c5d4b4/ascreenshot.jpeg?tl_px=978,191&br_px=2698,1152&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,277)

1. Confirm the signal looks correct and proceed to Alert condition.
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/d8dc6a69-f559-4399-b71d-583555266e35/ascreenshot.jpeg?tl_px=0,630&br_px=1719,1591&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=246,277)

4. Select the "Sudden Change" condition and proceed to Alert settings
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/3a4e5b88-befc-4af8-8736-5f4a5529d0aa/ascreenshot.jpeg?tl_px=0,838&br_px=1719,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=486,340)

5. Play with the settings and see how the estimated alert noise is previewed in the chart above. Tune the settings, and change the advanced settings if you'd like, before proceeding to the Alert message.
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/8a01627f-2287-494e-a2a3-20ff1592b641/ascreenshot.jpeg?tl_px=381,782&br_px=2101,1743&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,277)

25. Customize the secerity, runbook URL, any tips, and message payload before proceeding to add recipients.
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/0af4f210-2202-4daf-9754-c8719867b388/ascreenshot.jpeg?tl_px=94,838&br_px=1813,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,485)

26. For the sake of this workshop, only add your own email address as recipient. This is where you would add other options like webhooks, ticketing systems, and Slack channels if it's in your real environment.
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/006bf87f-d5cb-4b17-9658-4f381aff9c9e/ascreenshot.jpeg?tl_px=87,838&br_px=1807,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,457)

27. Finally, confirm the detector name before clicking {{% button style="blue" %}}Activate Alert Rule{{% /button %}}
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-17/146b3a5c-3c08-4fe8-a3fb-af44176963ca/ascreenshot.jpeg?tl_px=1160,838&br_px=2880,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=890,468)

