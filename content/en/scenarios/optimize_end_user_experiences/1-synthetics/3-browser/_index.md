---
title: Single Page Browser Test
linkTitle:  3. Browser Test
weight: 3
time: 5 minutes
---

We have started testing our endpoints, now let's test the front end browser experience.

Starting with a single page [browser test](https://docs.splunk.com/observability/en/synthetics/browser-test/browser-test.html) will let us capture how first- and third-party resources impact how our end users experience our browser-based site. It also allows us to start to understand our user experience metrics before introducing the complexity of multiple steps in one test.

A page where your users commonly "land" is a good choice to start with a single page test. This could be your site homepage, a section main page, or any other high-traffic URL that is important to you and your end users. 

1. Click {{% button style="blue" %}}Create new test{{% /button %}} and select Browser test
![Create new browser test](../_img/create-browser.png)

2. Include your **team name** and **initials** in the test name. Add to the Name and Custom properties to describe the scope of the test (like Desktop for device type). Then click {{< button >}}+ Edit steps{{< /button >}}
![Browser test content fields](../_img/browser-name.png)

3. Change the transaction label (top left) and step name (on the right) to something readable that describes the step. Add the URL you'd like to test. Your workshop instructor can provide you with a URL as well. In the below example, the transaction is "Home" and the step name is "Go to homepage".
![Transaction and step label](../_img/single-step.png)

4. To validate the test, change the location as needed and click {{< button >}}Try now{{< /button >}}. See the docs for more information on the [try now feature](https://docs.splunk.com/observability/en/synthetics/test-config/try-now.html).
![browser test try now buttons](../_img/browser-try-now.png)

5. Wait for the test validation to complete. If the test validation failed, double check your URL and test location and try again. With {{< button >}}Try now{{< /button >}} you can see what the result of the test will be if it were saved and run as-is.
![Try Now browser test results](../_img/browser-try-now-result.png)

6. Click {{% button style="blue" %}}< Return to test{{% /button %}} to continue the configuration.
![Return to test button](../_img/return.png)

7. Edit the locations you want to use, keeping in mind any regional rules you have for your site.<p></p>
![Browser test details](../_img/browser-test-details.png)

8. You can edit the Device and Frequency or leave them at their default values for now. Click {{% button style="blue" %}}Submit{{% /button %}} at the bottom of the form to save the test and start running it.<p></p>
![browser test submit button](../_img/browser-submit.png)

{{% notice title="Bonus Exercise" style="green" icon="running" %}}
Have a few spare seconds? Copy this test and change just the title and device type, and save. Now you have visibility into the end user experience on another device and connection speed!
{{% /notice %}}

While our Synthetic tests are running, let's see how RUM is instrumented to start getting data from our real users.