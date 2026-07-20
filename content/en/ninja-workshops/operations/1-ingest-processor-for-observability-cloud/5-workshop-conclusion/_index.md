---
title: Conclusion
linkTitle: 5. Conclusion
weight: 1
---

In this workshop, you walked through the entire process of optimizing Kubernetes log management by converting detailed log events into actionable metrics using **Splunk Ingest Pipelines**. You started by defining a pipeline that efficiently converts Kubernetes audit logs into metrics, drastically reducing the data volume while retaining critical information. You then ensured the raw log events were securely stored in S3 for long-term retention and deeper analysis.

![Kubernetes Audit Event](../images/audit_event.png?width=40vw)

Next, you demonstrated how to enhance these metrics by adding key dimensions from the raw events, enabling us to drill down into specific actions and resources. you created a chart that filtered the metrics to focus on errors, breaking them out by resource and action. This allowed us to pinpoint exactly where issues were occurring in real-time.

![Ingest Pipeline](../images/ingest_pipeline_dimensions.png?width=40vw)

The real-time architecture of **Splunk Observability Cloud** means that these metrics can trigger alerts the moment an issue is detected, significantly reducing the Mean Time to Detection (MTTD). Additionally, you showed how this chart can be easily saved to new or existing dashboards, ensuring ongoing visibility and monitoring of critical metrics.

![Audit Dashboard](../images/audit_dashboard.png?width=40vw)

The value behind this approach is clear: by converting logs to metrics using **Ingest Processor**, you not only streamline data processing and reduce storage costs but also gain the ability to monitor and respond to issues in real-time using **Splunk Observability Cloud**. This results in faster problem resolution, improved system reliability, and more efficient resource utilization, all while maintaining the ability to retain and access the original logs for compliance or deeper analysis.

<center><h1>Happy Splunking!</h1></center>

![Dancing Buttercup](../images/Splunk-dancing-buttercup-GIF-103.gif?width=30vw)
