---
title: 3. Verify, Then Tally the Friction
weight: 3
---

You should now have APM and infrastructure in both AppDynamics and Splunk Observability Cloud, all served by a single OTel collector process the AppD launcher manages. Confirm that, then look at exactly what running in this configuration cost you.

## Verify Splunk APM

1. Open [Splunk Observability Cloud](https://app.signalfx.com).
2. Click **APM** in the left navigation panel.
3. In the **Environment** dropdown, choose `<INSTANCE>-appd-dual`. The workshop config's `resource/workshop` processor stamps that environment name on every signal regardless of what the Java agent sends.

You should see the **OrderService** service. Click it, open **Traces**, and pick a `GET /order` trace.

Click the root span and confirm the AppDynamics correlation attributes are present:

| Attribute | Example value |
|---|---|
| `appd.app.name` | `Dual-Ingest-YOURINITIALS` |
| `appd.tier.name` | `OrderService` |
| `appd.bt.name` | `/order` or `/inventory` |
| `appd.request.guid` | The AppDynamics request GUID |

These attributes are the proof that the trace went through a Java agent in dual mode and that the OTel pipeline preserved them all the way to Splunk.

{{% notice title="Give it a few minutes" style="info" icon="info-circle" %}}
Allow 2 to 5 minutes for the first traces to appear after restarting the Java app.
{{% /notice %}}

## Verify Splunk Infrastructure

Host metrics still flow through the bundled collector's `hostmetrics` receiver, exported by `signalfx`:

1. Click **Metric Finder** in the left navigation panel.
2. Search for `cpu.utilization` and open the chart.
3. Filter on `host.name=${INSTANCE}` (use your actual `${INSTANCE}` value).

You should see a live time series. The `resource/workshop` processor stamped `deployment.environment=${INSTANCE}-appd-dual` on the metrics too, so you can also filter or split by that.

## Verify AppDynamics is Unaffected

The AppD side of both signals continues to flow unchanged:

- **AppDynamics Controller > Applications > `Dual-Ingest-${INSTANCE}` > OrderService** still shows business transactions for `/order` and `/inventory`.
- **AppDynamics Controller > Servers** still shows the host with CPU, memory, disk, and network from the machine agent's SIM data.

Dual mode and the workshop OTel config do not touch the AppDynamics protocols, they only add an OTel pipeline alongside them.

## Now the Friction

Everything works. The problem is what it took to get here, and what is silently still broken.

### The environment variable tax

Count the lines you exported on the previous page. Eight extra `SPLUNK_*` variables that the AppDynamics launcher does not know about. They live in your shell. The next person who logs in does not have them. A reboot wipes them. There is no `/etc/...conf` file the OTel binary reads on its own when AppD launches it. Persisting them means writing them into your shell rc, the AppD startup script, or a wrapper, every one of which is somebody you have to keep current when the workshop config grows.

### The Smart Agent components do nothing

Tail the bundled collector log:

```bash
tail -f ~/workshop/appd/machine-agent/logs/otel/otel-collector.log
```

You will see the `smartagent/processlist` receiver attempting to scrape and failing because `/usr/lib/splunk-otel-collector/agent-bundle` is not on disk. The receiver is in the `logs/signalfx` pipeline of the workshop config because it powers the **process list** view per host in Splunk Observability Cloud Infrastructure. With the AppD machine agent install you do not get the bundle, so that view stays empty. To fix this without leaving the bundled-collector path you would have to install the `splunk-otel-collector` package separately just for the bundle directory and mask its `systemd` service to keep AppD in charge of the process. That is an awful lot of work to get one process list panel.

### The lifecycle is glued to AppD

Stopping the machine agent stops the OTel collector with it. There is no `systemctl status otel-collector` and no separate journal. Restart the machine agent to pick up a config change and you also bounce all your OTel pipelines. An AppDynamics machine agent upgrade can also overwrite `conf/otel/agent_config.yaml` because it is part of the AppD install tree. You would need to remember to re-cp the workshop config after every upgrade.

### The collector binary is on AppD's release cadence

The OTel binary inside the AppD machine agent ships when AppD ships. New OTel features and security fixes you might want from a more recent Splunk Distribution release have to wait for the next AppD machine agent release. Inside the standalone install you control the upgrade cadence directly.

## What This Means

The bundled collector path is not wrong. It is honest about what it is: a single OTel process on the host, managed by the AppDynamics admin, configured to do as much as you are willing to wire up by hand. Some teams accept all of these costs to avoid running a second OTel process.

For most teams running a Splunk Observability stack alongside AppDynamics, the standalone Splunk OTel Collector is a much better deal. The install script writes every `SPLUNK_*` environment variable into `/etc/otel/collector/splunk-otel-collector.conf`, ships the Smart Agent monitor bundle so `smartagent/processlist` actually has process data, runs the collector as its own `systemd` service with independent restart and upgrade behavior, and follows the Splunk Distribution release cadence.

That is what Phase 4 sets up, using the same workshop `collector-config.yaml` you just used here. The difference between this phase and the next is almost entirely operational.
