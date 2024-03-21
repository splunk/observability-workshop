---
title: 1.6 Edit test steps
weight: 6
---

To edit the steps click on the {{< button >}}+ Edit steps or synthetic transactions{{< /button >}} button. From here, we are going to give meaningful names to each step.

![Edit steps](../../_img/edit-steps.png)

For each of the four steps, we are going to give them a meaningful, readable name. For our demo site, that looks like:

- **Step 1** replace the text **Go to URL** with **HomePage - Online Boutique**
- **Step 2** enter the text **Select Vintage Camera Lens**.
- **Step 3** enter **Add to Cart**.
- **Step 4** enter **Place Order**.

![Step names](../../_img/step-names.png)

{{% notice note %}}
If you'd like, group the test steps into Transactions and edit the transaction names. This is especially useful for Single Page Apps (SPAs), where the resource waterfall is not split by URL. We can also chart and alert based on transactions.
{{% /notice %}}

Click {{% button style="blue" %}}< Return to test{{% /button %}} to return to the test configuration page and click {{% button style="blue" %}}Save{{% /button %}} to save the test.

You will be returned to the test dashboard where you will see test results start to appear.

![Scatterplot](../../_img/scatterplot.png)

**Congratulations!** You have successfully created a Real Browser Test in Splunk Synthetic Monitoring. Next, we will look into a test result in more detail.
