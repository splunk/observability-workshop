# Working with Muting Rules - Lab Summary

* Learn how to configure how to mute Alerts
  
---

## 1. Learn how to configure muting your alerts

There will be times when you might want to mute certain notifications. For example, if you want to schedule downtime for maintenance on a server or set of servers, or if you are testing new code or settings etc. For that you can use muting rules in SignalFx. Let's create one!

Hover over **Alerts** in the menu and from the drop down click on **Detectors**.

![Detectors](../images/detectors/detectors-menu.png){: .zoom}

You will see a list of active detectors.

![Detectors](../images/detectors/detector-list.png){: .zoom}

If you created an detector in **Working with Detectors** you can click on the three dots **`...`** on the far right for that detector; if not, do that for another detector.  

From the drop-down click on **Create Muting Rule...**.

![Create Muting Rule](../images/detectors/create-muting-rule.png){: .zoom}

In the **Muting Rule** window check **Mute Indefinitely** and enter a reason.

!!! note
    This will mute the notifications permanently until you come back here and un-check this box or resume notifications for this detector.

![Mute Indefinitely](../images/detectors/mute-indefinitely.png){: .shadow .center}

Click **Next** and in the new modal window confirm the muting rule setup.

![Confirm Rule](../images/detectors/confirm-rule.png){: .shadow .center}

Click on **Mute Indefinitely**{: .label-button .sfx-ui-button-blue} to confirm.

![List muted rule](../images/detectors/alert-muted.png){: .zoom}

You won't be receiving any email notifications from you detector until you resume notifications again. Let's now see how to do that!

---

## 2. Resuming notifications

To Resume notifications, hover over **Alerts** in the top menu and click on **Muting Rules**. You will see the name of the detector you muted notifications for under **Detector**.

![Resume](../images/detectors/muting-rules-menu.png){: .zoom}
![Resume](../images/detectors/muting-list.png){: .zoom}

---

Click on the thee dots **`...`** on the far right.

Click on **Resume Notifications**.

![Resume](../images/detectors/resume-notifications.png){: .zoom}

Click on **Resume**{: .label-button .sfx-ui-button-blue} to confirm and resume notifications for this detector.

![Resume](../images/detectors/resume.png){: .shadow .center}

**Congratulations!** You have now resumed your alert notifications!
