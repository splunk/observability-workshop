---
title: "Phase 3: Global Data Links"
linkTitle: 4. Global Data Links
weight: 4
archetype: chapter
time: 10 minutes
description: Create a global data link in Splunk Observability Cloud that navigates directly to the corresponding AppDynamics tier view using the appd.* span attributes.
---

The `appd.*` attributes on your traces are more than metadata -- they can power **global data links** that let anyone viewing a trace in Splunk Observability Cloud jump straight into the corresponding AppDynamics view with a single click.

## What are Global Data Links?

Global data links are a Splunk Observability Cloud feature that creates clickable links on span attributes, tag values, or metric dimensions. When a user clicks a linked value, they are taken to an external URL you define -- with the actual attribute value substituted into the URL template.

### Pre-requisite for our Data Link
Copy the URL to your application in AppDynamics. The important part of the URL that identifies your application is a query parameter on the url (E.G. `&application=99999`)
The full url including the application query parameter are used to build your global data link
![AppD Application ID](../_images/app-url.png)

## Create the Global Data Link

1. In Splunk Observability Cloud, click **Settings** (gear icon) in the left navigation panel.
2. Click **Global Data Links**.
3. Click **New Link**.
4. Configure the link:


| Field               | Value                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Link Label**      | `Open in AppDynamics`                                                                                                                        |
| **Link to**         | `Custom URL`                                                                                                                                 |
| **Show on**         | `Property:Value pair` - Choose `appd.app.name:<YOUR APPLICATION NAME>` (E.G. `appd.app.name:Dual-Ingest-JRH`)                                                                                                                                 |
| **URL**             | `https://se-lab.saas.appdynamics.com/controller/#/location=APP_DASHBOARD&timeRange=Custom_Time_Range.BETWEEN_TIMES.{{ end_time }}.{{ start_time }}.6&application=<YOUR_APPLICATION_ID_NUMBER>&dashboardMode=force` |
| **Time format**         | `Unix time: epoch milliseconds`                                                                                                                                 |
| **Minimum trigger** | `appd.tier.name`                                                                                                                             |


{{% notice title="URL Template Syntax" style="primary" icon="lightbulb" %}}
The double curly braces `{{ end_time }}` and `{{ start_time }}` are template variables. Splunk Observability Cloud substitutes them with the actual values at click time. 

`<YOUR_APPLICATION_ID_NUMBER>` is the number from your query parameters for your specific application
{{% /notice %}}
![Global Datalink Config](../_images/global-datalink-config.png?width=50vw)

5. Click **Save**.

## Test the Global Data Link

1. Navigate back to **APM** and open a trace for your **OrderService** service.
2. Click on the root span to view its attributes.
3. Find `appd.app.name` in the attributes list -- it should now be a clickable link labeled **Open in AppDynamics**.
4. Click the link. A new browser tab should open, taking you directly to the **OrderService** application view in the AppDynamics Controller.
![Global Datalink Config](../_images/datalink.png?width=20vw)

{{% notice title="Note" style="info" icon="info-circle" %}}
You must be logged into the AppDynamics Controller in the same browser for the link to work. If you're prompted to log in, use your Cisco credentials.
{{% /notice %}}

## Navigating the Other Direction (AppD to Splunk)

Navigation in the opposite direction is also possible. AppDynamics snapshots captured in dual mode include the OTel `TraceId` under the **Data Collectors** tab.

To find the corresponding trace in Splunk Observability Cloud:

1. In the AppDynamics Controller, open a **Transaction Snapshot** for a business transaction.
2. Go to the **Data Collectors** tab.
3. Find the `TraceId` value.
4. In Splunk Observability Cloud, go to **APM → Traces** and search for that trace ID.

This gives you **bidirectional association** between the two platforms.
![AppDynamics Trace ID](../_images/appd-traceid.png?width=30vw)
