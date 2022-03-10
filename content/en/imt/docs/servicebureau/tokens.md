---
title: Controlling Usage
linkTitle: Control Usage
weight: 70
---
* Discover how you can restrict usage by creating separate Access Tokens and set limits.

## 1. Access Tokens

If you wish to control the consumption of Hosts, Containers, Custom Metrics and High Resolution Metrics, you can create multiple Access Tokens and allocate them to different parts of your organization.

In the UI click on the **>>** bottom left and select the **Settings → Access Tokens** under **General Settings**.

The **Access Tokens** Interface provides an overview of your allotments in the form of a list of Access Tokens that have been generated. Every Organization will have a **Default** token generated when they are first setup, but there will typically be multiple Tokens configured.

Each Token is unique and can be assigned limits for the amount of Hosts, Containers, Custom Metrics and High Resolution Metrics it can consume.

The **Usage Status** Column quickly shows if a token is above or below its assigned limits.

![New token](../../../images/access-tokens.png)

## 2. Creating a new token

Let create a new token by clicking on  the {{% labelbutton color="ui-button-blue" %}}**New Token**{{% /labelbutton %}} button. This will provide you with the **Name Your Access Token** dialog.

Enter the new name of the new Token by using your Initials e.g. RWC-Token and make sure to tick both **Ingest Token** and **API Token** checkboxes!

![Name Your token](../../../images/new-access-token.png)

After you press {{% labelbutton color="ui-button-blue" %}}**OK**{{% /labelbutton %}} you will be taken back to the **Access Token** UI. Here your new token should be present, among the ones created by others.

![full tokenlist](../../../images/access-token-created.png)

If you have made an error in your naming, want to disable/enable a token or set a Token limit, click on the ellipsis (**...**) menu button behind a token limit to open the manage token menu.

![Show Menu](../../../images/manage-access-token.png)

If you made a typo you can use the **Rename Token** option to correct the name of your token.

## 3. Disabling a token

If you need to make sure a token cannot be used to send Metrics in you can disable a token.

Click on **Disable** to disable the token, this means the token cannot be used for sending in data to Splunk Observability Cloud.

The line with your token should have become greyed out to indicate that is has been disabled as you can see in the screenshot below.

![Token disabled](../../../images/disable-access-token.png)

Go ahead and click on the ellipsis (**...**) menu button to Disable and Enable your token.

## 4. Manage token usage limits

Now Lets start limiting usage by clicking on Manage Token Limit in the 3 **...** menu.

This will show the Manage Token Limit Dialog:

![Set Limits on token](../../../images/manage-token-limit.png)

In this Dialog you can set the limits per category.

Please go ahead and specify the limits as follows for each usage metric:

| Limit | Value |
| ----- | ----- |
| Host Limit | 5 |
| Container Limit | 15 |
| Custom Metric Limit | 20 |
| High Resolution Metric Limit | 0 |

For our lab use your own email address, and double check that you have the correct numbers in your dialog box as shown in the table above.

Token limits are used to trigger an alert that notify one or more recipients when the usage has been above 90% of the limit for 5 minutes.

To specify the recipients, click {{% labelbutton color="ui-button-blue" %}}**Add Recipient**{{% /labelbutton %}}, then select the recipient or notification method you want to use (specifying recipients is optional but highly recommended).

The severity for token alerts is always Critical.

Click on {{% labelbutton color="ui-button-blue" %}}**Update**{{% /labelbutton %}} to save your Access Tokens limits and The Alert Settings.

{{% alert title="Note: Going above token limit" color="primary" %}}
When a token is at or above its limit in a usage category, new metrics for that usage category will not be stored and processed by Observability Cloud. This will make sure you there  will be no unexpected cost due to a team sending in data without restriction.
{{% /alert %}}

{{% alert title="Note: Advanced alerting" color="primary" %}}
If you wish to get alerts before you hit 90%, you can create additional detectors using whatever values you want. These detectors could target the Teams consuming the specific Access Tokens so they can take action before the admins need to get involved.
{{% /alert %}}

In your company you would distribute these new Access Tokens to various teams, controlling how much information/data they can send to Observability Cloud.

This will allow you to fine tune the way you consume your Observability Cloud allotment and prevent overages from happening.

**Congratulations!** You have now have completed the Service Bureau module.
