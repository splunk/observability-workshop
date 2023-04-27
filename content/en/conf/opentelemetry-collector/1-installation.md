---
title: Installing OpenTelemetry Collector Contrib
linkTitle: 1. Installation
weight: 1
---

## 1. Downloading the OpenTelemetry Collector Contrib distribution

Obtain the `.deb` package for your platform from the [OpenTelemetry Collector Contrib releases page](https://github.com/open-telemetry/opentelemetry-collector-releases/releases)

``` bash
wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.75.0/otelcol-contrib_0.75.0_linux_amd64.deb
```

## 2. Installing the OpenTelemetry Collector Contrib distribution

Install the `.deb` package using `dpkg`:

``` bash
sudo dpkg -i otelcol-contrib_0.75.0_linux_amd64.deb
```

``` text
Selecting previously unselected package otelcol-contrib.
(Reading database ... 64218 files and directories currently installed.)
Preparing to unpack otelcol-contrib_0.75.0_linux_amd64.deb ...
Unpacking otelcol-contrib (0.75.0) ...
Setting up otelcol-contrib (0.75.0) ...
Created symlink /etc/systemd/system/multi-user.target.wants/otelcol-contrib.service → /lib/systemd/system/otelcol-contrib.service.
```

## 3. Confirm the Collector is running

``` bash
ps -ax | grep otel
```

``` text
ubuntu@otel:~$ ps -ax | grep otel
   1658 ?        Ssl    0:00 /usr/bin/otelcol-contrib --config=/etc/otelcol-contrib/config.yaml
```
