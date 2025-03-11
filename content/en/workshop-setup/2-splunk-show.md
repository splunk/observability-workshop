---
title: 2. Using Splunk Show
weight: 2
---

##### **Observability Workshop Templates**

Splunk Show offers two templates for Observability workshops. Select the one that best fits your needs:

| Workshop Type | Description | Template | |
| --- | --- | --- | --- |
| **Splunk4Rookies - Observability** | This workshop template is designed for beginners. The template pre-deploys the **OpenTelemetry Collector** and the **Online Boutique** application. Attendees only need a browser to participate and complete the workshop. | [**Rookies**](https://show.splunk.com/template/262/) | ![Rookies](../images/rookies.png) |
| **Splunk4Ninjas - Observability** | This workshop template is tailored for **advanced** users. The template sets up an instance with all necessary tools for hands-on activities. No resources are deployed or running at launch, allowing attendees to configure and deploy as needed. | [**Ninja**](https://show.splunk.com/template/428/) | ![Ninjas](../images/ninjas.png) |

{{% notice  style="primary" title="**Ninja Workshops Only**" icon="user-ninja" %}}

Set the **Estimated Participants** to the number of attendees you expect, and match this value in the **O11y Shop Quantity** field.  
> [!TIP]
> **Tip:** Over-provision by **10% - 20%** to accommodate last-minute attendees.  

{{% /notice %}}

---

##### **Important Configuration Tips**

When provisioning your instances, keep the following in mind:

1. **Operating Hours**
   - Set **Operating hours** to **Run always (24/7)**.
   - This prevents the instance from being suspended, which could result in a new IP address and break RUM and Synthetics configurations.

2. **DNS Name**
   - Assign a **DNS name** to the instance(s).
   - This makes it easier to locate and manage environments in Splunk Observability Cloud during the workshop.

3. **Splunk Observability Cloud Realm and SWiPE ID**
   - Select your Splunk Observability Cloud **Realm**.
   - Enter the **SWiPE ID** generated for your workshop.

4. Select the appropriate event type: **Normal Workshop**, **Private Event**, or **Public Event**.

---

### **Additional Resources**

For more detailed guidance on using Splunk Show, refer to the [**Splunk Show User Guide**](http://go/show/user-guide).
