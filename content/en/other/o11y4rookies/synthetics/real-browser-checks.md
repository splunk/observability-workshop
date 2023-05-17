---
title: Real Browser Checks
linkTitle: 1. Real Browser Checks
weight: 2
---

This Lab walks your through using the [Chrome Selenium IDE](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd?hl=en) extension to create a synthetic transaction against a Splunk demo instance and creating a Splunk Synthetic Monitoring Real Browser Check (RBC). In addition you also get to learn other Splunk Synthetic Monitoring checks like REST API checks and Uptime Checks.

## 1. Prerequisites

Ensure you can login with your username and password at [https://monitoring.rigor.com](https://monitoring.rigor.com) and [https://optimization.rigor.com](https://optimization.rigor.com). Also, make sure you are assigned to your own account for example: **O11y Workshop**.

Edit your Splunk Synthetic Monitoring account personal information and adjust your timezone and email notifications. Splunk Synthetic Monitoring will default to start sending you notifications, you can turn them off at the monitor configuration level.

![Edit Personal Information](../../../../synthetics/images/image5.png)

Add the [Chrome Selenium IDE](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd?hl=en-US) extension to your **Chrome** Browser. Once installed click on the extension and you will see the following screen:

![Selenium IDE](../../../../synthetics/images/image17.png)

## 2. Using Selenium IDE

You can now go ahead and record a web transaction using Selenium IDE to check on [http://splunk.o11ystore.com](http://splunk.o11ystore.com).

Click on **Record a new test in a new project**, name the project **[YOUR_INITIALS] - O11y Store** e.g. RWC - O11y Store.

!!! question "What is Selenium IDE?"
    - Selenium IDE is an open source record and playback test automation for the web.
    - Selenium is a portable framework for testing web applications.
    - Selenium provides a playback tool for authoring functional tests without the need to learn a test scripting language (Selenium IDE).
    - It also provides a test domain-specific language (Selenese) to write tests in a number of popular programming languages, including C#, Groovy, Java, Perl, PHP, Python, Ruby and Scala.
    - The tests can then run against most modern web browsers.
    - Selenium runs on Windows, Linux, and macOS.
    - It is open-source software released under the Apache License 2.0.

![placeholder](../../../../synthetics/images/image29.png)

Enter [http://splunk.o11ystore.com](http://splunk.o11ystore.com) as your base URL.

![placeholder](../../../../synthetics/images/image11.png)

 Click {{% button style="grey" %}}Start Recording{{% /button %}}, a new window should open up with [splunk.o11ystore.com](http://splunk.o11ystore.com). Click **Vintage Camera Lens**, click **Add To Cart** and then click **Place Order**.

Close the window and then stop the recording by navigating back to Selenium IDE. Finally name the test: **[YOUR_INITIALS] - Checkout Flow (Desktop)** e.g. RWC - Checkout Flow (Desktop).

![placeholder](../../../../synthetics/images/image10.png)

Your Selenium IDE Project will look something like this:

![placeholder](../../../../synthetics/images/image19.png)

Test your recording by pressing on the play button, make sure your recording successfully completes the transaction:

![Run](../../../../synthetics/images/image26.png)

Save your Selenium IDE Project to your Downloads folder as `Workshop.side`

![Save](../../../../synthetics/images/image30.png)

![Save SIDE Project](../../../../synthetics/images/save-side-project.png)

## 3. Create Real Browser Check

Login to Splunk Synthetic Monitoring using [https://monitoring.rigor.com](https://monitoring.rigor.com). Click on **REAL BROWSER** and click **+New**{: .label-button .sfx-ui-button-blue}.

![placeholder](../../../../synthetics/images/image3.png)

Click on "**From File**" and select your recording then click on Import

![placeholder](../../../../synthetics/images/image1.png)

Set the **Frequency** to **5 Minutes**

![placeholder](../../../../synthetics/images/image15.png)

Click on Steps and make the following adjustments to your recording provide a friendly name to Steps 1 (Click Camera), 2 (Add to Cart) & 3 (Place Order).

![placeholder](../../../../synthetics/images/image6.png)

Next, click **+ Add Step**, with this new step we will add some validation to the monitor. This is to ensure the checkout completed successfully.

Enter **Confirm Order** for the **Name** and change the **Action** to **Wait for text present** and finally enter **Your order is complete!** for the **Value**. You will now have a **Start Url** and 4 steps in your monitor configuration.

![placeholder](../../../../synthetics/images/image2.png)

{{% notice title="Tip" color="info" %}}
As you are creating the steps think about how to go about using the **Business Transaction** feature in Splunk Synthetic Monitoring which is very powerful.

*"Business Transactions are a combined group of contiguous steps in a Real Browser script that are to be measured as a whole. These transactions logically group similar parts of a flow together, so that users can view the performance of multiple steps and page(s) grouped under one Business Transaction."*
{{% /notice %}}

Click on **Advanced** and make sure the **Viewport Size** is set to **Default desktop: 1366 x 768**

![Viewport Size](../../../../synthetics/images/viewport-size.png)

Click on "**Test**" to test your monitor. Once the test has successfully completed make sure to click on "**AFTER**" in Step 4 to validate the monitor was able to get to the order complete screenshot.

![placeholder](../../../../synthetics/images/image22.png)

Click on **Create**{: .label-button .sfx-ui-button-blue} to save your Real Browser Monitor. After 5-10 minutes validate your monitor is working and producing successful checks e.g.

![placeholder](../../../../synthetics/images/image27.png)

{{% notice title="Tip" color="info" %}}
You can force to run your monitor now using **Run Now**

![placeholder](../../../../synthetics/images/image8.png)
{{% /notice %}}

Change your view to **Segment by location** and observe the difference. You can turn off/on locations by clicking on them.

!!! question "Question?"
    Which Location has the poorest **Response Time**?

![placeholder](../../../../synthetics/images/image9.png)

Click on one of the successful circles to drill-down into that Run:

![placeholder](../../../../synthetics/images/image33.png)

Take a moment to explore the metrics with the **CONFIGURE METRICS/HIDE METRICS** dropdown.

![placeholder](../../../../synthetics/images/image14.png)

Click **Page 2** in the dropdown, and scroll down to view the **Filmstrip** and the **Waterfall Chart.**

![placeholder](../../../../synthetics/images/image16.png)

![Filmstrip](../../../../synthetics/images/filmstrip.png)

![Waterfall](../../../../synthetics/images/waterfall.png)

Click on **Click Here to Analyze with Optimization** which will prompt you to login to your Splunk Synthetic Monitoring Optimization Account. If you **don't have this option**, navigate to this [page](https://optimization.rigor.com/s/2373818/?sh=3AF8C48AADD6D3E5F5DAA8B4B7BB7F45).

![placeholder](../../../../synthetics/images/image31.png)

Click the "**Best Practices Score**" tab. Scroll down, and review all the findings

![placeholder](../../../../synthetics/images/image23.png)

![Best Practices](../../../../synthetics/images/best-practices.png)

Spend some time to review the findings. Click into any line item

## 4. Create Mobile Check

Copy the RBC you created above:

![Copy Check](../../../../synthetics/images/copy-check.png)

Rename it, for example: **RWC - Checkout Flow (Tablet)**

![Copy Check](../../../../synthetics/images/rename-check.png)

Under the **Advanced** tab, update the following three settings and create your new mobile RBC.

![placeholder](../../../../synthetics/images/image18.png)

Test & Validate the new monitor

{{% notice title="Tip" color="info" %}}
As you are creating the steps try using the **Business Transaction** feature in Splunk Synthetic Monitoring.

*"Business Transactions are a combined group of contiguous steps in a Real Browser script that are to be measured as a whole. These transactions logically group similar parts of a flow together, so that users can view the performance of multiple steps and page(s) grouped under one Business Transaction."*
{{% /notice %}}

## 5. Resources

- [Getting Started With Selenium IDE](https://help.rigor.com/hc/en-us/articles/115004652007?flash_digest=b1ef7d1a07b68d5279ee5fef8adb87fb878cf010)

- [Splunk Synthetic Monitoring Scripting Guide](http://www2.rigor.com/scripting-guide)

- [How Can I Fix A Broken Script?](https://help.rigor.com/hc/en-us/articles/115004443988-How-Can-I-Fix-A-Broken-Script)

- [Introduction to the DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction) (Document Object Model (DOM)

- [Selenium IDE](https://www.selenium.dev/selenium-ide/)
