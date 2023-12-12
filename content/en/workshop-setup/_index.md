---
title: Workshop Setup
weight: 99
linkTitle: Workshop Setup
hidden: true
---

Welcome to the Observability Workshop Setup Guide. This guide will walk you through the steps required to set up your workshop environments.

## Existing Workshop Orgs

The following Organizations can be used for running Observability Workshops. They have all the features enabled to successfully run any of the available workshops:

- [**CoE Workshop EMEA (EU0)**](https://app.eu0.signalfx.com/#/home/EsGF1sXAEAA)
- [**Observability Workshop EMEA (EU0)**](https://app.eu0.signalfx.com/#/home/EaJHc4vAEAA)
- [**Observability Workshop AMER (US1)**](https://app.us1.signalfx.com/#/home/EPNXccRAwAA)
- [**APAC-O11y-Workshop (US1)**](https://app.us1.signalfx.com/#/home/FA-6LDcA4AA)

## Trial Orgs

It is also possible to create workshop environments in any trial Org. A default trial provides 25 hosts, 25 APM hosts and 25 x 10k RUM sessions per month. Please note, the following features are not available in Trial Orgs by default and must be enabled:

- Synthetic Monitoring

Also, a Splunk Cloud/Enterprise environment is required to be able to send logs. In Splunk Cloud/Enterprise make sure an index exists called **splunk4rookies-workshop**. A Log Observer Connect configuration will also need to be completed.

The following Orgs are blacklisted and cannot be used for running workshops:

- **EU Splunk Show (EU0)**
- **US Splunk Show (US1)**
- **Show Playground (US1)**

## Splunk4Rookies Workshop Presentation

Click [**here**](https://docs.google.com/presentation/d/1EnP-V7mQ6c7w7yPdiiD-4szUR0SZITLFTPniz6yutqk/edit#slide=id.g260cba4d093_0_1533) to access the Splunk4Rookies Workshop Presentation.
