---
title: Splunk Integration
linkTitle: 3. Splunk Integration
weight: 3
time: 10 minutes
description: Configure the OpenTelemetry-based metrics stream from ThousandEyes into Splunk Observability Cloud.
---

## About Splunk Observability Cloud

Splunk Observability Cloud is a real-time observability platform purpose-built for monitoring metrics, traces, and logs at scale. It ingests OpenTelemetry data and provides advanced dashboards and analytics to help teams detect and resolve performance issues quickly. This section explains how to integrate ThousandEyes data with Splunk Observability Cloud using OpenTelemetry.

{{% notice title="Scope Of This Section" style="info" %}}
This section covers the **metrics streaming** path from ThousandEyes into Splunk Observability Cloud. The next section adds the separate **distributed tracing** workflow that creates bi-directional links between ThousandEyes and Splunk APM.
{{% /notice %}}

{{% notice title="Only need 1 integration" style="warning" %}}
Rather than having each workshop attendee set this up, watch your instructor perform the following steps.

You will continue performing steps on the next page.
{{% /notice %}}


### Step 1: Get or Create a Splunk Observability Cloud Access Token

To send ThousandEyes metrics to Splunk Observability Cloud, you need an access token with the **Ingest** scope.

For this workshop we will use the token provided. You can get it from the instance:

```bash
. ~/workshop/petclinic/scripts/check_env.sh | grep ACCESS_TOKEN
```

Or you can get it from the Splunk Observability Cloud UI, as shown in the clip below.

### Step 2: Create an Integration

This integration is the one-way telemetry stream that gets ThousandEyes metrics into Splunk Observability Cloud dashboards and detectors.

#### Using the ThousandEyes UI

To integrate Splunk Observability Cloud with ThousandEyes:

1. Log in to your account on the ThousandEyes platform and go to **Manage > Integration > Integration 1.0**
2. Click **New Integration** and select **ThousandEyes for OpenTelemetry**
3. Enter a **Name** for the integration
4. Set the **Target** to **HTTP**
5. Enter the **Endpoint URL**: `https://ingest.{REALM}.signalfx.com/v2/datapoint/otlp`
   - Replace `{REALM}` with your Splunk environment (e.g., `us1`, `eu0`)
6. For **Preset Configuration**, select **Splunk Observability Cloud**
7. For **Auth Type**, select **Custom**
8. Add the following **Custom Headers**:
   - `X-SF-Token: {TOKEN}` (Enter your Splunk Observability Cloud access token created in Step 1)
   - `Content-Type: application/x-protobuf`
9. For **OpenTelemetry Signal**, select **Metric**
10. For **Data Model Version**, select **v2**
11. Select the tests you want to send.
{{% notice title="Add test later" style="primary" icon="lightbulb" %}}
If you add a new test, you will need to add it back to this integration later
{{% /notice %}}
12. Click **Save** to complete the integration setup

![Integration Complete](../images/te2.gif?width=45vw)

You have now successfully integrated your ThousandEyes data with Splunk Observability Cloud.

{{% notice title="Pending State" style="note" %}}
The integration may state in a **Pending** state for a bit. You may need to refresh before it turns to **Connected**.
{{% /notice %}}

{{% notice title="What Comes Next" style="primary" icon="lightbulb" %}}
After you finish the metrics integration, continue to **Distributed Tracing** to add the reverse investigation path from ThousandEyes into Splunk APM and back again.
{{% /notice %}}

### Step 3: ThousandEyes Dashboard in Splunk Observability Cloud

Once the integration is set up, you can view real-time monitoring data in the ThousandEyes Network Monitoring Dashboard within Splunk Observability Cloud. The dashboard includes:

- **HTTP Server Availability (%)**: Displays the availability of monitored HTTP servers
- **HTTP Throughput (bytes/s)**: Shows the data transfer rate over time
- **Client Request Duration (seconds)**: Measures the latency of client requests
- **Web Page Load Completion (%)**: Indicates the percentage of successful page loads
- **Page Load Duration (seconds)**: Displays the time taken to load pages

#### Deploy the Dashboard Template

You can download the dashboard template from the following link: [Download ThousandEyes Splunk Observability Cloud dashboard template (Google Drive)](https://github.com/thousandeyes/thousandeyes-observability-dashboards/blob/main/splunk/ThousandEyesDashboard.json). Then you can import it into Splunk Observability Cloud. (This has already been done.)

If you  have any tests running you will see data already.

![Splunk Observability Cloud Dashboard for ThousandEyes](../images/splunk-o11y-dashboard-te.png?width=45vw)

{{% notice title="Success" style="success" icon="check" %}}
Your ThousandEyes data is now streaming to Splunk Observability Cloud. Next, add the distributed tracing connector so you can pivot between ThousandEyes and Splunk APM during troubleshooting.
{{% /notice %}}
