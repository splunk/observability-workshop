---
title: Single Page Browser Test
linkTitle:  3. Browser Test
weight: 3
hidden: false
---

We have started testing our endpoints, now let's test the front end browser experience.

Starting with a single page [browser test](https://docs.splunk.com/observability/en/synthetics/browser-test/browser-test.html) will let us capture how first- and third-party resources impact how our end users experience our browser-based site. It also allows us to start to understand our user experience metrics before introducing the complexity of multiple steps in one test.

A page where your users commonly "land" is a good choice to start with a single page test. This could be your site homepage, a section main page, or any other high-traffic URL that is important to you and your end users. 

1. Click {{% button style="blue" %}}Add new test{{% /button %}} and select Browser test<p></p>
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-09/e75aa6a0-c7f2-4e6d-86cf-3da32e0a087c/ascreenshot.jpeg?tl_px=1160,489&br_px=2880,1450&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=936,276)

2. Use the test Name and Custom properties to describe the scope of the test. Then click {{< button >}}+ Edit steps{{< /button >}}<p></p>
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-09/8e3f2a3f-31b3-49b5-9bd1-735775d84652/ascreenshot.jpeg?tl_px=137,197&br_px=1856,1158&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,276)

3. Change the transaction label (top left) and step name (on the right) to something readable that describes the step. Add the URL you'd like to test. Your workshop instructor can provide you with a URL as well. In the below example, the transaction is "Home" and the step name is "Go to homepage".<p></p>
![Transaction and step label](../_img/single-step.png)

4. To validate the test, change the location as needed and click {{< button >}}Try now{{< /button >}}. See the docs for more information on the [try now feature](https://docs.splunk.com/observability/en/synthetics/test-config/try-now.html).<p></p>
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-09/e2d14ced-1538-4a58-9f90-0e71b17724ee/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1236,684&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=395,134)

5. Wait for the test validation to complete. If the test validation failed, double check your URL and test location and try again. With {{< button >}}Try now{{< /button >}} you can see what the result of the test will be if it were saved and run as-is.<p></p>
![Try Now browser test results](../_img/try-now.png)

6. Click {{% button style="blue" %}}< Return to test{{% /button %}} to continue the configuration.<p></p>
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-09/a0d97692-7e01-45da-b8b6-7ea3e8bda236/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1268,699&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=232,116)

7. Edit the locations you want to use, keeping in mind any regional rules you have for your site.<p></p>
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-09/5eb326ef-6214-4b98-9e57-073dded99f58/ascreenshot.jpeg?tl_px=0,451&br_px=1719,1412&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=491,277)

8. You can edit the Device and Frequency or leave them at their default values for now. Click {{% button style="blue" %}}Submit{{% /button %}} to save the test and start running it.<p></p>
![](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-09/a37a8de3-b1d2-4edc-929e-0ee9994d646a/ascreenshot.jpeg?tl_px=0,838&br_px=1719,1799&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=133,559)

While our Synthetic tests are running, let's see how RUM is instrumented to start getting data from our real users!