---
title: Teams
linkTitle: 1.1 Teams
weight: 1
---

## Aim

The aim of this module is for you to complete the first step of Team configuration by adding users to your Team.

## 1. Find your Team

Navigate to the **Teams** tab on the main toolbar, you should find you that a Team has been created for you as part of the workshop pre-setup and you would have been informed of your Team Name via e-mail.

If you have found your pre-configured Team, **skip Step 2.** and proceed to **[Step 3. Configure Your Team](./team/#3-configure-your-team)**. However, if you cannot find your allocated Team, you will need to create a new one, so proceed with **Step 2. Create Team**

## 2. Create Team

Only complete this step if you **cannot** find your pre-allocated Team as detailed in your workshop e-mail. Select **Add Team**, then enter your allocated team name, this will typically be in the format of "AttendeeID Workshop" and then save by clicking the **Add Team** button.

## 3. Configure Your Team

You now need to add other users to your team.  If you are running this workshop using the Splunk provided environment, the following accounts are available for testing. If you are running this lab in your own environment, you will have been provided a list of usernames you can use in place of the table below.

These users are dummy accounts who will not receive notifications when they are on call.

| Name                 | Username     | Shift      |
| -------------------- | ------------ | ---------- |
| Duane Chow           | duanechow    | Europe     |
| Steven Gomez         | gomez        | Europe     |
| Walter White         | heisenberg   | Europe     |
| Jim Halpert          | jimhalpert   | Asia       |
| Lydia Rodarte-Quayle | lydia        | Asia       |
| Marie Schrader       | marie        | Asia       |
| Maximo Arciniega     | maximo       | West Coast |
| Michael Scott        | michaelscott | West Coast |
| Tuco Salamanca       | tuco         | West Coast |
| Jack Welker          | jackwelker   | 24/7       |
| Hank Schrader        | hank         | 24/7       |
| Pam Beesly           | pambeesly    | 24/7       |

Add the users to your team, using either the above list or the alternate one provided to you. The value in the **Shift** column can be ignored for now, but will be required for a later step.

Click {{% button color="#00bce4" %}}Invite User{{% /button %}} button on the right hand side, then either start typing the usernames (this will filter the list), or copy and paste them into the dialogue box. Once all users are added to the list click the **Add User** button.

![Add Team Members](../../images/add-team-members.png)

To make a team member a Team Admin, simply click the :fontawesome-regular-edit: icon in the right hand column, pick any user and make them an Admin.

![Add Admin](../../images/team-admin.png)

{{% notice title="Tip" color="info" %}}
For large team management you can use the APIs to streamline this process.
{{% /notice %}}

Continue and also complete the [Configure Rotations](./rotations) module.
