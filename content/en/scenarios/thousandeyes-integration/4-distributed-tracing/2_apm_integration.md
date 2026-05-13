---
title: APM Integration
linkTitle: 4.2 APM Integration
weight: 1
time: 10 minutes
description: Configure bi-directional drilldowns between APM and ThousandEyes
---

## Summary

In this section we will configure the APM Connector in ThousandEyes.

{{% notice title="Only need 1 integration" style="warning" %}}
Rather than having each workshop attendee set this up, watch your instructor perform the following steps.

You will continue performing steps on the next page.
{{% /notice %}}


### Step 1: Create the Splunk APM Connector in ThousandEyes

The metric streaming integration from the previous section uses an **Ingest** token. This step is different: ThousandEyes needs to query Splunk APM and build trace links, so it uses a Splunk **API** token instead.

1. In Splunk Observability Cloud, create an access token with the **API** scope.
2. In ThousandEyes, go to **Manage > Integrations > Integrations 2.0**, and change to the **Connectors** tab.
3. Create a **Generic Connector**. You can select the Preset as **Splunk Observability APM**:
  - **Name**: `Splunk APM`
  - **Target URL**: `https://api.<REALM>.signalfx.com`
  - **Header**: `X-SF-Token: <your-api-scope-token>`
4. **Save and Assign Operation**

![Splunk APM Generic Connector in ThousandEyes](../../images/splunk-apm-generic-connector.png)

5. Create a **New Operation** and select **Splunk Observability APM**.
6. Name it `Splunk APM`.
7. **Save & Assign Connector** to enable the operation and save the integration.

![Splunk APM Operation in ThousandEyes](../../images/splunk-apm-operation.png)

8. Select the connector and click **Save**.

![Splunk APM Manage Operations in ThousandEyes](../../images/splunk-apm-manage-operations.png)