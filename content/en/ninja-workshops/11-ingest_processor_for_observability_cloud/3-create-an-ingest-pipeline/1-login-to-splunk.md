---
title: Login to Splunk Cloud
linkTitle: 3.1 Login to Splunk Cloud
weight: 2
---

In this section you will create an Ingest Pipeline which will convert Kubernetes Audit Logs to metrics which are sent to the Splunk Observability Cloud workshop organization. Before getting started you will need to access the Splunk Cloud and Ingest Processor SCS Tenant environments provided in the Splunk Show event details.

{{% notice title="Pre-requisite: Login to Splunk Enterprise Cloud" style="green" icon="running" %}}

**1.** Open the **Ingest Processor Cloud Stack** URL provided in the Splunk Show event details.

![Splunk Cloud Instance Details](../../images/show_instances_sec.png)

**2.** In the Connection info click on the **Stack URL** link to open your Splunk Cloud stack.

![Splunk Cloud Connection Details](../../images/sec_connection_details.png)

**3.** Use the `admin` username and password to login to Splunk Cloud.

![Splunk Cloud Login](../../images/sec_login.png)

**4.** After logging in, if prompted, accept the Terms of Service and click **OK**

![Splunk Cloud Login](../../images/sec_terms.png)

**5.** Navigate back to the Splunk Show event details and select the Ingest Processor SCS Tenant

![Ingest Processor Connection Details](../../images/show_instances_scs.png)

**6.** Click on the **Console URL** to access the **Ingest Processor SCS Tenant**

{{% notice title="Note" style="primary" icon="lightbulb" %}}
**Single Sign-On (SSO)**
Single Sign-on (SSO) is configured between the Splunk Data Management service (‘SCS Tenant’) and Splunk Cloud environments, so if you already logged in to your Splunk Cloud stack you should automatically be logged in to Splunk Data Management service. If you are prompted for credentials, use the credentials provided in the Splunk Cloud Stack on Splunk Show event (listed under the ‘Splunk Cloud Stack’ section.)
{{% /notice %}}

{{% /notice %}}

