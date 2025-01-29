---
title: How to connect to your workshop environment
linkTitle: 1.1 How to connect to your workshop environment
weight: 2
---

1. How to retrieve the URL for your Splunk Enterprise Cloud instances.
2. How to access the Splunk Observability Cloud workshop organization.

---

## 1. Splunk Cloud Instances

There are three instances that will be used throughout this workshop which have already been provisioned for you:
1. Splunk Enterprise Cloud
2. Splunk Ingest Processor (SCS Tenant)
3. Splunk Observability Cloud

The Splunk Enterprise Cloud and Ingest Processor instances are hosted in [Splunk Show](https://show.splunk.com). If you were invited to the workshop, you should have received an email with an invite to the event in [Splunk Show](https://show.splunk.com) or a link to the event will have been provided at the beginning of the workshop. 

Login to Splunk Show using your [splunk.com](https://login.splunk.com/) credentials. You should see the event for this workshop. Open the event to see the instance details for your Splunk Cloud and Ingest Processor instances. 

{{% notice title="Note" style="primary"  icon="lightbulb" %}}

Take note of the Participant Number provided in your Splunk Show event details. This number will be included in the `sourcetype` that you will use for searching and filtering the Kubernetes data. Because this is a shared environment only use the participant number provided so that other participants data is not effected.

{{% /notice %}}

## 2. Splunk Observability Cloud Instances

You should have also received an email to access the Splunk Observability Cloud workshop organization (You may need to check your spam folder). If you have not received an email, let your workshop instructor know. To access the environment click the **Join Now** button.

![Splunk Observability Cloud Invitation](../../images/workshop_invitation.png)

{{% notice title="Important" style="info" %}}
If you access the event before the workshop start time, your instances may not be available yet. Don't worry, they will provided once the workshop begins.
{{% /notice %}}

Additionally, you have been invited to a Splunk Observability Cloud workshop organization. The invitation includes a link to the environment. If you don't have a Splunk Observability Cloud account already, you will be asked to create one. If you already have one, you can login to the instance and you will see the workshop organization in your available organizations.

