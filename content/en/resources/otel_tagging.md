---
title: Naming Conventions for Tagging with OpenTelemetry and Splunk
linkTitle: OpenTelemetry Tagging
description: When deploying OpenTelemetry in a large organization, it’s critical to define a standardized naming convention for tagging, and a governance process to ensure the convention is adhered to.
weight: 2
---

## Introduction

When deploying OpenTelemetry in a large organization, it’s critical to define a standardized naming convention for tagging, and a governance process to ensure the convention is adhered to.

This ensures that MELT data collected via OpenTelemetry can be efficiently utilized for alerting, dashboarding, and troubleshooting purposes.  It also ensures that users of Splunk Observability Cloud can quickly find the data they’re looking for.

Naming conventions also ensure that data can be aggregated effectively.  For example, if we wanted to count the number of unique hosts by environment, then we must use a standardized convention for capturing the host and environment names.

## Attributes vs. Tags

Before we go further, let’s make a note regarding terminology.  Tags in OpenTelemetry are called “attributes”.  Attributes can be attached to metrics, logs, and traces, either via manual instrumentation or automated instrumentation.

Attributes can also be attached to metrics, logs, and traces at the OpenTelemetry collector level, using various processors such as the [Resource Detection processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourcedetectionprocessor).

Once traces with attributes are ingested into Splunk Observability Cloud, they are available as “tags”. Optionally, attributes collected as part of traces can be used to create [Troubleshooting Metric Sets](https://docs.splunk.com/Observability/apm/span-tags/metricsets.html#troubleshooting-metricsets), which can in turn be used with various features such as [Tag Spotlight](https://docs.splunk.com/Observability/apm/span-tags/tag-spotlight.html).

Alternatively, attributes can be used to create [Monitoring Metric Sets](https://docs.splunk.com/Observability/apm/span-tags/metricsets.html#monitoring-metricsets), which can be used to drive alerting.

## Resource Semantic Conventions

[OpenTelemetry resource semantic conventions](https://github.com/open-telemetry/semantic-conventions/tree/main) should be used as a starting point when determining which attributes an organization should standardize on. In the following sections, we’ll review some of the more commonly used attributes.

### Service Attributes

A number of attributes are used to describe the service being monitored.

`service.name` is a required attribute that defines the logical name of the service. It’s added automatically by the OpenTelemetry SDK but can be customized.  It’s best to keep this simple (i.e. `inventoryservice` would be better than `inventoryservice-prod-hostxyz`, as other attributes can be utilized to capture other aspects of the service instead).

The following service attributes are recommended:

- `service.namespace` this attribute could be utilized to identify the team that owns the service
- `service.instance.id` is used to identify a unique instance of the service
- `service.version` is used to identify the version of the service

### Telemetry SDK

These attributes are set automatically by the SDK, to record information about the instrumentation libraries being used:

- `telemetry.sdk.name` is typically set to `opentelemetry`
- `telemetry.sdk.language` is the language of the SDK, such as `java`
- `telemetry.sdk.version` identifies which version of the SDK is utilized

### Containers

For services running in containers, there are numerous attributes used to describe the container runtime, such as `container.id`, `container.name`, and `container.image.name`.  The full list can be found [here](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/resource/container.md).

### Hosts

These attributes describe the host where the service is running, and include attributes such as `host.id`, `host.name`, and `host.arch`. The full list can be found [here](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/resource/host.md).

### Deployment Environment

The `deployment.environment` attribute is used to identify the environment where the service is deployed, such as **staging** or **production**.

Splunk Observability Cloud uses this attribute to enable related content (as described [here](https://docs.splunk.com/observability/metrics-and-metadata/enablerelatedcontent.html)), so it’s important to include it.

### Cloud

There are also attributes to capture information for services running in public cloud environments, such as AWS.  Attributes include cloud.provider, `cloud.account.id`, and `cloud.region`.

The full list of attributes can be found [here](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/resource/cloud.md).

Some cloud providers, such as [GCP](https://github.com/open-telemetry/semantic-conventions/tree/main/docs/resource/cloud-provider/gcp), define semantic conventions specific to their offering.

### Kubernetes

There are a number of standardized attributes for applications running in Kubernetes as well. Many of these are added automatically by Splunk’s distribution of the OpenTelemetry collector, as described [here](https://docs.splunk.com/observability/metrics-and-metadata/enablerelatedcontent.html#splunk-infrastructure-monitoring).

These attributes include `k8s.cluster.name`, `k8s.node.name`, `k8s.pod.name`, `k8s.namespace.name`, and `kubernetes.workload.name`.

## Best Practices for Creating Custom Attributes

Many organizations require attributes that go beyond what’s defined in OpenTelemetry’s resource semantic conventions.

In this case, it’s important to avoid naming conflicts with attribute names already included in the semantic conventions.  So it’s a good idea to check the semantic conventions before deciding on a particular attribute name for your naming convention.

In addition to a naming convention for attribute names, you also need to consider attribute values.  For example, if you’d like to capture the particular business unit with which an application belongs, then you’ll also want to have a standardized list of business unit values to choose from, to facilitate effective filtering.

The OpenTelemetry community provides guidelines that should be followed when naming attributes as well, which can be found [here](https://opentelemetry.io/docs/specs/otel/common/attribute-naming/).

The [Recommendations for Application Developers](https://opentelemetry.io/docs/specs/otel/common/attribute-naming/#recommendations-for-application-developers) section is most relevant to our discussion.

They recommend:

- Prefixing the attribute name with your company’s domain name, e.g. `com.acme.shopname` (if the attribute may be used outside your company as well as inside).
- Prefixing the attribute name with the application name, if the attribute is unique to a particular application and is only used within your organization.
- Not using existing OpenTelemetry semantic convention names as a prefix for your attribute name.
- Consider submitting a proposal to add your attribute name to the OpenTelemetry specification, if there’s a general need for it across different organizations and industries.
- Avoid having attribute names start with `otel.*`, as this is reserved for OpenTelemetry specification usage.

## Metric Cardinality Considerations

One final thing to keep in mind when deciding on naming standards for attribute names and values is related to metric cardinality.

Metric cardinality is defined as **the number of unique metric time series (MTS) produced by a combination of metric **names and their associated dimensions**.

A metric has high cardinality when it has a high number of dimension keys and a high number of possible unique values for those dimension keys.

For example, suppose your application sends in data for a metric named `custom.metric`.  In the absence of any attributes, `custom.metric` would generate a single metric time series (MTS).  

On the other hand, if `custom.metric` includes an attribute named `customer.id`, and there are thousands of customer ID values, this would generate thousands of metric time series, which may impact costs and query performance.

Splunk Observability Cloud provides a [report](https://docs.splunk.com/Observability/infrastructure/metrics-pipeline/metrics-usage-report.html) that allows for the management of metrics usage. And [rules](https://docs.splunk.com/Observability/infrastructure/metrics-pipeline/use-metrics-pipeline.html) can be created to drop undesirable dimensions.  However, the first line of defence is understanding how attribute name and value combinations can drive increased metric cardinality.

## Summary

In this document, we highlighted the importance of defining naming conventions for OpenTelemetry tags, preferably before starting a large rollout of OpenTelemetry instrumentation.

We discussed how OpenTelemetry’s resource semantic conventions define the naming conventions for several attributes, many of which are automatically collected via the OpenTelemetry SDKs, as well as processors that run within the OpenTelemetry collector.

Finally, we shared some best practices for creating your attribute names, for situations where the resource semantic conventions are not sufficient for your organization’s needs.
