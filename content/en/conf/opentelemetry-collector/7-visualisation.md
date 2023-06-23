---
title: Data Visualisations
linkTitle: 7. Visualisation
weight: 7
---

## Splunk Observability Cloud

Now that we have configured the OpenTelemetry Collector to send metrics to Splunk Observability Cloud, let's take a look at the data in Splunk Observability Cloud. If you have not received an invite to Splunk Observability Cloud, your instructor will provide you with login credentials.

Once logged into Splunk Observability Cloud, using the left-hand navigation, navigate to **Dashboards**:

![menu-dashboards](../images/menu-dashboards.png)

In the search box, search for **OTel Contrib**:

![search-dashboards](../images/search-dashboards.png)

Click on the **OTel Contrib Dashboard** dashboard to open it:

![otel-dashboard](../images/otel-dashboard.png)

In the **Filter** box, at the top of the dashboard, type in **conf** and select **conf.attendee.name**:

![search-filter](../images/search-filter.png)

You can either start typing in your name you configured for `conf.attendee.name` in the `config.yaml` or you can select your name from the list:

![select-conf-attendee-name](../images/select-conf-attendee-name.png)

You can now see the host metrics for the host upon which you configured the OpenTelemetry Collector.

{{% attachments sort="asc" /%}}
