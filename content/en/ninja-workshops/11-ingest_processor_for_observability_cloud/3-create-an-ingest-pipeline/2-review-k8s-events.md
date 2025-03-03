---
title: Review Kubernetes Audit Logs
linkTitle: 3.2 Review Kubernetes Audit Logs
weight: 3
---

In this section you will review the Kubernetes Audit Logs that are being collected. You can see that the events are quite robust, which can make charting them inefficient. To address this, you will create an Ingest Pipeline in Ingest Processor that will convert these events to metrics that will be sent to Splunk Observability Cloud. This will allow you to chart the events much more efficiently and take advantage of the real-time streaming metrics in Splunk Observability Cloud.

{{% notice title="Exercise: Create Ingest Pipeline" style="green" icon="running" %}}

**1.** Open your **Ingest Processor Cloud Stack** instance using the URL provided in the Splunk Show workshop details.

**2.** Navigate to **Apps** → **Search and Reporting**

![Search and Reporting](../../images/search_and_reporting.png?width=20vw)

**3.** In the search bar, enter the following SPL search string.

{{% notice title="Note" style="primary" icon="lightbulb" %}}
Make sure to replace `USER_ID` with the User ID provided in your Splunk Show instance information.
{{% /notice %}}

``` sh
### Replace USER_ID with the User ID provided in your Splunk Show instance information
index=main sourcetype="kube:apiserver:audit:USER_ID"
```

**4.** Press **Enter** or click the green magnifying glass to run the search.

![Kubernetes Audit Log](../../images/k8s_audit_log.png)

{{% notice title="Note" style="info" %}}
You should now see the Kubernetes Audit Logs for your environment. Notice that the events are fairly robust. Explore the available fields and start to think about what information would be good candidates for metrics and dimensions. Ask yourself: What fields would I like to chart, and how would I like to be able to filter, group, or split those fields?
{{% /notice %}}

{{%/ notice %}}
