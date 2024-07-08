---
title: Working with Muting Rules
linkTitle: 4.1 Creating a Muting Rule
weight: 1
---

* Learn how to configure Muting Rules
* Learn how to resume notifications
  
---

## 1. Configuring Muting Rules

There will be times when you might want to mute certain notifications. For example, if you want to schedule downtime for maintenance on a server or set of servers, or if you are testing new code or settings etc. For that you can use muting rules in Splunk Observability Cloud. Let's create one!

Click on **Alerts & Detectors** in the sidebar and then click **Detectors** to see the list of active detectors.

![detectors list](../../images/detectors.png)

If you created a detector in **Creating a Detector** you can click on the three dots **`...`** on the far right for that detector; if not, do that for another detector.

From the drop-down click on **Create Muting Rule...**

![Create Muting Rule](../../images/create-muting-rule.png)

In the **Muting Rule** window check **Mute Indefinitely** and enter a reason.

{{% notice title="Important" style="info" %}}
This will mute the notifications permanently until you come back here and un-check this box or resume notifications for this detector.
{{% /notice %}}

![Mute Indefinitely](../../images/mute-indefinitely.png)

Click **Next** and in the new modal window confirm the muting rule setup.

![Confirm Rule](../../images/confirm-rule.png)

Click on {{% button style="blue" %}}Mute Indefinitely{{% /button %}} to confirm.

![List muted rule](../../images/alert-muted.png)

You won't be receiving any email notifications from your detector until you resume notifications again. Let's now see how to do that!

---

## 2. Resuming notifications

To Resume notifications, click on **Muting Rules**, you will see the name of the detector you muted notifications for under **Detector** heading.

Click on the thee dots **`...`** on the far right, and click on **Resume Notifications**.

![Resume](../../images/muting-list.png)

Click on {{% button style="blue" %}}Resume{{% /button %}} to confirm and resume notifications for this detector.

![Resume](../../images/resume.png)

**Congratulations!** You have now resumed your alert notifications!
