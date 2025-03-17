---
title: 1. Using SWiPE
weight: 1
---

##### **Configure your Org using SWiPE**

**SWiPE** is an online tool designed to help you configure a workshop environment in Splunk Observability Cloud. You can access **SWiPE** [**here**](https://swipe.splunk.show).

{{% notice style="info" title="Important Information" %}}
**SWiPE** does **not** provision EC2 instances. These instances are provisioned separately using **Splunk Show**.
{{% /notice %}}

![SWiPE](../images/swipe.png)

**SWiPE** automates the following tasks for your workshop environment:

1. **Create and Invite Users to the Organization**
   - Provide a list of email addresses for the users. You can either:
     - Upload a `.csv` file containing the email addresses (one per line), **or**
     - Copy and paste the email addresses directly (one per line).

2. **Admin Access for Ninja Workshops**
   - If the **Ninja Workshop** option is enabled, all users will be provisioned with **Admin** access control.

3. **Custom HEC URL and Token (Optional)**
   - If **Override HEC URL and Token** is enabled, you can configure a custom HTTP Event Collector (HEC) URL and token. This overrides the default values used for sending logs to Splunk.

4. **Create a Team and Add Users**
   - **SWiPE** will create a team and automatically add the users to it.

5. **Generate a SWiPE ID**
   - **SWiPE** will create a unique **SWiPE ID** for your workshop. You’ll need to copy this ID and use it when provisioning workshop instances in [**Splunk Show**](https://show.splunk.com/home/).

> [!WARNING] **Workshops with More Than 40 Users**
> If your workshop has more than **40 users**, we recommend informing the support team in advance. This ensures that the trial or workshop environment is properly scaled to handle the load.
