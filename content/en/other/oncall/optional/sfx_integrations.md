---
title: Splunk OnCall Integrations
linkTitle: Integrations
weight: 4
draft: true
---

This module covers configuring the Integrations between SignalFx and VictorOps. Whilst the detailed steps below walk you through the process, you will find that the intergrations are already active within the Splunk systems being used for this workhop so Steps 1 & 2 are for info only.  **You only need to complete Step 3. Copy ID**

## 1. VictorOps Service API Endpoint

!!! warning
    The SignalFx Integration only needs to be enabled once per VictorOps instance, so you will probably find it has already been enabled, please **DO NOT** disable an already active integration when completing this lab.

**This is for info only as the Integration has already been enabled**

In order to integrate SignalFx with VictorOps we need to first obtain the Service API Endpoint for VictorOps. Within the VictorOps UI navigate to **Integrations** main tab and then use the search feature to find the SignalFx Integration.

If it is not already enabled, click the Enable Integration button to activate it.

![Endpoint](../../../images/endpoint.png)

This would be used when configuring the VictorOps Integration within the Splunk UI if it had not already been enabled.

## 2. Enable VictorOps Integration within SignalFx

In the Splunk UI navigate to **Integrations** and use the search feature to find the VictorOps integration.

!!! danger "Do not create a new integration!"
    Please do not create additional VictorOps integrations if one already exists, it will not break anything but simply creates extra clean up work after the workshop has completed.  The aim of this part of the lab was to show you how you would go about configuring the Integration if it was not already enabled.

Assuming you are using the AppDev EMEA instance of VictorOps you will find the VictorOps Integration has already been configured so there is **no need** to create a new one.

However the process of creating a new Integration is simply to click on **Create New Integration** like in the image below, or if there are existing integrations and you want to add another one you would click **New Integration**.

![VictorOps Integration](../../../images/m7-sfx-new-vo-integration.png)

Enter a descriptive **Name** then paste the **Service_API_Endpoint** value you copied in the previous step into the **Post URL** field, then save it.

![VictorOps Integration](../../../images/m7-sfx-vo-integration-url.png)

!!! important "Handling multiple VictorOps integrations"
    SignalFx can integrate with multiple VictorOps accounts so it is important when creating one to use a descriptive name and to not simply call it VictorOps.  This name will be used within the Splunk UI when selecting this integration, so ensure it is unambiguous

## 3. Copy ID

In Splunk UI navigate to **Integrations** and use the search feature to find the VictorOps Integration.

Copy the ID field and save it for use in the next steps.  We suggest you create a notepad document or similar as you will be gathering some additional values in the next steps.

![VictorOps Integration](../../../images/m7-sfx-vo-integration-id.png)
