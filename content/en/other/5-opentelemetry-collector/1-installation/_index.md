---
title: Installing OpenTelemetry Collector Contrib
linkTitle: 1. Installation
weight: 1
---

## Download the OpenTelemetry Collector Contrib distribution

The first step in installing the Open Telemetry Collector is downloading it. For our lab, we will use the `wget` command to download the `.deb` package from the OpenTelemetry Github repository.

Obtain the `.deb` package for your platform from the [**OpenTelemetry Collector Contrib releases page**](https://github.com/open-telemetry/opentelemetry-collector-releases/releases)

``` bash
wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.96.0/otelcol-contrib_0.96.0_linux_amd64.deb
```

## Install the OpenTelemetry Collector Contrib distribution

Install the `.deb` package using `dpkg`. Take a look at the **dpkg Output** tab below to see what the example output of a successful install will look like:

{{< tabs >}}
{{% tab title="Install" %}}

``` bash
sudo dpkg -i otelcol-contrib_0.96.0_linux_amd64.deb
```

{{% /tab %}}
{{% tab title="dpkg Output" %}}

``` text
Selecting previously unselected package otelcol-contrib.
(Reading database ... 64218 files and directories currently installed.)
Preparing to unpack otelcol-contrib_0.96.0_linux_amd64.deb ...
Unpacking otelcol-contrib (0.96.0) ...
Setting up otelcol-contrib (0.96.0) ...
Created symlink /etc/systemd/system/multi-user.target.wants/otelcol-contrib.service → /lib/systemd/system/otelcol-contrib.service.
```

{{% /tab %}}
{{< /tabs >}}
