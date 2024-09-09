---
title: 1. Using SWiPE
weight: 1
hidden: false
---

## Configure Your Org Using SWiPE

**SWiPE** is an online tool to help configure a workshop environment in Splunk Observability Cloud and is available [**here**](https://swipe.splunk.show).

> [!INFO]
> **SWiPE does not** provision EC2 instances - these are provisioned using Splunk Show.

![SWiPE](../images/swipe.png)

**SWiPE** will configure the following:

- Create and invite users to the Org.
  - Create a `.csv` file containing the e-mail addresses (one per line) **or** copy and paste e-mail addresses (one per line).
- If **Ninja Workshop** is enabled, then the users will be provisioned with **Admin** access control.
- If **Override HEC URL and Token** is enabled, then a custom HEC URL and Token can be configured to override the default values which are used for sending logs to Splunk.
- Create a team and add users to the team.
- Create a **SWiPE ID** for use in Splunk Show. You will need to copy the **SWiPE ID** to provision the workshop instance(s) in [**Splunk Show**](https://show.splunk.com/home/).

> [!WARNING]
> If you have more than **40 users** in your workshop, we suggest informing the support team to ensure the trial or workshop environment is properly scaled.
