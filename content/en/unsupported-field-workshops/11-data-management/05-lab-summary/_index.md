---
title: "Lab Summary"
linkTitle: "5. Lab Summary"
date: 2025-07-24T14:37:54
weight: 6
draft: false
---
In this workshop, we explored three flexible and powerful ways to ingest data into the Splunk environment.

**Ingest Actions (IA)** allow you to quickly author, preview, and deploy transformation rules at ingest time through an intuitive user interface. These rulesets allow you to define one or more rules with a few clicks, masking, truncating, routing, or eliminating data without having to handwrite stanzas in configuration files.

In this workshop, we used Ingest Actions to route certain higher-volume, lower-value data sources to lower-cost S3 storage for future use with Splunk Federated Search for S3.

**Edge Processor (EP)** goes beyond the built-in “getting data in (GDI)” functionality available in the core platform with Ingest Actions. EP uses dedicated Edge Nodes to route, filter, mask, transform, and convert data where it resides in the customer-managed infrastructure. Edge Nodes are high-performance OTel data processors that reside proximally to the source data.

As we explored today, Edge Nodes are managed centrally by a Splunk-hosted management user interface. In the lab, we created a workspace, uploaded sample data, and built a data pipeline using SPL2. We then enriched the data in the stream via a lookup and validated functionality.

**Ingest Processor (IP)** is a data processing capability that works within your Splunk Cloud Platform deployment. Use IP to configure data flows, control data format, apply transformation rules prior to indexing, and route to destinations. The Ingest Processor solution is suitable for Splunk Cloud Platform administrators who use forwarders or HTTP Event Collector (HEC) to get data into their deployments. Ingest Processor. While IP/EP management interfaces are quite similar in scope and capability, the IP removes the administrative burden of managing and maintaining edge nodes.

In the lab, we extended the base use case that we built in the IA and EP labs. We created a workspace and a pipeline to process data in the stream. We were able to preview, save, and deploy filtering, masking, and routing use cases. Finally, we converted log data to metric-formatted data and reviewed our work.

The workshop authors hope that you enjoyed these labs and are able to take with you knowledge of both how to manage your data and when to use each Splunk capability to build more effective data pipelines.

Thank you for attending today’s workshop. Happy Splunking!

# Get Started with Splunk Data Management Today

## Request access to Edge Processor or Ingest Processor

Fill out this [*form*](https://splunk.sjc1.qualtrics.com/jfe/form/SV_3BKzhdbFhr7N0NM) to request access to Data Management Pipeline Builders. If you already have access, you can directly navigate to it using the instructions on this form.

## Join the Slack channel

Get direct access to the Data Management team, ask questions, get help, and collaborate with the Community. Request access [*here*](http://splk.it/slack).

## 

## Splunk Adoption Hub

Access curated [*Splunk resources*](https://www.splunk.com/en_us/customer-success/adopt-splunk/adoption-boards.html?board=data-management) to get started and maximize value—all in one place. Tailored to your needs and regularly updated by Splunk experts.