---
title: Generate traffic using Locust
weight: 3
---

## 1. Generate traffic

The Online Boutique deployment contains a container running Locust that we can use to generate load traffic against the website to generate metrics, traces and spans.

Locust is available on port 8080 of the EC2 instance's IP address. Open a new tab in your web browser and go to `http://{==EC2-IP==}:8080/`, you will then be able to see the Locust running.

![Locust](../../../images/locust.png)

Set the **Spawn rate** to be 2 and click **Start Swarming**, this will start a gentle continous load on the application.

![Spawn Rate](../../../images/locust-spawn-rate.png)

![Statistics](../../../images/locust-statistics.png)

---

Now go to **![dashboards button](../../../images/dashboards.png) Dashboards → All Dashboards → APM Services → Service**.

For this we need to know the name of your application environment. In this workshop all the environments use: `{==hostname==}-apm-env`.

To find the hostname, on the AWS/EC2 instance run the following command:

{{< tabpane >}}
  {{< tab header="Echo Hostname" lang="bash" >}}
    echo $(hostname)-apm-env
  {{< /tab >}}
  {{< tab header="Output Example" lang= "bash" >}}
    bdzx-apm-env
  {{< /tab >}}
{{< /tabpane >}}

Select your environment you found in the previous step then select the `frontend` service and set time to Past 15 minutes.

![APM Dashboard](../../../images/online-boutique-service-dashboard.png)

With this automatically generated dashboard you can keep an eye out for the health of your service(s) using RED (Rate, Error & Duration) metrics. It provides various performance related charts as well as correlated information on the underlying host and Kubernetes pods (if applicable).

Take some time to explore the various charts in this dashboard

---

## 2. Verify Splunk APM metrics

In the left hand menu card click on APM ![apm button](../../../images/apm.png) this will bring you to the APM Overview dashboard:

![select APM](../../../images/online-boutique-apm.png)

Select the **Explore** on the right hand side and select your environment you found before and set the time to 15 minutes. This will show you the automatically generated Dependency/Service Map for the Online Boutique application.

It should look similar to the screenshot below:

![Online Boutique in APM](../../../images/online-boutique-map.png)

The legend at the bottom of the page explains the different visualizations in the Dependency/Service Map.

![APM Legend](../../../images/apm-legend.png)

* Service requests, error rate and root error rate.
* Request rate, latency and error rate

Also in this view you can see the overall Error and Latency rates over time charts.

## 3. OpenTelemetry Dashboard

Once the Open Telemetery Collector is deployed the platform will automatically provide a built in dashboard display OpenTelemetry Collector metrics.

From the top left hamburger menu, select ![dashboards button](../../../images/dashboards.png) **Dashboards → OpenTelemetry Collector**, scroll all the way to the bottom of the page and validate metrics and spans are being sent:

![OpenTelemetry Collector dashboard](../../../images/otel-dashboard.png)

## 4. OpenTelemetry zpages

To debug the traces being sent you can use the zpages extension. [zpages][zpages] are part of the OpenTelemetry collector and provide live data for troubleshooting and statistics. They are available on port `55679` of the EC2 instance's IP address. Open a new tab in your web browser and enter in `http://{==EC2-IP==}:55679/debug/tracez`, you will then be able to see the zpages output.

[zpages]: https://github.com/open-telemetry/opentelemetry-specification/blob/main/experimental/trace/zpages.md#tracez

![zpages](../../../images/zpages.png)

Alternatively, from your shell prompt you can run a text based browser:

{{< tabpane >}}
  {{< tab header="Lynx Command" lang="text" >}}
    lynx http://localhost:55679/debug/tracez
  {{< /tab >}}
{{< /tabpane >}}
