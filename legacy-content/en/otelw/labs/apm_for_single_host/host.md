---
title: 'Install Otel Collector On Host'
weight: 1
---

`Splunk Observability -> Data Setup -> Linux`

Choose the following:

| Key | Value |
| ----- | ---- |
| **Access Token** | Select from list |
| **Mode** | Agent |
| **Log Collection** | No |  

Follow Data Setup Wizard for instructions on Linux installation:

![Data Setup](../../../images/03-datasetup.png)

![Linux](../../../images/04-datasetup-linux.png)

![Linux Install](../../../images/05-datasetup-linuxinstall.png)

Check status of collector:

```bash
sudo systemctl status splunk-otel-collector
```

Should output something like:

```
● splunk-otel-collector.service - Splunk OpenTelemetry Collector
     Loaded: loaded (/lib/systemd/system/splunk-otel-collector.service; enabled; vendor preset: enabled)
    Drop-In: /etc/systemd/system/splunk-otel-collector.service.d
             └─service-owner.conf
     Active: active (running) since Sun 2021-10-31 13:07:27 UTC; 1min 11s ago
   Main PID: 37949 (otelcol)
      Tasks: 9 (limit: 19200)
     Memory: 100.2M
     CGroup: /system.slice/splunk-otel-collector.service
             └─37949 /usr/bin/otelcol

Oct 31 13:07:27 ip-172-31-70-180 otelcol[37949]: 2021-10-31T13:07:27.556Z        info        builder/receivers_builder.go:73  >
Oct 31 13:07:27 ip-172-31-70-180 otelcol[37949]: 2021-10-31T13:07:27.556Z        info        builder/receivers_builder.go:68  >
Oct 31 13:07:27 ip-172-31-70-180 otelcol[37949]: 2021-10-31T13:07:27.556Z        info        builder/receivers_builder.go:73  >
Oct 31 13:07:27 ip-172-31-70-180 otelcol[37949]: 2021-10-31T13:07:27.556Z        info        healthcheck/handler.go:129       >
Oct 31 13:07:27 ip-172-31-70-180 otelcol[37949]: 2021-10-31T13:07:27.556Z        info        service/telemetry.go:92        Se>
Oct 31 13:07:27 ip-172-31-70-180 otelcol[37949]: 2021-10-31T13:07:27.557Z        info        service/telemetry.go:116        S>
Oct 31 13:07:27 ip-172-31-70-180 otelcol[37949]: 2021-10-31T13:07:27.557Z        info        service/collector.go:230        S>
Oct 31 13:07:27 ip-172-31-70-180 otelcol[37949]: 2021-10-31T13:07:27.557Z        info        service/collector.go:132        E>
Oct 31 13:07:37 ip-172-31-70-180 otelcol[37949]: 2021-10-31T13:07:37.826Z        info        hostmetadata/metadata.go:75      >
Oct 31 13:07:37 ip-172-31-70-180 otelcol[37949]: 2021-10-31T13:07:37.826Z        info        hostmetadata/metadata.go:83      >
```

Your machine will be visible in Splunk Observability in `Infrastructure` either in the public cloud platform you are using or `My Data Center` if you are using Multipass or any other non public cloud machine.