---
title: 3. Verify Under the New Substrate
weight: 3
---

The Java app from Phase 3 has been emitting OTLP at `localhost:4318` continuously through this whole transition. Once the standalone collector came up in the previous step, those traces resumed flowing through the new pipeline. Verify the data is intact and look at what was painful in Phase 3 that is now solved.

## Verify AppDynamics is Unaffected

Open the [AppDynamics Controller](https://se-lab.saas.appdynamics.com/controller/), open your application, and confirm:

- The **OrderService** tier is still visible in the flow map.
- Business transactions for `/order` and `/inventory` are still recording.
- **Servers** still shows the host with CPU, memory, disk, and network from the machine agent's SIM data.

The AppD side of both APM and infrastructure flows the same way it did in Phase 3. Swapping the OTel runtime did not touch AppDynamics.

## Verify Splunk APM

1. Open [Splunk Observability Cloud](https://app.signalfx.com).
2. Click **APM** in the left navigation panel.
3. In the **Environment** dropdown, select `<INSTANCE>-appd-dual`. The `resource/workshop` processor in the workshop config stamps that environment regardless of which collector substrate is running it.

![AppDynamics Application](../../_images/o11y-service.png?width=30vw)

{{% notice title="Give it a few minutes" style="info" icon="info-circle" %}}
Allow 2 to 5 minutes after the standalone collector starts for any in-flight queue to drain and the new pipeline to fully populate.
{{% /notice %}}

You should still see **OrderService** in the service list, with traces continuous from Phase 3.

## Explore a Trace

1. Click on the **OrderService** service.
2. Click **Traces** to view individual traces.
3. Select a trace for `GET /order` to open the trace detail waterfall.

![APM waterall](../../_images/waterfall.png)

## Confirm the AppDynamics Correlation Attributes

Click on a **root span** and look at the span attributes. The AppDynamics correlation attributes are still there because they are added by the AppD agent itself, independent of which collector forwards the span:

| Attribute | Example value |
|---|---|
| `appd.app.name` | `Dual-Ingest-YOURINITIALS` |
| `appd.tier.name` | `OrderService` |
| `appd.bt.name` | `/order` or `/inventory` |
| `appd.request.guid` | The AppDynamics request GUID |

{{% notice title="Key insight" style="primary" icon="lightbulb" %}}
The `appd.tier.name` attribute also appears on spans in the middle of a trace whenever the tier changes. In a multi-tier application, each span carries the correct AppDynamics tier identity.
{{% /notice %}}

## Verify Splunk Infrastructure

1. Click **Metric Finder** in the left navigation panel.
2. Search for `cpu.utilization` and open the chart.
3. Filter on `host.name=${INSTANCE}`.

You should see a continuous time series. The data path is now the standalone collector's `hostmetrics` receiver, exporting via `signalfx`. The `resource/workshop` processor still stamps `deployment.environment=${INSTANCE}-appd-dual`, same as Phase 3.

## What Got Better Versus Phase 3

Now look at the things that hurt in Phase 3 and confirm the standalone install handled them.

### Environment variables are persistent

```bash
sudo cat /etc/otel/collector/splunk-otel-collector.conf
```

Every `SPLUNK_*` variable you exported by hand in Phase 3 is now in this file. `systemd` reads it on every restart and reboot. No more shell-rc plumbing.

### The Smart Agent process list works

The install script shipped the bundle at `/usr/lib/splunk-otel-collector/agent-bundle`. The workshop config's `smartagent/processlist` receiver now finds it, scrapes process data, and exports it through `signalfx`. In Splunk Observability Cloud, open **Infrastructure > Hosts**, click your host, and the **Top processes** view should populate within a couple of minutes. In Phase 3 that view stayed empty.

### Lifecycle is independent

```bash
sudo systemctl status splunk-otel-collector --no-pager
sudo journalctl -u splunk-otel-collector -n 20 --no-pager
```

The collector is its own service. Restart it, reload its config, or upgrade it without touching the AppDynamics machine agent and vice versa. AppD agent upgrades cannot overwrite `/etc/otel/collector/agent_config.yaml` because it is not in their install tree.

### Update cadence is Splunk's

`apt list --installed 2>/dev/null | grep splunk-otel-collector` shows the version. Future upgrades come through the same package channel on the Splunk OTel Collector release cadence rather than waiting for the next AppDynamics machine agent release.

## The Path Forward

You walked the workshop from AppDynamics-only, through infrastructure dual signal, through "yes you can run the workshop config inside AppD's bundled collector if you accept the friction", and finally to the standalone install we recommend for production.

The next step on this path is OTel-native: drop the AppDynamics agent on a service, instrument it with the OpenTelemetry Java SDK or auto-instrumentation directly, and let the standalone Splunk OTel Collector you just installed pick the data up unchanged. The `appd.*` correlation attributes go away on those services because there is no AppD agent to add them, but everything else in the pipeline (resource processors, high-cardinality trim, host metrics, profiling, log forwarding) keeps working with no changes.

For services where AppDynamics still earns its place (SIM, the L1/L2 mental model, business transaction analytics), dual mode and the standalone collector are how you keep both teams happy while the migration runs.

Move on to wire up global data links so any Splunk trace gives you a one-click jump back into the matching AppDynamics view.
