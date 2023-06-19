---
title: Team Notifications
linkTitle: 2.2 Team Notifications
weight: 2
---

* Introduction to Teams
* Create a Team and add members to Team

---

## 1. Adding Team Notification Rules

You can set up specific Notification rules per team, click on the **Notification Policy** tab, this will open the notification edit menu.

![Base notification menu](../../images/notification-policy.png)

By default the system offers you the ability to set up a general notification rule for your team.

{{% notice title="Note" style="info" %}}
The **Email all team members** option means all members of this Team will receive an email with the Alert information, regardless of the alert type.
{{% /notice %}}

## 2. Adding recipients

You can add other recipients, by clicking {{% button style="blue" %}}Add Recipient{{% /button %}}. These recipients do not need to be Observability Cloud users.

However if you click on the link **Configure separate notification tiers for different severity alerts** you can configure every alert level independently.

![Multiple Notifications](../../images/single-policy.png)

Different alert rules for the different alert levels can be configured, as shown in the above image.

Critical and Major are using [Splunk\'s On-Call](https://www.splunk.com/en_us/observability/on-call.html) Incident Management solution. For the Minor alerts we send it to the Teams Slack channel and for Warning and Info we send an email.

## 3 Notification Integrations

In addition to sending alert notifications via email, you can configure Observability Cloud to send alert notifications to the services shown below.

![Notifications options](../../images/integrations.png)

Take a moment to create some notification rules for you Team.
