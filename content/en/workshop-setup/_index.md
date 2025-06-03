---
title: Workshop Setup
weight: 99
linkTitle: Workshop Setup
hidden: true
---

##### **Welcome to the Observability Workshop Setup Guide**

This guide will walk you through the steps required to set up your workshop environments in Splunk Observability Cloud. Whether you’re using a pre-configured organization or setting up a trial, this guide has you covered.

---

##### **Provided Organizations (For Splunk Employees Only)**

If you’re a Splunk employee, you can use the following pre-configured organizations to run Observability Workshops. These organizations have all the necessary features enabled to support any of the available workshops:

##### **Available Workshop Organizations**

- **[CoE Workshop EMEA (EU0)](https://app.eu0.signalfx.com/#/home/EsGF1sXAEAA)**  
- **[Observability Workshop EMEA (EU0)](https://app.eu0.signalfx.com/#/home/EaJHc4vAEAA)**  
- **[Observability Workshop AMER (US1)](https://app.us1.signalfx.com/#/home/EPNXccRAwAA)**  
- **[APAC-O11y-Workshop (US1)](https://app.us1.signalfx.com/#/home/FA-6LDcA4AA)**  

##### **Blocked Organizations**

The following organizations are **blocked** and cannot be used for running workshops:

- **EU Splunk Show (EU0)**  
- **US Splunk Show (US1)**  
- **Show Playground (US1)**  

---

##### **Trial Organizations**

If you’re not using a pre-configured organization, you can create a workshop environment in any **trial organization**. A default trial provides the following resources per month:

- 25 hosts
- 25 APM hosts
- 25 x 10k RUM sessions

##### **Limitations in Trial Orgs**

The following feature is **not available** in trial organizations by default and must be enabled:

- **Synthetic Monitoring**

##### **Splunk Cloud/Enterprise Requirements**

To send logs to Splunk Observability Cloud, you’ll need access to a **Splunk Cloud** or **Splunk Enterprise** environment. Ensure the following:

- An index named **splunk4rookies-workshop** exists in your Splunk environment.  
- Log Observer Connect is configured. If you’re using **Splunk Enterprise** or **Splunk Cloud Platform**, follow the [**Log Observer Connect setup instructions**](https://help.splunk.com/en/splunk-observability-cloud/manage-data/view-splunk-platform-logs/introduction-to-splunk-log-observer-connect).

##### **Trial Org Configuration**

For new trial organizations, you’ll also need to complete the steps outlined in the [**Trial Org Configuration**](4-org-configuration) section.

---

##### **Splunk4Rookies - Observability Cloud Workshop Presentation**

The official workshop presentation is available [**here**](https://docs.google.com/presentation/d/1EnP-V7mQ6c7w7yPdiiD-4szUR0SZITLFTPniz6yutqk/edit#slide=id.g260cba4d093_0_1533). Use this resource to guide your workshop participants through the material.

##### **Splunk4Rookies - FSI Vertical Observability Cloud Workshop Presentation**

The official FSI workshop presentation is available [**here**](https://docs.google.com/presentation/d/162ucBDaAEuJamtBDYEWe07js0ju4dkxfFdG2uAw0Vwc/edit?usp=sharing). Use this resource to prepare your workshop and to guide your participants through the material.