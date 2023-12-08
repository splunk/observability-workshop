---
title: Teams
linkTitle: 6.1 Teams
weight: 1
---

* Introduction to Teams
* Create a Team and add members to the Team

---

## 1. Introduction to Teams

To make sure that users see the dashboards and alerts that are relevant to them when using Observability Cloud, most organizations will use Observability Cloud's Teams feature to assign a member to one or more Teams.

Ideally, this matches work-related roles, for example, members of a Dev-Ops or Product Management group would be assigned to the corresponding Teams in Observability Cloud.

When a user logs into Observability Cloud, they can choose which Team Dashboard will be their home page and they will typically select the page for their primary role.

In the example below, the user is a member of the Development, Operations and Product Management Teams, and is currently viewing the Dashboard for the Operations Team.

This Dashboard has specific Dashboard Groups for Usage, SaaS and APM Business Workflows assigned but any Dashboard Group can be linked to a Teams Dashboard.

They can use the menu along the top left to quickly navigate between their allocated teams, or they can use the **ALL TEAMS** dropdown on the right to select specific Team Dashboards, as well as quickly access **ALL Dashboards**** using the adjacent link.

![Teams](../../images/teams-homepage.png)

Alerts can be linked to specific Teams so the Team can monitor only the Alerts they are interested in, and in the above example, they currently have 1 active Critical Alert.

The Description for the Team Dashboard can be customized and can include links to team-specific resources (using Markdown).

---

## 2. Creating a new Team

To work with Splunk's Team UI click on the hamburger icon top left and select the **Organizations Settings → Teams**.

When the **Team** UI is selected you will be presented with the list of current Teams.

To add a new **Team** click on the {{% button style="blue" %}}Create New Team{{% /button %}} button. This will present you with the **Create New Team** dialog.

![Add Team](../../images/create-new-team.png)

Create your own team by naming it `[YOUR-INITIALS]-Team and` add yourself by searching for your name and selecting the **Add** link next to your name. This should result in a dialog similar to the one below:

![Add Team complete](../../images/add-to-team.png)

You can remove selected users by pressing  **Remove** or the small **x**.

Make sure you have your group created with your initials and with yourself added as a member, then click {{% button style="blue" %}}Done{{% /button %}}

This will bring you back to the **Teams** list that will now show your Team and the ones created by others.

{{% notice title="Note" style="info" %}}
The Teams(s) you are a member of have a grey **Member** icon in front of it.
{{% /notice %}}

If no members are assigned to your Team, you should see a blue **Add Members** link instead of the member count, clicking on that link will get you to the **Edit Team** dialog where you can add yourself.

This is the same dialog you get when pressing the 3 dots **...** at the end of the line with your Team and selecting **Edit Team**

The **...** menu gives you the option to Edit, Join, Leave or Delete a Team (leave and join will depend on if you are currently a member).

---

## 3. Adding Notification Rules

You can set up specific Notification rules per team, by clicking on the **Notification Policy** tab, this will open the notification edit menu.

![Base notification menu](../../images/notification-policy.png)

By default, the system offers you the ability to set up a general notification rule for your team.

{{% notice title="Note" style="info" %}}
The **Email all team members** option means all members of this Team will receive an email with the Alert information, regardless of the alert type.
{{% /notice %}}

### 3.1 Adding recipients

You can add other recipients, by clicking {{% button style="blue" %}}Add Recipient{{% /button %}}. These recipients do not need to be Observability Cloud users.

However, if you click on the link **Configure separate notification tiers for different severity alerts** you can configure every alert level independently.

![Multiple Notifications](../../images/single-policy.png)

Different alert rules for the different alert levels can be configured, as shown in the above image.

Critical and Major are using [Splunk\'s On-Call](https://www.splunk.com/en_us/observability/on-call.html) Incident Management solution. For the Minor alerts, we send it to the Teams Slack channel and for Warning and Info we send an email.

### 3.2 Notification Integrations

In addition to sending alert notifications via email, you can configure Observability Cloud to send alert notifications to the services shown below.

![Notifications options](../../images/integrations.png)

Take a moment to create some notification rules for your Team.
