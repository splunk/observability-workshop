---
title: 4. Trial Org Configuration
weight: 4
---

## Log Observer Connect

The workshops require a Log Observer Connect configuration to be setup. This is required to be able to send logs from the workshop instances to Splunk Cloud/Enterprise. **SWiPE** provides a simple form to configure this and is available [**here**](https://swipe.splunk.show/log_observer_connect).

![Log Observer Connect](../images/log-observer-connect.png)

## Log Field Aliasing

Log Field Aliasing configuration is required to ensure Related Content works correctly in the Splunk Observability Cloud UI. Configure as per the following:

![Log Field Aliasing](../images/log-field-aliasing.png)

## APM MetricSets

APM MetricSets need to be configured for the tags in the screenshot below.
![APM MetricSets](../images/apm-metricsets.png)
