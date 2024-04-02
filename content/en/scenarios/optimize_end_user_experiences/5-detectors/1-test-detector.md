---
title: Test Detectors
linkTitle: 1. Test Detectors
weight: 1
hidden: false
---

Why would we want a [detector on a single Synthetic test](https://docs.splunk.com/observability/en/synthetics/test-config/synth-alerts.html)? Some examples:
- The endpoint, API transaction, or browser journey is highly critical
- We have deployed code changes and want to know if the resulting KPI is or is not as we expect
- We need to temporarily keep a close eye on a specific change we are testing and don't want to create a lot of noise, and will disable the detector later
- We want to know about unexpected issues before a real user encounters them


1. On the test overview page, click {{% button %}}Create Detector{{% /button %}} on the top right.
![create detector on a single synthetic test](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/5ff84106-52ac-4519-8835-999446227709/user_cropped_screenshot.jpeg?tl_px=1144,0&br_px=2864,961&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=902,79)

1. Name the detector with your **team name** and your **initials** and **LCP** (the signal we will eventually use), so that the instructor can better keep track of everyone's progress.

1. Change the signal to First byte time.
![change the signal](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/e443d816-7608-4073-905f-45f36d189665/ascreenshot.jpeg?tl_px=440,240&br_px=2160,1201&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,276)

1. Change the alert details, and see how the chart to the right shows the amount of alert events under those conditions. This is where you can decide how much alert noise you want to generate, based on how much your team tolerates. Play with the settings to see how they affect estimated alert noise.
![alert noise preview](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/35b475b5-4e66-498d-971a-06c5368bc0ce/ascreenshot.jpeg?tl_px=0,233&br_px=1719,1194&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=404,277)

1. Now, **change the signal to Largest contentful paint**. This is a key web vital related to the user experience as it relates to loading time. Change the threshold to **2500ms**. It's okay if there is no sample alert event in the detector preview.

1. Scroll down in this window to see the notification options, including severity and recipients.
![notification options](../_img/detector-notifications.png)

1. Click the notifications link to customize the alert subject, message, tip, and runbook link.
![notification customization dialog](../_img/notification-custom.png)

1. When you are happy with the amount of alert noise this detector would generate, click Activate.
![activate the detector](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-16/6a80893a-fffc-475b-a22c-98c89c239095/ascreenshot.jpeg?tl_px=0,838&br_px=1719,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=168,451)