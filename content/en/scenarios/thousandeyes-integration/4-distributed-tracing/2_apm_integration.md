---
title: APM Integration
linkTitle: 4.2 APM Integration
weight: 1
time: 10 minutes
description: Configure bi-directional drilldowns between APM and ThousandEyes
---

## Summary

In this section we will configure the APM Connector in ThousandEyes.

{{< acknowledge "Only need 1 integration" >}}
Rather than each attendee setting this up, watch your instructor perform the following steps.

You will continue performing steps on the next page.
{{< /acknowledge >}}

### Step 1: Create the Splunk APM Connector in ThousandEyes

The metric streaming integration from the previous section uses an **Ingest** token. This step is different: ThousandEyes needs to query Splunk APM and build trace links, so it uses a Splunk **API** token instead.

1. In Splunk Observability Cloud, create an access token with the **API** scope.
2. In ThousandEyes, go to **Manage > Integrations > Integrations 2.0**, and change to the **Connectors** tab.
3. Create a **Generic Connector**. You can select the Preset as **Splunk Observability APM**:
    - **Name**: `Splunk APM`
    - **Target URL**: `https://api.<REALM>.signalfx.com`
    - **Header**: `X-SF-Token: <your-api-scope-token>`
4. Click **Save and Assign Operation**


    ![Splunk APM Generic Connector in ThousandEyes](../../images/splunk-apm-generic-connector.png?width=35vw)
5. Click **New Operation** and select **Splunk Observability APM**.
6. Name it `Splunk APM`.
7. Click **Save & Assign Connector**.
    ![Splunk APM Operation in ThousandEyes](../../images/splunk-apm-operation.png?width=35vw)
8. Select the connector you just created and click **Save**.

![Splunk APM Manage Operations in ThousandEyes](../../images/splunk-apm-manage-operations.png?width=35vw)

{{< checkpoint "If you see your connector with your assigned operations you are in a good state." >}}

{{% notice title="Troubleshooting Guidance" style="note" %}}
If you see something like **No assigned operation** then you need to click **Manage** to assign it.
![Splunk APM Integration Summary](../../images/splunk-apm-integration-summary.png?width=35vw)
{{% /notice %}}
