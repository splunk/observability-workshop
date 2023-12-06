---
title: 1. Using SWiPE
weight: 1
hidden: false
---

## Configure Your Org Using SWiPE

**SWiPE** is an online tool to help configure a workshop environment in Splunk Observability Cloud and is available [**here**](https://swipe.splunk.show).

{{% notice info %}}

**SWiPE does not** provision EC2 instances - these are provisioned using Splunk Show.

{{% /notice %}}

![SWiPE](../images/swipe.png)

**SWiPE** will configure the following:

- Create and invite users to the Org.
  - Create a `.csv` file containing the e-mail addresses (one per line) **or** copy and paste e-mail addresses (one per line).
- Create a team and add users to the team.
- Create tokens for:
  - INGEST
  - API
  - RUM

**SWiPE** will also provide a HEC Token and HEC URL for dedicated workshop Splunk Cloud environments. If you wish to use a different Splunk Cloud environment, you will need to provide a HEC Token and HEC URL for that environment in Splunk Show.

You will need to make a copy of the above to provision the workshop instances in Splunk Show.
