---
title: Viewing the Logs
linkTitle: 5. Viewing the Logs
weight: 5
---

Once the containers are patched they will be restarted, let's go back to the **Splunk Observability Cloud** with the URL provided by the Instructor to check our cluster in the Kubernetes Navigator.

After a couple of minutes or so you should see that the Pods are being restarted by the operator and the Zero config container will be added. This will look similar to the screenshot below:

![restart](../../images/k8s-navigator-restarted-pods.png)

Wait for the pods to turn green again (you may want to refresh the screen), then from the left-hand menu click on the **Log Observer** ![Logo](../images/logo-icon.png?classes=inline&height=25px) and ensure **Index** is set to **splunk4rookies-workshop**.

Next, click **Add Filter** search for the field `deployment.environment` and select the value of rou Workshop (Remember the INSTANCE value ?) and click `=` (include). You should now see only the log messages from your PetClinic application.

Next search for the field  `service_name` select the value `customers-service` and click `=` (include). Now the log files should be reduced to just the lines from your `customers-service`.

Wait for Log Lines to show up with an injected trace-id like trace_id=08b5ce63e46ddd0ce07cf8cfd2d6161a as shown below **(1)**:

![Log Observer](../../images/log-observer-trace-info.png)

Click on a line with an injected trace_id, this should be all log lines created by your services that are part of a trace **(1)**.

A Side pane opens where you can see the related information about your logs. including the relevant Trace and Span IDs **(2**).
