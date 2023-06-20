---
title: Team Dashboards
linkTitle: 1.7 Team Dashboards
weight: 7
---

* Introduction to Teams
* Create a Team and add members to Team

---

## 1. Introduction to Teams

To make sure that users see the dashboards and alerts that are relevant to them when using Observability Cloud, most organizations will use Observability Cloud's Teams feature to assign a member to one or more Teams.

Ideally, this matches work related roles, for example, members of a Dev-Ops or Product Management group would be assigned to the corresponding Teams in Observability Cloud.

When a user logs into Observability Cloud, they can choose which Team Dashboard will be their home page and they will typically select the page for their primary role.

In the example below, the user is a member of the Development, Operations and Product Management Teams, and is currently viewing the Dashboard for the Operations Team.

This Dashboard has specific Dashboard Groups for Usage, SaaS and APM Business Workflows assigned but any Dashboard Group can be linked to a Teams Dashboard.

They can use the menu along the top left to quickly navigate between their allocated teams, or they can use the **ALL TEAMS** dropdown on the right to select specific Team Dashboards, as well as quickly accessing **ALL Dashboards** using the adjacent link.

![Teams](../../images/teams-homepage.png)

Alerts can be linked to specific Teams so the Team can monitor only the Alerts they are interested in, and in the above example they currently have 1 active Critical Alert.

The Description for the Team Dashboard can be customized and can include links to team specific resources (using Markdown).

## 2. Creating a new Team

To work with to Splunk's Team UI click on the hamburger icon top left and select the **Organizations Settings → Teams**.

When the **Team** UI is selected you will be presented with the list of current Teams.

To add a new **Team** click on the {{% button style="blue" %}}Create New Team{{% /button %}} button. This will present you with the **Create New Team** dialog.

![Add Team](../../images/create-new-team.png)

Create your own team by naming it `[YOUR-INITIALS]-Team and` add yourself by searching for your name and selecting the **Add** link next to your name. This should result in a dialog similar to the one below:

![Add Team complete](../../images/add-to-team.png)

You can remove selected users by pressing  **Remove** or the small **x**.

Make sure you have your group created with your initials and with yourself added as a member, then click {{% button style="blue" %}}Done{{% /button %}}

This will bring you back to the **Teams** list that will now show your Team and the one's created by others.

{{% notice title="Note" style="info" %}}
The Teams(s) you are a member of have a grey **Member** icon in front of it.
{{% /notice %}}

If no members are assigned to your Team, you should see a blue **Add Members** link instead of the member count, clicking on that link will get you to the **Edit Team** dialog where you can add yourself.

This is the same dialog you get when pressing the 3 dots **...** at the end of the line with your Team and selecting **Edit Team**

The **...** menu gives you the option to Edit, Join, Leave or Delete a Team (leave and join will depend on if you are currently a member).
