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
sudo systemctl status otelcol-contrib
```

``` text
● otelcol-contrib.service - OpenTelemetry Collector Contrib
     Loaded: loaded (/lib/systemd/system/otelcol-contrib.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2023-04-27 12:38:27 BST; 1h 51min ago
   Main PID: 3393 (otelcol-contrib)
      Tasks: 7 (limit: 1116)
     Memory: 49.1M
        CPU: 28.741s
     CGroup: /system.slice/otelcol-contrib.service
             └─3393 /usr/bin/otelcol-contrib --config=/etc/otelcol-contrib/config.yaml

Apr 27 14:30:16 otel otelcol-contrib[3393]: Timestamp: 2023-04-27 13:30:15.958341145 +0000 UTC
Apr 27 14:30:16 otel otelcol-contrib[3393]: Value: 0.000000
Apr 27 14:30:16 otel otelcol-contrib[3393]: NumberDataPoints #7
Apr 27 14:30:16 otel otelcol-contrib[3393]: Data point attributes:
Apr 27 14:30:16 otel otelcol-contrib[3393]:      -> cpu: Str(cpu0)
Apr 27 14:30:16 otel otelcol-contrib[3393]:      -> state: Str(wait)
Apr 27 14:30:16 otel otelcol-contrib[3393]: StartTimestamp: 2023-04-27 09:01:16 +0000 UTC
Apr 27 14:30:16 otel otelcol-contrib[3393]: Timestamp: 2023-04-27 13:30:15.958341145 +0000 UTC
Apr 27 14:30:16 otel otelcol-contrib[3393]: Value: 9.700000
Apr 27 14:30:16 otel otelcol-contrib[3393]:         {"kind": "exporter", "data_type": "metrics", "name": "logging"}
```
