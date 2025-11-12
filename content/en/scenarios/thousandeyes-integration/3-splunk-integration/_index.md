---
title: Splunk Integration
linkTitle: 3. Splunk Integration
weight: 3
---

## About Splunk Observability Cloud

Splunk Observability Cloud is a real-time observability platform purpose-built for monitoring metrics, traces, and logs at scale. It ingests OpenTelemetry data and provides advanced dashboards and analytics to help teams detect and resolve performance issues quickly. This section explains how to integrate ThousandEyes data with Splunk Observability Cloud using OpenTelemetry.

## Step 1: Create a Splunk Observability Cloud Access Token

To send data to Splunk Observability Cloud, you need an access token. Follow these steps:

1. In the Splunk Observability Cloud platform, go to **Settings > Access Token**
2. Click **Create Token**
3. Enter a **Name**
4. Select **Ingest** scope
5. Select **Create** to generate your access token
6. Copy the access token and store it securely

You need the access token to send telemetry data to Splunk Observability Cloud.

## Step 2: Create an Integration

### Using the ThousandEyes UI

To integrate Splunk Observability Cloud with ThousandEyes:

1. Log in to your account on the ThousandEyes platform and go to **Manage > Integration > Integration 1.0**
2. Click **New Integration** and select **OpenTelemetry Integration**

   ![ThousandEyes Integration Setup](../images/te1.gif)

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
11. Select a test 
12. Click **Save** to complete the integration setup

   ![Integration Complete](../images/te2.gif)

You have now successfully integrated your ThousandEyes data with Splunk Observability Cloud.

### Using the ThousandEyes API

For a programmatic integration, use the following API commands:

#### HTTP Protocol

```bash
curl -v -XPOST https://api.thousandeyes.com/v7/stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "type": "opentelemetry",
    "testMatch": [{
      "id": "281474976717575",
      "domain": "cea"
    }],
    "endpointType": "http",
    "streamEndpointUrl": "https://ingest.{REALM}.signalfx.com:443/v2/datapoint/otlp",
    "customHeaders": {
      "X-SF-Token": "{TOKEN}",
      "Content-Type": "application/x-protobuf"
    }
  }'
```

#### gRPC Protocol

```bash
curl -v -XPOST https://api.thousandeyes.com/v7/stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "type": "opentelemetry",
    "testMatch": [{
      "id": "281474976717575",
      "domain": "cea"
    }],
    "endpointType": "grpc",
    "streamEndpointUrl": "https://ingest.{REALM}.signalfx.com:443",
    "customHeaders": {
      "X-SF-Token": "{TOKEN}",
      "Content-Type": "application/x-protobuf"
    }
  }'
```

Replace `streamEndpointUrl` and `X-SF-Token` values with the correct values for your Splunk Observability Cloud instance.

{{% notice title="Note" style="info" %}}
Make sure to replace `{REALM}` with your Splunk environment realm (e.g., `us1`, `us2`, `eu0`) and `{TOKEN}` with your actual Splunk access token.
{{% /notice %}}

## Step 3: ThousandEyes Dashboard in Splunk Observability Cloud

Once the integration is set up, you can view real-time monitoring data in the ThousandEyes Network Monitoring Dashboard within Splunk Observability Cloud. The dashboard includes:

- **HTTP Server Availability (%)**: Displays the availability of monitored HTTP servers
- **HTTP Throughput (bytes/s)**: Shows the data transfer rate over time
- **Client Request Duration (seconds)**: Measures the latency of client requests
- **Web Page Load Completion (%)**: Indicates the percentage of successful page loads
- **Page Load Duration (seconds)**: Displays the time taken to load pages

### Dashboard Template

You can download the dashboard template from the following link: [Download ThousandEyes Splunk Observability Cloud dashboard template (Google Drive)](https://drive.google.com/file/d/1xpdjr5CRBC-JBM9tGsNFcVYp3C-tJC8s/view?usp=sharing).

{{% notice title="Success" style="success" icon="check" %}}
Your ThousandEyes data is now streaming to Splunk Observability Cloud! You can now correlate synthetic test results with APM traces and infrastructure metrics for comprehensive observability.
{{% /notice %}}
