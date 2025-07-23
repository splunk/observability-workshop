---
title: Create Custom Detector
linkTitle: 5.1 Create Custom Detector
weight: 5
authors: ["Tim Hard"]
time: 10 minutes
draft: false
---

Splunk Observability Cloud provides detectors, events, alerts, and notifications to keep you informed when certain criteria are met. There are a number of pre-built **AutoDetect Detectors** that automatically surface when common problem patterns occur, such as when an EC2 instance’s CPU utilization is expected to reach its limit. Additionally, you can also create custom detectors if you want something more optimized or specific. For example, you want a message sent to a Slack channel or to an email address for the Ops team that manages this Kubernetes cluster when Memory Utilization on their pods has reached 85%.

{{% notice title="Exercise: Create Custom Detector" style="green" icon="running" %}}
In this section you'll create a detector on **Pod Memory Utilization** which will trigger if utilization surpasses 85%

1. On the **Kubernetes Pods Dashboard** you cloned in section [3.2 Dashboard Cloning](../../3-reuse-content-across-teams/2-clone-dashboards), click the **Get Alerts** button (bell icon) for the **Memory usage (%)** chart -> Click **New detector from chart**.

    ![New Detector from Chart](../../images/new-detector.png?width=40vw)

2. In the **Create detector** add your initials to the detector name.

    ![Create Detector: Update Detector Name](../../images/create-detector-name.png?width=40vw)

3. Click **Create alert rule**.

    These conditions are expressed as one or more rules that trigger an alert when the conditions in the rules are met. Importantly, multiple rules can be included in the same detector configuration which minimizes the total number of alerts that need to be created and maintained. You can see which signal this detector will alert on by the bell icon in the **Alert On** column. In this case, this detector will alert on the Memory Utilization for the pods running in this Kubernetes cluster.

    ![Alert Signal](../../images/alert-signals.png?width=60vw)

4. Click **Proceed To Alert Conditions**.

    Many pre-built alert conditions can be applied to the metric you want to alert on. This could be as simple as a static threshold or something more complex, for example, is memory usage deviating from the historical baseline across any of your 50,000 containers?

    ![Alert Conditions](../../images/alert-conditions.png?width=60vw)

5. Select **Static Threshold**.
6. Click **Proceed To Alert Settings**.

    In this case, you want the alert to trigger if any pods exceed 85% memory utilization. Once you’ve set the alert condition, the configuration is back-tested against the historical data so you can confirm that the alert configuration is accurate, meaning will the alert trigger on the criteria you’ve defined? This is also a great way to confirm if the alert generates too much noise.

    ![Alert Settings](../../images/alert-settings.png?width=60vw)

7. Enter 85 in the **Threshold** field.
8. Click **Proceed To Alert Message**.

    Next, you can set the severity for this alert, you can include links to runbooks and short tips on how to respond, and you can customize the message that is included in the alert details. The message can include parameterized fields from the actual data, for example, in this case, you may want to include which Kubernetes node the pod is running on, or the `store.location` configured when you deployed the application, to provide additional context.

    ![Alert Message](../../images/alert-message.png?width=60vw)

9. Click **Proceed To Alert Recipients**.

    You can choose where you want this alert to be sent when it triggers. This could be to a team, specific email addresses, or to other systems such as ServiceNow, Slack, Splunk On-Call or Splunk ITSI. You can also have the alert execute a webhook which enables me to leverage automation or to integrate with many other systems such as homegrown ticketing tools. **For the purpose of this workshop do not include a recipient**

    ![Alert Recipients](../../images/alert-recipients.png?width=60vw)

10. Click **Proceed To Alert Activation**.

    ![Activate Alert](../../images/alert-activate-alert.png?width=60vw)

11. Click **Activate Alert**.

    ![Activate Alert Message](../../images/alert-activation.png?width=40vw)

    You will receive a warning because no recipients were included in the Notification Policy for this detector. This can be warning can be dismissed.

12. Click **Save**.

    ![Activate Alert Message](../../images/alert-new-detector.png?width=60vw)

    You will be taken to your newly created detector where you can see any triggered alerts.

13. In the upper right corner, Click **Close** to close the Detector.

The detector status and any triggered alerts will automatically be included in the chart because this detector was configured for this chart.

![Alert Chart](../../images/alert-chart.png?width=40vw)

**Congratulations! You've successfully created a detector that will trigger if pod memory utilization exceeds 85%. After a few minutes, the detector should trigger some alerts. You can click the detector name in the chart to view the triggered alerts.**

{{% /notice %}}
