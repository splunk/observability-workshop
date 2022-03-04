---
title: Custom Charts and Alerts based on RUM Metrics
linkTitle: Alerts
weight: 15
---

* Use RUM Metrics to set up Alerts to be warned in case of an issue
* Create a Custom Chart based on RUM Metrics

---

## 1.  Overview

The fact that Splunk's RUM is designed as a full fidelity solution, and thus can take 100% of your traces, allows it to detect and alert you to any change to the behavior of your website. It also give you the ability to to give you accurate insight in how your website is behaving by allowing you to creating custom Chart and Dashboards.
This allows you to combine data from your Website, Backend service and underlying Infrastructure. Allowing you to observe the complete stack that makes up your application/solution.

Creating charts or alerts for RUM Metrics are done in the same way as we do for Infrastructure Metrics. In this section we will create a simple chart, detector and alert.

If you previously done the Splunk IMT Part of the Workshop, you will find this section very familiar. If you have not done the Splunk IMT workshop before, it is recommended that you run though the [Dashboards](../dashboards/intro.md) and [Detectors](../detectors/intro.md) modules after completing the RUM workshop to get a better understanding of the capabilities.

## 2. Create an alert on one of the RUM Metrics

From the top left hamburger menu icon click **Alerts** in the menu and then select **Detectors**.

## 3. Create a Chart based on Rum Metrics

### 3.1 Overview

Creating charts or alerts for RUM Metrics are done in the same way as we do for Infrastructure Metrics.
In this section we will create a simple chart, detector and alert
If you previously done the Splunk IMT Part of the Workshop, you will find this section very familiar.

![RUM-Cart2](../../images/RUM-select-cart.png)

u have added to the trace as part of the configuration of your website.

{{% alert title="Addtional Tags" color="info" %}}
We are already sending two additional tags, you have seen them defined in the *Beacon url* that was added to your website in the first section of this workshop! You can add additional tag in a similar way.

```javascript
app: "[nodename]-rum-app", environment: "[nodename]-rum-env"
```

{{% /alert %}}
