---
title: Using Observability Cloud Detectors in ITSI
linkTitle: 6. Using Observability Cloud Detectors in ITSI
weight: 1
---

## Part 2: Sending Alerts from Splunk Observability Cloud to Splunk ITSI

Since we have a detector configured in Splunk Observability Cloud that we set up earlier, the next step is to ensure that when it triggers an alert, this alert is sent to Splunk IT Service Intelligence (ITSI). This integration allows ITSI to ingest these alerts as notable events, which can then be correlated with other events and contribute to service health scores. The most common method to achieve this is by using a webhook in Splunk Observability Cloud to send alert data to an HTTP Event Collector (HEC) endpoint configured in Splunk ITSI.

**Step 1: Configure an HTTP Event Collector (HEC) in Splunk (ITSI)**

Before Splunk Observability Cloud can send alerts to ITSI, you need an HEC endpoint in your Splunk instance (where ITSI is running) to receive them. 

1.  Log in to your Splunk Enterprise or Splunk Cloud instance that hosts ITSI.
2.  Navigate to **Settings > Data Inputs**.
3.  Click on **HTTP Event Collector**.
4.  Click **Global Settings**. Ensure HEC is enabled. If not, enable it and specify a default port (e.g., 8088, though this might be managed differently in Splunk Cloud).
5.  Click **New Token**.
6.  Give your HEC token a descriptive name, for example, `o11y_alerts_for_itsi`.
7.  For **Source name override**, you can optionally specify a sourcetype, or leave it blank to specify it in Observability Cloud or let it default.
8.  For **Default Index**, select an appropriate index where ITSI can access these events. Often, there's a dedicated index for ITSI events, or you might use a general events index like `main` or `itsi_event_management`.
9.  Ensure the token is enabled and click **Submit**.
10. Copy the **Token Value** that is generated. You will need this for the webhook configuration in Splunk Observability Cloud.

**Step 2: Configure a Webhook Integration in Splunk Observability Cloud**

Now, return to Splunk Observability Cloud to set up the webhook that will use the HEC token you just created.

1.  In Splunk Observability Cloud, navigate to **Data Management > Available Integrations**.
2.  Look for an option to add a new **Splunk platform**.
3.  Give the Integration a name, for example, `Splunk ITSI HEC`.
4.  In the **URL** field, enter the HEC endpoint URI for your Splunk instance. This will typically be in the format `https://<your-splunk-hec-host-or-ip>:<hec-port>/services/collector/event`.
5.  You will need to add an **HEC token** that you created earlier.
6.  For the **Payload**, you need to construct a JSON payload that ITSI can understand. Splunk Observability Cloud provides an out of the box payload configured to include fields needed for ITSI event correlation.
7. Review the Integration and click **Save**

**Step 3: Update the Detector to Use the Webhook**

Now, go back to the detector you created in Part 1 and update its notification settings to use the newly configured webhook.

1.  Navigate to **Detectors & SLOs** in Splunk Observability Cloud.
2.  Find and edit the detector you created for EC2 CPU utilization.
3.  Click the Alert rule that we created earlier
4.  Go to the **Alert Recipients** section.
5.  Click **Add recipient > Splunk platform** and select the integration you just configured (`Splunk ITSI HEC`) for the desired alert severities (e.g., Critical, Warning).
6.  Save the changes to your detector.

**Step 4: Validate**

To test the integration, you can wait for a genuine alert to trigger or, if your detector settings allow, you might be able to manually trigger a test alert or temporarily lower the threshold to force an alert. Once an alert triggers in Splunk Observability Cloud, it should send the payload via the webhook to your Splunk HEC endpoint.

Verify in Splunk by searching your target index (e.g., `index=itsi_event_management sourcetype=o11y:itsi:alert host=<your-ec2-instance-id>`). You should see the event data arriving from Splunk Observability Cloud.

With these steps, alerts from your Splunk Observability Cloud detector are now being sent to Splunk ITSI. Correlating Events and generating Notables all function exactly the same as we covered earlier in this workshop.

