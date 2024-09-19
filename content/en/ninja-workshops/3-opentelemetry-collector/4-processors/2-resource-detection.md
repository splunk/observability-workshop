---
title: OpenTelemetry Collector Processors
linkTitle: 4.2 Resource Detection
weight: 2
---

## Resource Detection Processor

The **resourcedetection** processor can be used to detect resource information from the host and append or override the resource value in telemetry data with this information.

By default, the hostname is set to the FQDN if possible, otherwise, the hostname provided by the OS is used as a fallback. This logic can be changed from using using the `hostname_sources` configuration option. To avoid getting the FQDN and use the hostname provided by the OS, we will set the `hostname_sources` to `os`.

{{% tab title="System Resource Detection Processor Configuration" %}}

``` yaml {hl_lines="3-7"}
processors:
  batch:
  resourcedetection/system:
    detectors: [system]
    system:
      hostname_sources: [os]
```

{{% /tab %}}

If the workshop instance is running on an AWS/EC2 instance we can gather the following tags from the EC2 metadata API (this is not available on other platforms).

- `cloud.provider ("aws")`
- `cloud.platform ("aws_ec2")`
- `cloud.account.id`
- `cloud.region`
- `cloud.availability_zone`
- `host.id`
- `host.image.id`
- `host.name`
- `host.type`

We will create another processor to append these tags to our metrics.

{{% tab title="EC2 Resource Detection Processor Configuration" %}}

``` yaml {hl_lines="7-8"}
processors:
  batch:
  resourcedetection/system:
    detectors: [system]
    system:
      hostname_sources: [os]
  resourcedetection/ec2:
    detectors: [ec2]
```

{{% /tab %}}
