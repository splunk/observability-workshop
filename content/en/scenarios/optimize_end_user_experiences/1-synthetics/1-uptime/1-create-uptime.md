---
title: Creating a test
linkTitle: 1.1 Creating a test
weight: 1
---

1. Open Synthetics
![o11y nav with Synthetics icon highlighted](../_img/o11y-nav-syn.png)

1. Click the {{% button style="blue" %}}Add new test{{% /button %}} button on the right side of the screen, then select Uptime and HTTP test.
![image](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-01/1457c466-904f-4801-b06a-0062a3ea321a/ascreenshot.jpeg?tl_px=1160,671&br_px=2880,1632&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=632,276)

1. Name your test with your **team name** (provided by your workshop instructor), your initials, and any other details you'd like to include, like geographic region.

1. For now let's test a **GET** request. Fill in the URL field. You can use one of your own, or one of ours like [https://frontend-eu.splunko11y.com](https://frontend-eu.splunko11y.com), [https://frontend-us.splunko11y.com](https://frontend-us.splunko11y.com), or [https://www.splunk.com](https://www.splunk.com).

1. Click {{% button %}}Try now{{% /button %}} to validate that the endpoint is accessible before the selected location before saving the test. {{% button %}}Try now{{% /button %}} does not count against your subscription usage, so this is a good practice to make sure you're not wasting real test runs on a misconfigured test.
![image](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-01/4168460c-aa9e-4c47-b856-eab08ff0425d/ascreenshot.jpeg?tl_px=0,521&br_px=1719,1482&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=452,277)
{{% notice title="Tip" style="primary"  icon="lightbulb" %}}A common reason for {{% button %}}Try now{{% /button %}} to fail is that there is a non-2xx response code. If that is expected, add a Validation for the correct response code.{{% /notice %}}

1. Add any additional validations needed, for example: response code, response header, and response size.
![Advanced settings for test configuration](../_img/uptime-security.png)

1. Add and remove any locations you'd like. Keep in mind where you expect your endpoint to be available.

1. Change the frequency to test your more critical endpoints more often, up to one minute.
![image](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-01/74e0492f-13a5-4a93-9f3c-f1f311d3dd8a/ascreenshot.jpeg?tl_px=0,560&br_px=1719,1521&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=385,277)

1. Make sure "Round-robin" is on so the test will run from one location at a time, rather than from all locations at once. 
   - If an endpoint is **highly** critical, think about if it is worth it to have all locations tested at the same time every single minute. If you have automations built in with a webhook from a detector, or if you have strict SLAs you need to track, this *could* be worth it to have as much coverage as possible. But if you are doing more manual investigation, or if this is a less critical endpoint, you could be wasting test runs that are executing while an issue is being investigated.
   - Remember that your license is based on the number of test runs per month. Turning Round-robin off will multiply the number of test runs by the number of locations you have selected.

1. When you are ready for the test to start running, make sure "Active" is on, then scroll down and click {{% button style="blue" %}}Submit{{% /button %}} to save the test configuration. 
![image](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-01/404871c6-55cd-40e0-83a2-a9a12dd183ce/ascreenshot.jpeg?tl_px=0,838&br_px=1719,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=134,553)

Now the test will start running with your saved configuration. Take a water break, then we'll look at the results!
