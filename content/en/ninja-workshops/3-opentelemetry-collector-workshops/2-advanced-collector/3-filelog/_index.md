---
title: 3. FileLog Setup
linkTitle: 3. FileLog Setup
time: 10 minutes
weight: 3
---

The [**FileLog Receiver**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/filelogreceiver/README.md) in the OpenTelemetry Collector is used to ingest logs from files.

It monitors specified files for new log entries and streams those logs into the Collector for further processing or exporting. It is useful for testing and development purposes.

For this part of the workshop, the `loadgen` will generate logs using random quotes:

```golang
lotrQuotes := []string{
    "One does not simply walk into Mordor.",
    "Even the smallest person can change the course of the future.",
    "All we have to decide is what to do with the time that is given us.",
    "There is some good in this world, and it's worth fighting for.",
}

starWarsQuotes := []string{
    "Do or do not, there is no try.",
    "The Force will be with you. Always.",
    "I find your lack of faith disturbing.",
    "In my experience, there is no such thing as luck.",
}
```

The **FileLog receiver** in the `agent` will read these log lines and send them to the `gateway`.

{{% notice title="Exercise" style="green" icon="running" %}}

- In the **Logs terminal** window, change into the `[WORKSHOP]` directory and create a new subdirectory named `3-filelog`.
- Next, copy `*.yaml` from `2-gateway` into `3-filelog`.

> [!IMPORTANT]
> **Change _ALL_ terminal windows to the `[WORKSHOP]/3-filelog` directory.**

```text { title="Updated Directory Structure" }
[WORKSHOP]
└── 3-filelog
    ├── agent.yaml
    └── gateway.yaml
```

Start the `loadgen` and this will begin writing lines to a file named `quotes.log`:

{{% tabs %}}
{{% tab title="Log Load Generator" %}}

```bash
../loadgen -logs
```

{{% /tab %}}
{{% tab title="Log Load Generator Output" %}}

```text
Writing logs to quotes.log. Press Ctrl+C to stop.
```

{{% /tab %}}
{{% /tabs %}}
{{% /notice %}}
